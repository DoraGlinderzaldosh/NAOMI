"""
Unit tests for LLM Virtual Population Market Simulator (Huang & Wang, Columbia 2026).
Validates:
1. Persona willingness-to-pay purchase probabilities lie in [0, 1].
2. Monotone probability decay as price increases (∂q/∂p <= 0).
3. Binomial aggregate demand simulation and quantile consistency (p05 <= mean <= p95).
"""

import pytest
from src.llm.virtual_population import (
    DEFAULT_PERSONAS,
    elicit_persona_purchase_probability,
    simulate_virtual_population_demand,
)


def test_persona_probabilities_and_monotonicity():
    base_p = 5.00
    prices = [3.00, 4.00, 5.00, 6.00, 7.50]

    for persona in DEFAULT_PERSONAS:
        probs = [elicit_persona_purchase_probability(persona, p, base_p) for p in prices]

        # Assert bounds [0, 1]
        for pr in probs:
            assert 0.0 <= pr <= 1.0

        # Assert strictly non-increasing in price
        for i in range(len(probs) - 1):
            assert probs[i] >= probs[i + 1], (
                f"Persona {persona.name} violated monotonicity at price {prices[i]} -> {prices[i+1]}"
            )


def test_virtual_market_demand_aggregation():
    base_p = 4.50
    cand_p = 5.20
    traffic = 600

    sim = simulate_virtual_population_demand(
        sku_id="FOODS_3_090_CA_1",
        base_price=base_p,
        candidate_price=cand_p,
        total_shopper_traffic=traffic,
    )

    assert sim["sku_id"] == "FOODS_3_090_CA_1"
    assert sim["candidate_price"] == cand_p
    assert sim["total_shopper_traffic"] == traffic
    assert 0.0 <= sim["aggregate_conversion_rate"] <= 1.0

    # Demand quantiles consistency
    assert sim["demand_p05"] <= sim["expected_demand_units"] <= sim["demand_p95"]
    assert len(sim["personas"]) == 5
    for p in sim["personas"]:
        assert "weight_pct" in p
        assert "candidate_prob" in p
        assert "baseline_prob" in p

