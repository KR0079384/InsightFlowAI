# frontend/src/api/

## Purpose
Network client layer managing asynchronous HTTP communication between the React Decision Canvas UI and the FastAPI backend.

## Files

### `client.ts`
API functions:
- `fetchOverview()`: Retrieves summary of tables and total records.
- `analyzeQuestion(question)`: Dispatches natural language business queries to `/api/v1/analyze`.
- `runSimulation(params)`: Executes what-if scenario parameter adjustments via `/api/v1/simulate`.
- `fetchEvidenceDetail(evidenceId)`: Retrieves full calculation steps and source rows for an evidence claim.

## Relationships
```text
client.ts ──(HTTP Fetch)──> FastAPI backend /api/v1/*
```
