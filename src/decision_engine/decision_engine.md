# src/decision_engine/

## Purpose
Orchestrates the TraceIQ **Observe → Explain → Recommend → Simulate** workflow. Bridges user questions and intents with deterministic calculation engines, synthesizes executive answers, attaches verifiable evidence records, and produces decision reports.

## Files

### `intent.py`
Natural language intent classifier & parameter extractor. Identifies whether the query relates to revenue decline analysis, stock-out investigations, product performance comparisons, anomaly detection, or scenario simulations. Maps product aliases to verified catalog IDs, extracts numerical simulation parameters, and returns an `unknown` intent for off-topic/ambiguous queries.

### `evidence.py`
Builds verifiable evidence objects:
- Links claims to exact formulas (`(current - previous) / previous`).
- Identifies participating data sources (`orders.csv`, `inventory.csv`, `products.csv`, `marketing.csv`).
- Extracts verifiable sample rows showing timestamps, quantities, and raw prices.

### `llm.py`
Local LLM synthesis module for TraceIQ using local Ollama (`qwen3:8b`). Constructs grounded prompts from verified deterministic context, validates generated numerical claims against input context, and handles connection failures/timeouts gracefully.

### `engine.py`
Primary decision orchestration engine:
- Ingests user query.
- Executes deterministic calculations from `data_engine/metrics.py` and `data_engine/drivers.py`.
- Delegates narrative synthesis to `llm.py` with dependency injection, falling back to deterministic template strings if Ollama is unavailable, times out, or fails grounding validation.
- Links structured evidence and generates prescriptive recommendations with default simulation parameters.

## Relationships
```text
intent.py ──> engine.py <── evidence.py
                 │
                 ├──> src/data_engine/metrics.py
                 ├──> src/data_engine/drivers.py
                 └──> src/data_engine/simulator.py
```

## Agent Notes
- The Decision Engine enforces the core principle: *LLM proposes, data engine proves.*
- No analytical claim can be emitted without an attached deterministic EvidenceItem.
