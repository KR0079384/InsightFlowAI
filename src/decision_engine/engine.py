from datetime import datetime
from typing import Dict, Any, Optional
from src.data_engine.metrics import metrics_engine
from src.data_engine.drivers import drivers_engine
from src.data_engine.simulator import simulator_engine
from src.decision_engine.evidence import evidence_engine
from src.decision_engine.intent import intent_classifier
from src.decision_engine.llm import llm_synthesizer
from src.models.schemas import (
    DecisionReport,
    RecommendationAction,
    SimulationRequest,
    SimulationResponse
)

class DecisionEngine:
    def __init__(self, metrics=None, drivers=None, evidence=None, simulator=None, intent=None, llm=None):
        self.metrics = metrics or metrics_engine
        self.drivers = drivers or drivers_engine
        self.evidence = evidence or evidence_engine
        self.simulator = simulator or simulator_engine
        self.intent = intent or intent_classifier
        self.llm = llm or llm_synthesizer

    def analyze_query(self, query: str) -> DecisionReport:
        """Processes a business question, orchestrating deterministic metrics, drivers, evidence, and simulations."""
        parsed_intent = self.intent.classify(query)
        
        # 5. Default Simulation baseline
        default_sim_req = SimulationRequest(
            product_id="PROD-001",
            reorder_quantity_delta_pct=20.0,
            lead_time_days_reduction=3,
            marketing_budget_delta_pct=0.0,
            price_change_pct=0.0
        )
        sim_response = self.simulator.run_simulation(default_sim_req)

        # Safe response for ambiguous or unsupported queries
        if parsed_intent.get("intent") == "unknown":
            return DecisionReport(
                query=query,
                executive_answer=(
                    "TraceIQ could not classify your query into a supported business decision topic. "
                    "Supported domains include: Revenue Decline & Root Cause Analysis, Stock-out & Inventory Depletion, "
                    "Product & SKU Performance, Anomalies & Variances, and What-If Scenario Simulations."
                ),
                why_explanation=(
                    "Your query does not match TraceIQ's supported business decision domains. Please rephrase your question around one of the following topics:\n"
                    "• Revenue Decline: 'Why did revenue drop in September?' or 'What drove the sales decline?'\n"
                    "• Stockouts: 'Which products ran out of stock?' or 'Show inventory depletion for AeroMax'\n"
                    "• Product Performance: 'How are AeroMax headphones performing?' or 'Show SKU breakdown'\n"
                    "• Simulations: 'What if we increase reorder quantity by 20%?'"
                ),
                key_metrics=[],
                drivers=[],
                recommendation=RecommendationAction(
                    id="rec-unsupported-000",
                    title="Rephrase Question Around Supported Business Domains",
                    description="No automated recommendation can be generated for unsupported or ambiguous questions.",
                    urgency="low",
                    expected_impact="N/A - Query outside supported scope",
                    estimated_revenue_recovery=0.0,
                    action_type="none",
                    default_parameters={}
                ),
                evidence_list=[],
                default_simulation=sim_response,
                timestamp=datetime.utcnow().isoformat() + "Z"
            )

        # 1. Deterministic Metrics
        key_metrics = self.metrics.get_key_metrics_summary(current_period="2026-09", previous_period="2026-08")
        growth_info = self.metrics.get_revenue_growth(current_period="2026-09", previous_period="2026-08")
        
        # 2. Proven Drivers
        driver_items = self.drivers.analyze_revenue_drivers(current_period="2026-09", previous_period="2026-08")
        
        # 3. Verifiable Evidence
        evidence_list = self.evidence.get_all_evidences()
        
        # 4. Recommendation Formulation
        recommendation = RecommendationAction(
            id="rec-replenish-aeromax-001",
            title="Prioritize Replenishment & Increase Safety Stock for AeroMax Pro Headphones",
            description="Increase baseline reorder quantity from 500 units to 600 units (+20%) and enforce expedited 7-day supplier SLA with Apex Electronics Ltd (SUPP-101) to eliminate stockout recurrence.",
            urgency="high",
            expected_impact="Recovers an estimated $18,250/mo by eliminating 8 stock-out days and fulfilling uncaptured customer demand.",
            estimated_revenue_recovery=18250.0,
            action_type="reorder",
            default_parameters={
                "product_id": "PROD-001",
                "reorder_quantity_delta_pct": 20.0,
                "lead_time_days_reduction": 3
            }
        )

        # 6. Executive Narrative (Deterministic Fallback Baseline)
        default_exec_answer = (
            f"September 2026 revenue declined by {abs(growth_info['growth_pct']):.2f}% "
            f"(${growth_info['current_revenue']:,.2f} vs ${growth_info['previous_revenue']:,.2f} in August). "
            f"The primary cause was an 8-day inventory stock-out on our flagship AeroMax Pro Headphones (PROD-001), "
            f"compounded by reduced top-of-funnel marketing for PulseFit Smartwatch."
        )

        default_why_explanation = (
            "• AeroMax Pro Headphones (PROD-001) sales dropped 30.93% (-$18,250) after inventory hit 0 from Sep 11 to Sep 18 due to supplier lead-time delay.\n"
            "• PulseFit Smartwatch (PROD-002) sales decreased 18.00% (-$7,020) after regional digital marketing spend was curtailed by 50%.\n"
            "• ClearVision 4K Webcam (+65.0% / +$6,500) and EchoSound Speaker (+2.5%) saw positive growth, partially offsetting top-line contraction."
        )

        exec_answer = default_exec_answer
        why_explanation = default_why_explanation

        # 7. LLM Narrative Synthesis (Grounded Narrative override)
        if self.llm:
            try:
                llm_res = self.llm.synthesize(
                    query=query,
                    intent_metadata=parsed_intent,
                    key_metrics=key_metrics,
                    drivers=driver_items,
                    evidence_list=evidence_list,
                    simulation=sim_response
                )
                if llm_res and llm_res.get("success") and llm_res.get("executive_answer") and llm_res.get("why_explanation"):
                    exec_answer = str(llm_res["executive_answer"]).strip()
                    why_explanation = str(llm_res["why_explanation"]).strip()
            except Exception:
                # Retain deterministic narrative fallback on any unexpected exception
                exec_answer = default_exec_answer
                why_explanation = default_why_explanation

        return DecisionReport(
            query=query,
            executive_answer=exec_answer,
            why_explanation=why_explanation,
            key_metrics=key_metrics,
            drivers=driver_items,
            recommendation=recommendation,
            evidence_list=evidence_list,
            default_simulation=sim_response,
            timestamp=datetime.utcnow().isoformat() + "Z"
        )

decision_engine = DecisionEngine()
