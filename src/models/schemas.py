from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field

class MetricValue(BaseModel):
    name: str
    key: str
    current_value: float
    previous_value: Optional[float] = None
    change_pct: Optional[float] = None
    unit: str = "$"
    formatted: str
    description: str

class DriverItem(BaseModel):
    id: str
    title: str
    impact_type: str = "negative" # "negative" | "positive" | "neutral"
    impact_amount: float
    impact_formatted: str
    explanation: str
    product_id: Optional[str] = None
    evidence_id: str

class EvidenceItem(BaseModel):
    id: str
    claim: str
    metric: str
    period: str
    comparison: Optional[str] = None
    calculation: str
    formula: str
    source_files: List[str]
    sample_rows: List[Dict[str, Any]]
    confidence_score: float = 1.0 # 1.0 = deterministic prove

class RecommendationAction(BaseModel):
    id: str
    title: str
    description: str
    urgency: str = "high" # "high" | "medium" | "low"
    expected_impact: str
    estimated_revenue_recovery: float
    action_type: str # "reorder" | "marketing_boost" | "supplier_escalate" | "pricing_adjust"
    default_parameters: Dict[str, Any]

class SimulationRequest(BaseModel):
    product_id: str = "PROD-001"
    reorder_quantity_delta_pct: float = Field(default=20.0, description="Percentage change in reorder qty")
    lead_time_days_reduction: int = Field(default=3, description="Days reduced from supplier lead time")
    marketing_budget_delta_pct: float = Field(default=0.0, description="Percentage change in ad budget")
    price_change_pct: float = Field(default=0.0, description="Percentage change in unit price")

class SimulationScenarioMetric(BaseModel):
    name: str
    current: str
    simulated: str
    difference: str
    is_positive: bool

class SimulationResponse(BaseModel):
    scenario_title: str
    product_id: str
    product_name: str
    parameters_applied: Dict[str, Any]
    metrics: List[SimulationScenarioMetric]
    projected_revenue_current: float
    projected_revenue_simulated: float
    projected_revenue_delta: float
    stockout_days_current: int
    stockout_days_simulated: int
    executive_summary: str
    evidence_link: str

class QueryRequest(BaseModel):
    question: str
    dataset_name: Optional[str] = "demo_retail"

class DecisionReport(BaseModel):
    query: str
    executive_answer: str
    why_explanation: str
    key_metrics: List[MetricValue]
    drivers: List[DriverItem]
    recommendation: RecommendationAction
    evidence_list: List[EvidenceItem]
    default_simulation: SimulationResponse
    timestamp: str

class DatasetOverview(BaseModel):
    total_orders: int
    total_revenue: float
    active_products: int
    date_range: str
    datasets: Dict[str, int]
