import os
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional
from dotenv import load_dotenv

# Load .env file explicitly
load_dotenv()

class Settings(BaseSettings):
    MONGODB_URI: str
    MONGODB_DB_NAME: str
    
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000
    
    GEMINI_API_KEY: str
    
    SELF_CONSISTENCY_RUNS: int = 3
    CONFIDENCE_THRESHOLD: float = 0.7
    
    LOG_LEVEL: str = "INFO"

    model_config = SettingsConfigDict(
        extra="ignore"
    )

settings = Settings()
