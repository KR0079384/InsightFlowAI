import json
import logging
import re
from typing import Dict, Any, List, Optional, Tuple
import httpx
from src.config import settings

logger = logging.getLogger(__name__)

class LLMSynthesizer:
    """
    Local LLM synthesis module for TraceIQ using local Ollama (qwen3:8b).
    Enforces grounded narrative generation:
    - Generates 'executive_answer' and 'why_explanation'.
    - Relies exclusively on deterministic context supplied to it.
    - Validates narrative against strict non-causal, grounded allowlist rules.
    - Performs 1-shot repair retry if narrative validation fails.
    - Gracefully fails over to deterministic fallback if Ollama is offline or invalid.
    """

    def __init__(self, base_url: Optional[str] = None, model_name: Optional[str] = None, timeout: float = 120.0):
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

    def validate_causation(self, narrative_text: str) -> bool:
        """
        Validates that narrative text does not assert unproven direct causation or unsupported inferences.
        Legacy helper maintained for backward compatibility.
        """
        if not narrative_text:
            return False
        causal_patterns = [
            r"\bprimary cause\b", r"\bcaused\b", r"\bdue to\b", r"\bbecause of\b", r"\bdriven by\b",
            r"\bresulted in\b", r"\bresulted from\b", r"\bdirectly impacted\b", r"\bcompounded by\b",
            r"\bled to\b", r"\bbrought about\b", r"\bresponsible for\b", r"\bcontributed to\b",
            r"\bcontributing to\b", r"\bwas caused\b", r"\bis the cause\b", r"\broot cause\b",
            r"\bcurtailed by\b", r"\bafter marketing spend\b", r"\bafter regional digital marketing\b",
            r"\bafter ad spend\b", r"\bsensitivity of sales\b", r"\bsales sensitivity\b",
            r"\breverse stockout-driven\b", r"\blead-time delay\b", r"\blead time delay\b",
            r"\bROI\b", r"\bcampaign effectiveness\b", r"\blinked to\b", r"\breorder buffer\b",
            r"\bextended lead time\b", r"\breduced visibility\b", r"\bconversions\b", r"\bboosts revenue\b"
        ]
        for pattern in causal_patterns:
            if re.search(pattern, narrative_text, re.IGNORECASE):
                return False
        return True

    def validate_narrative(
        self,
        exec_answer: Any,
        why_explanation: Any,
        context_payload: Dict[str, Any]
    ) -> Tuple[bool, List[str]]:
        """
        Strict centralized validator checking executive_answer and why_explanation together.
        Rejects complete narrative if any check fails.
        """
        errors = []

        if not isinstance(exec_answer, str) or not exec_answer.strip():
            errors.append("executive_answer must be a non-empty string.")
            return False, errors

        if not isinstance(why_explanation, str) or not why_explanation.strip():
            errors.append("why_explanation must be a non-empty string.")
            return False, errors

        # Reject raw serialized dict / list signatures in string output
        polluted_signatures = ["'summary':", "'key_actions':", "['", "':", "{'"]
        for p in polluted_signatures:
            if p in exec_answer or p in why_explanation:
                errors.append("Narrative contains raw code, dictionary, or list artifacts.")
                return False, errors

        full_text = f"{exec_answer} {why_explanation}"

        # 1. Explanation bullet count check (max 3 bullets)
        bullets = [b.strip() for b in why_explanation.split("\n") if b.strip()]
        if len(bullets) > 3:
            errors.append(f"why_explanation contains {len(bullets)} bullets, exceeding the 3-bullet maximum.")

        # 2. Unsupported Causal & Speculative Language check
        causal_patterns = [
            r"\bprimary cause\b",
            r"\bcaused\b",
            r"\bcauses\b",
            r"\bcausing\b",
            r"\bdue to\b",
            r"\bbecause of\b",
            r"\bdriven by\b",
            r"\bresulted in\b",
            r"\bresulted from\b",
            r"\bresulted\b",
            r"\bdirectly impacted\b",
            r"\bcompounded by\b",
            r"\bled to\b",
            r"\bleads to\b",
            r"\bbrought about\b",
            r"\bresponsible for\b",
            r"\bcontributed to\b",
            r"\bcontributing to\b",
            r"\bwas caused\b",
            r"\bis the cause\b",
            r"\broot cause\b",
            r"\bcurtailed by\b",
            r"\bafter marketing spend\b",
            r"\bafter regional digital marketing\b",
            r"\bafter ad spend\b",
            r"\breducing marketing spend caused\b",
            r"\bspend reduction caused\b",
            r"\bsales dropped due\b",
            r"\bsales decreased due\b",
            r"\bsales declined due\b",
            r"\bdue to supplier\b",
            r"\bdue to delayed\b",
            r"\bsupply chain failure caused\b",
            r"\bstockout caused\b",
            r"\bstock-out caused\b",
            r"\blead-time delay\b",
            r"\blead time delay\b",
            r"\blinked to\b",
            r"\blinked\b",
            r"\breorder buffer\b",
            r"\bextended lead time\b",
            r"\bextended lead times\b",
            r"\binsufficient reorder\b",
            r"\breduced visibility\b",
            r"\bconversions\b",
            r"\bconversion\b",
            r"\bvisibility\b",
            r"\bdirectly reduces\b",
            r"\breduces\b",
            r"\bboosts revenue\b",
            r"\bboosts\b"
        ]
        for cp in causal_patterns:
            if re.search(cp, full_text, re.IGNORECASE):
                errors.append(f"Contains unsupported causal claim matching pattern: '{cp}'")

        # 3. Unsupported Marketing Claims check
        marketing_patterns = [
            r"\bROI\b",
            r"\bcampaign effectiveness\b",
            r"\bsensitivity of sales\b",
            r"\bsales sensitivity\b",
            r"\bmarketing effectiveness\b"
        ]
        for mp in marketing_patterns:
            if re.search(mp, full_text, re.IGNORECASE):
                errors.append(f"Contains unsupported marketing claim matching pattern: '{mp}'")

        # 4. Simulation Certainty / Framing check
        sim_mention = any(k in full_text.lower() for k in ["simulation", "scenario", "reorder", "projected", "recovery"])
        sim_numbers = {40750.0, 55750.0, 15000.0}
        extracted_nums = self._extract_all_numbers(full_text)
        has_sim_number = any(n in sim_numbers for n in extracted_nums)

        if sim_mention or has_sim_number:
            framing_keywords = ["hypothetical", "projected", "scenario", "simulation", "estimate", "estimated", "potential", "what-if", "model"]
            if not any(fk in full_text.lower() for fk in framing_keywords):
                errors.append("Simulation figures or scenario references must use explicit hypothetical/projected framing.")

            certainty_patterns = [
                r"\beliminates stockouts\b",
                r"\beliminated stockouts\b",
                r"\breverses losses\b",
                r"\breverse stockout-driven\b",
                r"\bwill recover\b",
                r"\bgenerates recovered\b",
                r"\bproves\b",
                r"\bguarantees\b",
                r"\bboosts revenue\b",
                r"\bdirectly reduces\b"
            ]
            for cert in certainty_patterns:
                if re.search(cert, full_text, re.IGNORECASE):
                    errors.append(f"Simulation outcome asserts certainty matching pattern: '{cert}'")

        # 5. Numeric Grounding check
        context_numbers = self._extract_all_numbers(context_payload)
        if not self.validate_grounding(full_text, context_numbers):
            logger.warning("Ollama response rejected by validation: failed numeric grounding check.")
            errors.append("Narrative contains numerical values not found in approved deterministic context.")

        # 6. SKU / Entity ID check
        known_entities = {"PROD-001", "PROD-002", "PROD-003", "PROD-004", "SUPP-101"}
        found_entities = set(re.findall(r"PROD-\d+|SUPP-\d+", full_text))
        unknown_entities = found_entities - known_entities
        if unknown_entities:
            errors.append(f"Narrative contains ungrounded SKU or entity IDs: {unknown_entities}")

        is_valid = len(errors) == 0
        return is_valid, errors

    def build_system_prompt(self) -> str:
        return (
            "You are TraceIQ's executive narrative synthesis engine.\n"
            "Your task is to summarize verified business analysis based STRICTLY on the provided deterministic context.\n"
            "STRICT CONSTRAINTS:\n"
            "1. Use ONLY facts, figures, percentages, dates, and amounts explicitly provided in the context.\n"
            "2. Never calculate, infer, or invent any numbers, causes, recommendations, or evidence.\n"
            "3. Clearly distinguish HISTORICAL metrics (e.g., August $130,000 revenue, September $112,060 revenue) from SIMULATION metrics. Do NOT mix historical numbers with what-if scenario projections.\n"
            "4. Do NOT mix the simulation's projected figures (such as $40,750 or $55,750) with historical actual monthly revenue.\n"
            "5. Preserve exact evidence dates and figures (e.g., stockout period September 11 to September 18; marketing spend reduction of 51.6%). Never alter or approximate dates or percentages.\n"
            "6. Do NOT state or imply that events (such as ad spend reductions or stockouts) are proven primary causes, or that ad spend reductions 'contributed to', 'led to', or 'directly impacted' revenue declines. Describe observed relationships using strictly non-causal correlation language such as 'was associated with' or 'coincided with'.\n"
            "7. Do NOT infer or assert marketing effectiveness, campaign ROI, or 'sensitivity of sales to marketing investment' from correlation data alone.\n"
            "8. Always describe simulation scenario figures using hypothetical/projected terms (e.g., 'could potentially recover' or 'is projected to increase revenue by X in a hypothetical scenario'), and NEVER treat simulation projections as proven historical outcomes (e.g., do NOT say 'reverse stockout-driven losses').\n"
            "9. Ensure each explanation bullet point covers a distinct factor without repeating information across bullets. Return a concise executive_answer and NO MORE THAN 3 distinct explanation bullets in why_explanation.\n"
            "10. Return output strictly as a flat JSON object with EXACTLY two string fields: 'executive_answer' and 'why_explanation'. Both MUST be clean string values.\n"
            "Do NOT include <think> reasoning tags, markdown formatting, or extra text."
        )

    def _extract_context_dict(
        self,
        query: str,
        intent_metadata: Dict[str, Any],
        key_metrics: List[Any],
        drivers: List[Any],
        evidence_list: List[Any],
        simulation: Optional[Any] = None
    ) -> Dict[str, Any]:
        def serialize_item(obj):
            if hasattr(obj, "model_dump") and callable(getattr(obj, "model_dump")):
                return obj.model_dump()
            if hasattr(obj, "dict") and callable(getattr(obj, "dict")):
                return obj.dict()
            if hasattr(obj, "__dict__"):
                return obj.__dict__
            return obj

        return {
            "query": query,
            "intent": intent_metadata,
            "historical_actual_metrics": [serialize_item(m) for m in key_metrics],
            "drivers": [serialize_item(d) for d in drivers],
            "verifiable_evidence": [serialize_item(e) for e in evidence_list],
            "what_if_simulation_scenario": serialize_item(simulation) if simulation else None
        }

    def build_user_prompt(
        self,
        query: str,
        intent_metadata: Dict[str, Any],
        key_metrics: List[Any],
        drivers: List[Any],
        evidence_list: List[Any],
        simulation: Optional[Any] = None
    ) -> str:
        context_payload = self._extract_context_dict(query, intent_metadata, key_metrics, drivers, evidence_list, simulation)

        return (
            f"User Question: {query}\n\n"
            f"Verified Deterministic Context:\n"
            f"{json.dumps(context_payload, indent=2)}\n\n"
            f"Synthesize a concise executive_answer and non-redundant why_explanation JSON object (maximum 3 bullets) using ONLY the context above. "
            f"Keep historical actual metrics ($130,000 / $112,060) separate from simulation scenario projections."
        )

    def _extract_narrative_string(self, val: Any, is_explanation: bool = False) -> Optional[str]:
        """
        Extracts a clean, human-readable narrative string from str, list, or dict structures.
        Rejects raw serialized dictionaries, JSON strings, or Python code artifacts.
        Sanitizes non-ASCII Unicode characters to plain ASCII to prevent encoding corruption.
        Deduplicates repeated explanation bullets and caps explanations at 3 bullets.
        """
        if val is None:
            return None

        def sanitize_string(text: str) -> str:
            # Replace Unicode bullet and en-dash with plain ASCII
            return text.replace("•", "").replace("–", " to ").strip()

        # Handle string value
        if isinstance(val, str):
            cleaned = sanitize_string(val)
            # If string is encoded JSON or Python dict syntax, try parsing it first
            if (cleaned.startswith("{") and cleaned.endswith("}")) or (cleaned.startswith("[") and cleaned.endswith("]")):
                try:
                    parsed = json.loads(cleaned)
                    return self._extract_narrative_string(parsed, is_explanation=is_explanation)
                except Exception:
                    pass
            # Reject polluted strings containing raw dictionary syntax
            if "'summary':" in cleaned or "'key_actions':" in cleaned or "['" in cleaned or "':" in cleaned:
                return None
            return cleaned if cleaned else None

        # Handle list value
        if isinstance(val, list):
            extracted_items = []
            for item in val:
                item_str = self._extract_narrative_string(item, is_explanation=False)
                if item_str:
                    extracted_items.append(item_str)
            if not extracted_items:
                return None

            if is_explanation:
                # Format explanation list into clean, non-redundant bullet points (max 3 bullets) using plain ASCII dash
                bullets = []
                seen = set()
                for item in extracted_items:
                    clean_item = sanitize_string(item).lstrip("•- ")
                    norm_key = re.sub(r"\s+", " ", clean_item.lower())
                    if clean_item and norm_key not in seen:
                        seen.add(norm_key)
                        bullets.append(f"- {clean_item}")
                        if len(bullets) == 3:
                            break
                return "\n".join(bullets) if bullets else None
            else:
                # Join sentences for executive_answer
                return " ".join(extracted_items)

        # Handle dictionary value
        if isinstance(val, dict):
            # Known narrative keys in priority order
            narrative_keys = [
                "summary", "executive_answer", "executive_summary", "answer",
                "why_explanation", "explanation", "reasons", "details", "narrative",
                "description", "text", "content", "points", "drivers"
            ]

            # 1. Search for explicit narrative key inside dictionary
            for key in narrative_keys:
                if key in val:
                    extracted = self._extract_narrative_string(val[key], is_explanation=is_explanation)
                    if extracted:
                        return extracted

            # 2. Extract values from dict if all values are valid narrative strings (excluding metadata keys)
            valid_values = []
            for k, v in val.items():
                if k.lower() in ["key_actions", "actions", "metadata", "recommendations", "code", "status", "id"]:
                    continue
                extracted_v = self._extract_narrative_string(v, is_explanation=is_explanation)
                if extracted_v:
                    valid_values.append(extracted_v)

            if not valid_values:
                return None

            if is_explanation:
                bullets = []
                seen = set()
                for item in valid_values:
                    clean_item = sanitize_string(item).lstrip("•- ")
                    norm_key = re.sub(r"\s+", " ", clean_item.lower())
                    if clean_item and norm_key not in seen:
                        seen.add(norm_key)
                        bullets.append(f"- {clean_item}")
                        if len(bullets) == 3:
                            break
                return "\n".join(bullets) if bullets else None
            else:
                return " ".join(valid_values)

        return None

    def _parse_and_extract_response(self, content_str: str) -> Tuple[Optional[str], Optional[str], Optional[str]]:
        """Parses LLM response content string and extracts narrative fields."""
        if not content_str:
            logger.warning("Ollama API returned an empty content response.")
            return None, None, "Empty content response"

        clean_content = re.sub(r"<think>.*?</think>", "", content_str, flags=re.DOTALL).strip()
        clean_content = re.sub(r"^```(?:json)?\s*", "", clean_content)
        clean_content = re.sub(r"\s*```$", "", clean_content).strip()

        json_match = re.search(r"\{.*\}", clean_content, re.DOTALL)
        if json_match:
            clean_content = json_match.group(0)

        try:
            parsed_narrative = json.loads(clean_content)
            if isinstance(parsed_narrative, dict):
                logger.info("Ollama response returned valid JSON dict with keys: %s", list(parsed_narrative.keys()))
            else:
                logger.info("Ollama response returned valid JSON of non-dict type: %s", type(parsed_narrative).__name__)
        except json.JSONDecodeError as e:
            logger.warning("Ollama response failed JSON parsing: JSONDecodeError - %s", str(e))
            return None, None, "JSONDecodeError"

        if not isinstance(parsed_narrative, dict):
            logger.warning("Ollama response rejected by validation: root JSON payload is not a dictionary (%s).", type(parsed_narrative).__name__)
            return None, None, "Malformed JSON root object"

        if len(parsed_narrative) == 1:
            wrapper_key = list(parsed_narrative.keys())[0]
            if wrapper_key.lower() in ["response", "narrative", "data", "result", "analysis", "output"] and isinstance(parsed_narrative[wrapper_key], dict):
                logger.info("Unwrapping nested JSON container under key '%s'", wrapper_key)
                parsed_narrative = parsed_narrative[wrapper_key]

        raw_exec = parsed_narrative.get("executive_answer")
        if raw_exec is None:
            for alias in ["executive_summary", "answer", "summary"]:
                if alias in parsed_narrative:
                    raw_exec = parsed_narrative[alias]
                    break

        raw_why = parsed_narrative.get("why_explanation")
        if raw_why is None:
            for alias in ["explanation", "why", "reasons", "detailed_explanation"]:
                if alias in parsed_narrative:
                    raw_why = parsed_narrative[alias]
                    break

        logger.info(
            "Ollama response narrative raw field types: executive_answer=%s, why_explanation=%s",
            type(raw_exec).__name__,
            type(raw_why).__name__
        )

        exec_answer = self._extract_narrative_string(raw_exec, is_explanation=False)
        why_explanation = self._extract_narrative_string(raw_why, is_explanation=True)

        if not exec_answer or not why_explanation:
            logger.warning(
                "Ollama response rejected by validation: missing or unparseable narrative fields (executive_answer type: %s, why_explanation type: %s).",
                type(raw_exec).__name__,
                type(raw_why).__name__
            )
            return None, None, "Invalid or missing narrative fields"

        return exec_answer.strip(), why_explanation.strip(), None

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
        Enforces centralized validation and 1-shot repair retry.
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
        context_payload = self._extract_context_dict(query, intent_metadata, key_metrics, drivers, evidence_list, simulation)

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
        timeout_config = httpx.Timeout(self.timeout, connect=3.0)

        try:
            with httpx.Client(timeout=timeout_config) as client:
                response = client.post(url, json=payload)
                if response.status_code != 200:
                    logger.warning("Ollama API request failed with HTTP status %s from endpoint %s", response.status_code, url)
                    fallback_signal["error"] = f"HTTP {response.status_code}"
                    return fallback_signal

                res_json = response.json()
                content_str = res_json.get("message", {}).get("content", "")

                exec_answer, why_explanation, parse_err = self._parse_and_extract_response(content_str)
                if parse_err:
                    fallback_signal["error"] = parse_err
                    return fallback_signal

                is_valid, validation_errors = self.validate_narrative(exec_answer, why_explanation, context_payload)
                if is_valid:
                    logger.info("Ollama response successfully passed all validation checks.")
                    return {
                        "success": True,
                        "executive_answer": exec_answer,
                        "why_explanation": why_explanation,
                        "error": None
                    }

                # Validation failed -> Attempt 1-Shot Repair Retry
                logger.warning("Ollama response failed narrative validation: %s. Attempting 1-shot repair retry...", validation_errors)

                retry_user_prompt = (
                    f"Your previous narrative response was REJECTED by strict validation due to errors:\n"
                    + "\n".join(f"- {err}" for err in validation_errors) + "\n\n"
                    f"Regenerate executive_answer and why_explanation (maximum 3 bullets) strictly resolving these errors.\n"
                    f"Rules: NO causal words ('primary cause', 'due to', 'driven by', 'resulted from', 'linked to', 'reduced visibility', 'conversions'). Label simulation as hypothetical scenario. Use only numbers in approved context.\n"
                    f"Approved Context:\n"
                    f"{json.dumps(context_payload, indent=2)}"
                )

                retry_payload = {
                    "model": self.model_name,
                    "messages": [
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt},
                        {"role": "assistant", "content": content_str},
                        {"role": "user", "content": retry_user_prompt}
                    ],
                    "stream": False,
                    "format": "json"
                }

                retry_resp = client.post(url, json=retry_payload)
                if retry_resp.status_code != 200:
                    logger.warning("Ollama 1-shot retry request failed with HTTP status %s", retry_resp.status_code)
                    fallback_signal["error"] = f"Retry HTTP {retry_resp.status_code}"
                    return fallback_signal

                retry_json = retry_resp.json()
                retry_content = retry_json.get("message", {}).get("content", "")
                r_exec, r_why, r_parse_err = self._parse_and_extract_response(retry_content)

                if r_parse_err:
                    logger.warning("Ollama 1-shot retry parsing failed: %s", r_parse_err)
                    fallback_signal["error"] = f"Retry parse error: {r_parse_err}"
                    return fallback_signal

                r_is_valid, r_errors = self.validate_narrative(r_exec, r_why, context_payload)
                if r_is_valid:
                    logger.info("Ollama 1-shot repair retry successfully passed validation.")
                    return {
                        "success": True,
                        "executive_answer": r_exec,
                        "why_explanation": r_why,
                        "error": None
                    }

                logger.warning("Ollama response failed validation after 1-shot repair retry: %s. Triggering fallback.", r_errors)
                fallback_signal["error"] = "Validation failed after retry"
                return fallback_signal

        except (httpx.RequestError, httpx.TimeoutException, Exception) as e:
            logger.warning("Ollama API call error: %s - %s", type(e).__name__, str(e))
            fallback_signal["error"] = str(type(e).__name__)
            return fallback_signal

llm_synthesizer = LLMSynthesizer()
