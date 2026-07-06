from __future__ import annotations


class MirageException(Exception):
    """Base application exception."""


class UnauthorizedException(MirageException):
    """Raised when authentication fails or a token is invalid/expired."""


class ForbiddenException(MirageException):
    """Raised when an authenticated user lacks required permissions."""


class NotFoundException(MirageException):
    """Raised when a requested resource does not exist."""

    def __init__(self, message: str = "Resource not found.", error_code: str | None = "NOT_FOUND") -> None:
        super().__init__(message)
        self.error_code = error_code
