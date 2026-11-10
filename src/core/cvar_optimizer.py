"""
Risk-Aware Strategic CVaR Optimizer (Huang & Wang 2026; Rockafellar & Uryasev 2000).

Dual-objective optimization maximizing:
    U(p) = (1 - λ) * E[Π(p)] + λ * CVaR_β(Π(p))

where:
    - λ in [0, 1] is the C-suite risk-aversion parameter (0 = risk-neutral, 1 = maximum tail defense).
    - CVaR_β is the Conditional Value at Risk (expected profit in the worst β-percentile tail states).
    - Enterprise profit includes gross margin, fixed cost F, and inventory proxy holding (h) / stockout penalties (p_stockout):
      Π(p) = (p - c)*D - F - [h * max(0, I - D) + p_stockout * max(0, D - I)]
"""

from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Tuple

import numpy as np
from scipy.optimize import minimize_scalar

from src.core.elasticity import iso_elastic_demand

logger = logging.getLogger("naomi.core.cvar_optimizer")


@dataclass
class FrontierPoint:
    """A single coordinate along the Executive Risk-Return Efficient Frontier."""
    lambda_risk_aversion: float
    optimal_price: float
    expected_profit: float
    cvar_profit: float
    expected_demand: float
    tail_risk_exposure: float  # Absolute downside gap: E[Profit] - CVaR_Profit


def compute_cvar_profit(
    price: float,
    base_price: float,
    base_demand: float,
    elasticity: float,
    unit_cost: float,
    fixed_cost: float = 0.0,
    inventory_buffer: Optional[float] = None,
    holding_cost_rate: float = 0.15,
    stockout_penalty_rate: float = 0.35,
    tail_beta: float = 0.10,
    n_simulations: int = 500,
    random_seed: int = 42,
) -> Tuple[float, float, float]:
    """
    Simulate profit distribution across random demand realizations to compute E[Profit],
    VaR_beta, and CVaR_beta.
    """
    mean_demand = iso_elastic_demand(price, base_price, base_demand, elasticity)
    target_inventory = inventory_buffer if inventory_buffer is not None else mean_demand * 1.05

    # Simulated demand with log-normal or Poisson variance
    rng = np.random.default_rng(random_seed)
    # Demand noise with standard deviation ~ 18% of mean demand
    sim_demands = rng.lognormal(
        mean=np.log(max(1.0, mean_demand)) - 0.5 * 0.18**2,
        sigma=0.18,
        size=n_simulations,
    )

    profits = np.zeros(n_simulations, dtype=np.float64)
    h_cost = unit_cost * holding_cost_rate
    p_penalty = (price - unit_cost) * stockout_penalty_rate

    for i, d in enumerate(sim_demands):
        # Gross profit from sold units (capped by available inventory)
        sold = min(d, target_inventory)
        gross = (price - unit_cost) * sold - fixed_cost

        # Inventory holding cost if excess inventory
        holding = h_cost * max(0.0, target_inventory - d)
        # Lost sales penalty if unmet customer demand
        stockout = p_penalty * max(0.0, d - target_inventory)

        profits[i] = gross - holding - stockout

    expected_profit = float(np.mean(profits))

    # Calculate beta-quantile (VaR) and worst beta-fraction expectation (CVaR)
    k_tail = max(1, int(tail_beta * n_simulations))
    sorted_profits = np.sort(profits)
    tail_losses = sorted_profits[:k_tail]

    var_beta = float(sorted_profits[k_tail - 1])
    cvar_beta = float(np.mean(tail_losses))

    return expected_profit, cvar_beta, mean_demand


def optimize_price_cvar(
    base_price: float,
    base_demand: float,
    elasticity: float,
    unit_cost: float,
    fixed_cost: float = 0.0,
    risk_aversion_lambda: float = 0.0,
    tail_beta: float = 0.10,
    price_band_pct: float = 0.30,
) -> Dict[str, Any]:
    """
    Find the optimal price under dual-objective CVaR criteria:
        argmax_p (1 - λ) * E[Π(p)] + λ * CVaR_β(Π(p))
    """
    lower = max(unit_cost * 1.02, (1.0 - price_band_pct) * base_price)
    upper = (1.0 + price_band_pct) * base_price

    lam = float(np.clip(risk_aversion_lambda, 0.0, 1.0))

    def objective(p: float) -> float:
        exp_p, cvar_p, _ = compute_cvar_profit(
            price=p,
            base_price=base_price,
            base_demand=base_demand,
            elasticity=elasticity,
            unit_cost=unit_cost,
            fixed_cost=fixed_cost,
            tail_beta=tail_beta,
        )
        score = (1.0 - lam) * exp_p + lam * cvar_p
        return -score

    # Grid search for global stability
    grid_prices = np.linspace(lower, upper, 60)
    scores = [-objective(p) for p in grid_prices]
    best_grid = grid_prices[np.argmax(scores)]

    # Refine with bounded scalar optimization
    res = minimize_scalar(
        objective,
        bounds=(lower, upper),
        method="bounded",
    )
    optimal_price = float(res.x)

    exp_prof, cvar_prof, opt_demand = compute_cvar_profit(
        price=optimal_price,
        base_price=base_price,
        base_demand=base_demand,
        elasticity=elasticity,
        unit_cost=unit_cost,
        fixed_cost=fixed_cost,
        tail_beta=tail_beta,
    )

    base_exp, base_cvar, _ = compute_cvar_profit(
        price=base_price,
        base_price=base_price,
        base_demand=base_demand,
        elasticity=elasticity,
        unit_cost=unit_cost,
        fixed_cost=fixed_cost,
        tail_beta=tail_beta,
    )

    is_constrained = (abs(optimal_price - lower) < 1e-3) or (abs(optimal_price - upper) < 1e-3)

    return {
        "optimal_price": round(optimal_price, 4),
        "risk_aversion_lambda": round(lam, 2),
        "expected_profit": round(exp_prof, 2),
        "cvar_downside_profit": round(cvar_prof, 2),
        "tail_risk_gap": round(exp_prof - cvar_prof, 2),
        "forecasted_demand": round(opt_demand, 2),
        "base_expected_profit": round(base_exp, 2),
        "profit_uplift_pct": round((exp_prof - base_exp) / max(abs(base_exp), 1e-4) * 100, 2),
        "is_constrained": is_constrained,
    }


def compute_executive_risk_frontier(
    base_price: float,
    base_demand: float,
    elasticity: float,
    unit_cost: float,
    fixed_cost: float = 0.0,
    lambdas: Optional[List[float]] = None,
) -> List[Dict[str, Any]]:
    """
    Generate points along the Executive Risk-Return Efficient Frontier
    as λ moves from 0.0 (risk neutral) to 1.0 (conservative tail defense).
    """
    lambda_list = lambdas or [0.0, 0.20, 0.40, 0.60, 0.80, 1.0]
    frontier = []

    for lam in lambda_list:
        res = optimize_price_cvar(
            base_price=base_price,
            base_demand=base_demand,
            elasticity=elasticity,
            unit_cost=unit_cost,
            fixed_cost=fixed_cost,
            risk_aversion_lambda=lam,
        )
        frontier.append({
            "lambda": lam,
            "optimal_price": res["optimal_price"],
            "expected_profit": res["expected_profit"],
            "cvar_downside_profit": res["cvar_downside_profit"],
            "tail_risk_exposure": res["tail_risk_gap"],
            "forecasted_demand": res["forecasted_demand"],
        })

    return frontier

