import json
import asyncio
from app.services import query_llm
from app.models.domain import Session
from app.core.config import settings
from app.core.logger import logger

class DecisionEngine:
    async def evaluate(self, session: Session, history_text: str) -> str:
        """
        Determines whether to ASK (get more info) or ANSWER (provide advice).
        Uses self-consistency (majority vote/confidence aggregation).
        Returns: "ASK" or "ANSWER" and updates session.confidence.
        """
        
        prompt = f"""
        You are a medical AI assistant.
        Current Session Context:
        Risk Flags: {session.risk_flags}
        Missing Info: {session.missing_info}
        
        Conversation History:
        {history_text}
        
        Task: Decide if you have enough information to provide a safe and helpful medical answer, or if you need to ask more questions.
        If there are any high risk flags or ambiguity, prefer ASK.
        
        Return ONLY a JSON object:
        {{
            "decision": "ASK" or "ANSWER",
            "confidence": <float between 0.0 and 1.0>,
            "rationale": "<short reason>"
        }}
        """
        
        # Self-consistency loop
        tasks = [query_llm(prompt) for _ in range(settings.SELF_CONSISTENCY_RUNS)]
        results = await asyncio.gather(*tasks)
        
        ask_votes = 0
        answer_votes = 0
        total_confidence = 0.0
        valid_responses = 0
        
        for i, res in enumerate(results):
            try:
                res = res.replace("```json", "").replace("```", "").strip()
                data = json.loads(res)
                decision = data.get("decision", "ASK").upper()
                conf = float(data.get("confidence", 0.0))
                rationale = data.get("rationale", "No rationale provided.")
                
                logger.debug(f"Run {i+1}: {decision} (conf: {conf}) - {rationale}")
                
                if decision == "ANSWER":
                    answer_votes += 1
                else:
                    ask_votes += 1
                
                total_confidence += conf
                valid_responses += 1
            except Exception as e:
                logger.error(f"Decision parsing error: {e}")
        
        # Aggregation
        if valid_responses == 0:
            avg_confidence = 0.0
            final_decision = "ASK"
        else:
            avg_confidence = total_confidence / valid_responses
            # Majority vote
            if answer_votes > ask_votes:
                final_decision = "ANSWER"
            else:
                final_decision = "ASK"
        
        # Override by threshold or hard constraints
        if avg_confidence < settings.CONFIDENCE_THRESHOLD:
            final_decision = "ASK"
        
        # Strict Abstention: IF (confidence < 0.7) OR (gaps_remaining > 0): → ASK
        if session.gaps_remaining > 0:
             final_decision = "ASK"

        session.confidence = avg_confidence
        return final_decision
