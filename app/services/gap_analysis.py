import json
from app.services import query_llm
from app.models.domain import Session
from app.core.logger import logger

class GapAnalysisService:
    async def analyze(self, session: Session, history_text: str) -> dict:
        """
        Re-evaluates which original gaps are still missing after considering the conversation.
        Returns: { "still_missing": [...], "answered": [...] }
        """
        if not session.missing_info:
            return {"still_missing": [], "answered": []}
        
        missing_list = ", ".join([f'"{item}"' for item in session.missing_info])
        
        prompt = f"""
        You are a medical AI assistant tracking information gaps.
        
        Original missing information needed: {missing_list}
        
        Conversation History:
        {history_text}
        
        Task: Review the conversation and determine which items from the original missing_info list have been clearly answered by the user.
        
        IMPORTANT: If the user has provided information that broadly addresses the topic of a gap, mark it as answered even if the wording differs. Be generous in your interpretation — the goal is to track what information has been gathered, not to demand exact keyword matches.
        
        Return ONLY a JSON object:
        {{
            "still_missing": ["list of items still not answered"],
            "answered": ["list of items that were answered"]
        }}
        """
        
        try:
            response_text = await query_llm(prompt)
            response_text = response_text.replace("```json", "").replace("```", "").strip()
            data = json.loads(response_text)
            
            still_missing = data.get("still_missing", [])
            answered = data.get("answered", [])
            
            # Fallback only if the LLM returns a malformed type (e.g., a string instead of a list).
            # An empty list is valid — it means all gaps are resolved.
            if not isinstance(still_missing, list):
                still_missing = session.missing_info
            if not isinstance(answered, list):
                answered = []
            
            logger.debug(f"Gap analysis: {len(answered)} answered, {len(still_missing)} still missing")
            
            return {
                "still_missing": still_missing,
                "answered": answered
            }
        except Exception as e:
            logger.error(f"Gap analysis failed: {e}")
            # Fallback: keep original gaps
            return {
                "still_missing": session.missing_info,
                "answered": []
            }
