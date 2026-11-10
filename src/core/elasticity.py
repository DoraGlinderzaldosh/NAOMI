"""
Price Elasticity Engine for NAOMI.

Provides:
1. estimate_elasticity: Classic log-log OLS elasticity estimation.
2. estimate_elasticity_with_diagnostics: Guarded OLS estimation with p-value, standard error,
   R^2, automatic clipping [-3.0, -0.3], fallback category prior, and reliability flag.
3. iso_elastic_demand: Constant elasticity demand curve Q(P) = Q_base * (P / P_base)^e.
4. SeparableDemandModel: MIT Shape-Constrained Separable Elasticity Engine (Simchi-Levi et al.).
"""

from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import Optional, Tuple

import numpy as np
import pandas as pd
from scipy.stats import linregress
from sklearn.linear_model import LinearRegression

from src.core.separable_elasticity import SeparableDemandModel, SeparableFitResult

logger = logging.getLogger("naomi.core.elasticity")

# Sensible category fallback elasticity when empirical estimate is noisy or non-negative
DEFAULT_FALLBACK_ELASTICITY = -1.50
MIN_ELASTICITY_BOUND = -3.00
MAX_ELASTICITY_BOUND = -0.30


@dataclass
class ElasticityDiagnostic:
    """Detailed econometric diagnostics for a price elasticity estimate."""
    raw_elasticity: float
    guarded_elasticity: float
    standard_error: float
    p_value: float
    r_squared: float
    is_reliable: bool
    fallback_used: bool
    sample_size: int


def estimate_elasticity(df_sku: pd.DataFrame) -> float:
    """
    Estimate price elasticity using log-log OLS regression.

    Required columns:
        sell_price
        units_sold
    """
    df = df_sku.copy()

    df = df[
        (df["sell_price"] > 0)
        & (df["units_sold"] > 0)
    ]

    x = np.log(df["sell_price"]).values.reshape(-1, 1)
    y = np.log(df["units_sold"]).values

    model = LinearRegression()
    model.fit(x, y)

    elasticity = float(model.coef_[0])
    return elasticity


def estimate_elasticity_with_diagnostics(
    df_sku: pd.DataFrame,
    p_value_threshold: float = 0.05,
    fallback_prior: float = DEFAULT_FALLBACK_ELASTICITY,
) -> ElasticityDiagnostic:
    """
    Estimate price elasticity with econometric hypothesis testing and safety guards.

    Guards:
    1. If raw elasticity >= 0 (violating law of demand), fall back to fallback_prior.
    2. If p-value > p_value_threshold (statistically insignificant), fall back to fallback_prior.
    3. Always clip resulting elasticity to [MIN_ELASTICITY_BOUND, MAX_ELASTICITY_BOUND].
    """
    df = df_sku.copy()
    df = df[(df["sell_price"] > 0) & (df["units_sold"] > 0)]

    if len(df) < 5:
        return ElasticityDiagnostic(
            raw_elasticity=fallback_prior,
            guarded_elasticity=fallback_prior,
            standard_error=0.0,
            p_value=1.0,
            r_squared=0.0,
            is_reliable=False,
            fallback_used=True,
            sample_size=len(df),
        )

    log_p = np.log(df["sell_price"].values)
    log_q = np.log(df["units_sold"].values)

    res = linregress(log_p, log_q)
    raw_e = float(res.slope)
    stderr = float(res.stderr) if res.stderr is not None else 0.0
    pval = float(res.pvalue) if res.pvalue is not None else 1.0
    r2 = float(res.rvalue ** 2)

    fallback_needed = (raw_e >= 0.0) or (pval > p_value_threshold)
    if fallback_needed:
        guarded_e = fallback_prior
        is_reliable = False
    else:
        guarded_e = float(np.clip(raw_e, MIN_ELASTICITY_BOUND, MAX_ELASTICITY_BOUND))
        is_reliable = True

    return ElasticityDiagnostic(
        raw_elasticity=raw_e,
        guarded_elasticity=guarded_e,
        standard_error=stderr,
        p_value=pval,
        r_squared=r2,
        is_reliable=is_reliable,
        fallback_used=fallback_needed,
        sample_size=len(df),
    )


def iso_elastic_demand(
    p_candidate: float,
    p_base: float,
    q_base: float,
    elasticity: float,
) -> float:
    """
    Predict demand for a candidate price under iso-elastic demand curve:
        Q(P) = Q_base * (P / P_base)^elasticity
    """
    if p_candidate <= 0 or p_base <= 0:
        return 0.0
    return float(q_base * (p_candidate / p_base) ** elasticity)


__all__ = [
    "estimate_elasticity",
    "estimate_elasticity_with_diagnostics",
    "iso_elastic_demand",
    "ElasticityDiagnostic",
    "SeparableDemandModel",
    "SeparableFitResult",
    "DEFAULT_FALLBACK_ELASTICITY",
    "MIN_ELASTICITY_BOUND",
    "MAX_ELASTICITY_BOUND",
]
