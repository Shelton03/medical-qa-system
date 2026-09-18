from __future__ import annotations

import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker

from app.core.config import settings
from app.db.models import Base  # Unified Base

engine = create_async_engine(settings.database_url, echo=False, future=True)
AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def get_db() -> AsyncSession:
    """Yield an async database session."""
    async with AsyncSessionLocal() as session:
        yield session


async def init_db() -> None:
    """Create all tables if AUTO_CREATE_TABLES is set (default: rely on migrations)."""
    if os.getenv("AUTO_CREATE_TABLES", "false").lower() != "true":
        return
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
