import json
from app.services import query_llm
from app.models.domain import Session
from app.core.logger import logger

class AssessmentService:
    async def perform_initial_assessment(self, session: Session, user_text: str, processed_input: dict) -> Session:
        """
        Performs initial triage/assessment to identify candidate domains, risks, and gaps.
        """
        prompt = f"""
        Perform an initial medical assessment based on this input.
        User Input: "{user_text}"
        Extracted Symptoms: {processed_input.get('symptoms')}
        
        Return ONLY a JSON object with:
        - candidate_domains (list of strings, e.g., "Cardiology", "Gastroenterology")
        - key_symptoms (list of strings)
        - missing_info (list of strings - what critical info is missing?)
        - risk_flags (list of strings - red flags e.g., "chest pain", "difficulty breathing")

        JSON:
        """
        
        try:
            response_text = await query_llm(prompt)
            response_text = response_text.replace("```json", "").replace("```", "").strip()
            data = json.loads(response_text)
            
            session.candidate_domains = data.get("candidate_domains", [])
            session.key_symptoms = data.get("key_symptoms", [])
            session.missing_info = data.get("missing_info", [])
            session.risk_flags = data.get("risk_flags", [])
            session.assessment_done = True
            
            # Initial simplistic gap count
            session.gaps_remaining = len(session.missing_info)
            
        except Exception as e:
            logger.error(f"Assessment failed: {e}")
            # Fallback
            session.assessment_done = True
            
        return session
