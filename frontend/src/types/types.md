# frontend/src/types/

## Purpose
TypeScript interface definitions corresponding to the backend data models and analytical structures.

## Files

### `index.ts`
Exports core interfaces:
- `MetricValue`: Deterministic KPI representations.
- `DriverItem`: Root-cause items linked to evidence IDs.
- `EvidenceItem`: Verifiable evidence schemas with sample row arrays.
- `RecommendationAction`: Prescriptive executive decisions.
- `SimulationResponse` & `SimulationScenarioMetric`: What-if simulation outcome interfaces.
- `DecisionReport`: Complete Decision Canvas state.
- `DatasetOverview`: Ingested table statistics.

## Relationships
Used across all frontend UI components and API client calls.
