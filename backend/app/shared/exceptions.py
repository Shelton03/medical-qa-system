#!/usr/bin/env python3
"""Mirage domain exceptions."""

from __future__ import annotations


class MirageException(Exception):
    """Base exception for all application errors."""

    def __init__(self, message: str, error_code: str | None = None) -> None:
        super().__init__(message)
        self.message = message
        self.error_code = error_code


class NotFoundException(MirageException):
    """Raised when a requested resource does not exist."""

    def __init__(self, message: str = "Resource not found.", error_code: str | None = "NOT_FOUND") -> None:
        super().__init__(message, error_code)


class ValidationException(MirageException):
    """Raised when input validation fails."""

    def __init__(self, message: str = "Validation failed.", error_code: str | None = "VALIDATION_ERROR") -> None:
        super().__init__(message, error_code)


class UnauthorizedException(MirageException):
    """Raised when authentication is required or invalid."""

    def __init__(self, message: str = "Authentication required.", error_code: str | None = "UNAUTHORIZED") -> None:
        super().__init__(message, error_code)


class ForbiddenException(MirageException):
    """Raised when the authenticated principal lacks permission."""

    def __init__(self, message: str = "Access forbidden.", error_code: str | None = "FORBIDDEN") -> None:
        super().__init__(message, error_code)


class ConflictException(MirageException):
    """Raised when a conflicting state prevents the operation."""

    def __init__(self, message: str = "Conflict occurred.", error_code: str | None = "CONFLICT") -> None:
        super().__init__(message, error_code)
