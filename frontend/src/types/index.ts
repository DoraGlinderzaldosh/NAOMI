export interface SKUInfo {
  item_id: string;
  item_name: string;
  category: string;
  department: string;
  store_id: string;
  base_price: number;
  historical_elasticity: number;
  description: string;
}

export interface ForecastData {
  sku_id: string;
  horizon: number;
  model_name: string;
  forecast_dates: string[];
  y_pred: number[];
  lower_ci: number[];
  upper_ci: number[];
  lower_95?: number[];
  upper_95?: number[];
  mae?: number;
  rmse?: number;
  mape?: number;
}

export interface OptimizationData {
  sku_id: string;
  optimal_price: number;
  optimal_profit: number;
  optimal_revenue: number;
  optimal_demand: number;
  profit_uplift_pct: number;
  price_change_pct: number;
  gross_margin_pct: number;
  breakeven_units: number;
  fixed_costs: number;
  curve_prices: number[];
  curve_profits: number[];
  curve_revenues: number[];
}

export interface FinancialKPIs {
  demand: number;
  revenue: number;
  cogs: number;
  gross_profit: number;
  gross_margin_pct: number;
  breakeven_units: number;
}

export interface SimulationResult {
  scenario_type: string;
  sku_id: string;
  candidate_price: number;
  baseline_kpis: FinancialKPIs;
  shocked_kpis: FinancialKPIs;
  demand_change_pct: number;
  revenue_change_pct: number;
  profit_change_pct: number;
  risk_label: "Positive" | "Stable" | "Moderate Risk" | "High Risk" | "Critical Risk";
  executive_brief: string;
}

export interface SimulationSliders {
  priceDeltaPct: number;      // -30% to +40%
  demandShockPct: number;     // -50% to +30%
  costSurgePct: number;       // 0% to +50%
  competitorDropPct: number;  // 0% to 30%
}

export interface HistoricalPoint {
  date: string;
  actual: number;
}

export interface PersonaDetail {
  persona_id: string;
  name: string;
  weight_pct: number;
  baseline_prob: number;
  candidate_prob: number;
  delta_prob_pct: number;
  reserve_price: number;
  elasticity: number;
}

export interface VirtualPopulationResponse {
  sku_id: string;
  base_price: number;
  candidate_price: number;
  total_shopper_traffic: number;
  aggregate_conversion_rate: number;
  baseline_conversion_rate: number;
  expected_demand_units: number;
  demand_p05: number;
  demand_p95: number;
  demand_std_dev: number;
  demand_delta_pct: number;
  personas: PersonaDetail[];
}

export interface FrontierPoint {
  lambda: number;
  optimal_price: number;
  expected_profit: number;
  cvar_downside_profit: number;
  tail_risk_exposure: number;
  forecasted_demand: number;
}

export interface CVaROptimizeResponse {
  sku_id: string;
  base_price: number;
  optimal_price: number;
  risk_aversion_lambda: number;
  expected_profit: number;
  cvar_downside_profit: number;
  tail_risk_gap: number;
  forecasted_demand: number;
  base_expected_profit: number;
  profit_uplift_pct: number;
  is_constrained: boolean;
  efficient_frontier: FrontierPoint[];
}

export interface NarrativeResponse {
  sku_id: string;
  narrative: string;
  source: string;
  disclaimer: string;
  validated: boolean;
}
