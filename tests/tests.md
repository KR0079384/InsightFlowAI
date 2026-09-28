# tests/

## Purpose
Automated test suite validating deterministic calculations, verifiable evidence schemas, scenario simulations, and FastAPI endpoints for TraceIQ.

## Files

### `test_metrics.py`
Validates deterministic mathematical computations:
- Exact monthly revenues for August ($130,000) and September ($112,060).
- Topline growth rate calculation (-13.80% decline).
- Product-level revenue declines and 8-day stockout count on `PROD-001`.

### `test_evidence.py`
Validates evidence structure integrity:
- Checks that evidence objects contain non-empty claims, metrics, formulas, source files, and sample rows.
- Validates 100% confidence scores on deterministic metrics.

### `test_simulator.py`
Tests scenario simulation calculations:
- Ensures increasing safety stock and reducing lead times yields fewer stockout days and positive revenue recovery.

### `test_api.py`
Integration tests for FastAPI endpoints:
- `GET /api/v1/health`
- `GET /api/v1/overview`
- `POST /api/v1/analyze`
- `POST /api/v1/simulate`

## Running Tests
```bash
pytest tests/ -v
```
