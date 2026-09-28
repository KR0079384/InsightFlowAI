import { DecisionReport, SimulationResponse, DatasetOverview, EvidenceItem } from '../types';

const API_BASE = '/api/v1';

export async function fetchOverview(): Promise<DatasetOverview> {
  const res = await fetch(`${API_BASE}/overview`);
  if (!res.ok) throw new Error('Failed to fetch dataset overview');
  return res.json();
}

export async function analyzeQuestion(question: string): Promise<DecisionReport> {
  const res = await fetch(`${API_BASE}/analyze`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ question }),
  });
  if (!res.ok) throw new Error('Failed to analyze question');
  return res.json();
}

export async function runSimulation(params: {
  product_id: string;
  reorder_quantity_delta_pct: number;
  lead_time_days_reduction: number;
  marketing_budget_delta_pct: number;
  price_change_pct: number;
}): Promise<SimulationResponse> {
  const res = await fetch(`${API_BASE}/simulate`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(params),
  });
  if (!res.ok) throw new Error('Failed to run simulation');
  return res.json();
}

export async function fetchEvidenceDetail(evidenceId: string): Promise<EvidenceItem> {
  const res = await fetch(`${API_BASE}/evidence/${encodeURIComponent(evidenceId)}`);
  if (!res.ok) throw new Error('Failed to fetch evidence details');
  return res.json();
}
