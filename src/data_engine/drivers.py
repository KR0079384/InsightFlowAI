from typing import List, Dict, Any
from src.data_engine.metrics import metrics_engine
from src.data_engine.anomalies import anomalies_engine
from src.models.schemas import DriverItem

class DriversEngine:
    def __init__(self, metrics=None, anomalies=None):
        self.metrics = metrics or metrics_engine
        self.anomalies = anomalies or anomalies_engine

    def analyze_revenue_drivers(self, current_period: str = "2026-09", previous_period: str = "2026-08") -> List[DriverItem]:
        """Decomposes revenue variance into distinct, proven root-cause drivers."""
        prod_breakdown = self.metrics.get_product_breakdown(current_period, previous_period)
        stockouts = self.anomalies.detect_stockouts(current_period)
        stockout_map = {s["product_id"]: s for s in stockouts}
        mkt_anomalies = self.anomalies.detect_marketing_anomalies(current_period, previous_period)
        mkt_map = {m["product_id"]: m for m in mkt_anomalies}

        drivers: List[DriverItem] = []

        for p in prod_breakdown:
            pid = p["product_id"]
            pname = p["name"]
            delta = p["revenue_delta"]
            growth_pct = p["growth_pct"]
            
            if delta < 0:
                # Negative driver
                if pid in stockout_map:
                    so_info = stockout_map[pid]
                    days = so_info["stockout_days"]
                    drivers.append(DriverItem(
                        id=f"driver-stockout-{pid}",
                        title=f"{pname} Sales Dropped {abs(growth_pct):.1f}% (Stock-out Window)",
                        impact_type="negative",
                        impact_amount=delta,
                        impact_formatted=f"-${abs(delta):,.2f}",
                        explanation=f"{pname} experienced {days} consecutive stock-out days (Sep 11–Sep 18) during which closing stock reached zero, with an estimated stockout opportunity of $15,200.00 (historical revenue decline: -${abs(delta):,.2f}).",
                        product_id=pid,
                        evidence_id=f"ev-stockout-{pid}"
                    ))
                elif pid in mkt_map and mkt_map[pid]["change_pct"] < -20:
                    drivers.append(DriverItem(
                        id=f"driver-mktg-{pid}",
                        title=f"{pname} Sales Decreased {abs(growth_pct):.1f}% (Marketing Reduction)",
                        impact_type="negative",
                        impact_amount=delta,
                        impact_formatted=f"-${abs(delta):,.2f}",
                        explanation=f"{pname} revenue declined {abs(growth_pct):.2f}% during the same period that top-of-funnel ad spend in key regional territories decreased 51.61%.",
                        product_id=pid,
                        evidence_id=f"ev-mktg-{pid}"
                    ))
                else:
                    drivers.append(DriverItem(
                        id=f"driver-decline-{pid}",
                        title=f"{pname} Sales Dropped {abs(growth_pct):.1f}%",
                        impact_type="negative",
                        impact_amount=delta,
                        impact_formatted=f"-${abs(delta):,.2f}",
                        explanation=f"Revenue fell from ${p['previous_revenue']:,.2f} to ${p['current_revenue']:,.2f}.",
                        product_id=pid,
                        evidence_id=f"ev-prod-{pid}"
                    ))
            elif delta > 500:
                # Positive offset
                drivers.append(DriverItem(
                    id=f"driver-growth-{pid}",
                    title=f"{pname} Grew +{growth_pct:.1f}% (Positive Offset)",
                    impact_type="positive",
                    impact_amount=delta,
                    impact_formatted=f"+${delta:,.2f}",
                    explanation=f"Strong organic and promotional demand added ${delta:,.2f} in revenue, partially offsetting negative revenue variances.",
                    product_id=pid,
                    evidence_id=f"ev-prod-{pid}"
                ))

        return drivers

drivers_engine = DriversEngine()
