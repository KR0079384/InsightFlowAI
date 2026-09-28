# src/models/

## Purpose
Defines the Pydantic data schemas, request/response models, evidence objects, and simulation payload structures for the TraceIQ API and internal decision engine.

## Files

### `schemas.py`
Contains type definitions and validation schemas:
- `MetricValue`: Deterministic metric representation with current/prior values and formatted representations.
- `DriverItem`: Root cause / variance contributor with impact estimation and evidence linkage.
- `EvidenceItem`: Verifiable evidence linking business claims to metrics, calculations, formula steps, and source rows.
- `RecommendationAction`: Prescriptive executive action with urgency and estimated recovery impact.
- `SimulationRequest` & `SimulationResponse`: Scenario what-if parameters and before-and-after outcome comparisons.
- `DecisionReport`: Unified executive decision payload returned by TraceIQ Decision Canvas API.
- `DatasetOverview`: High-level summary of ingested tables and record counts.

## Relationships
```text
schemas.py
  ├── Used by data_engine/ for typed calculations
  ├── Used by decision_engine/ for structured reports
  └── Used by main.py for FastAPI endpoint validation
```
