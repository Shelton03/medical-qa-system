import json
from app.services import query_llm
from app.models.domain import Session
from app.core.logger import logger

class ConversationSummarizer:
    async def summarize(self, history_text: str) -> str:
        """
        Generates a 2-3 sentence patient-friendly summary of the conversation.
        Returns fallback text if summarization fails.
        """
        prompt = f"""
        You are a medical AI assistant summarizing a patient conversation.
        
        Conversation History:
        {history_text}
        
        Task: Summarize the key health concerns and information this patient shared in 2-3 plain sentences.
        Be brief, patient-friendly, and avoid medical jargon.
        
        Return ONLY the summary text (no JSON, no extra formatting).
        """
        
        try:
            summary = await query_llm(prompt)
            summary = summary.strip()
            
            # Ensure it's a reasonable length (2-3 sentences)
            if len(summary) < 50:
                summary = "The patient shared health concerns that require further medical evaluation."
            
            return summary
        except Exception as e:
            logger.error(f"Conversation summarization failed: {e}")
            return "(summary unavailable)"
