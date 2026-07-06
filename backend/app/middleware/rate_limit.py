"""Simple in-memory rate-limiting middleware."""

from __future__ import annotations

import time
from typing import Any

from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import JSONResponse, Response

# 100 requests per minute per IP per endpoint
_RATE_LIMIT = 100
_WINDOW_SECONDS = 60

# In-memory store: {ip: {endpoint_key: [(timestamp, count), ...]}}
_store: dict[str, dict[str, list[tuple[float, int]]]] = {}


def _is_limited(ip: str, endpoint: str) -> tuple[bool, dict[str, Any]]:
    now = time.monotonic()
    window_start = now - _WINDOW_SECONDS

    ip_store = _store.setdefault(ip, {})
    endpoint_history = ip_store.setdefault(endpoint, [])

    # Prune old entries
    endpoint_history[:] = [entry for entry in endpoint_history if entry[0] > window_start]

    total = sum(count for _ts, count in endpoint_history)
    if total >= _RATE_LIMIT:
        return True, {
            "success": False,
            "data": None,
            "errors": [
                {
                    "code": "RATE_LIMITED",
                    "message": "Rate limit exceeded. Try again later.",
                }
            ],
            "meta": {"reset_after": _WINDOW_SECONDS},
        }

    if endpoint_history:
        endpoint_history[-1] = (now, endpoint_history[-1][1] + 1)
    else:
        endpoint_history.append((now, 1))

    return False, {}


class RateLimitMiddleware(BaseHTTPMiddleware):
    """
    In-memory rate-limiting middleware.

    - Tracks requests per IP per endpoint.
    - Limit: 100 req/min per IP.
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
        endpoint = f"{request.method}:{path}"

        limited, error_body = _is_limited(ip, endpoint)
        if limited:
            return JSONResponse(status_code=429, content=error_body)

        return await call_next(request)
