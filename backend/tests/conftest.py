"""Pytest configuration and shared fixtures for Mirage backend tests."""

from __future__ import annotations

import asyncio
import os
import sys
import uuid
from pathlib import Path
from typing import AsyncGenerator

# Ensure backend root is on path for imports
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

# Force test DB to SQLite in-memory before any app imports read settings
os.environ["DATABASE_URL"] = "sqlite+aiosqlite:///:memory:"
os.environ["REDIS_URL"] = "redis://localhost:6379/1"

import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.ext.compiler import compiles
from sqlalchemy.dialects.postgresql import UUID, JSONB

from app.core.database import get_db
from app.db.models import Base, User, Doctor, Patient
from app.auth.demo import generate_demo_tokens, _DEMO_DOCTOR_UUID, _DEMO_PATIENT_UUID

# Make PostgreSQL-specific types compatible with SQLite for tests
@compiles(UUID, "sqlite")
def compile_uuid_sqlite(type_, compiler, **kw):
    return "VARCHAR(36)"

@compiles(JSONB, "sqlite")
def compile_jsonb_sqlite(type_, compiler, **kw):
    return "TEXT"

test_engine = create_async_engine("sqlite+aiosqlite:///:memory:", echo=False, future=True)
TestingSessionLocal = async_sessionmaker(
    test_engine, class_=AsyncSession, expire_on_commit=False
)


async def override_get_db() -> AsyncGenerator[AsyncSession, None]:
    async with TestingSessionLocal() as session:
        yield session


class _MockRedis:
    """No-op redis client."""

    async def setex(self, *args):
        pass

    async def get(self, key):
        return None

    async def publish(self, *args):
        pass


# Patch middleware and redis BEFORE any app imports that would cache them
from app.middleware.audit_log import AuditLogMiddleware

_original_audit_dispatch = AuditLogMiddleware.dispatch

async def _patched_audit_dispatch(self, request, call_next):
    return await call_next(request)

AuditLogMiddleware.dispatch = _patched_audit_dispatch

from app.core.redis import get_redis as _original_get_redis

async def _patched_get_redis():
    return _MockRedis()

import app.core.redis as _redis_module

_redis_module.get_redis = _patched_get_redis

import app.auth.service as _auth_service_module

_auth_service_module.get_redis = _patched_get_redis


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope="session")
async def db_engine():
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    await test_engine.dispose()


@pytest_asyncio.fixture
async def db_session(db_engine) -> AsyncSession:
    session = TestingSessionLocal()
    yield session
    await session.close()
    async with test_engine.begin() as conn:
        # Clean all data between tests
        for table in reversed(Base.metadata.sorted_tables):
            await conn.execute(table.delete())


@pytest_asyncio.fixture
async def client(db_engine) -> AsyncGenerator[AsyncClient, None]:
    from main import app

    app.dependency_overrides[get_db] = override_get_db
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test", follow_redirects=True) as ac:
        yield ac


@pytest_asyncio.fixture
async def demo_patient_token(db_session: AsyncSession) -> str:
    access, _, _ = generate_demo_tokens("patient")
    # Ensure demo patient exists so profile lookups succeed
    existing = await db_session.get(User, _DEMO_PATIENT_UUID)
    if existing is None:
        user = User(
            id=_DEMO_PATIENT_UUID,
            email="demo-patient@mirage.health",
            password_hash="",
            role="patient",
            first_name="Demo",
            last_name="Patient",
            is_active=True,
        )
        db_session.add(user)
        await db_session.flush()
        patient = Patient(
            id=uuid.uuid4(),
            user_id=_DEMO_PATIENT_UUID,
            medical_record_number="MRN-DEMO-001",
            national_identifier="ZIM-89-4567234",
        )
        db_session.add(patient)
        await db_session.commit()
    return access


@pytest_asyncio.fixture
async def demo_doctor_token(db_session: AsyncSession) -> str:
    access, _, _ = generate_demo_tokens("doctor")
    # Ensure demo doctor exists so profile lookups succeed
    existing = await db_session.get(User, _DEMO_DOCTOR_UUID)
    if existing is None:
        user = User(
            id=_DEMO_DOCTOR_UUID,
            email="dr.sarah.mirage@mirage.health",
            password_hash="",
            role="doctor",
            first_name="Sarah",
            last_name="Mirage",
            is_active=True,
        )
        db_session.add(user)
        await db_session.flush()
        doctor = Doctor(
            id=uuid.uuid4(),
            user_id=_DEMO_DOCTOR_UUID,
            registration_number="DEMO-DR-001",
            specialty="General Practice",
        )
        db_session.add(doctor)
        await db_session.commit()
    return access


@pytest.fixture
def demo_admin_token() -> str:
    access, _, _ = generate_demo_tokens("admin")
    return access
