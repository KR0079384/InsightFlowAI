import pytest
from fastapi.testclient import TestClient
from src.main import app

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

def test_api_analyze_unsupported_query():
    res = client.post("/api/v1/analyze", json={"question": "What is the weather in Tokyo?"})
    assert res.status_code == 200
    data = res.json()
    assert "could not classify" in data["executive_answer"].lower()
    assert len(data["key_metrics"]) == 0
    assert len(data["drivers"]) == 0
    assert len(data["evidence_list"]) == 0
    assert data["recommendation"]["action_type"] == "none"

def test_api_analyze_with_llm_synthesis_success(monkeypatch):
    mock_llm_result = {
        "success": True,
        "executive_answer": "LLM Synthesized: Revenue dropped by 13.80% in September due to stockouts.",
        "why_explanation": "LLM Explanation: AeroMax Pro suffered 8 stockout days."
    }
    monkeypatch.setattr(
        "src.decision_engine.engine.llm_synthesizer.synthesize",
        lambda **kwargs: mock_llm_result
    )

    res = client.post("/api/v1/analyze", json={"question": "Why did revenue drop in September?"})
    assert res.status_code == 200
    data = res.json()
    assert data["executive_answer"] == mock_llm_result["executive_answer"]
    assert data["why_explanation"] == mock_llm_result["why_explanation"]
    # Verify deterministic fields remain intact
    assert len(data["key_metrics"]) > 0
    assert len(data["drivers"]) > 0
    assert len(data["evidence_list"]) > 0
    assert "recommendation" in data
    assert "default_simulation" in data

def test_api_analyze_with_llm_fallback(monkeypatch):
    # Mock LLM failure (e.g. Ollama offline or grounding validation fail)
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
    # Verify deterministic fallback narrative is returned
    assert "September 2026 revenue declined" in data["executive_answer"]
    assert "AeroMax Pro Headphones" in data["why_explanation"]
    assert len(data["key_metrics"]) > 0

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
