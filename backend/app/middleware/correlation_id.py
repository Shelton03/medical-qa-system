"""Correlation ID middleware for request tracing."""

from __future__ import annotations

import contextvars
import uuid

from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response

_correlation_id: contextvars.ContextVar[str] = contextvars.ContextVar("correlation_id")


class CorrelationIdMiddleware(BaseHTTPMiddleware):
    """
    FastAPI middleware that:
      - Reads ``X-Request-ID`` header or generates a UUID.
      - Adds it to response headers.
      - Stores it in a contextvar for logging.
    """

    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        header_value = request.headers.get("X-Request-ID")
        correlation_id = header_value or str(uuid.uuid4())
        _correlation_id.set(correlation_id)

        response = await call_next(request)
        response.headers["X-Request-ID"] = correlation_id
        return response


def get_correlation_id() -> str | None:
    """Return the current request's correlation ID, or None if not set."""
    try:
        return _correlation_id.get()
    except LookupError:
        return None
