import pytest
from unittest.mock import MagicMock
from src.decision_engine.engine import DecisionEngine

def test_engine_deterministic_narrative_authoritative_with_mock_llm():
    mock_llm = MagicMock()
    mock_llm.synthesize.return_value = {
        "success": True,
        "executive_answer": "Injected LLM Executive Answer",
        "why_explanation": "Injected LLM Why Explanation"
    }

    engine = DecisionEngine(llm=mock_llm)
    report = engine.analyze_query("Why did revenue drop in September?")

    # Verifies deterministic narrative is returned and not overwritten by injected mock LLM
    assert "September 2026 revenue was" in report.executive_answer
    assert "AeroMax Pro Headphones" in report.why_explanation
    assert report.executive_answer != "Injected LLM Executive Answer"
    assert report.why_explanation != "Injected LLM Why Explanation"
    assert len(report.key_metrics) > 0
    assert len(report.drivers) > 0

def test_engine_llm_exception_handling():
    mock_llm = MagicMock()
    mock_llm.synthesize.side_effect = RuntimeError("Unexpected LLM error")

    engine = DecisionEngine(llm=mock_llm)
    report = engine.analyze_query("Why did revenue drop in September?")

    # Verifies deterministic narrative is returned cleanly even if LLM raises exception
    assert "September 2026 revenue was" in report.executive_answer
    assert "AeroMax Pro Headphones" in report.why_explanation
    assert len(report.key_metrics) > 0

def test_engine_invalid_narrative_types_fallback():
    mock_llm = MagicMock()
    # LLM returning dict and list instead of strings
    mock_llm.synthesize.return_value = {
        "success": True,
        "executive_answer": {"summary": "Revenue dropped by 13.80%"},
        "why_explanation": ["AeroMax Pro stockouts", "Marketing drop"]
    }

    engine = DecisionEngine(llm=mock_llm)
    report = engine.analyze_query("Why did revenue drop in September?")

    # Verifies deterministic narrative is returned
    assert "September 2026 revenue was" in report.executive_answer
    assert "AeroMax Pro Headphones" in report.why_explanation
    assert isinstance(report.executive_answer, str)
    assert isinstance(report.why_explanation, str)
    assert len(report.key_metrics) > 0

def test_engine_unknown_intent_does_not_call_llm():
    mock_llm = MagicMock()

    engine = DecisionEngine(llm=mock_llm)
    report = engine.analyze_query("What is the weather in Tokyo?")

    assert not mock_llm.synthesize.called
    assert "could not classify" in report.executive_answer.lower()
    assert len(report.key_metrics) == 0
