import pytest
from src.decision_engine.intent import IntentClassifier

@pytest.fixture
def classifier():
    return IntentClassifier()

def test_revenue_decline_formulations(classifier):
    queries = [
        "Why did revenue fall this month?",
        "What caused our sales to decrease in September?",
        "Explain why top-line sales plummeted",
        "What drove the revenue loss?",
        "Main root causes of sales decline",
        "Why are we losing money compared to last month?"
    ]
    for q in queries:
        res = classifier.classify(q)
        assert res["intent"] == "revenue_decline_analysis", f"Failed for query: {q}"
        assert res["confidence"] > 0.8

def test_stockout_analysis_formulations(classifier):
    queries = [
        "Did we have any stockouts?",
        "Which products ran out of stock?",
        "Show me out of stock days for AeroMax headphones",
        "Are there any inventory depletion issues?",
        "Supply chain bottlenecks and stock-out report"
    ]
    for q in queries:
        res = classifier.classify(q)
        assert res["intent"] == "stockout_analysis", f"Failed for query: {q}"

def test_product_performance_formulations(classifier):
    queries = [
        "Which products are performing worst?",
        "How is PulseFit smartwatch performing?",
        "SKU breakdown for webcam",
        "Show me product sales performance summary",
        "Compare product revenue"
    ]
    for q in queries:
        res = classifier.classify(q)
        assert res["intent"] == "product_performance", f"Failed for query: {q}"

def test_simulation_formulations_and_percentages(classifier):
    # Test percentage extractions
    res1 = classifier.classify("What if we increase reorder quantity by 25%?")
    assert res1["intent"] == "simulation"
    assert res1["reorder_delta_pct"] == 25.0

    res2 = classifier.classify("Simulate increasing safety stock by 15.5 percent for smartwatch")
    assert res2["intent"] == "simulation"
    assert res2["reorder_delta_pct"] == 15.5
    assert res2["product_id"] == "PROD-002"

    res3 = classifier.classify("What happens if we reorder 30% more headphones?")
    assert res3["intent"] == "simulation"
    assert res3["reorder_delta_pct"] == 30.0
    assert res3["product_id"] == "PROD-001"

def test_anomaly_detection_formulations(classifier):
    queries = [
        "Were there any marketing budget anomalies?",
        "Show me inventory variance and unusual spend shifts"
    ]
    for q in queries:
        res = classifier.classify(q)
        assert res["intent"] == "anomaly_detection", f"Failed for query: {q}"

def test_product_alias_resolution(classifier):
    assert classifier._extract_product_id("aeromax pro headphones") == "PROD-001"
    assert classifier._extract_product_id("pulsefit smartwatch") == "PROD-002"
    assert classifier._extract_product_id("echosound speaker") == "PROD-003"
    assert classifier._extract_product_id("clearvision 4k webcam") == "PROD-004"
    assert classifier._extract_product_id("ergolift laptop stand") == "PROD-005"

def test_ambiguous_and_unsupported_queries(classifier):
    off_topic_queries = [
        "What is the weather in Tokyo?",
        "Tell me a joke about computers",
        "Who won the cricket world cup?",
        "How do I repair an engine?",
        "asdfghjkl",
        ""
    ]
    for q in off_topic_queries:
        res = classifier.classify(q)
        assert res["intent"] == "unknown", f"Failed to mark as unknown for query: '{q}'"
        assert res["confidence"] == 0.0
