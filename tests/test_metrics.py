import pytest
from src.data_engine.metrics import metrics_engine
from src.data_engine.loader import loader

def test_monthly_revenue():
    rev = metrics_engine.get_monthly_revenue()
    assert "2026-08" in rev
    assert "2026-09" in rev
    assert rev["2026-08"] == 130000.0
    assert rev["2026-09"] == 112060.0

def test_revenue_growth_decline():
    growth = metrics_engine.get_revenue_growth("2026-09", "2026-08")
    assert growth["growth_pct"] == pytest.approx(-13.80, rel=1e-2)
    assert growth["current_revenue"] == 112060.0
    assert growth["previous_revenue"] == 130000.0
    assert growth["delta_amount"] == -17940.0

def test_prod_001_stockouts_and_drop():
    breakdown = metrics_engine.get_product_breakdown("2026-09", "2026-08")
    prod1 = next(p for p in breakdown if p["product_id"] == "PROD-001")
    assert prod1["stockout_days"] == 8
    assert prod1["growth_pct"] < -30.0 # Sales dropped ~30.9%
