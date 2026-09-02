import httpx
from openai import AsyncOpenAI
from app.core.config import settings
from app.core.logger import logger
import asyncio

http_client = httpx.AsyncClient(verify=False)

client = None
if settings.LLM_API_KEY:
    try:
        client = AsyncOpenAI(
            base_url=settings.LLM_BASE_URL,
            api_key=settings.LLM_API_KEY,
            http_client=http_client
        )
        logger.info(f"Connected to LLM: {settings.LLM_MODEL}")
    except Exception as e:
        logger.error(f"Failed to initialize LLM Client: {e}")
else:
    logger.warning("LLM_API_KEY not set. LLM features will fail.")

async def query_llm(prompt: str) -> str:
    if not client:
        raise ValueError("LLM Client not configured")
    try:
        response = await client.chat.completions.create(
            model=settings.LLM_MODEL,
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content
    except Exception as e:
        logger.error(f"LLM Query failed: {e}")
        return ""
