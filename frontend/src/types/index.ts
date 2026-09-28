export interface MetricValue {
  name: string;
  key: string;
  current_value: number;
  previous_value?: number | null;
  change_pct?: number | null;
  unit: string;
  formatted: string;
  description: string;
}

export interface DriverItem {
  id: string;
  title: string;
  impact_type: 'negative' | 'positive' | 'neutral';
  impact_amount: number;
  impact_formatted: string;
  explanation: string;
  product_id?: string | null;
  evidence_id: string;
}

export interface EvidenceItem {
  id: string;
  claim: string;
  metric: string;
  period: string;
  comparison?: string | null;
  calculation: string;
  formula: string;
  source_files: string[];
  sample_rows: Record<string, any>[];
  confidence_score: number;
}

export interface RecommendationAction {
  id: string;
  title: string;
  description: string;
  urgency: 'high' | 'medium' | 'low';
  expected_impact: string;
  estimated_revenue_recovery: number;
  action_type: string;
  default_parameters: Record<string, any>;
}

export interface SimulationScenarioMetric {
  name: string;
  current: string;
  simulated: string;
  difference: string;
  is_positive: boolean;
}

export interface SimulationResponse {
  scenario_title: string;
  product_id: string;
  product_name: string;
  parameters_applied: Record<string, any>;
  metrics: SimulationScenarioMetric[];
  projected_revenue_current: number;
  projected_revenue_simulated: number;
  projected_revenue_delta: number;
  stockout_days_current: number;
  stockout_days_simulated: number;
  executive_summary: string;
  evidence_link: string;
}

export interface DecisionReport {
  query: string;
  executive_answer: string;
  why_explanation: string;
  key_metrics: MetricValue[];
  drivers: DriverItem[];
  recommendation: RecommendationAction;
  evidence_list: EvidenceItem[];
  default_simulation: SimulationResponse;
  timestamp: string;
}

export interface DatasetOverview {
  total_orders: number;
  total_revenue: number;
  active_products: number;
  date_range: string;
  datasets: Record<string, number>;
}
