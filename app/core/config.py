import os
from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    POSTGRES_URL: str
    POSTGRES_PASSWORD: str

    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000

    LLM_BASE_URL: str
    LLM_API_KEY: str
    LLM_MODEL: str

    SELF_CONSISTENCY_RUNS: int = 3
    CONFIDENCE_THRESHOLD: float = 0.7

    LOG_LEVEL: str = "INFO"

    JWT_SECRET: str
    JWT_EXPIRY_HOURS: int = 24

    # MinIO / S3-compatible object storage (bytes in bucket, metadata in Postgres)
    S3_ENDPOINT: str = ""          # e.g. http://localhost:9000 (MinIO); empty = disabled
    S3_ACCESS_KEY: str = ""
    S3_SECRET_KEY: str = ""
    S3_BUCKET: str = "mirage-attachments"
    S3_REGION: str = ""            # MinIO needs none; AWS/R2 set explicitly

    model_config = SettingsConfigDict(
        extra="ignore"
    )

settings = Settings()
