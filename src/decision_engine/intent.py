import re
from typing import Dict, Any

class IntentClassifier:
    def classify(self, query: str) -> Dict[str, Any]:
        q = query.lower().strip()
        
        # Check simulation intent
        if any(w in q for w in ["simulate", "what if", "scenario", "reorder quantity", "increase reorder"]):
            # Extract target product and percentage if mentioned
            reorder_match = re.search(r"(\d+)%", q)
            pct = float(reorder_match.group(1)) if reorder_match else 20.0
            pid = "PROD-001"
            if "smartwatch" in q or "pulsefit" in q or "prod-002" in q:
                pid = "PROD-002"
            return {
                "intent": "simulation",
                "product_id": pid,
                "reorder_delta_pct": pct,
                "primary_metric": "projected_revenue"
            }
        
        # Check stockout intent
        if any(w in q for w in ["stockout", "stock-out", "out of stock", "inventory", "stock level"]):
            return {
                "intent": "stockout_analysis",
                "product_id": "PROD-001" if "aeromax" in q or "headphone" in q or "prod-001" in q else None,
                "primary_metric": "stockout_days"
            }
            
        # Check product performance intent
        if any(w in q for w in ["product", "top product", "declining product", "sku", "headphone", "smartwatch", "webcam"]):
            return {
                "intent": "product_performance",
                "product_id": "PROD-001" if ("headphone" in q or "aeromax" in q) else None,
                "primary_metric": "product_revenue"
            }

        # Default is revenue decline / root cause decision intent
        return {
            "intent": "revenue_decline_analysis",
            "period": "2026-09",
            "comparison": "2026-08",
            "primary_metric": "revenue_growth"
        }

intent_classifier = IntentClassifier()
