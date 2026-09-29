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

### `test_intent.py`
Unit test suite for natural language intent classification:
- Tests multiple natural language formulations for `revenue_decline_analysis`, `stockout_analysis`, `product_performance`, `simulation`, and `anomaly_detection`.
- Validates product alias mapping to catalog IDs (`PROD-001` through `PROD-005`).
- Verifies explicit percentage parameter extraction for simulation queries.
- Tests safe fallback to `unknown` intent for ambiguous, off-topic, or empty queries.

### `test_llm.py`
Unit test suite for local Ollama LLM synthesizer:
- Tests grounded prompt generation, valid narrative parsing, connection failure fallback, request timeouts, malformed JSON handling, and ungrounded number rejection.

### `test_engine.py`
Unit test suite for `DecisionEngine` orchestration:
- Validates LLM dependency injection, exception handling, and unknown intent behavior.

### `test_api.py`
Integration tests for FastAPI endpoints:
- `GET /api/v1/health`
- `GET /api/v1/overview`
- `POST /api/v1/analyze` (supported queries, LLM synthesis success, LLM fallback, unsupported queries)
- `POST /api/v1/simulate`

## Running Tests
```bash
pytest tests/ -v
```
