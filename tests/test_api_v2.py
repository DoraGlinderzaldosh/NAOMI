"""
Automated Integration Tests for NAOMI 2.0 REST API Endpoints.
Covers:
- POST /narrative
- POST /virtual-population
- POST /pricing/cvar
- POST /conformal-forecast
"""

import pytest
from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)


def test_narrative_endpoint():
    response = client.post(
        "/narrative",
        json={"sku_id": "FOODS_3_090_CA_1", "horizon": 14},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["sku_id"] == "FOODS_3_090_CA_1"
    assert "narrative" in data
    assert "AI-assisted, not binding." in data["narrative"]
    assert data["validated"] is True


def test_virtual_population_endpoint():
    response = client.post(
        "/virtual-population",
        json={
            "sku_id": "FOODS_3_090_CA_1",
            "candidate_price": 2.75,
            "total_shopper_traffic": 500,
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["sku_id"] == "FOODS_3_090_CA_1"
    assert data["candidate_price"] == 2.75
    assert len(data["personas"]) == 5
    assert 0.0 <= data["aggregate_conversion_rate"] <= 1.0
    assert data["demand_p05"] <= data["expected_demand_units"] <= data["demand_p95"]


def test_cvar_pricing_endpoint():
    response = client.post(
        "/pricing/cvar",
        json={
            "sku_id": "FOODS_3_090_CA_1",
            "risk_aversion_lambda": 0.4,
            "tail_beta": 0.10,
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["sku_id"] == "FOODS_3_090_CA_1"
    assert data["optimal_price"] > 0
    assert data["cvar_downside_profit"] <= data["expected_profit"]
    assert len(data["efficient_frontier"]) >= 3


def test_conformal_forecast_endpoint():
    response = client.post(
        "/conformal-forecast",
        json={"sku_id": "FOODS_3_090_CA_1", "horizon": 14},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["sku_id"] == "FOODS_3_090_CA_1"
    assert len(data["point_forecast"]) == 14
    assert len(data["lower_90"]) == 14
    assert len(data["upper_90"]) == 14
    assert len(data["lower_95"]) == 14
    assert len(data["upper_95"]) == 14
    assert data["q_hat_95"] >= data["q_hat_90"]
    assert data["safety_stock_buffer_95"] > 0

