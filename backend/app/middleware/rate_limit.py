"""In-memory rate-limiting middleware aligned with API Contract."""

from __future__ import annotations

import time
from typing import Any

from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import JSONResponse, Response

# API Contract §Rate Limiting
_LIMITS: dict[str, tuple[int, int]] = {
    "auth": (10, 60),      # 10 per 60s
    "ai": (30, 60),        # 30 per 60s
    "search": (60, 60),    # 60 per 60s
    "default": (100, 60),  # 100 per 60s
}

# In-memory store: {ip: {category: [(timestamp, 1), ...]}}
_store: dict[str, dict[str, list[tuple[float, int]]]] = {}


def _get_category(path: str) -> str:
    """Map request path to rate-limit category."""
    if path.startswith("/api/v1/auth"):
        return "auth"
    if path.startswith("/api/v1/ai"):
        return "ai"
    if path.startswith("/api/v1/doctor/search") or path.startswith("/api/v1/patients/search"):
        return "search"
    return "default"


def _is_limited(ip: str, category: str) -> tuple[bool, dict[str, Any]]:
    now = time.monotonic()
    limit, window = _LIMITS.get(category, _LIMITS["default"])
    window_start = now - window

    ip_store = _store.setdefault(ip, {})
    history = ip_store.setdefault(category, [])

    # Prune expired entries
    history[:] = [entry for entry in history if entry[0] > window_start]

    total = len(history)
    if total >= limit:
        return True, {
            "success": False,
            "data": None,
            "errors": [
                {
                    "code": "RATE_LIMITED",
                    "message": "Rate limit exceeded. Try again later.",
                }
            ],
            "meta": {"reset_after": window},
        }

    # Append new entry (fixed: no longer replaces single entry)
    history.append((now, 1))
    return False, {}


class RateLimitMiddleware(BaseHTTPMiddleware):
    """
    In-memory rate-limiting middleware.

    - Per-IP, per-category sliding window.
    - Auth: 10/min, AI: 30/min, Search: 60/min, General: 100/min.
    - Returns 429 with standard envelope when exceeded.
    - Skips rate limit for health endpoints.
    """

    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        path = request.url.path
        if path in ("/health", "/api/v1/health", "/"):
            return await call_next(request)

        ip = request.client.host if request.client else "unknown"
        category = _get_category(path)

        limited, error_body = _is_limited(ip, category)
        if limited:
            return JSONResponse(status_code=429, content=error_body)

        return await call_next(request)
