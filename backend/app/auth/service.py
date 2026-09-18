from __future__ import annotations

import uuid
from datetime import timedelta

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.password import verify_password
from app.auth.jwt import (
    create_access_token,
    create_refresh_token,
    decode_refresh_token,
)
from app.auth.demo import (
    authenticate_demo_doctor,
    authenticate_demo_patient,
    generate_demo_tokens,
    _DEMO_DOCTOR_UUID,
    _DEMO_PATIENT_UUID,
    is_demo_token,
)
from app.core.config import settings
from app.core.exceptions import UnauthorizedException
from app.core.redis import get_redis
from app.models import User
from app.schemas.token import TokenPair


async def login_admin(
    email: str,
    password: str,
    db: AsyncSession,
) -> TokenPair:
    """Authenticate an admin by email/password, falling back to demo credentials."""
    stmt = select(User).where(User.email == email, User.role == "admin")
    result = await db.execute(stmt)
    user = result.scalar_one_or_none()

    if user and verify_password(password, user.password_hash):
        access = create_access_token(user.id, role=user.role)
        refresh = create_refresh_token(user.id, role=user.role)
        return TokenPair(
            access_token=access,
            refresh_token=refresh,
            expires_in=settings.jwt_expiration_seconds,
            role=user.role,
            demo_mode=False,
        )

    # Demo fallback for admin
    from app.auth.demo import authenticate_demo_admin
    if authenticate_demo_admin(email, password):
        access, refresh, _ = generate_demo_tokens("admin")
        return TokenPair(
            access_token=access,
            refresh_token=refresh,
            expires_in=settings.jwt_expiration_seconds,
            role="admin",
            demo_mode=True,
        )

    raise UnauthorizedException("Invalid credentials.")


async def login_doctor(
    email: str,
    password: str,
    db: AsyncSession,
) -> TokenPair:
    """Authenticate a doctor by email/password, falling back to demo credentials."""
    stmt = select(User).where(User.email == email, User.role == "doctor")
    result = await db.execute(stmt)
    user = result.scalar_one_or_none()

    if user and verify_password(password, user.password_hash):
        access = create_access_token(user.id, role=user.role)
        refresh = create_refresh_token(user.id, role=user.role)
        return TokenPair(
            access_token=access,
            refresh_token=refresh,
            expires_in=settings.jwt_expiration_seconds,
            role=user.role,
            demo_mode=False,
        )

    if authenticate_demo_doctor(email, password):
        access, refresh, _ = generate_demo_tokens("doctor")
        return TokenPair(
            access_token=access,
            refresh_token=refresh,
            expires_in=settings.jwt_expiration_seconds,
            role="doctor",
            demo_mode=True,
        )

    raise UnauthorizedException("Invalid credentials.")


async def login_patient(
    national_id: str,
    pin: str,
    db: AsyncSession,
) -> TokenPair:
    """Authenticate a patient by national_id/pin, falling back to demo credentials."""
    from app.db.models import Patient

    stmt = (
        select(User)
        .join(Patient, Patient.user_id == User.id)
        .where(Patient.national_identifier == national_id, User.role == "patient")
    )
    result = await db.execute(stmt)
    user = result.scalar_one_or_none()

    if user and verify_password(pin, user.password_hash):
        access = create_access_token(user.id, role=user.role)
        refresh = create_refresh_token(user.id, role=user.role)
        return TokenPair(
            access_token=access,
            refresh_token=refresh,
            expires_in=settings.jwt_expiration_seconds,
            role=user.role,
            demo_mode=False,
        )

    if authenticate_demo_patient(national_id, pin):
        access, refresh, _ = generate_demo_tokens("patient")
        return TokenPair(
            access_token=access,
            refresh_token=refresh,
            expires_in=settings.jwt_expiration_seconds,
            role="patient",
            demo_mode=True,
        )

    raise UnauthorizedException("Invalid credentials.")


async def refresh_access_token(refresh_token: str) -> str:
    """Validate a refresh token and return a new access token."""
    payload = decode_refresh_token(refresh_token)
    if payload.get("type") != "refresh":
        raise UnauthorizedException("Invalid token type.")

    subject_str: str | None = payload.get("sub")
    if not subject_str:
        raise UnauthorizedException("Token missing subject.")

    subject = uuid.UUID(subject_str)

    redis = await get_redis()
    jti = payload.get("jti")
    if jti and await redis.get(f"blacklist:{jti}"):
        raise UnauthorizedException("Refresh token has been revoked.")

    # Re-issue access token with role from refresh token payload
    role = payload.get("role", "unknown")
    if role == "unknown":
        raise UnauthorizedException("Token missing role.")

    return create_access_token(subject, role=role)


async def logout(token_jti: str) -> None:
    """Add a token JTI to the Redis blacklist with TTL matching token expiry."""
    max_ttl = max(settings.jwt_expiration_seconds, settings.refresh_expiration_seconds)
    redis = await get_redis()
    await redis.setex(f"blacklist:{token_jti}", max_ttl, "1")
