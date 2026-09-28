"""
Deterministic Data Generator for TraceIQ
Generates high-fidelity retail business datasets with controlled anomalies and drivers:
1. August 2026 Revenue: ~$130,000.00 ($13.0L equivalent)
2. September 2026 Revenue: ~$112,060.00 ($11.2L equivalent, exact -13.8% decline)
3. Primary Driver 1: PROD-001 (AeroMax Pro) sales fell 31.0% due to 8 stockout days (Sept 11-18)
4. Primary Driver 2: PROD-002 (PulseFit Smartwatch) sales fell 18.0% due to regional marketing reduction
5. High-performing / stable products: PROD-003, PROD-004, PROD-005
"""

import os
import random
import pandas as pd
from datetime import datetime, timedelta

def generate_all_datasets():
    os.makedirs(os.path.dirname(__file__), exist_ok=True)
    base_dir = os.path.dirname(__file__)
    
    # 1. PRODUCTS
    products_data = [
        {"product_id": "PROD-001", "name": "AeroMax Pro Headphones", "category": "Audio", "cost_price": 120.0, "unit_price": 250.0, "target_reorder_qty": 500, "lead_time_days": 10},
        {"product_id": "PROD-002", "name": "PulseFit Smartwatch", "category": "Wearables", "cost_price": 60.0, "unit_price": 130.0, "target_reorder_qty": 600, "lead_time_days": 7},
        {"product_id": "PROD-003", "name": "EchoSound Speaker", "category": "Audio", "cost_price": 35.0, "unit_price": 80.0, "target_reorder_qty": 400, "lead_time_days": 5},
        {"product_id": "PROD-004", "name": "ClearVision 4K Webcam", "category": "Accessories", "cost_price": 45.0, "unit_price": 100.0, "target_reorder_qty": 350, "lead_time_days": 6},
        {"product_id": "PROD-005", "name": "ErgoLift Laptop Stand", "category": "Accessories", "cost_price": 20.0, "unit_price": 50.0, "target_reorder_qty": 300, "lead_time_days": 4},
    ]
    df_products = pd.DataFrame(products_data)
    df_products.to_csv(os.path.join(base_dir, "products.csv"), index=False)

    # 2. SUPPLIERS
    suppliers_data = [
        {"supplier_id": "SUPP-101", "name": "Apex Electronics Ltd", "product_id": "PROD-001", "avg_lead_days": 10, "reliability_score": 0.74, "on_time_rate": 0.68, "notes": "Experienced shipping delays in Sep 2026"},
        {"supplier_id": "SUPP-102", "name": "Zenith MicroTech", "product_id": "PROD-002", "avg_lead_days": 7, "reliability_score": 0.92, "on_time_rate": 0.95, "notes": "Stable supplier"},
        {"supplier_id": "SUPP-103", "name": "SonicCraft Audio", "product_id": "PROD-003", "avg_lead_days": 5, "reliability_score": 0.90, "on_time_rate": 0.91, "notes": "Stable supplier"},
        {"supplier_id": "SUPP-104", "name": "VisionWare Optical", "product_id": "PROD-004", "avg_lead_days": 6, "reliability_score": 0.88, "on_time_rate": 0.89, "notes": "Consistent deliveries"},
        {"supplier_id": "SUPP-105", "name": "Forma Ergonomics", "product_id": "PROD-005", "avg_lead_days": 4, "reliability_score": 0.95, "on_time_rate": 0.97, "notes": "Local partner"},
    ]
    df_suppliers = pd.DataFrame(suppliers_data)
    df_suppliers.to_csv(os.path.join(base_dir, "suppliers.csv"), index=False)

    # 3. CUSTOMERS
    random.seed(42)
    regions = ["North", "South", "East", "West"]
    segments = ["Enterprise", "SMB", "Consumer"]
    customers_data = []
    for i in range(1, 101):
        cid = f"CUST-{i:03d}"
        customers_data.append({
            "customer_id": cid,
            "name": f"Customer {i}",
            "segment": random.choice(segments),
            "region": random.choice(regions),
            "loyalty_tier": random.choice(["Platinum", "Gold", "Silver", "Bronze"])
        })
    df_customers = pd.DataFrame(customers_data)
    df_customers.to_csv(os.path.join(base_dir, "customers.csv"), index=False)

    # 4. ORDERS & INVENTORY (Aug 1 to Sep 30, 2026)
    # Aug: 31 days, Sep: 30 days
    # Target totals: Aug = $130,000.00, Sep = $112,060.00 (Exact -13.80% drop)
    # Breakdown August:
    # PROD-001: 236 units * $250 = $59,000
    # PROD-002: 300 units * $130 = $39,000
    # PROD-003: 200 units * $80  = $16,000
    # PROD-004: 100 units * $100 = $10,000
    # PROD-005: 120 units * $50  = $6,000
    # Total Aug = $130,000

    # Breakdown September:
    # PROD-001: 163 units * $250 = $40,750 (-30.93% drop, 8 stockout days Sep 11-18)
    # PROD-002: 246 units * $130 = $31,980 (-18.0% drop)
    # PROD-003: 201 units * $80  = $16,080 (+0.5%)
    # PROD-004: 168 units * $100 = $16,800 (+68% bump due to office return)
    # PROD-005: 129 units * $50  = $6,450 (+7.5%)
    # Total Sep = $40,750 + $31,980 + $16,080 + $16,800 + $6,450 = $112,060 (Exact 13.80% decline)

    orders = []
    order_id_counter = 1000

    # Distribute August orders (Aug 1 - Aug 31)
    aug_targets = {"PROD-001": 236, "PROD-002": 300, "PROD-003": 200, "PROD-004": 100, "PROD-005": 120}
    for day in range(1, 32):
        d_str = f"2026-08-{day:02d}"
        for pid, total_units in aug_targets.items():
            # Daily units
            daily_u = total_units // 31
            if day <= (total_units % 31):
                daily_u += 1
            if daily_u > 0:
                p_info = next(p for p in products_data if p["product_id"] == pid)
                cust = random.choice(customers_data)
                orders.append({
                    "order_id": f"ORD-{order_id_counter}",
                    "order_date": d_str,
                    "customer_id": cust["customer_id"],
                    "product_id": pid,
                    "quantity": daily_u,
                    "unit_price": p_info["unit_price"],
                    "discount": 0.0,
                    "order_value": round(daily_u * p_info["unit_price"], 2),
                    "region": cust["region"],
                    "status": "Delivered"
                })
                order_id_counter += 1

    # Distribute September orders (Sep 1 - Sep 30)
    # Note: For PROD-001, days Sep 11 to Sep 18 are stockout days (0 units)
    sep_targets = {"PROD-001": 163, "PROD-002": 246, "PROD-003": 201, "PROD-004": 168, "PROD-005": 129}
    prod1_active_days = [d for d in range(1, 31) if not (11 <= d <= 18)] # 22 days active

    for day in range(1, 31):
        d_str = f"2026-09-{day:02d}"
        for pid, total_units in sep_targets.items():
            if pid == "PROD-001":
                if 11 <= day <= 18:
                    daily_u = 0 # Stockout!
                else:
                    active_idx = prod1_active_days.index(day)
                    daily_u = total_units // len(prod1_active_days)
                    if active_idx < (total_units % len(prod1_active_days)):
                        daily_u += 1
            else:
                daily_u = total_units // 30
                if day <= (total_units % 30):
                    daily_u += 1
            
            if daily_u > 0:
                p_info = next(p for p in products_data if p["product_id"] == pid)
                cust = random.choice(customers_data)
                # Adjust discount slightly on one item to hit exact target $112,060
                discount = 0.0
                orders.append({
                    "order_id": f"ORD-{order_id_counter}",
                    "order_date": d_str,
                    "customer_id": cust["customer_id"],
                    "product_id": pid,
                    "quantity": daily_u,
                    "unit_price": p_info["unit_price"],
                    "discount": discount,
                    "order_value": round(daily_u * p_info["unit_price"] * (1 - discount), 2),
                    "region": cust["region"],
                    "status": "Delivered"
                })
                order_id_counter += 1

    df_orders = pd.DataFrame(orders)
    df_orders.to_csv(os.path.join(base_dir, "orders.csv"), index=False)

    # 5. INVENTORY TRACKING (Aug 1 - Sep 30)
    inventory_rows = []
    # Initialize stock for each product
    current_stocks = {
        "PROD-001": 350,
        "PROD-002": 420,
        "PROD-003": 300,
        "PROD-004": 250,
        "PROD-005": 200,
    }

    start_date = datetime(2026, 8, 1)
    end_date = datetime(2026, 9, 30)
    cur_date = start_date

    while cur_date <= end_date:
        d_str = cur_date.strftime("%Y-%m-%d")
        for pid in products_data:
            p_id = pid["product_id"]
            # Check sales today
            day_orders = df_orders[(df_orders["order_date"] == d_str) & (df_orders["product_id"] == p_id)]
            units_sold = int(day_orders["quantity"].sum()) if not day_orders.empty else 0
            
            opening = current_stocks[p_id]
            received = 0
            
            # Stock replenishment schedule
            if d_str == "2026-08-15":
                received = 200
            elif d_str == "2026-09-01":
                if p_id != "PROD-001":
                    received = 250
            elif d_str == "2026-09-19" and p_id == "PROD-001":
                received = 300 # Delayed shipment finally arrived!
            elif d_str == "2026-09-20" and p_id != "PROD-001":
                received = 200
                
            # PROD-001 stockout logic
            if p_id == "PROD-001" and "2026-09-11" <= d_str <= "2026-09-18":
                closing = 0
                stock_out = True
            else:
                closing = max(0, opening + received - units_sold)
                stock_out = (closing == 0)
                
            current_stocks[p_id] = closing
            
            inventory_rows.append({
                "date": d_str,
                "product_id": p_id,
                "opening_stock": opening,
                "units_received": received,
                "units_sold": units_sold,
                "closing_stock": closing,
                "is_stock_out": 1 if stock_out else 0
            })
        cur_date += timedelta(days=1)

    df_inventory = pd.DataFrame(inventory_rows)
    df_inventory.to_csv(os.path.join(base_dir, "inventory.csv"), index=False)

    # 6. MARKETING DATA (Aug 1 - Sep 30)
    marketing_rows = []
    cur_date = start_date
    while cur_date <= end_date:
        d_str = cur_date.strftime("%Y-%m-%d")
        month = cur_date.month
        for p in products_data:
            p_id = p["product_id"]
            # In Sept, PROD-002 marketing budget was cut by 40%
            base_spend = 150.0
            if month == 9 and p_id == "PROD-002":
                base_spend = 75.0 # Budget cut
            elif month == 9 and p_id == "PROD-004":
                base_spend = 220.0 # Boosted for back-to-office
            
            spend = base_spend + random.uniform(-10, 10)
            cpc = 1.25
            clicks = int(spend / cpc)
            impressions = clicks * 25
            
            marketing_rows.append({
                "date": d_str,
                "product_id": p_id,
                "channel": random.choice(["Google Ads", "Meta Ads", "LinkedIn", "Newsletter"]),
                "spend": round(spend, 2),
                "impressions": impressions,
                "clicks": clicks,
                "conversions": int(clicks * 0.04)
            })
        cur_date += timedelta(days=1)
    df_marketing = pd.DataFrame(marketing_rows)
    df_marketing.to_csv(os.path.join(base_dir, "marketing.csv"), index=False)

    print("Demo dataset generated successfully in data/ folder!")

if __name__ == "__main__":
    generate_all_datasets()
