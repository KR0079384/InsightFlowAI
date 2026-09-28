from typing import List, Dict, Any
import pandas as pd
from src.data_engine.loader import loader

class AnomaliesEngine:
    def __init__(self, data_loader=None):
        self.loader = data_loader or loader

    def detect_stockouts(self, period: str = "2026-09") -> List[Dict[str, Any]]:
        """Identifies days and products where closing stock dropped to 0."""
        inv = self.loader.inventory
        if inv.empty:
            return []
        
        stockouts = inv[(inv["year_month"] == period) & (inv["is_stock_out"] == 1)]
        grouped = stockouts.groupby("product_id").agg(
            stockout_days=("date", "count"),
            start_date=("date", "min"),
            end_date=("date", "max")
        ).reset_index()

        results = []
        for _, row in grouped.iterrows():
            pid = row["product_id"]
            p_name = ""
            prod_row = self.loader.products[self.loader.products["product_id"] == pid]
            if not prod_row.empty:
                p_name = prod_row.iloc[0]["name"]
                
            results.append({
                "product_id": pid,
                "product_name": p_name,
                "stockout_days": int(row["stockout_days"]),
                "start_date": row["start_date"].strftime("%Y-%m-%d"),
                "end_date": row["end_date"].strftime("%Y-%m-%d"),
                "anomaly_type": "INVENTORY_DEPLETION"
            })
        return results

    def detect_marketing_anomalies(self, period: str = "2026-09", prev_period: str = "2026-08") -> List[Dict[str, Any]]:
        """Identifies significant shifts in marketing spend or conversion efficiency."""
        mkt = self.loader.marketing
        if mkt.empty:
            return []
            
        curr_mkt = mkt[mkt["year_month"] == period].groupby("product_id")["spend"].sum()
        prev_mkt = mkt[mkt["year_month"] == prev_period].groupby("product_id")["spend"].sum()
        
        anomalies = []
        for pid in curr_mkt.index:
            curr_s = curr_mkt.get(pid, 0.0)
            prev_s = prev_mkt.get(pid, 0.0)
            if prev_s > 0:
                change_pct = (curr_s - prev_s) / prev_s * 100.0
                if abs(change_pct) >= 25.0:
                    anomalies.append({
                        "product_id": pid,
                        "current_spend": round(curr_s, 2),
                        "previous_spend": round(prev_s, 2),
                        "change_pct": round(change_pct, 2),
                        "anomaly_type": "MARKETING_BUDGET_SHIFT"
                    })
        return anomalies

anomalies_engine = AnomaliesEngine()
