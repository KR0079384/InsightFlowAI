# data/

## Purpose
Contains the raw deterministic business datasets used by TraceIQ for ingestion, metric calculations, anomaly detection, evidence extraction, and scenario simulation.

## Files

### `generate_demo_data.py`
Deterministic data generation script. Seeds reproducible retail datasets (Aug 2026 – Sep 2026) with explicit business events:
- Overall monthly revenue drop from $130,000 (Aug) to $112,060 (Sep), reflecting a **-13.80% decline**.
- 8 stock-out days on **PROD-001 (AeroMax Pro Headphones)** due to supplier delivery delay from Apex Electronics (`SUPP-101`), causing a 30.93% drop in product sales.
- Marketing reduction on **PROD-002 (PulseFit Smartwatch)** causing an 18.0% drop in sales.

### `orders.csv`
Transaction log of retail orders.
- Columns: `order_id`, `order_date`, `customer_id`, `product_id`, `quantity`, `unit_price`, `discount`, `order_value`, `region`, `status`.

### `products.csv`
Master product catalog with pricing and lead times.
- Columns: `product_id`, `name`, `category`, `cost_price`, `unit_price`, `target_reorder_qty`, `lead_time_days`.

### `inventory.csv`
Daily inventory ledger tracking stock movements.
- Columns: `date`, `product_id`, `opening_stock`, `units_received`, `units_sold`, `closing_stock`, `is_stock_out`.

### `suppliers.csv`
Supplier directory with delivery reliability metrics.
- Columns: `supplier_id`, `name`, `product_id`, `avg_lead_days`, `reliability_score`, `on_time_rate`, `notes`.

### `marketing.csv`
Daily ad channel spend and campaign conversions.
- Columns: `date`, `product_id`, `channel`, `spend`, `impressions`, `clicks`, `conversions`.

### `customers.csv`
Customer cohort and segment profiles.
- Columns: `customer_id`, `name`, `segment`, `region`, `loyalty_tier`.

## Relationships
```text
customers.csv ──┐
                ├──> orders.csv <─── products.csv <─── suppliers.csv
marketing.csv ──┘         │                 │
                          ▼                 ▼
                   inventory.csv <──────────┘
```

## Agent Notes
- All mathematical metrics must be computed deterministically directly from these files.
- Never hardcode or fabricate values outside what is derived from this data layer.
