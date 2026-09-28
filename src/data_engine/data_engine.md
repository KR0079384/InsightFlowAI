# src/data_engine/

## Purpose
Contains the core deterministic computation and analytical data layer of TraceIQ. All calculations, metrics, driver decompositions, and simulation models are executed here deterministically with zero numerical hallucination.

## Files

### `loader.py`
In-memory singleton data provider that loads and indexes `orders.csv`, `inventory.csv`, `products.csv`, `suppliers.csv`, `marketing.csv`, and `customers.csv`. Standardizes datetime fields and validates data integrity.

### `metrics.py`
Contains deterministic business metric calculators:
- Monthly aggregated revenue.
- Revenue growth rate: `(current - previous) / previous`.
- Product-level revenue, units, variance, and out-of-stock counts.
- Catalog-level summary metrics.

### `anomalies.py`
Rule-based deterministic anomaly detector:
- `detect_stockouts`: Isolates consecutive zero-stock spans per SKU.
- `detect_marketing_anomalies`: Flags major shifts in channel marketing budgets and conversion efficiency.

### `drivers.py`
Variance decomposition engine that isolates exact negative and positive contributors to revenue fluctuations and associates each with structured evidence identifiers.

### `simulator.py`
Deterministic what-if scenario calculator. Simulates operational adjustments (reorder quantity increases, supplier lead time compression, price adjustments, marketing changes) and computes projected stockout reduction, recovered units, and revenue uplift.

## Relationships
```text
loader.py
  ├──> metrics.py ──┐
  ├──> anomalies.py ┼──> drivers.py ──> decision_engine/
  └──> simulator.py ┘
```

## Agent Notes
- LLMs must not perform business mathematics that this data engine handles.
- All formulas and calculations must remain deterministic and verifiable against source CSV rows.
