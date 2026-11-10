"""
Profit Optimization Engine for NAOMI.

Provides:
1. profit: Classical iso-elastic gross profit computation.
2. optimize_price: Bounded grid search & scalar optimization.
3. optimize_price_cvar: Huang & Wang (2026) Risk-Aware CVaR optimization.
4. compute_executive_risk_frontier: Trade-off curve between Expected Profit and Downside CVaR.
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional

import numpy as np
from scipy.optimize import minimize_scalar

from src.core.elasticity import iso_elastic_demand
from src.core.cvar_optimizer import (
    compute_cvar_profit,
    optimize_price_cvar,
    compute_executive_risk_frontier,
    FrontierPoint,
)


def profit(
    price: float,
    base_price: float,
    base_demand: float,
    elasticity: float,
    unit_cost: float,
    fixed_cost: float = 0.0,
) -> float:
    """Compute enterprise gross profit under iso-elastic demand."""
    demand = iso_elastic_demand(
        price,
        base_price,
        base_demand,
        elasticity,
    )

    return (price - unit_cost) * demand - fixed_cost


def optimize_price(
    base_price: float,
    base_demand: float,
    elasticity: float,
    unit_cost: float,
    fixed_cost: float = 0.0,
    price_band_pct: float = 0.30,
) -> Dict[str, float]:
    """
    Grid-search and bounded scalar optimization to find profit-maximizing price.
    
    Searches within [max(unit_cost * 1.05, (1 - price_band_pct) * base_price), (1 + price_band_pct) * base_price].
    """
    lower = max(unit_cost * 1.05, (1.0 - price_band_pct) * base_price)
    upper = (1.0 + price_band_pct) * base_price

    prices = np.linspace(lower, upper, 100)

    profits = [
        profit(
            p,
            base_price,
            base_demand,
            elasticity,
            unit_cost,
            fixed_cost,
        )
        for p in prices
    ]

    best_grid_price = prices[np.argmax(profits)]

    result = minimize_scalar(
        lambda p: -profit(
            p,
            base_price,
            base_demand,
            elasticity,
            unit_cost,
            fixed_cost,
        ),
        bounds=(lower, upper),
        method="bounded",
    )

    optimal_price = result.x

    optimal_profit = profit(
        optimal_price,
        base_price,
        base_demand,
        elasticity,
        unit_cost,
        fixed_cost,
    )

    optimal_demand = iso_elastic_demand(
        optimal_price,
        base_price,
        base_demand,
        elasticity,
    )

    return {
        "optimal_price": float(optimal_price),
        "optimal_profit": float(optimal_profit),
        "forecasted_demand": float(optimal_demand),
        "grid_price": float(best_grid_price),
    }


__all__ = [
    "profit",
    "optimize_price",
    "optimize_price_cvar",
    "compute_cvar_profit",
    "compute_executive_risk_frontier",
    "FrontierPoint",
]
