import pytest
from src.data_engine.simulator import simulator_engine
from src.models.schemas import SimulationRequest

def test_simulation_reorder_increase():
    req = SimulationRequest(
        product_id="PROD-001",
        reorder_quantity_delta_pct=20.0,
        lead_time_days_reduction=3,
        marketing_budget_delta_pct=0.0,
        price_change_pct=0.0
    )
    res = simulator_engine.run_simulation(req)
    assert res.stockout_days_simulated < res.stockout_days_current
    assert res.projected_revenue_simulated > res.projected_revenue_current
    assert res.projected_revenue_delta > 0
    assert "PROD-001" in res.product_id
    assert len(res.metrics) >= 4
