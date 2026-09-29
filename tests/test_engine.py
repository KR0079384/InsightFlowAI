import pytest
from unittest.mock import MagicMock
from src.decision_engine.engine import DecisionEngine

def test_engine_dependency_injection():
    mock_llm = MagicMock()
    mock_llm.synthesize.return_value = {
        "success": True,
        "executive_answer": "Injected LLM Executive Answer",
        "why_explanation": "Injected LLM Why Explanation"
    }

    engine = DecisionEngine(llm=mock_llm)
    report = engine.analyze_query("Why did revenue drop in September?")

    assert mock_llm.synthesize.called
    assert report.executive_answer == "Injected LLM Executive Answer"
    assert report.why_explanation == "Injected LLM Why Explanation"
    assert len(report.key_metrics) > 0
    assert len(report.drivers) > 0

def test_engine_llm_exception_handling():
    mock_llm = MagicMock()
    mock_llm.synthesize.side_effect = RuntimeError("Unexpected LLM error")

    engine = DecisionEngine(llm=mock_llm)
    report = engine.analyze_query("Why did revenue drop in September?")

    assert mock_llm.synthesize.called
    # Verifies graceful fallback to deterministic narrative strings
    assert "September 2026 revenue declined" in report.executive_answer
    assert "AeroMax Pro Headphones" in report.why_explanation
    assert len(report.key_metrics) > 0

def test_engine_unknown_intent_does_not_call_llm():
    mock_llm = MagicMock()

    engine = DecisionEngine(llm=mock_llm)
    report = engine.analyze_query("What is the weather in Tokyo?")

    assert not mock_llm.synthesize.called
    assert "could not classify" in report.executive_answer.lower()
    assert len(report.key_metrics) == 0
