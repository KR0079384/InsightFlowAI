import json
import re
from typing import Dict, Any, List, Optional
import httpx
from src.config import settings

class LLMSynthesizer:
    """
    Local LLM synthesis module for TraceIQ using local Ollama (qwen3:8b).
    Enforces grounded narrative generation:
    - Generates 'executive_answer' and 'why_explanation'.
    - Relies exclusively on deterministic context supplied to it.
    - Validates generated business numbers against input context.
    - Gracefully fails over if Ollama is disconnected, times out, or returns ungrounded data.
    """

    def __init__(self, base_url: Optional[str] = None, model_name: Optional[str] = None, timeout: float = 10.0):
        self.base_url = (base_url or settings.OLLAMA_BASE_URL).rstrip("/")
        self.model_name = model_name or settings.OLLAMA_MODEL
        self.timeout = timeout

    def _extract_all_numbers(self, data: Any) -> set:
        """Recursively extracts all float/int numeric values from structured data or strings."""
        numbers = set()

        if isinstance(data, (int, float)):
            val = round(abs(float(data)), 2)
            numbers.add(val)
            if val.is_integer():
                numbers.add(int(val))
        elif isinstance(data, str):
            found = re.findall(r"[-+]?\d+(?:\.\d+)?", data.replace(",", ""))
            for f in found:
                try:
                    val = round(abs(float(f)), 2)
                    numbers.add(val)
                    if val.is_integer():
                        numbers.add(int(val))
                except ValueError:
                    pass
        elif isinstance(data, dict):
            for v in data.values():
                numbers.update(self._extract_all_numbers(v))
        elif isinstance(data, (list, tuple)):
            for item in data:
                numbers.update(self._extract_all_numbers(item))
        elif hasattr(data, "model_dump") and callable(getattr(data, "model_dump")):
            numbers.update(self._extract_all_numbers(data.model_dump()))
        elif hasattr(data, "dict") and callable(getattr(data, "dict")):
            numbers.update(self._extract_all_numbers(data.dict()))
        elif hasattr(data, "__dict__"):
            numbers.update(self._extract_all_numbers(data.__dict__))

        return numbers

    def validate_grounding(self, narrative_text: str, context_numbers: set) -> bool:
        """
        Validates that numerical values in generated narrative exist in context_numbers.
        Allows common formatting, calendar dates (1-31), year numbers (2026), and bullet indices.
        Fails safely if ungrounded business metrics are introduced.
        """
        if not narrative_text:
            return False

        clean_text = narrative_text.replace(",", "")
        found_matches = re.findall(r"[-+]?\d+(?:\.\d+)?", clean_text)

        for match in found_matches:
            try:
                num = round(abs(float(match)), 2)
                # Allow matching context number
                if num in context_numbers:
                    continue
                # Allow calendar dates 1-31, year 2026, or bullet counts 1-10
                if num.is_integer() and (1 <= int(num) <= 31 or int(num) == 2026):
                    continue
                return False
            except ValueError:
                continue

        return True

    def validate_narrative(
        self,
        exec_answer: str,
        why_explanation: str,
        context_payload: Dict[str, Any],
    ) -> tuple[bool, List[str]]:
        # """
        # Validates an LLM-generated narrative before it can be accepted.

        # The LLM is not allowed to:
        # - introduce unsupported business numbers
        # - assert unsupported causality
        # - introduce unsupported recommendations
        # - make guarantees about simulations or outcomes

        # Returns:
        #     (True, []) when the narrative is safe.
        #     (False, [errors]) when validation fails.
        # """
        errors: List[str] = []

        if not exec_answer or not why_explanation:
            errors.append("Missing required narrative fields")
            return False, errors

        full_text = f"{exec_answer} {why_explanation}"

        # ---------------------------------------------------------
        # 1. Numeric grounding
        # ---------------------------------------------------------
        context_numbers = self._extract_all_numbers(context_payload)

        if not self.validate_grounding(full_text, context_numbers):
            errors.append(
                "Narrative contains numeric values not present in deterministic context"
            )

        # ---------------------------------------------------------
        # 2. Unsupported causal claims
        # ---------------------------------------------------------
        causal_patterns = [
            r"\bprimary cause\b",
            r"\bmain cause\b",
            r"\broot cause\b",
            r"\bcaused by\b",
            r"\bdue to\b",
            r"\bresulted from\b",
            r"\bresulting from\b",
            r"\bled to\b",
            r"\blead to\b",
            r"\bdriven by\b",
            r"\bcaused\b",
            r"\bcontributed to\b",
            r"\bcompounded by\b",
            r"\blinked to\b",
            r"\bbecause of\b",
        ]

        lowered_text = full_text.lower()

        for pattern in causal_patterns:
            if re.search(pattern, lowered_text):
                errors.append(
                    f"Unsupported causal language detected: {pattern}"
                )

        # ---------------------------------------------------------
        # 3. Unsupported recommendation / outcome claims
        # ---------------------------------------------------------
        unsafe_outcome_patterns = [
            r"\bguarantees?\b",
            r"\beliminates?\b",
            r"\bdirectly reduces?\b",
            r"\bboosts revenue\b",
            r"\brecovers revenue\b",
            r"\bimproves roi\b",
            r"\bwill recover\b",
            r"\bwill eliminate\b",
            r"\bwill increase\b",
            r"\bwill reduce\b",
        ]

        for pattern in unsafe_outcome_patterns:
            if re.search(pattern, lowered_text):
                errors.append(
                    f"Unsupported outcome/recommendation language detected: {pattern}"
                )

        return len(errors) == 0, errors
    
    def build_system_prompt(self) -> str:
        return (
            "You are TraceIQ's executive narrative synthesis engine.\n"
            "Your task is to summarize verified business analysis based STRICTLY on the provided deterministic context.\n"
            "STRICT CONSTRAINTS:\n"
            "1. Use ONLY facts, figures, percentages, and amounts explicitly provided in the context.\n"
            "2. Never calculate, infer, or invent any numbers, causes, recommendations, or evidence.\n"
            "3. If the context is empty or insufficient, explicitly state that insufficient data is available.\n"
            "4. Return output strictly in valid JSON format with keys: 'executive_answer' and 'why_explanation'.\n"
            "Do NOT include code block markdown syntax."
        )

    def build_user_prompt(
        self,
        query: str,
        intent_metadata: Dict[str, Any],
        key_metrics: List[Any],
        drivers: List[Any],
        evidence_list: List[Any],
        simulation: Optional[Any] = None
    ) -> str:
        def serialize_item(obj):
            if hasattr(obj, "model_dump") and callable(getattr(obj, "model_dump")):
                return obj.model_dump()
            if hasattr(obj, "dict") and callable(getattr(obj, "dict")):
                return obj.dict()
            if hasattr(obj, "__dict__"):
                return obj.__dict__
            return obj

        context_payload = {
            "query": query,
            "intent": intent_metadata,
            "key_metrics": [serialize_item(m) for m in key_metrics],
            "drivers": [serialize_item(d) for d in drivers],
            "evidence_list": [serialize_item(e) for e in evidence_list],
            "simulation": serialize_item(simulation) if simulation else None
        }

        return (
            f"User Question: {query}\n\n"
            f"Verified Deterministic Context:\n"
            f"{json.dumps(context_payload, indent=2)}\n\n"
            f"Synthesize an executive_answer and detailed why_explanation JSON object using ONLY the context above."
        )

    def synthesize(
        self,
        query: str,
        intent_metadata: Dict[str, Any],
        key_metrics: List[Any],
        drivers: List[Any],
        evidence_list: List[Any],
        simulation: Optional[Any] = None
    ) -> Dict[str, Any]:
        """
        Executes Ollama synthesis call via local HTTP endpoint.
        Returns {'success': True, 'executive_answer': str, 'why_explanation': str} or fallback signal.
        """
        fallback_signal = {
            "success": False,
            "executive_answer": None,
            "why_explanation": None,
            "error": None
        }

        if not query or intent_metadata.get("intent") == "unknown":
            return fallback_signal

        user_prompt = self.build_user_prompt(query, intent_metadata, key_metrics, drivers, evidence_list, simulation)
        system_prompt = self.build_system_prompt()

        payload = {
            "model": self.model_name,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            "stream": False,
            "format": "json"
        }

        url = f"{self.base_url}/api/chat"

        try:
            with httpx.Client(timeout=self.timeout) as client:
                response = client.post(url, json=payload)
                if response.status_code != 200:
                    fallback_signal["error"] = f"HTTP {response.status_code}"
                    return fallback_signal

                res_json = response.json()
                content_str = res_json.get("message", {}).get("content", "")
                if not content_str:
                    fallback_signal["error"] = "Empty content response"
                    return fallback_signal

                clean_content = re.sub(r"^```(?:json)?\s*", "", content_str.strip())
                clean_content = re.sub(r"\s*```$", "", clean_content)

                parsed_narrative = json.loads(clean_content)
                exec_answer = parsed_narrative.get("executive_answer")
                why_explanation = parsed_narrative.get("why_explanation")

                if not exec_answer or not why_explanation:
                    fallback_signal["error"] = "Missing required narrative fields"
                    return fallback_signal

            context_payload = {
                "metrics": key_metrics,
                "drivers": drivers,
                "evidence": evidence_list,
                "simulation": simulation,
                "intent": intent_metadata,
            }

            is_valid, validation_errors = self.validate_narrative(
                exec_answer=exec_answer,
                why_explanation=why_explanation,
                context_payload=context_payload,
            )

            if not is_valid:
                if any(
                    "numeric values not present" in error
                    for error in validation_errors
                ):
                    fallback_signal["error"] = "Numeric grounding validation failed"
                else:
                    fallback_signal["error"] = "Narrative validation failed"

                return fallback_signal

            return {
                "success": True,
                "executive_answer": str(exec_answer),
                "why_explanation": str(why_explanation),
                "error": None,
            }

        except (httpx.RequestError, httpx.TimeoutException, json.JSONDecodeError, Exception) as e:
            fallback_signal["error"] = str(type(e).__name__)
            return fallback_signal

llm_synthesizer = LLMSynthesizer()
