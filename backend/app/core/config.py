from __future__ import annotations

from pydantic import AliasChoices, Field, computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Unified application settings loaded from environment variables."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        populate_by_name=True,
    )

    # Database
    database_url: str = Field(
        default="postgresql+asyncpg://postgres:postgres@localhost:5432/mirage",
        validation_alias="DATABASE_URL",
    )

    test_database_url: str = Field(
        default="postgresql+asyncpg://postgres:postgres@localhost:5432/mirage_test",
        validation_alias="TEST_DATABASE_URL",
    )

    # Redis
    redis_url: str = Field(
        default="redis://localhost:6379/0",
        validation_alias="REDIS_URL",
    )

    # Security / JWT
    jwt_secret: str = Field(
        default="change-me-jwt-secret",
        validation_alias=AliasChoices("JWT_SECRET", "SECRET_KEY"),
    )
    jwt_algorithm: str = Field(default="HS256", validation_alias="JWT_ALGORITHM")
    access_token_expire_minutes: int = Field(
        default=60,
        validation_alias="ACCESS_TOKEN_EXPIRE_MINUTES",
    )
    refresh_secret: str = Field(
        default="change-me-refresh-secret",
        validation_alias=AliasChoices("REFRESH_SECRET", "JWT_SECRET", "SECRET_KEY"),
    )
    refresh_token_expire_days: int = Field(
        default=30,
        validation_alias="REFRESH_TOKEN_EXPIRE_DAYS",
    )

    # Feature flags
    demo_mode_enabled: bool = Field(
        default=False,
        validation_alias=AliasChoices("DEMO_MODE", "DEMO_MODE_ENABLED"),
    )
    ai_provider: str = Field(default="mock", validation_alias="AI_PROVIDER")

    # Observability
    log_level: str = Field(default="INFO", validation_alias="LOG_LEVEL")

    # Password hashing
    bcrypt_rounds: int = Field(default=12, validation_alias="BCRYPT_ROUNDS")

    # Assessment pipeline
    self_consistency_runs: int = Field(
        default=3,
        validation_alias="SELF_CONSISTENCY_RUNS",
    )
    confidence_threshold: float = Field(
        default=0.7,
        validation_alias="CONFIDENCE_THRESHOLD",
    )

    @computed_field
    @property
    def jwt_expiration_seconds(self) -> int:
        """Access token time-to-live in seconds."""
        return self.access_token_expire_minutes * 60

    @computed_field
    @property
    def refresh_expiration_seconds(self) -> int:
        """Refresh token time-to-live in seconds."""
        return self.refresh_token_expire_days * 24 * 60 * 60


settings = Settings()
