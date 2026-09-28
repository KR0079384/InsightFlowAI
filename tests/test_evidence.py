import pytest
from src.decision_engine.evidence import evidence_engine

def test_evidence_structure():
    ev_rev = evidence_engine.build_revenue_decline_evidence()
    assert ev_rev.metric == "monthly_revenue_growth"
    assert "13.8" in ev_rev.claim or "13.80" in ev_rev.claim
    assert "orders.csv" in ev_rev.source_files
    assert len(ev_rev.sample_rows) > 0
    assert ev_rev.confidence_score == 1.0

def test_stockout_evidence():
    ev_so = evidence_engine.build_stockout_evidence("PROD-001")
    assert ev_so.metric == "stockout_days"
    assert "8 consecutive stock-out days" in ev_so.claim
    assert "inventory.csv" in ev_so.source_files
    assert len(ev_so.sample_rows) == 8 # 8 stockout days
