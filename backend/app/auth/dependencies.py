from __future__ import annotations

from typing import Callable

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.exceptions import ForbiddenException, UnauthorizedException
from app.auth.jwt import decode_token
from app.auth.demo import is_demo_token, _DEMO_DOCTOR_UUID, _DEMO_PATIENT_UUID
from app.models import User
from app.schemas.envelope import ErrorDetail

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login", auto_error=False)


async def get_current_user(
    token: str | None = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db),
) -> User:
    """Decode the bearer token and return the corresponding User database row."""
    if not token:
        raise UnauthorizedException("Authentication required.")

    payload = decode_token(token)
    if is_demo_token(payload):
        role = payload.get("role", "unknown")
        if role == "doctor":
            synthetic_uuid = _DEMO_DOCTOR_UUID
        elif role == "patient":
            synthetic_uuid = _DEMO_PATIENT_UUID
        else:
            raise UnauthorizedException("Invalid demo token role.")
        # Build a lightweight synthetic user for demo sessions
        return User(
            id=synthetic_uuid,
            email=f"demo-{role}@mirage.health",
            password_hash="",
            role=role,
            first_name="Demo",
            last_name=role.capitalize(),
            is_active=True,
        )

    user_id_str: str | None = payload.get("sub")
    if not user_id_str:
        raise UnauthorizedException("Token payload missing subject.")

    from uuid import UUID

    try:
        user_id = UUID(user_id_str)
    except ValueError as exc:
        raise UnauthorizedException("Malformed user identifier in token.") from exc

    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if not user:
        raise UnauthorizedException("User not found.")
    if not user.is_active:
        raise UnauthorizedException("Account is deactivated.")

    return user


def require_role(*roles: str) -> Callable:
    """Dependency factory that checks the current user's role."""

    async def _role_checker(current_user: User = Depends(get_current_user)) -> User:
        if current_user.role not in roles:
            raise ForbiddenException("Insufficient permissions.")
        return current_user

    return _role_checker


get_current_doctor = require_role("doctor", "admin")
get_current_patient = require_role("patient", "admin")


async def get_current_active_user(
    current_user: User = Depends(get_current_user),
) -> User:
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Inactive user",
        )
    return current_user
