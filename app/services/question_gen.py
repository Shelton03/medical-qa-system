from app.services import query_llm
from app.models.domain import Session

class QuestionGenerator:
    async def generate_next_question(self, session: Session, history_text: str) -> str:
        prompt = f"""
        You are a medical AI.
        Context:
        - Identified Gaps: {session.missing_info}
        - Risk Flags: {session.risk_flags}
        
        Conversation History:
        {history_text}
        
        Task: Generate the SINGLE most important next question to ask the user to clarify their condition or rule out risks.
        Be polite, professional, and concise. Do not number the question.
        """
        
        question = await query_llm(prompt)
        return question.strip()
