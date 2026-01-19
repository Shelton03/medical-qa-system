import json
from app.services import query_llm
from app.core.logger import logger

class InputProcessor:
    async def process(self, text: str) -> dict:
        """
        Extracts medical entities, symptoms, duration, severity.
        Simulates MedSpaCy/BioBERT using LLM for this prototype.
        """
        prompt = f"""
        Analyze the following medical query and extract structured data.
        Return ONLY a JSON object with these keys:
        - symptoms (list of strings)
        - duration (string or null)
        - severity (string or null)
        - entities (list of other medical entities like medications, conditions)

        Query: "{text}"
        """
        
        try:
            response_text = await query_llm(prompt)
            # Cleanup json block if present
            response_text = response_text.replace("```json", "").replace("```", "").strip()
            data = json.loads(response_text)
            return data
        except Exception as e:
            logger.error(f"Input processing failed: {e}")
            # Fallback
            return {
                "symptoms": [],
                "duration": None,
                "severity": None,
                "entities": []
            }
