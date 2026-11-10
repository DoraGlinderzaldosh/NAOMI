"""
Pydantic request/response schemas for the NAOMI REST API.
Includes core endpoints and NAOMI 2.0 enhancements (Conformal, CVaR, Virtual Population, Narrative).
"""

from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


# ------------------------------------------------------------------ #
# Shared
# ------------------------------------------------------------------ #

class HealthResponse(BaseModel):
    status: str = "ok"
    version: str
    message: str


class SKUInfo(BaseModel):
    item_id: str
    item_name: str
    category: str
    department: str
    store_id: str
    base_price: float
    historical_elasticity: float
    description: str


class SKUListResponse(BaseModel):
    skus: List[SKUInfo]
    count: int


# ------------------------------------------------------------------ #
# /forecast
# ------------------------------------------------------------------ #

class ForecastRequest(BaseModel):
    sku_id: str = Field(..., description="SKU identifier (must be in CURATED_SKUS)")
    horizon: int = Field(
        default=7,
        ge=1,
        le=30,
        description="Number of days ahead to forecast (1, 7, or 30)",
    )
    model: str = Field(
        default="lstm",
        description="Model to use: lstm | naive | seasonal_naive | moving_average | ridge",
    )


class ForecastResponse(BaseModel):
    sku_id: str
    horizon: int
    model_name: str
    forecast_dates: List[str]
    y_pred: List[float]
    lower_ci: List[float]
    upper_ci: List[float]
    mae: Optional[float] = None
    rmse: Optional[float] = None
    mape: Optional[float] = None


# ------------------------------------------------------------------ #
# /pricing/optimize
# ------------------------------------------------------------------ #

class OptimizePricingRequest(BaseModel):
    sku_id: str = Field(..., description="SKU identifier")
    base_demand: float = Field(
        ...,
        gt=0,
        description="Expected demand units at current base price",
    )
    override_elasticity: Optional[float] = Field(
        default=None,
        description="Override the SKU's historical elasticity (must be ≤ 0)",
    )
    override_unit_cost: Optional[float] = Field(
        default=None,
        gt=0,
        description="Override the SKU's unit cost",
    )
    fixed_costs: float = Field(
        default=500.0,
        ge=0,
        description="Periodic fixed overhead ($)",
    )
    price_grid_points: int = Field(
        default=100,
        ge=10,
        le=500,
        description="Resolution of the profit curve grid search",
    )


class OptimizePricingResponse(BaseModel):
    sku_id: str
    base_price: float
    optimal_price: float
    price_change_pct: float
    base_demand: float
    optimal_demand: float
    demand_change_pct: float
    base_profit: float
    optimal_profit: float
    profit_uplift_pct: float
    optimal_revenue: float
    elasticity: float
    candidate_prices: List[float]
    candidate_profits: List[float]
    candidate_revenues: List[float]


# ------------------------------------------------------------------ #
# /simulate
# ------------------------------------------------------------------ #

class SimulateRequest(BaseModel):
    sku_id: str = Field(
        ...,
        description="SKU identifier — used to pull baseline price, cost, and elasticity",
    )
    scenario_type: str = Field(
        ...,
        description=(
            "Scenario to run: price_policy | macro_demand_shock | "
            "supply_chain_inflation | competitor_price_war | stagflation"
        ),
    )
    base_demand: float = Field(
        ...,
        gt=0,
        description="Baseline demand units (e.g. last 7-day average)",
    )
    params: Dict[str, Any] = Field(
        default_factory=dict,
        description=(
            "Scenario-specific parameters:\n"
            "  price_policy            → delta_price_pct (float)\n"
            "  macro_demand_shock      → shock_pct (float, default 15)\n"
            "  supply_chain_inflation  → cost_pct (float, default 10)\n"
            "  competitor_price_war    → competitor_price_drop_pct (float, default 10)\n"
            "  stagflation             → cost_surge_pct (float), demand_contraction_pct (float)"
        ),
    )
    override_unit_cost: Optional[float] = Field(
        default=None,
        gt=0,
        description="Override the SKU's unit cost for this simulation",
    )
    override_elasticity: Optional[float] = Field(
        default=None,
        description="Override the SKU's historical elasticity (must be ≤ 0)",
    )
    fixed_costs: float = Field(
        default=500.0,
        ge=0,
        description="Periodic fixed overhead ($)",
    )


class FinancialKPIsSchema(BaseModel):
    price: float
    demand: float
    revenue: float
    cogs: float
    gross_profit: float
    gross_margin_pct: float
    breakeven_units: float
    breakeven_revenue: float


class SimulateResponse(BaseModel):
    scenario_id: str
    scenario_name: str
    parameters: Dict[str, Any]
    baseline_kpis: FinancialKPIsSchema
    shocked_kpis: FinancialKPIsSchema
    demand_delta_pct: float
    revenue_delta_pct: float
    profit_delta_pct: float
    risk_assessment: str


# ------------------------------------------------------------------ #
# Phase 8 / NAOMI 2.0 Schemas
# ------------------------------------------------------------------ #

class NarrativeRequest(BaseModel):
    sku_id: str = Field(..., description="Target SKU identifier")
    horizon: int = Field(default=14, ge=1, le=30)
    current_price: Optional[float] = Field(default=None, gt=0)
    optimal_price: Optional[float] = Field(default=None, gt=0)
    base_demand: Optional[float] = Field(default=None, gt=0)
    risk_scenario: Optional[str] = Field(default="supply_chain_inflation")


class NarrativeResponse(BaseModel):
    sku_id: str
    narrative: str
    source: str
    disclaimer: str
    validated: bool


class VirtualPopulationRequest(BaseModel):
    sku_id: str = Field(..., description="Target SKU identifier")
    candidate_price: Optional[float] = Field(default=None, gt=0)
    total_shopper_traffic: int = Field(default=500, ge=50, le=5000)


class PersonaDetail(BaseModel):
    persona_id: str
    name: str
    weight_pct: float
    baseline_prob: float
    candidate_prob: float
    delta_prob_pct: float
    reserve_price: float
    elasticity: float


class VirtualPopulationResponse(BaseModel):
    sku_id: str
    base_price: float
    candidate_price: float
    total_shopper_traffic: int
    aggregate_conversion_rate: float
    baseline_conversion_rate: float
    expected_demand_units: float
    demand_p05: float
    demand_p95: float
    demand_std_dev: float
    demand_delta_pct: float
    personas: List[PersonaDetail]


class CVaROptimizeRequest(BaseModel):
    sku_id: str = Field(..., description="Target SKU identifier")
    base_demand: Optional[float] = Field(default=None, gt=0)
    risk_aversion_lambda: float = Field(default=0.30, ge=0.0, le=1.0)
    tail_beta: float = Field(default=0.10, ge=0.01, le=0.50)
    override_unit_cost: Optional[float] = Field(default=None, gt=0)
    fixed_costs: float = Field(default=500.0, ge=0.0)


class FrontierPointSchema(BaseModel):
    lambda_val: float = Field(..., alias="lambda")
    optimal_price: float
    expected_profit: float
    cvar_downside_profit: float
    tail_risk_exposure: float
    forecasted_demand: float


class CVaROptimizeResponse(BaseModel):
    sku_id: str
    base_price: float
    optimal_price: float
    risk_aversion_lambda: float
    expected_profit: float
    cvar_downside_profit: float
    tail_risk_gap: float
    forecasted_demand: float
    base_expected_profit: float
    profit_uplift_pct: float
    is_constrained: bool
    efficient_frontier: List[Dict[str, Any]]


class ConformalForecastRequest(BaseModel):
    sku_id: str = Field(..., description="Target SKU identifier")
    horizon: int = Field(default=14, ge=1, le=30)


class ConformalForecastResponse(BaseModel):
    sku_id: str
    horizon: int
    dates: List[str]
    point_forecast: List[float]
    lower_90: List[float]
    upper_90: List[float]
    lower_95: List[float]
    upper_95: List[float]
    q_hat_90: float
    q_hat_95: float
    safety_stock_buffer_95: float
