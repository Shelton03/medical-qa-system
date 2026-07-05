from __future__ import annotations

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    # Database
    database_url: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/mirage"

    # Redis
    redis_url: str = "redis://localhost:6379/0"

    # JWT
    jwt_secret: str = "change-me-jwt-secret"
    jwt_expiration: int = 3600  # seconds
    refresh_secret: str = "change-me-refresh-secret"
    refresh_expiration: int = 604_800  # 7 days in seconds
    access_token_expire_minutes: int = 30

    # Demo mode
    demo_mode_enabled: bool = False

    # AI Provider
    ai_provider: str = "mock"

    # Security
    bcrypt_rounds: int = 12


settings = Settings()
