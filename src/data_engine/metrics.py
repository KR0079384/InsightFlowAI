from typing import Dict, Any, List, Optional
import pandas as pd
from src.data_engine.loader import loader
from src.models.schemas import MetricValue

class MetricsEngine:
    def __init__(self, data_loader=None):
        self.loader = data_loader or loader

    def get_monthly_revenue(self) -> Dict[str, float]:
        """Calculates total revenue aggregated by year_month."""
        if self.loader.orders.empty:
            return {}
        rev_by_month = self.loader.orders.groupby("year_month")["order_value"].sum().to_dict()
        return {k: round(float(v), 2) for k, v in rev_by_month.items()}

    def get_revenue_growth(self, current_period: str = "2026-09", previous_period: str = "2026-08") -> Dict[str, Any]:
        """Calculates revenue growth rate between two periods deterministically."""
        rev_map = self.get_monthly_revenue()
        curr_rev = rev_map.get(current_period, 0.0)
        prev_rev = rev_map.get(previous_period, 0.0)
        
        if prev_rev == 0.0:
            growth_pct = 0.0
        else:
            growth_pct = ((curr_rev - prev_rev) / prev_rev) * 100.0

        return {
            "current_period": current_period,
            "previous_period": previous_period,
            "current_revenue": curr_rev,
            "previous_revenue": prev_rev,
            "delta_amount": round(curr_rev - prev_rev, 2),
            "growth_pct": round(growth_pct, 2),
            "formatted_change": f"{growth_pct:+.2f}%",
            "calculation_str": f"SUM(order_value[{current_period}]) - SUM(order_value[{previous_period}]) / SUM(order_value[{previous_period}])",
            "formula": f"({curr_rev:,.2f} - {prev_rev:,.2f}) / {prev_rev:,.2f} = {growth_pct:+.2f}%"
        }

    def get_product_breakdown(self, current_period: str = "2026-09", previous_period: str = "2026-08") -> List[Dict[str, Any]]:
        """Calculates product-level performance, variance, and stockout metrics."""
        orders = self.loader.orders
        products = self.loader.products
        inventory = self.loader.inventory

        results = []
        for _, prod in products.iterrows():
            pid = prod["product_id"]
            pname = prod["name"]
            
            # Aug / Sep revenue & units
            curr_orders = orders[(orders["product_id"] == pid) & (orders["year_month"] == current_period)]
            prev_orders = orders[(orders["product_id"] == pid) & (orders["year_month"] == previous_period)]
            
            curr_rev = float(curr_orders["order_value"].sum()) if not curr_orders.empty else 0.0
            prev_rev = float(prev_orders["order_value"].sum()) if not prev_orders.empty else 0.0
            curr_units = int(curr_orders["quantity"].sum()) if not curr_orders.empty else 0
            prev_units = int(prev_orders["quantity"].sum()) if not prev_orders.empty else 0
            
            # Stockout days
            curr_inv = inventory[(inventory["product_id"] == pid) & (inventory["year_month"] == current_period)]
            stockout_days = int(curr_inv["is_stock_out"].sum()) if not curr_inv.empty else 0

            growth_pct = ((curr_rev - prev_rev) / prev_rev * 100.0) if prev_rev > 0 else 0.0
            rev_delta = curr_rev - prev_rev

            results.append({
                "product_id": pid,
                "name": pname,
                "category": prod["category"],
                "unit_price": float(prod["unit_price"]),
                "current_revenue": round(curr_rev, 2),
                "previous_revenue": round(prev_rev, 2),
                "revenue_delta": round(rev_delta, 2),
                "growth_pct": round(growth_pct, 2),
                "current_units": curr_units,
                "previous_units": prev_units,
                "stockout_days": stockout_days
            })

        # Sort by largest negative revenue delta (most declining first)
        results.sort(key=lambda x: x["revenue_delta"])
        return results

    def get_key_metrics_summary(self, current_period: str = "2026-09", previous_period: str = "2026-08") -> List[MetricValue]:
        """Returns structured Key Metrics for the Decision Canvas."""
        growth = self.get_revenue_growth(current_period, previous_period)
        prod_breakdown = self.get_product_breakdown(current_period, previous_period)
        
        # Total stockout days across catalog
        total_stockout_days = sum(p["stockout_days"] for p in prod_breakdown)
        
        # Order volume
        curr_orders_count = len(self.loader.orders[self.loader.orders["year_month"] == current_period])
        prev_orders_count = len(self.loader.orders[self.loader.orders["year_month"] == previous_period])
        orders_change_pct = ((curr_orders_count - prev_orders_count) / prev_orders_count * 100.0) if prev_orders_count > 0 else 0.0

        return [
            MetricValue(
                name="Monthly Revenue",
                key="monthly_revenue",
                current_value=growth["current_revenue"],
                previous_value=growth["previous_revenue"],
                change_pct=growth["growth_pct"],
                unit="$",
                formatted=f"${growth['current_revenue']:,.2f}",
                description=f"Revenue changed by {growth['growth_pct']:+.2f}% compared to previous month (${growth['previous_revenue']:,.2f})"
            ),
            MetricValue(
                name="Revenue Growth Rate",
                key="revenue_growth_rate",
                current_value=growth["growth_pct"],
                previous_value=0.0,
                change_pct=growth["growth_pct"],
                unit="%",
                formatted=f"{growth['growth_pct']:+.2f}%",
                description="Month-over-Month topline change"
            ),
            MetricValue(
                name="Stock-out Days",
                key="stockout_days",
                current_value=float(total_stockout_days),
                previous_value=0.0,
                change_pct=100.0 if total_stockout_days > 0 else 0.0,
                unit="days",
                formatted=f"{total_stockout_days} days",
                description="Total out-of-stock days experienced across all catalog SKUs"
            ),
            MetricValue(
                name="Completed Orders",
                key="completed_orders",
                current_value=float(curr_orders_count),
                previous_value=float(prev_orders_count),
                change_pct=round(orders_change_pct, 2),
                unit="orders",
                formatted=f"{curr_orders_count:,}",
                description="Total completed customer purchase transactions"
            )
        ]

metrics_engine = MetricsEngine()
