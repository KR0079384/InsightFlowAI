# TraceIQ Project Overview

## Product Identity
- **Name**: TraceIQ
- **Tagline**: Turn scattered business data into accurate answers and decisions you can trace.
- **Goal**: Decision-support intelligence system that analyzes structured business datasets, proves business claims through a deterministic calculation engine, links every claim to evidence, and provides what-if simulation capabilities.

## Architecture

```text
                 BUSINESS DATA
        CSV / Excel / Parquet / Relational
                       │
                       ▼
                DATA INGESTION
          (data/loader.py: Pandas / In-Memory)
                       │
                       ▼
             SCHEMA / ENTITY LAYER
                       │
                       ▼
              BUSINESS DATA LAYER
                       │
          ┌────────────┼────────────┐
          ▼            ▼            ▼
       METRICS      ANOMALIES    DATA QUALITY
       ENGINE        ENGINE         ENGINE
          │            │            │
          └────────────┼────────────┘
                       ▼
                DECISION ENGINE
          (LLM Synthesis + Intent Routing)
                       │
                       ▼
                EVIDENCE LAYER
      (Claim → Metric → Calculation → Source Rows)
                       │
                       ▼
          TRACEIQ DECISION CANVAS (UI)
```

## Directory Structure
- [`src/src.md`](file:///k:/Projects/TraceIQ/src/src.md): Backend API & analytical engines.
- [`data/data.md`](file:///k:/Projects/TraceIQ/data/data.md): Synthetic deterministic business dataset.
- [`frontend/frontend.md`](file:///k:/Projects/TraceIQ/frontend/frontend.md): Web frontend Decision Canvas.
- [`tests/tests.md`](file:///k:/Projects/TraceIQ/tests/tests.md): Test suite.

## Engineering Rules
1. LLMs must never perform business mathematics that the deterministic engine can prove.
2. Every major business claim must include structured evidence (claim, metric, periods, calculation, source data).
3. If evidence is lacking, state "Insufficient evidence" explicitly.
4. Keep navigation markdown files synchronized with code structure.
