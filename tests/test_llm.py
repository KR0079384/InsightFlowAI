import json
import logging
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
            },
            {
                "id": "driver-marketing-PROD-002",
                "title": "PulseFit Smartwatch Marketing Spend Reduced 51.6%",
                "impact_type": "negative",
                "impact_amount": -7020.0,
                "impact_formatted": "-$7,020.00",
                "explanation": "Marketing spend was cut 51.6% from $4,650 to $2,250.",
                "product_id": "PROD-002",
                "evidence_id": "ev-marketing-PROD-002"
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
            "executive_summary": "Increasing reorder eliminates 8 stockout days in scenario simulation.",
            "evidence_link": "ev-stockout-PROD-001"
        }
    }

def test_successful_synthesis(synthesizer, mock_context, caplog):
    valid_narrative = {
        "executive_answer": "September revenue dropped by 13.8% to $112,060.00 compared to $130,000.00 in August.",
        "why_explanation": "AeroMax Pro Headphones suffered 8 consecutive stockout days with negative impact -$18,250.00."
    }
    
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "message": {"content": json.dumps(valid_narrative)}
    }

    with caplog.at_level(logging.INFO):
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

def test_dictionary_returned_for_executive_answer(synthesizer, mock_context, caplog):
    structured_payload = {
        "executive_answer": {
            "summary": "September revenue dropped by 13.8% to $112,060.00.",
            "key_actions": ["Increase safety stock", "Expedite lead time"]
        },
        "why_explanation": {
            "reasons": [
                "AeroMax Pro Headphones suffered 8 consecutive stockout days.",
                "Sales dropped 30.9% coinciding with inventory depletion."
            ]
        }
    }
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"message": {"content": json.dumps(structured_payload)}}

    with caplog.at_level(logging.INFO):
        with patch("httpx.Client.post", return_value=mock_response):
            res = synthesizer.synthesize(
                query=mock_context["query"],
                intent_metadata=mock_context["intent_metadata"],
                key_metrics=mock_context["key_metrics"],
                drivers=mock_context["drivers"],
                evidence_list=mock_context["evidence_list"]
            )

    assert res["success"] is True
    assert res["executive_answer"] == "September revenue dropped by 13.8% to $112,060.00."
    assert "summary:" not in res["executive_answer"]
    assert "key_actions:" not in res["executive_answer"]
    assert "- AeroMax Pro Headphones suffered 8 consecutive stockout days." in res["why_explanation"]
    assert "- Sales dropped 30.9% coinciding with inventory depletion." in res["why_explanation"]

def test_list_returned_for_why_explanation(synthesizer, mock_context, caplog):
    valid_narrative_with_list = {
        "executive_answer": "September revenue dropped by 13.8%",
        "why_explanation": [
            "AeroMax Pro Headphones suffered 8 consecutive stockout days.",
            "Sales dropped 30.9% coinciding with inventory depletion."
        ]
    }
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"message": {"content": json.dumps(valid_narrative_with_list)}}

    with caplog.at_level(logging.INFO):
        with patch("httpx.Client.post", return_value=mock_response):
            res = synthesizer.synthesize(
                query=mock_context["query"],
                intent_metadata=mock_context["intent_metadata"],
                key_metrics=mock_context["key_metrics"],
                drivers=mock_context["drivers"],
                evidence_list=mock_context["evidence_list"]
            )

    assert res["success"] is True
    assert res["executive_answer"] == "September revenue dropped by 13.8%"
    assert "- AeroMax Pro Headphones suffered 8 consecutive stockout days." in res["why_explanation"]
    assert "- Sales dropped 30.9% coinciding with inventory depletion." in res["why_explanation"]

def test_thinking_tags_and_nested_json(synthesizer, mock_context):
    raw_content = (
        "<think>\nI need to summarize the context into JSON.\n</think>\n"
        "```json\n"
        "{\n"
        '  "response": {\n'
        '    "executive_summary": "September revenue dropped by 13.8%",\n'
        '    "explanation": "AeroMax Pro Headphones suffered 8 consecutive stockout days."\n'
        "  }\n"
        "}\n"
        "```"
    )
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"message": {"content": raw_content}}

    with patch("httpx.Client.post", return_value=mock_response):
        res = synthesizer.synthesize(
            query=mock_context["query"],
            intent_metadata=mock_context["intent_metadata"],
            key_metrics=mock_context["key_metrics"],
            drivers=mock_context["drivers"],
            evidence_list=mock_context["evidence_list"]
        )

    assert res["success"] is True
    assert res["executive_answer"] == "September revenue dropped by 13.8%"
    assert res["why_explanation"] == "AeroMax Pro Headphones suffered 8 consecutive stockout days."

def test_empty_string_narrative_fields(synthesizer, mock_context):
    invalid_narrative = {
        "executive_answer": "   ",
        "why_explanation": "AeroMax Pro Headphones suffered 8 stockout days."
    }
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"message": {"content": json.dumps(invalid_narrative)}}

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

def test_ollama_connection_failure_logging(synthesizer, mock_context, caplog):
    with caplog.at_level(logging.WARNING):
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
    assert "Ollama API call error: ConnectError" in caplog.text

def test_ollama_non_200_logging(synthesizer, mock_context, caplog):
    mock_response = MagicMock()
    mock_response.status_code = 500

    with caplog.at_level(logging.WARNING):
        with patch("httpx.Client.post", return_value=mock_response):
            res = synthesizer.synthesize(
                query=mock_context["query"],
                intent_metadata=mock_context["intent_metadata"],
                key_metrics=mock_context["key_metrics"],
                drivers=mock_context["drivers"],
                evidence_list=mock_context["evidence_list"]
            )

    assert res["success"] is False
    assert res["error"] == "HTTP 500"
    assert "Ollama API request failed with HTTP status 500" in caplog.text

def test_ollama_request_timeout_logging(synthesizer, mock_context, caplog):
    with caplog.at_level(logging.WARNING):
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
    assert "Ollama API call error: TimeoutException" in caplog.text

def test_empty_or_malformed_response_logging(synthesizer, mock_context, caplog):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"message": {"content": "Not valid JSON"}}

    with caplog.at_level(logging.WARNING):
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

def test_ungrounded_number_rejection_logging(synthesizer, mock_context, caplog):
    hallucinated_narrative = {
        "executive_answer": "Revenue plummeted by 85.5% to $999,999.00.",
        "why_explanation": "Company lost $500,000 due to unknown factors."
    }
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "message": {"content": json.dumps(hallucinated_narrative)}
    }

    with caplog.at_level(logging.WARNING):
        with patch("httpx.Client.post", return_value=mock_response):
            res = synthesizer.synthesize(
                query=mock_context["query"],
                intent_metadata=mock_context["intent_metadata"],
                key_metrics=mock_context["key_metrics"],
                drivers=mock_context["drivers"],
                evidence_list=mock_context["evidence_list"]
            )

    assert res["success"] is False
    assert res["error"] == "Validation failed after retry"
    assert "failed numeric grounding check" in caplog.text

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

def test_regression_explanation_capped_at_three_bullets(synthesizer, mock_context):
    four_bullets_narrative = {
        "executive_answer": "September revenue dropped by 13.8%",
        "why_explanation": [
            "AeroMax Pro Headphones suffered 8 consecutive stockout days.",
            "Sales dropped 30.9% coinciding with inventory depletion.",
            "Marketing spend declined by 51.6%.",
            "ClearVision webcam growth partially offset the decline."
        ]
    }
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"message": {"content": json.dumps(four_bullets_narrative)}}

    with patch("httpx.Client.post", return_value=mock_response):
        res = synthesizer.synthesize(
            query=mock_context["query"],
            intent_metadata=mock_context["intent_metadata"],
            key_metrics=mock_context["key_metrics"],
            drivers=mock_context["drivers"],
            evidence_list=mock_context["evidence_list"]
        )

    assert res["success"] is True
    bullets = res["why_explanation"].split("\n")
    assert len(bullets) == 3

def test_regression_deduplication_of_explanation_bullets(synthesizer, mock_context):
    duplicate_bullets_narrative = {
        "executive_answer": "September revenue dropped by 13.8%",
        "why_explanation": [
            "AeroMax Pro Headphones suffered 8 consecutive stockout days.",
            "AeroMax Pro Headphones suffered 8 consecutive stockout days.",
            "Sales dropped 30.9% coinciding with inventory depletion."
        ]
    }
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"message": {"content": json.dumps(duplicate_bullets_narrative)}}

    with patch("httpx.Client.post", return_value=mock_response):
        res = synthesizer.synthesize(
            query=mock_context["query"],
            intent_metadata=mock_context["intent_metadata"],
            key_metrics=mock_context["key_metrics"],
            drivers=mock_context["drivers"],
            evidence_list=mock_context["evidence_list"]
        )

    assert res["success"] is True
    bullets = res["why_explanation"].split("\n")
    assert len(bullets) == 2

def test_regression_unproven_causation_phrases_rejected(synthesizer, mock_context):
    overstated_causation = {
        "executive_answer": "September revenue dropped by 13.8% with ad spend reductions contributing to revenue decline.",
        "why_explanation": "Stockout directly impacted revenue, highlighting the sensitivity of sales to marketing investment and seeking to reverse stockout-driven losses."
    }
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"message": {"content": json.dumps(overstated_causation)}}

    with patch("httpx.Client.post", return_value=mock_response):
        res = synthesizer.synthesize(
            query=mock_context["query"],
            intent_metadata=mock_context["intent_metadata"],
            key_metrics=mock_context["key_metrics"],
            drivers=mock_context["drivers"],
            evidence_list=mock_context["evidence_list"]
        )

    assert res["success"] is False
    assert res["error"] == "Validation failed after retry"

def test_validation_failure_followed_by_successful_retry(synthesizer, mock_context):
    """Verifies that if 1st attempt fails validation, 1-shot retry can succeed if retried narrative is valid."""
    invalid_first_response = MagicMock()
    invalid_first_response.status_code = 200
    invalid_first_response.json.return_value = {
        "message": {"content": json.dumps({
            "executive_answer": "The primary cause was an 8-day inventory stockout.",
            "why_explanation": "Sales dropped due to supplier lead-time delay."
        })}
    }

    valid_retry_response = MagicMock()
    valid_retry_response.status_code = 200
    valid_retry_response.json.return_value = {
        "message": {"content": json.dumps({
            "executive_answer": "September revenue dropped by 13.8% to $112,060.00.",
            "why_explanation": "AeroMax Pro Headphones suffered 8 stockout days from Sep 11 to Sep 18 while inventory was 0."
        })}
    }

    with patch("httpx.Client.post", side_effect=[invalid_first_response, valid_retry_response]):
        res = synthesizer.synthesize(
            query=mock_context["query"],
            intent_metadata=mock_context["intent_metadata"],
            key_metrics=mock_context["key_metrics"],
            drivers=mock_context["drivers"],
            evidence_list=mock_context["evidence_list"],
            simulation=mock_context["simulation"]
        )

    assert res["success"] is True
    assert "13.8%" in res["executive_answer"]
    assert "primary cause" not in res["executive_answer"].lower()
