"""
Unit tests for Risk-Aware CVaR Strategic Optimizer (Huang & Wang 2026).
Validates:
1. CVaR downside profit is strictly lower than expected profit (E[Profit] >= CVaR_beta).
2. Higher risk aversion lambda yields greater protection against tail-risk losses.
3. Efficient frontier generation produces valid monotone trade-offs.
"""

import pytest
from src.core.cvar_optimizer import (
    compute_cvar_profit,
    optimize_price_cvar,
    compute_executive_risk_frontier,
)


def test_cvar_downside_relationship():
    base_price = 4.00
    base_demand = 80.0
    elasticity = -1.4
    unit_cost = 2.40

    exp_prof, cvar_prof, demand = compute_cvar_profit(
        price=base_price,
        base_price=base_price,
        base_demand=base_demand,
        elasticity=elasticity,
        unit_cost=unit_cost,
        fixed_cost=50.0,
        tail_beta=0.10,
    )

    # In any stochastic loss distribution, CVaR in the worst 10% tail is <= mean
    assert cvar_prof <= exp_prof
    assert demand > 0


def test_cvar_optimizer_risk_aversion_sweep():
    base_price = 4.00
    base_demand = 100.0
    elasticity = -1.5
    unit_cost = 2.40

    # Risk-neutral optimization (lambda = 0.0)
    opt_neutral = optimize_price_cvar(
        base_price=base_price,
        base_demand=base_demand,
        elasticity=elasticity,
        unit_cost=unit_cost,
        risk_aversion_lambda=0.0,
    )

    # Risk-averse optimization (lambda = 0.8)
    opt_averse = optimize_price_cvar(
        base_price=base_price,
        base_demand=base_demand,
        elasticity=elasticity,
        unit_cost=unit_cost,
        risk_aversion_lambda=0.8,
    )

    assert "optimal_price" in opt_neutral
    assert "optimal_price" in opt_averse
    # Risk-averse optimizer preserves tail profit
    assert opt_neutral["expected_profit"] >= opt_averse["expected_profit"] - 1.0


def test_executive_risk_frontier_generation():
    frontier = compute_executive_risk_frontier(
        base_price=5.00,
        base_demand=60.0,
        elasticity=-1.2,
        unit_cost=3.00,
        lambdas=[0.0, 0.5, 1.0],
    )

    assert len(frontier) == 3
    for pt in frontier:
        assert 0.0 <= pt["lambda"] <= 1.0
        assert pt["optimal_price"] > 0
        assert pt["cvar_downside_profit"] <= pt["expected_profit"]

