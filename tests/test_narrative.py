"""
Unit tests for Phase 8: LLM Executive Narrative Layer and Anti-Hallucination Guards.
Validates:
1. Deterministic fallback produces rich, non-empty executive text across all inputs.
2. Corporate disclaimer 'AI-assisted, not binding.' is always present.
3. Numerical validation guard accepts valid numbers and rejects ungrounded hallucinations.
4. Orchestrator defaults to fallback on missing credentials or validation mismatch.
"""

import pytest
from src.llm.fallback import DISCLAIMER_TEXT, generate_fallback_narrative
from src.llm.narrator import (
    generate_narrative,
    validate_narrative_numerics,
    extract_numbers_from_text,
)


@pytest.fixture
def sample_executive_payload():
    return {
        "sku_id": "FOODS_3_090_CA_1",
        "item_name": "Fresh Gala Apples 3lb",
        "horizon_days": 14,
        "total_forecast_units": 924.0,
        "daily_mean_demand": 66.0,
        "current_price": 2.50,
        "optimal_price": 2.80,
        "price_change_pct": 12.0,
        "profit_delta_pct": 8.5,
        "optimal_gross_profit": 850.0,
        "elasticity": -1.35,
        "is_constrained": False,
        "worst_scenario_name": "Supply-Chain Cost Inflation",
        "worst_scenario_profit_delta_pct": -23.3,
    }


def test_fallback_narrative_structure_and_disclaimer(sample_executive_payload):
    text = generate_fallback_narrative(sample_executive_payload)

    assert isinstance(text, str)
    assert len(text) > 100
    assert "FOODS_3_090_CA_1" in text
    assert "2.50" in text
    assert "2.80" in text
    assert DISCLAIMER_TEXT in text


def test_disclaimer_always_present_in_orchestrator(sample_executive_payload):
    result = generate_narrative(sample_executive_payload, api_key=None)

    assert result["source"] == "fallback"
    assert result["disclaimer"] == DISCLAIMER_TEXT
    assert DISCLAIMER_TEXT in result["narrative"]
    assert result["validated"] is True


def test_hallucination_guard_accepts_grounded_text(sample_executive_payload):
    grounded_text = (
        "Demand for FOODS_3_090_CA_1 is 924 units over 14 days. "
        "At price 2.80 vs 2.50, profit delta is 8.5% with elasticity -1.35. "
        "Worst downside is -23.3%."
    )
    is_valid = validate_narrative_numerics(grounded_text, sample_executive_payload)
    assert is_valid is True


def test_hallucination_guard_rejects_invented_numbers(sample_executive_payload):
    # Invented number 74.8% does not exist anywhere in sample_executive_payload
    hallucinated_text = (
        "Moving price to 2.80 will skyrocket profit by 74.8% without any downside risk."
    )
    is_valid = validate_narrative_numerics(hallucinated_text, sample_executive_payload)
    assert is_valid is False

