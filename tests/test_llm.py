import json
import pytest
from unittest.mock import MagicMock, patch
import httpx
from src.decision_engine.llm import LLMSynthesizer

@pytest.fixture
def synthesizer():
    return LLMSynthesizer(base_url="http://localhost:11434", model_name="qwen3:8b", timeout=5.0)

@pytest.fixture
def mock_context():
    return {
        "query": "Why did revenue drop this month?",
        "intent_metadata": {"intent": "revenue_decline_analysis", "confidence": 0.9},
        "key_metrics": [
            {
                "name": "Monthly Revenue",
                "key": "monthly_revenue",
                "current_value": 112060.0,
                "previous_value": 130000.0,
                "change_pct": -13.8,
                "unit": "$",
                "formatted": "$112,060.00",
                "description": "Revenue changed by -13.80%"
            }
        ],
        "drivers": [
            {
                "id": "driver-stockout-PROD-001",
                "title": "AeroMax Pro Headphones Sales Dropped 30.9%",
                "impact_type": "negative",
                "impact_amount": -18250.0,
                "impact_formatted": "-$18,250.00",
                "explanation": "AeroMax Pro experienced 8 consecutive stockout days.",
                "product_id": "PROD-001",
                "evidence_id": "ev-stockout-PROD-001"
            }
        ],
        "evidence_list": [
            {
                "id": "ev-stockout-PROD-001",
                "claim": "AeroMax Pro Headphones suffered 8 stockout days.",
                "metric": "stockout_days",
                "period": "2026-09",
                "calculation": "COUNT(inventory.is_stock_out == 1)",
                "formula": "8 days * $250 = $18,250",
                "source_files": ["inventory.csv"],
                "sample_rows": [],
                "confidence_score": 1.0
            }
        ],
        "simulation": {
            "scenario_title": "Scenario: Optimize Reorder",
            "product_id": "PROD-001",
            "product_name": "AeroMax Pro Headphones",
            "parameters_applied": {"reorder_quantity_delta_pct": 20.0},
            "metrics": [],
            "projected_revenue_current": 112060.0,
            "projected_revenue_simulated": 130310.0,
            "projected_revenue_delta": 18250.0,
            "stockout_days_current": 8,
            "stockout_days_simulated": 0,
            "executive_summary": "Increasing reorder eliminates 8 stockout days.",
            "evidence_link": "ev-stockout-PROD-001"
        }
    }

def test_successful_synthesis(synthesizer, mock_context):
    valid_narrative = {
        "executive_answer": "September revenue dropped by 13.8% to $112,060.00 compared to $130,000.00 in August.",
        "why_explanation": "AeroMax Pro Headphones suffered 8 consecutive stockout days costing -$18,250.00."
    }
    
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "message": {"content": json.dumps(valid_narrative)}
    }

    with patch("httpx.Client.post", return_value=mock_response):
        res = synthesizer.synthesize(
            query=mock_context["query"],
            intent_metadata=mock_context["intent_metadata"],
            key_metrics=mock_context["key_metrics"],
            drivers=mock_context["drivers"],
            evidence_list=mock_context["evidence_list"],
            simulation=mock_context["simulation"]
        )

    assert res["success"] is True
    assert res["executive_answer"] == valid_narrative["executive_answer"]
    assert res["why_explanation"] == valid_narrative["why_explanation"]
    assert res["error"] is None

def test_ollama_connection_failure(synthesizer, mock_context):
    with patch("httpx.Client.post", side_effect=httpx.ConnectError("Connection refused")):
        res = synthesizer.synthesize(
            query=mock_context["query"],
            intent_metadata=mock_context["intent_metadata"],
            key_metrics=mock_context["key_metrics"],
            drivers=mock_context["drivers"],
            evidence_list=mock_context["evidence_list"]
        )

    assert res["success"] is False
    assert res["executive_answer"] is None
    assert res["why_explanation"] is None
    assert "ConnectError" in res["error"]

def test_ollama_request_timeout(synthesizer, mock_context):
    with patch("httpx.Client.post", side_effect=httpx.TimeoutException("Timed out")):
        res = synthesizer.synthesize(
            query=mock_context["query"],
            intent_metadata=mock_context["intent_metadata"],
            key_metrics=mock_context["key_metrics"],
            drivers=mock_context["drivers"],
            evidence_list=mock_context["evidence_list"]
        )

    assert res["success"] is False
    assert res["executive_answer"] is None
    assert "TimeoutException" in res["error"]

def test_empty_or_malformed_response(synthesizer, mock_context):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"message": {"content": "Not valid JSON"}}

    with patch("httpx.Client.post", return_value=mock_response):
        res = synthesizer.synthesize(
            query=mock_context["query"],
            intent_metadata=mock_context["intent_metadata"],
            key_metrics=mock_context["key_metrics"],
            drivers=mock_context["drivers"],
            evidence_list=mock_context["evidence_list"]
        )

    assert res["success"] is False
    assert res["executive_answer"] is None
    assert res["error"] == "JSONDecodeError"

def test_ungrounded_number_rejection(synthesizer, mock_context):
    hallucinated_narrative = {
        "executive_answer": "Revenue plummeted by 85.5% to $999,999.00.",
        "why_explanation": "Company lost $500,000 due to unknown factors."
    }
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "message": {"content": json.dumps(hallucinated_narrative)}
    }

    with patch("httpx.Client.post", return_value=mock_response):
        res = synthesizer.synthesize(
            query=mock_context["query"],
            intent_metadata=mock_context["intent_metadata"],
            key_metrics=mock_context["key_metrics"],
            drivers=mock_context["drivers"],
            evidence_list=mock_context["evidence_list"]
        )

    assert res["success"] is False
    assert res["error"] == "Numeric grounding validation failed"

def test_unknown_intent_fallback(synthesizer):
    res = synthesizer.synthesize(
        query="What is the weather in Tokyo?",
        intent_metadata={"intent": "unknown"},
        key_metrics=[],
        drivers=[],
        evidence_list=[]
    )
    assert res["success"] is False
    assert res["executive_answer"] is None
