import json
from app.services import query_llm
from app.models.domain import Session

class AnswerGenerator:
    async def generate_answer(self, session: Session, history_text: str) -> dict:
        """
        Generates final answer, explanation, and disclaimer.
        """
        prompt = f"""
        You are a medical AI assistant.
        Context:
        - Risk Flags: {session.risk_flags}
        - Confidence: {session.confidence}
        
        Conversation History:
        {history_text}
        
        Task: Provide a final medical assessment/answer based on the info gathered.
        
        Return ONLY a JSON object:
        {{
            "content": "<The main advice/answer>",
            "explanation": "<Detailed reasoning>",
            "disclaimer": "<Appropriate medical disclaimer, e.g., 'This is not a diagnosis...'>",
            "confidence_level": "high" | "medium" | "low"
        }}
        """
        
        try:
            response = await query_llm(prompt)
            response = response.replace("```json", "").replace("```", "").strip()
            data = json.loads(response)
            return data
        except Exception:
            # Fallback
            return {
                "content": "I apologize, but I cannot provide a definitive answer at this time. Please consult a doctor.",
                "explanation": "Processing error occurred.",
                "disclaimer": "Medical advice should be sought from a professional.",
                "confidence_level": "low"
            }
