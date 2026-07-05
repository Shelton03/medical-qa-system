from __future__ import annotations

import uuid
from datetime import datetime, timezone, timedelta

from jose import JWTError, jwt

from app.core.config import settings
from app.core.exceptions import UnauthorizedException

_SECRET_KEY = settings.jwt_secret
_REFRESH_SECRET_KEY = settings.refresh_secret
_ALGORITHM = "HS256"
DEFAULT_ACCESS_DELTA = timedelta(minutes=settings.access_token_expire_minutes)
DEFAULT_REFRESH_DELTA = timedelta(seconds=settings.refresh_expiration)


def create_access_token(
    subject: uuid.UUID,
    role: str,
    expires_delta: timedelta | None = None,
) -> str:
    """Create a new JWT access token."""
    jti = str(uuid.uuid4())
    now = datetime.now(timezone.utc)
    expire = now + (expires_delta or DEFAULT_ACCESS_DELTA)
    payload = {
        "type": "access",
        "sub": str(subject),
        "role": role,
        "jti": jti,
        "iat": now,
        "exp": expire,
    }
    return jwt.encode(payload, _SECRET_KEY, algorithm=_ALGORITHM)


def create_refresh_token(
    subject: uuid.UUID,
    expires_delta: timedelta | None = None,
) -> str:
    """Create a new JWT refresh token."""
    jti = str(uuid.uuid4())
    now = datetime.now(timezone.utc)
    expire = now + (expires_delta or DEFAULT_REFRESH_DELTA)
    payload = {
        "type": "refresh",
        "sub": str(subject),
        "jti": jti,
        "iat": now,
        "exp": expire,
    }
    return jwt.encode(payload, _REFRESH_SECRET_KEY, algorithm=_ALGORITHM)


def decode_token(token: str) -> dict:
    """Decode and verify a JWT access token. Raises UnauthorizedException on failure."""
    try:
        return jwt.decode(token, _SECRET_KEY, algorithms=[_ALGORITHM])
    except jwt.ExpiredSignatureError as exc:
        raise UnauthorizedException("Token has expired.") from exc
    except JWTError as exc:
        raise UnauthorizedException("Invalid token.") from exc


def decode_refresh_token(token: str) -> dict:
    """Decode and verify a JWT refresh token. Raises UnauthorizedException on failure."""
    try:
        return jwt.decode(token, _REFRESH_SECRET_KEY, algorithms=[_ALGORITHM])
    except jwt.ExpiredSignatureError as exc:
        raise UnauthorizedException("Refresh token has expired.") from exc
    except JWTError as exc:
        raise UnauthorizedException("Invalid refresh token.") from exc
