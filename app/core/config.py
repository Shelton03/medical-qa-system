import os
from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    MONGODB_URI: str
    MONGODB_DB_NAME: str
    
    POSTGRES_URL: str
    POSTGRES_PASSWORD: str = "[REDACTED]"
    
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000
    
    LLM_BASE_URL: str = "https://[REDACTED]:9051/v1"
    LLM_API_KEY: str
    LLM_MODEL: str = "[REDACTED]"
    
    SELF_CONSISTENCY_RUNS: int = 3
    CONFIDENCE_THRESHOLD: float = 0.7
    
    LOG_LEVEL: str = "INFO"
    
    JWT_SECRET: str
    JWT_EXPIRY_HOURS: int = 24
    
    model_config = SettingsConfigDict(
        extra="ignore"
    )

settings = Settings()
