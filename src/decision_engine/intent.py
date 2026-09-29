import re
from typing import Dict, Any, Optional

class IntentClassifier:
    """
    Natural-language question understanding and intent classification layer.
    Classifies user queries into deterministic business decision intents:
    - revenue_decline_analysis: Revenue drop, sales contraction, root causes, drivers
    - stockout_analysis: Inventory depletion, out-of-stock days, supply delays
    - product_performance: SKU breakdown, product revenue, top/worst performing items
    - simulation: What-if scenarios, reorder quantity adjustments, safety stock changes
    - anomaly_detection: Unusual variance, inventory/marketing budget anomalies
    - unknown: Ambiguous, off-topic, or unsupported questions
    """

    # Exact product ID mapping aligned with data/products.csv
    PRODUCT_MAP = {
        "PROD-001": ["prod-001", "aeromax pro headphones", "aeromax pro", "aeromax", "headphone", "headphones", "headset"],
        "PROD-002": ["prod-002", "pulsefit smartwatch", "pulsefit", "smartwatch", "watch"],
        "PROD-003": ["prod-003", "echosound speaker", "echosound", "speaker", "speakers"],
        "PROD-004": ["prod-004", "clearvision 4k webcam", "clearvision webcam", "clearvision", "webcam", "camera"],
        "PROD-005": ["prod-005", "ergolift laptop stand", "ergolift stand", "ergolift", "laptop stand", "stand"],
    }

    # Semantic pattern regexes for intent matching
    SIMULATION_PATTERNS = [
        r"\bsimulat(e|ion|ing)\b",
        r"\bwhat[\s\-]*if\b",
        r"\bscenario\b",
        r"\breorder\s*(quantity|qty|amount)?\b",
        r"\bsafety\s*stock\b",
        r"\bincrease\s*reorder\b",
        r"\bdecrease\s*reorder\b",
        r"\bcut\s*lead\s*time\b",
        r"\breplenish(ment)?\s*scenario\b",
        r"\bmarketing\s*budget\s*(delta|increase|decrease)\b",
        r"\bprice\s*(change|adjust|elasticity)\b",
    ]

    STOCKOUT_PATTERNS = [
        r"\bstock[\s\-]*out(s)?\b",
        r"\bout\s*of\s*stock\b",
        r"\binventory\s*(depletion|shortage|issue|count)\b",
        r"\bran\s*out\s*of\b",
        r"\bzero\s*stock\b",
        r"\bsupply\s*(delay|bottleneck)\b",
        r"\bbackorder(s)?\b",
    ]

    PRODUCT_PERFORMANCE_PATTERNS = [
        r"\bproduct(s)?\s*(performance|breakdown|revenue|sales)\b",
        r"\bsku(s)?\s*(performance|breakdown|revenue|sales)\b",
        r"\b(top|worst|declining|best)\s*product(s)?\b",
        r"\bproduct(s)?\s*are\s*performing\b",
        r"\b(performing|selling)\s*(worst|best|poorly|well)\b",
        r"\bhow\s*is\s*([a-z0-9\s]+)\s*(doing|performing|selling)\b",
        r"\bsales\s*by\s*(product|sku)\b",
        r"\bcompare\s*product(s)?\b",
        r"\bitem(s)?\s*performance\b",
    ]

    ANOMALY_PATTERNS = [
        r"\banomal(y|ies)\b",
        r"\bvariance(s)?\b",
        r"\bunusual\s*(drop|spike|variance|change|spend)\b",
        r"\bunexpected\s*(drop|spend|shift|decline|change)\b",
        r"\bspend\s*shift(s)?\b",
        r"\b(marketing|budget)\s*shift(s)?\b",
        r"\boutlier(s)?\b",
        r"\birregularit(y|ies)\b",
    ]

    REVENUE_DECLINE_PATTERNS = [
        r"\b(revenue|sales|top[\s\-]*line|income|topline)\s*(and\s*\w+\s*)?(to\s*)?(decline|declined|declines|drop|dropped|drops|fall|fell|fallen|loss|losses|decrease|decreased|decreases|down|contraction|contracted|slump|slumped|plummet|plummeted|plummeting)\w*\b",
        r"\b(decline|declined|declines|drop|dropped|drops|fall|fell|fallen|loss|losses|decrease|decreased|decreases|down|slump|slumped|plummet|plummeted)\s*(in|of)?\s*(revenue|sales|top[\s\-]*line|income|topline)\b",
        r"\bwhy\s*(did|are|is|were)\s*(our\s*)?(revenue|sales|top[\s\-]*line|topline)?\b",
        r"\bwhat\s*caused\s*(our\s*)?(revenue|sales|top[\s\-]*line|topline)?\b",
        r"\b(revenue|sales|top[\s\-]*line|topline)\s*to\s*(decrease|drop|fall|decline|plummet|slump)\b",
        r"\broot\s*cause(s)?\b",
        r"\bdriver(s)?\b",
        r"\bmain\s*cause(s)?\b",
        r"\bmonth\s*over\s*month\s*(drop|decline)\b",
        r"\bseptember\s*(revenue|sales)\b",
        r"\blosing\s*money\b",
    ]

    def _extract_product_id(self, query_lower: str) -> Optional[str]:
        """Maps query tokens to verified product IDs in products.csv."""
        for pid, aliases in self.PRODUCT_MAP.items():
            for alias in aliases:
                if alias in query_lower:
                    return pid
        return None

    def _extract_reorder_percentage(self, query: str) -> float:
        """
        Unambiguously extracts numerical percentage parameter (e.g., 25%, 15.5 percent, 20 pct).
        Uses 'percent\b' and 'pct\b' word boundary assertions while allowing '%' without \b
        (since % is non-word \W in regex and not followed by \w word characters).
        """
        match = re.search(r"(\d+(?:\.\d+)?)\s*(?:%|percent\b|pct\b)", query, re.IGNORECASE)
        if match:
            return float(match.group(1))
        return 20.0

    def classify(self, query: str) -> Dict[str, Any]:
        """
        Classifies natural-language business questions into actionable intent specifications.
        Returns 'unknown' intent if the query is ambiguous, off-topic, or unsupported.
        """
        if not query or not query.strip():
            return {
                "intent": "unknown",
                "confidence": 0.0,
                "reason": "Query is empty or whitespace-only."
            }

        q = query.lower().strip()
        # Preserve decimal points in numbers and hyphens (like top-line), strip sentence punctuation
        q_clean = re.sub(r"[?!,:;\"']", " ", q)
        q_clean = " ".join(q_clean.split())

        pid = self._extract_product_id(q_clean)

        # Score all pattern categories
        sim_matches = sum(1 for pattern in self.SIMULATION_PATTERNS if re.search(pattern, q_clean))
        stockout_matches = sum(1 for pattern in self.STOCKOUT_PATTERNS if re.search(pattern, q_clean))
        anomaly_matches = sum(1 for pattern in self.ANOMALY_PATTERNS if re.search(pattern, q_clean))
        prod_matches = sum(1 for pattern in self.PRODUCT_PERFORMANCE_PATTERNS if re.search(pattern, q_clean))
        revenue_matches = sum(1 for pattern in self.REVENUE_DECLINE_PATTERNS if re.search(pattern, q_clean))

        # If a specific product is mentioned without explicit metric keywords, default to product_performance
        if pid and prod_matches == 0 and revenue_matches == 0 and stockout_matches == 0 and anomaly_matches == 0 and sim_matches == 0:
            prod_matches += 1

        # Select highest-scoring intent
        scores = {
            "simulation": sim_matches,
            "stockout_analysis": stockout_matches,
            "anomaly_detection": anomaly_matches,
            "product_performance": prod_matches,
            "revenue_decline_analysis": revenue_matches
        }

        best_intent = max(scores, key=scores.get)
        best_score = scores[best_intent]

        if best_score > 0:
            if best_intent == "simulation":
                pct = self._extract_reorder_percentage(q_clean)
                return {
                    "intent": "simulation",
                    "product_id": pid or "PROD-001",
                    "reorder_delta_pct": pct,
                    "primary_metric": "projected_revenue",
                    "confidence": min(1.0, 0.85 + (sim_matches * 0.05))
                }
            elif best_intent == "stockout_analysis":
                return {
                    "intent": "stockout_analysis",
                    "product_id": pid or ("PROD-001" if ("aeromax" in q_clean or "headphone" in q_clean) else None),
                    "primary_metric": "stockout_days",
                    "confidence": min(1.0, 0.85 + (stockout_matches * 0.05))
                }
            elif best_intent == "anomaly_detection":
                return {
                    "intent": "anomaly_detection",
                    "product_id": pid,
                    "period": "2026-09",
                    "primary_metric": "anomaly_count",
                    "confidence": min(1.0, 0.80 + (anomaly_matches * 0.05))
                }
            elif best_intent == "product_performance":
                return {
                    "intent": "product_performance",
                    "product_id": pid or ("PROD-001" if ("headphone" in q_clean or "aeromax" in q_clean) else None),
                    "primary_metric": "product_revenue",
                    "confidence": min(1.0, 0.80 + (prod_matches * 0.05))
                }
            elif best_intent == "revenue_decline_analysis":
                return {
                    "intent": "revenue_decline_analysis",
                    "product_id": pid,
                    "period": "2026-09",
                    "comparison": "2026-08",
                    "primary_metric": "revenue_growth",
                    "confidence": min(1.0, 0.85 + (revenue_matches * 0.05))
                }

        # Safe fallback for ambiguous or unsupported questions
        return {
            "intent": "unknown",
            "confidence": 0.0,
            "reason": "Query does not match supported business intents (revenue decline, stockouts, product performance, simulations, anomalies)."
        }

intent_classifier = IntentClassifier()
