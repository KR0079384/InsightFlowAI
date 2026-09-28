# src/

## Purpose
Root backend directory for TraceIQ. Implements the complete deterministic data engine, decision engine, evidence verification system, and FastAPI web service.

## Files

### `main.py`
Application entry point. Hosts the FastAPI REST API providing endpoints for health, dataset statistics, analytical query processing, verifiable evidence inspection, scenario simulation, and product catalog lookup.

### `config.py`
Application configuration, file paths, CORS policies, and environment variable management.

## Subdirectories

### [`models/`](file:///k:/Projects/TraceIQ/src/models/models.md)
Contains Pydantic schemas and typed request/response models (`schemas.py`).

### [`data_engine/`](file:///k:/Projects/TraceIQ/src/data_engine/data_engine.md)
Contains deterministic calculation modules:
- `loader.py`: In-memory multi-table dataset manager.
- `metrics.py`: Deterministic revenue, growth, margin, and stockout metrics.
- `anomalies.py`: Rule-based inventory depletion and marketing variance detectors.
- `drivers.py`: Topline variance decomposition into root causes.
- `simulator.py`: What-if simulation engine.

### [`decision_engine/`](file:///k:/Projects/TraceIQ/src/decision_engine/decision_engine.md)
Contains high-level decision orchestration:
- `intent.py`: Question classification and parameter parsing.
- `evidence.py`: Evidence builder linking claims to metrics and raw source rows.
- `engine.py`: Orchestrator generating end-to-end Decision Canvas reports.

## Relationships
```text
main.py
  ├──> models/
  ├──> data_engine/
  └──> decision_engine/
```

## Agent Notes
- All mathematical operations must remain in `data_engine/` and never be delegated to non-deterministic models.
- Always update this navigation file when modifying or adding backend services.
