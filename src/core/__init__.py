"""Core business logic package for NAOMI."""

from src.core.elasticity import (
    estimate_elasticity,
    estimate_elasticity_with_diagnostics,
    iso_elastic_demand,
    SeparableDemandModel,
    ElasticityDiagnostic,
)
from src.core.financial import compute_financial_kpis
from src.core.optimizer import optimize_price, profit
from src.core.simulator import simulate_scenario

__all__ = [
    "estimate_elasticity",
    "estimate_elasticity_with_diagnostics",
    "iso_elastic_demand",
    "SeparableDemandModel",
    "ElasticityDiagnostic",
    "compute_financial_kpis",
    "optimize_price",
    "profit",
    "simulate_scenario",
]
