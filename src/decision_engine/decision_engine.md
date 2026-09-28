# src/decision_engine/

## Purpose
Orchestrates the TraceIQ **Observe → Explain → Recommend → Simulate** workflow. Bridges user questions and intents with deterministic calculation engines, synthesizes executive answers, attaches verifiable evidence records, and produces decision reports.

## Files

### `intent.py`
Natural language intent classifier & parameter extractor. Identifies whether the query relates to revenue decline analysis, stock-out investigations, product performance comparisons, or scenario simulations.

### `evidence.py`
Builds verifiable evidence objects:
- Links claims to exact formulas (`(current - previous) / previous`).
- Identifies participating data sources (`orders.csv`, `inventory.csv`, `products.csv`, `marketing.csv`).
- Extracts verifiable sample rows showing timestamps, quantities, and raw prices.

### `engine.py`
Primary decision orchestration engine:
- Ingests user query.
- Executes deterministic calculations from `data_engine/metrics.py` and `data_engine/drivers.py`.
- Formulates high-level Executive Answer and Root-Cause Why breakdown.
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
