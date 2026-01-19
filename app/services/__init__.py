from google import genai
from app.core.config import settings
from app.core.logger import logger
import asyncio

# Initialize Gemini Client
client = None
if settings.GEMINI_API_KEY:
    try:
        client = genai.Client(api_key=settings.GEMINI_API_KEY)
    except Exception as e:
        logger.error(f"Failed to initialize Gemini Client: {e}")
else:
    logger.warning("GEMINI_API_KEY not set. LLM features will fail.")

async def query_llm(prompt: str) -> str:
    if not client:
        raise ValueError("LLM Client not configured")
    try:
        # Using synchronous call in a thread to keep it simple, 
        # or use the aio (async) client if preferred.
        # For this prototype, we'll use the sync client wrapped in a thread or just the sync client 
        # if the SDK doesn't have a direct async await on generate_content (it usually does via .aio)
        
        # New SDK Async usage:
        # response = await client.aio.models.generate_content(model='gemini-1.5-flash', contents=prompt)
        
        response = await client.aio.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt
        )
        return response.text
    except Exception as e:
        logger.error(f"LLM Query failed: {e}")
        return ""