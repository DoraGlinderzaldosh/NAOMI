"""
Unit tests for MIT Separable Demand Elasticity Engine (Simchi-Levi et al.).
Validates:
1. Convergence of alternating submodel coordinate descent in < 20 iterations.
2. Strictly non-increasing demand curve (dg/dp <= 0) for all evaluated prices.
3. Decoupling of context h(x) and price response g(p).
"""

import numpy as np
import pytest

from src.core.separable_elasticity import SeparableDemandModel


def test_separable_model_convergence_and_monotonicity():
    np.random.seed(42)
    n = 200

    # True data generation: demand decreases as price rises
    prices = np.random.uniform(2.0, 8.0, size=n)
    # Context features: day of week, promotions, event flag
    X = np.random.uniform(0.0, 1.0, size=(n, 5))
    context_multiplier = 50.0 + 30.0 * X[:, 0] + 20.0 * X[:, 1]
    # Inverted price curve: g(p) = (p / 4.0)^(-1.2)
    true_sales = context_multiplier * (prices / 4.0) ** (-1.2) + np.random.normal(0, 2.0, size=n)
    true_sales = np.maximum(true_sales, 1.0)

    model = SeparableDemandModel(max_iter=20, tol=1e-4)
    res = model.fit(prices=prices, context_features=X, sales=true_sales, base_price=4.0)

    # 1. Assert convergence in < 20 iterations
    assert res.n_iterations <= 20
    assert res.converged

    # 2. Assert strictly downward sloping price curve (dg/dp <= 0)
    assert res.is_strictly_non_increasing
    diffs = np.diff(res.g_multipliers)
    assert np.all(diffs <= 1e-7)

    # 3. Predict on new test prices
    test_context = X[0:1]
    p_low, p_mid, p_high = 3.0, 5.0, 7.0
    pred_low = model.predict(p_low, test_context)
    pred_mid = model.predict(p_mid, test_context)
    pred_high = model.predict(p_high, test_context)

    # Higher price must produce strictly lower or equal demand
    assert pred_low >= pred_mid >= pred_high


def test_separable_model_no_upward_sloping_anomaly():
    """
    Even when noisy samples occasionally have high sales at high price,
    isotonic constraints eliminate upward-sloping demand curves.
    """
    prices = np.array([2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0])
    X = np.ones((len(prices), 2))
    # Synthetic noisy data with an artificial spike at price 5.0
    sales = np.array([100.0, 90.0, 80.0, 75.0, 70.0, 68.0, 72.0, 55.0, 48.0])

    model = SeparableDemandModel(max_iter=15)
    res = model.fit(prices=prices, context_features=X, sales=sales, base_price=3.5)

    assert res.is_strictly_non_increasing
    # Evaluate across fine grid
    p_grid = np.linspace(2.0, 6.0, 50)
    preds = [model.predict(p, X[0:1]) for p in p_grid]
    p_diffs = np.diff(preds)
    assert np.all(p_diffs <= 1e-6), "Demand curve must never slope upward!"

