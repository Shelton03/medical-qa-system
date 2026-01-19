from app.services.nlp_service import get_qa_pipeline
from app.core.logger import logger
import asyncio

class InputProcessor:
    def __init__(self):
        self.qa_pipeline = get_qa_pipeline()

    async def _ask_question(self, question: str, context: str, score_threshold=0.1) -> str | None:
        """Helper to ask a single question and return the answer if score is high enough."""
        if not self.qa_pipeline:
            return None
        try:
            result = self.qa_pipeline(question=question, context=context)
            logger.debug(f"QA for '{question}': {result}")
            if result['score'] > score_threshold:
                return result['answer']
            return None
        except Exception as e:
            logger.error(f"Error during QA pipeline execution for question '{question}': {e}")
            return None

    async def process(self, text: str) -> dict:
        """
        Extracts entities by asking a series of questions using the BioBERT QA pipeline.
        """
        if not self.qa_pipeline:
            logger.error("QA pipeline is not available. Cannot process input.")
            return {"symptoms": [text], "duration": None, "severity": None, "entities": []}

        # Define questions to extract the required data
        questions = {
            "symptoms": "What are the symptoms?",
            "duration": "What is the duration?",
            "severity": "What is the severity?"
        }

        # Ask all questions concurrently
        tasks = {
            key: self._ask_question(question, text)
            for key, question in questions.items()
        }
        
        results = await asyncio.gather(*tasks.values())
        
        answered_data = dict(zip(tasks.keys(), results))
        
        symptoms_list = [answered_data["symptoms"]] if answered_data.get("symptoms") else []
        
        processed_data = {
            "symptoms": symptoms_list,
            "duration": answered_data.get("duration"),
            "severity": answered_data.get("severity"),
            "entities": [ans for ans in answered_data.values() if ans is not None]
        }

        logger.info(f"BioBERT QA processed data: {processed_data}")
        return processed_data
