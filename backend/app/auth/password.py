from __future__ import annotations

import bcrypt

from app.core.config import settings


def hash_password(plain: str) -> str:
    """Hash a plain-text password using bcrypt with configurable rounds."""
    # bcrypt has a 72-byte limit on password input
    plain_bytes = plain.encode("utf-8")[:72]
    hashed = bcrypt.hashpw(plain_bytes, bcrypt.gensalt(rounds=settings.bcrypt_rounds))
    return hashed.decode("utf-8")


def verify_password(plain: str, hashed: str) -> bool:
    """Verify a plain-text password against a bcrypt hash."""
    plain_bytes = plain.encode("utf-8")[:72]
    hash_bytes = hashed.encode("utf-8")
    return bcrypt.checkpw(plain_bytes, hash_bytes)
