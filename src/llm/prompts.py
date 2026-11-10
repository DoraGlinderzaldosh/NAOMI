"""
LLM Prompt Templates for NAOMI Decision Companion.
Enforces strict factual conditioning and anti-hallucination guardrails.
"""

from __future__ import annotations

import json
from typing import Any, Dict

DISCLAIMER_TEXT = "AI-assisted, not binding."

EXECUTIVE_SYSTEM_PROMPT = """You are an elite Chief Commercial Strategy Advisor writing an executive decision briefing for C-suite retail leaders.
Your analysis must be concise, mathematically grounded, and strictly objective.

CRITICAL INTEGRITY INSTRUCTIONS:
1. Use ONLY the empirical numbers and metrics present in the JSON DATA block below.
2. DO NOT invent, hallucinate, extrapolate, or round any numbers differently from the DATA block.
3. If an assumption or scenario is not in DATA, do not mention it.
4. Structure your response into exactly three concise paragraphs:
   - Paragraph 1: Demand Outlook & Forecast Trajectory
   - Paragraph 2: Pricing Recommendation, Elasticity & Gross Profit Impact
   - Paragraph 3: Strategic Risk Governance & Scenario Stress-Testing
5. Avoid technical ML jargon (e.g., avoid mentioning tensor dimensions, Adam learning rates). Focus on commercial business impact.
6. Never make guarantees. All projections are model-based decisions.
7. Always end with the mandatory corporate disclaimer.
"""

USER_BRIEF_TEMPLATE = """Please generate the C-Suite Executive Decision Brief based strictly on the following validated system data:

DATA:
{data_json}

Mandatory disclaimer to include at the very end on its own line:
{disclaimer}
"""


def build_narrative_prompt(data: Dict[str, Any]) -> Tuple[str, str]:
    """Generate system and user prompts with serialized JSON context."""
    # Clean data to contain only relevant analytical facts
    clean_facts = {
        "sku_id": data.get("sku_id"),
        "item_name": data.get("item_name"),
        "horizon_days": data.get("horizon_days", 14),
        "total_forecast_units": data.get("total_forecast_units"),
        "daily_mean_demand": data.get("daily_mean_demand"),
        "current_price": data.get("current_price"),
        "optimal_price": data.get("optimal_price"),
        "price_change_pct": data.get("price_change_pct"),
        "profit_delta_pct": data.get("profit_delta_pct"),
        "optimal_gross_profit": data.get("optimal_gross_profit"),
        "elasticity": data.get("elasticity"),
        "is_constrained": data.get("is_constrained", False),
        "worst_scenario_name": data.get("worst_scenario_name"),
        "worst_scenario_profit_delta_pct": data.get("worst_scenario_profit_delta_pct"),
        "macro_demand_shock_delta_pct": data.get("macro_demand_shock_delta_pct"),
        "supply_inflation_delta_pct": data.get("supply_inflation_delta_pct"),
        "competitor_price_war_delta_pct": data.get("competitor_price_war_delta_pct"),
        "stagflation_delta_pct": data.get("stagflation_delta_pct"),
    }

    # Filter out None values
    clean_facts = {k: v for k, v in clean_facts.items() if v is not None}
    data_json = json.dumps(clean_facts, indent=2)

    user_prompt = USER_BRIEF_TEMPLATE.format(
        data_json=data_json,
        disclaimer=DISCLAIMER_TEXT,
    )

    return EXECUTIVE_SYSTEM_PROMPT, user_prompt

