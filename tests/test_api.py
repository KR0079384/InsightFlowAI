import json
import pytest
from unittest.mock import MagicMock
from fastapi.testclient import TestClient
from src.main import app
from src.decision_engine.llm import LLMSynthesizer

client = TestClient(app)

def test_api_health():
    res = client.get("/api/v1/health")
    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "healthy"

def test_api_overview():
    res = client.get("/api/v1/overview")
    assert res.status_code == 200
    data = res.json()
    assert data["total_orders"] > 0
    assert data["total_revenue"] > 0
    assert data["active_products"] == 5

def test_api_analyze():
    res = client.post("/api/v1/analyze", json={"question": "Why did revenue fall this month?"})
    assert res.status_code == 200
    data = res.json()
    assert "executive_answer" in data
    assert "why_explanation" in data
    assert len(data["key_metrics"]) > 0
    assert len(data["drivers"]) > 0
    assert len(data["evidence_list"]) > 0
    assert "recommendation" in data
    assert "default_simulation" in data
    # Encoding check: no garbled UTF-8 artifacts
    assert "â" not in data["executive_answer"]
    assert "â" not in data["why_explanation"]

def test_api_analyze_unsupported_query():
    res = client.post("/api/v1/analyze", json={"question": "What is the weather in Tokyo?"})
    assert res.status_code == 200
    data = res.json()
    assert "could not classify" in data["executive_answer"].lower()
    assert len(data["key_metrics"]) == 0
    assert len(data["drivers"]) == 0
    assert len(data["evidence_list"]) == 0
    assert data["recommendation"]["action_type"] == "none"

def test_api_analyze_deterministic_narrative_authoritative(monkeypatch):
    mock_llm_result = {
        "success": True,
        "executive_answer": "Injected LLM Answer",
        "why_explanation": "Injected LLM Explanation"
    }
    monkeypatch.setattr(
        "src.decision_engine.engine.llm_synthesizer.synthesize",
        lambda **kwargs: mock_llm_result
    )

    res = client.post("/api/v1/analyze", json={"question": "Why did revenue drop in September?"})
    assert res.status_code == 200
    data = res.json()

    # Deterministic narrative remains authoritative and is returned
    assert "September 2026 revenue was $112,060.00" in data["executive_answer"]
    assert data["executive_answer"] != mock_llm_result["executive_answer"]
    assert data["why_explanation"] != mock_llm_result["why_explanation"]

    # Verify deterministic fields remain intact
    assert len(data["key_metrics"]) > 0
    assert len(data["drivers"]) > 0
    assert len(data["evidence_list"]) > 0
    assert "recommendation" in data
    assert "default_simulation" in data

def test_api_analyze_with_llm_fallback(monkeypatch):
    mock_llm_result = {
        "success": False,
        "executive_answer": None,
        "why_explanation": None,
        "error": "ConnectError"
    }
    monkeypatch.setattr(
        "src.decision_engine.engine.llm_synthesizer.synthesize",
        lambda **kwargs: mock_llm_result
    )

    res = client.post("/api/v1/analyze", json={"question": "Why did revenue drop in September?"})
    assert res.status_code == 200
    data = res.json()
    # Verify deterministic narrative is returned and non-causal
    assert "September 2026 revenue was $112,060.00" in data["executive_answer"]
    assert "primary cause" not in data["executive_answer"].lower()
    assert "due to" not in data["why_explanation"].lower()
    assert len(data["key_metrics"]) > 0
    assert "â" not in data["executive_answer"]
    assert "â" not in data["why_explanation"]

@pytest.mark.parametrize("unsafe_phrase", [
    "primary cause was the stockout",
    "compounded by reduced marketing",
    "sales declined due to lower ad spend",
    "marketing spend reduction improved ROI",
    "simulation guarantees recovered revenue and eliminates stockouts",
    "sales dropped after supplier lead-time delay",
    "Stockouts resulted from insufficient reorder buffer and extended lead times.",
    "The ad spend cut reduced visibility and conversions.",
    "Optimizing reorder quantities and lead times directly reduces stockout days and boosts revenue.",
    "Revenue declined linked to a reduction in ad spend."
])
def test_api_rejects_unsafe_llm_narratives(unsafe_phrase):
    """Proves unsafe LLM text can NEVER reach the API response payload."""

    # 1. Direct LLMSynthesizer validation verification
    synthesizer = LLMSynthesizer()
    is_valid, errors = synthesizer.validate_narrative(
        exec_answer=f"September revenue dropped 13.8%. {unsafe_phrase}",
        why_explanation=f"- AeroMax Pro hit 0 inventory, which {unsafe_phrase}",
        context_payload={}
    )
    assert is_valid is False
    assert len(errors) > 0

    # 2. API End-to-End verification (API always returns authoritative deterministic narrative)
    res = client.post("/api/v1/analyze", json={"question": "Why did revenue drop in September?"})
    assert res.status_code == 200
    data = res.json()

    # Unsafe text must be rejected and deterministic fallback returned
    assert unsafe_phrase not in data["executive_answer"]
    assert unsafe_phrase not in data["why_explanation"]
    assert "primary cause" not in data["executive_answer"].lower()
    assert "due to" not in data["why_explanation"].lower()
    assert "resulted from" not in data["executive_answer"].lower()
    assert "reduced visibility" not in data["executive_answer"].lower()
    assert "boosts revenue" not in data["executive_answer"].lower()

    # Structured fields MUST remain unchanged
    assert len(data["key_metrics"]) > 0
    assert len(data["drivers"]) > 0
    assert len(data["evidence_list"]) > 0
    assert data["recommendation"]["id"] == "rec-replenish-aeromax-001"
    assert data["default_simulation"]["stockout_days_current"] == 8

def test_api_simulate():
    res = client.post("/api/v1/simulate", json={
        "product_id": "PROD-001",
        "reorder_quantity_delta_pct": 20.0,
        "lead_time_days_reduction": 3,
        "marketing_budget_delta_pct": 0.0,
        "price_change_pct": 0.0
    })
    assert res.status_code == 200
    data = res.json()
    assert data["projected_revenue_delta"] > 0
    assert data["stockout_days_simulated"] < data["stockout_days_current"]
