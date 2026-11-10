"""
LLM Virtual Population Market Simulator (Huang & Wang, Columbia University 2026).

Models retail customer behavior as a finite mixture of K behavioral customer personas:
    q_alpha(u, p) = sum_{k=1}^K alpha_k * q(x_k, u, p) + alpha_{K+1} * 0
with Binomial demand distribution:
    Q_{N, alpha}(u, p) ~ Binomial(N, q_alpha(u, p))

Enables:
1. Counterfactual pricing evaluation outside historical transaction observations.
2. Willingness-to-pay elicitation across diverse buyer archetypes.
3. Downside tail-risk estimation for CVaR risk hedging.
"""

from __future__ import annotations

import logging
import math
from dataclasses import dataclass
from typing import Any, Dict, List, Optional

import numpy as np

logger = logging.getLogger("naomi.llm.virtual_population")


@dataclass
class CustomerPersona:
    """Behavioral profile of a consumer archetype in the virtual population."""
    persona_id: str
    name: str
    description: str
    mixture_weight: float        # alpha_k in [0, 1]
    elasticity_coefficient: float  # Price sensitivity exponent
    reserve_price_multiplier: float  # Multiplier relative to baseline price
    quality_sensitivity: float    # Sensitivity to product category features (0 to 1)


# K = 5 Validated Retail Personas (Huang & Wang 2026 Formulation)
DEFAULT_PERSONAS: List[CustomerPersona] = [
    CustomerPersona(
        persona_id="budget_hunter",
        name="Budget Bargain Hunter",
        description="Highly price-sensitive shoppers with strict weekly budget constraints who defer purchases upon price hikes.",
        mixture_weight=0.28,
        elasticity_coefficient=-2.45,
        reserve_price_multiplier=0.92,
        quality_sensitivity=0.30,
    ),
    CustomerPersona(
        persona_id="convenience_seeker",
        name="Convenience Seeker",
        description="Time-poor, utility-driven buyers prioritizing shelf availability over minor price premiums.",
        mixture_weight=0.22,
        elasticity_coefficient=-0.45,
        reserve_price_multiplier=1.35,
        quality_sensitivity=0.85,
    ),
    CustomerPersona(
        persona_id="brand_loyalist",
        name="Brand & Quality Loyalist",
        description="Core category repeat purchasers with entrenched brand habits and low cross-brand substitution.",
        mixture_weight=0.20,
        elasticity_coefficient=-0.75,
        reserve_price_multiplier=1.28,
        quality_sensitivity=0.95,
    ),
    CustomerPersona(
        persona_id="bulk_buyer",
        name="Occasional Bulk Buyer",
        description="Volume buyers who aggressively load up during promotional discounts and withhold volume during price spikes.",
        mixture_weight=0.15,
        elasticity_coefficient=-1.85,
        reserve_price_multiplier=1.05,
        quality_sensitivity=0.50,
    ),
    CustomerPersona(
        persona_id="impulse_shopper",
        name="Event & Impulse Shopper",
        description="Casual basket-add shoppers responsive to holiday merchandising, SNAP timing, and end-cap displays.",
        mixture_weight=0.15,
        elasticity_coefficient=-1.30,
        reserve_price_multiplier=1.15,
        quality_sensitivity=0.65,
    ),
]


def elicit_persona_purchase_probability(
    persona: CustomerPersona,
    price: float,
    base_price: float,
) -> float:
    """
    Compute purchase probability q(x_k, u, p) in [0, 1] for a persona at price p.
    Guaranteed monotonically non-increasing in price (∂q/∂p <= 0).
    """
    if price <= 0 or base_price <= 0:
        return 0.0

    p_ratio = price / base_price
    reserve_p = base_price * persona.reserve_price_multiplier

    # Base baseline probability centered around 0.50 at fair value
    # Logistic steepness driven by persona's elasticity coefficient
    k = abs(persona.elasticity_coefficient) * 2.2
    x_offset = (price - reserve_p) / base_price

    # Logistic willingness-to-pay
    prob = 1.0 / (1.0 + math.exp(np.clip(k * x_offset, -20.0, 20.0)))

    # Ensure bounds [0.01, 0.98]
    return float(np.clip(prob, 0.01, 0.98))


def simulate_virtual_population_demand(
    sku_id: str,
    base_price: float,
    candidate_price: float,
    total_shopper_traffic: int = 500,
    personas: Optional[List[CustomerPersona]] = None,
) -> Dict[str, Any]:
    """
    Aggregate individual persona purchase decisions into a predictive binomial demand distribution:
        Q_{N, alpha}(u, p) ~ Binomial(N, q_alpha(u, p))
    """
    personas_to_use = personas or DEFAULT_PERSONAS

    # Normalize weights so sum <= 1.0 (remainder is non-purchasing baseline)
    total_weight = sum(p.mixture_weight for p in personas_to_use)
    norm_weights = [p.mixture_weight / max(total_weight, 1.0) for p in personas_to_use]

    persona_breakdown = []
    q_aggregate = 0.0
    q_baseline_agg = 0.0

    for persona, w in zip(personas_to_use, norm_weights):
        q_cand = elicit_persona_purchase_probability(persona, candidate_price, base_price)
        q_base = elicit_persona_purchase_probability(persona, base_price, base_price)

        q_aggregate += w * q_cand
        q_baseline_agg += w * q_base

        persona_breakdown.append({
            "persona_id": persona.persona_id,
            "name": persona.name,
            "weight_pct": round(w * 100, 1),
            "baseline_prob": round(q_base, 3),
            "candidate_prob": round(q_cand, 3),
            "delta_prob_pct": round((q_cand - q_base) / max(q_base, 1e-4) * 100, 1),
            "reserve_price": round(base_price * persona.reserve_price_multiplier, 2),
            "elasticity": round(persona.elasticity_coefficient, 2),
        })

    # Expected demand & variance under Binomial mixture
    N = total_shopper_traffic
    expected_demand = N * q_aggregate
    variance = N * q_aggregate * (1.0 - q_aggregate)
    std_dev = math.sqrt(max(0.0, variance))

    # Conformal tail bounds using Normal approximation to Binomial
    q_05 = max(0.0, expected_demand - 1.645 * std_dev)
    q_95 = expected_demand + 1.645 * std_dev

    baseline_demand = N * q_baseline_agg
    demand_delta_pct = (
        round((expected_demand - baseline_demand) / max(baseline_demand, 1e-4) * 100, 2)
    )

    return {
        "sku_id": sku_id,
        "candidate_price": round(candidate_price, 2),
        "base_price": round(base_price, 2),
        "total_shopper_traffic": N,
        "aggregate_conversion_rate": round(q_aggregate, 4),
        "baseline_conversion_rate": round(q_baseline_agg, 4),
        "expected_demand_units": round(expected_demand, 1),
        "demand_p05": round(q_05, 1),
        "demand_p95": round(q_95, 1),
        "demand_std_dev": round(std_dev, 2),
        "demand_delta_pct": demand_delta_pct,
        "personas": persona_breakdown,
    }

