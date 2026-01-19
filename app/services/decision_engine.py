import json
import asyncio
from app.services import query_llm
from app.models.domain import Session
from app.core.config import settings
from app.core.logger import logger
from typing import Dict, Any

class DecisionEngine:
    async def evaluate(self, session: Session, history_text: str) -> Dict[str, Any]:
        """
        Analyzes the full conversation to decide the next action (ASK/ANSWER)
        and synthesizes a complete, updated state of the session.
        Returns a dictionary with the decision, confidence, and a state_update object.
        """
        
        prompt = f"""
        You are a medical AI assistant and state synthesizer.
        Your task is to analyze the full conversation history and the current session state
        to decide the next action and provide a complete, updated summary of all known facts.

        Current Session State:
        - Key Symptoms: {session.key_symptoms}
        - Risk Flags: {session.risk_flags}
        - Missing Info: {session.missing_info}

        Full Conversation History:
        {history_text}

        Tasks:
        1.  Synthesize the FULL list of key symptoms, risk flags, and missing information based on the ENTIRE conversation. For example, if the assistant asked "Do you have a fever?" and the user replied "Yes", you must add "fever" to the list of key symptoms.
        2.  Decide if you have enough information to provide a safe answer, or if you must ask more questions. Prefer to ASK if there is ambiguity or risk.
        
        Return ONLY a JSON object in this exact format:
        {{
            "decision": "ASK" or "ANSWER",
            "confidence": <float between 0.0 and 1.0>,
            "rationale": "<short reason for your decision>",
            "state_update": {{
                "key_symptoms": ["<list of ALL symptoms>"],
                "missing_info": ["<list of what is now missing>"],
                "risk_flags": ["<list of ALL identified risk flags>"]
            }}
        }}
        """
        
        # For this critical task, we will do a single, high-quality LLM call.
        # Self-consistency could be re-introduced by running this whole process N times,
        # but merging N different state_updates is complex. A single strong call is better here.
        try:
            response_text = await query_llm(prompt)
            response_text = response_text.replace("```json", "").replace("```", "").strip()
            data = json.loads(response_text)
            
            # Basic validation
            if "decision" not in data or "state_update" not in data:
                raise ValueError("LLM response is missing required fields.")
            
            logger.debug(f"Decision Engine synthesized data: {data}")
            
        except Exception as e:
            logger.error(f"Decision Engine parsing or execution error: {e}")
            # Fallback to a safe default: ASK and don't change the state
            return {
                "decision": "ASK",
                "confidence": 0.0,
                "rationale": "Fell back to safety default due to an internal error.",
                "state_update": {
                    "key_symptoms": session.key_symptoms,
                    "missing_info": session.missing_info,
                    "risk_flags": session.risk_flags
                }
            }

        # Apply Abstention Logic
        avg_confidence = float(data.get("confidence", 0.0))
        final_decision = data.get("decision", "ASK").upper()
        
        if avg_confidence < settings.CONFIDENCE_THRESHOLD:
            final_decision = "ASK"
        
        if data.get("state_update", {}).get("missing_info"):
             final_decision = "ASK"

        session.confidence = avg_confidence
        data["decision"] = final_decision # Ensure the final decision is in the returned dict
        
        return data
