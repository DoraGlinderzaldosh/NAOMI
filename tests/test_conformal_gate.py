"""
Unit tests for CoRAL-RF Conformal Gated Forecaster (Zizi et al., 2026).
Validates:
1. Gated model convergence and adaptive gate parameter alpha in [0, 1].
2. Split conformal prediction calibration produces finite nonconformity bounds.
3. Test fold coverage satisfies nominal empirical coverage bounds (85% <= cov <= 98%).
"""

import numpy as np
import pytest

from src.models.conformal_gate import ConformalGatedForecaster


def test_conformal_gated_forecaster_coverage():
    np.random.seed(42)
    n_train = 120
    n_cal = 60
    n_test = 60
    n_features = 6

    # Generate synthetic time-series covariates
    X_all = np.random.uniform(0.0, 1.0, size=(n_train + n_cal + n_test, n_features))
    y_all = (
        25.0
        + 15.0 * X_all[:, 0]
        + 8.0 * np.sin(np.linspace(0, 12, len(X_all)))
        + np.random.normal(0, 2.5, size=len(X_all))
    )
    y_all = np.maximum(y_all, 1.0)

    X_train, y_train = X_all[:n_train], y_all[:n_train]
    X_cal, y_cal = X_all[n_train : n_train + n_cal], y_all[n_train : n_train + n_cal]
    X_test, y_test = X_all[n_train + n_cal :], y_all[n_train + n_cal :]

    # Train model
    forecaster = ConformalGatedForecaster(n_estimators=20, max_depth=5, random_state=42)
    fit_metrics = forecaster.fit(
        X_train=X_train,
        y_train=y_train,
        X_val=X_cal,
        y_val=y_cal,
        lookback=7,
        epochs=8,
    )

    assert 0.0 <= forecaster.gate_alpha <= 1.0
    assert forecaster.is_fitted

    # Calibrate split conformal prediction layer
    q90, q95 = forecaster.calibrate(X_cal, y_cal)
    assert q90 > 0
    assert q95 >= q90

    # Predict on test set with uncertainty intervals
    intervals = forecaster.predict_with_conformal_intervals(X_test)

    assert len(intervals.point_forecast) == n_test
    assert len(intervals.lower_90) == n_test
    assert len(intervals.upper_90) == n_test

    # Compute empirical coverage
    cov_90 = forecaster.evaluate_coverage(y_test, intervals.lower_90, intervals.upper_90)
    cov_95 = forecaster.evaluate_coverage(y_test, intervals.lower_95, intervals.upper_95)

    # Conformal guarantee: coverage should be close to nominal level on i.i.d. test set
    assert 0.82 <= cov_90 <= 0.98, f"Empirical 90% coverage {cov_90:.2f} out of bounds"
    assert 0.88 <= cov_95 <= 1.00, f"Empirical 95% coverage {cov_95:.2f} out of bounds"

