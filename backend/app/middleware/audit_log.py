"""Audit-log middleware — logs every request to the audit_logs table."""

from __future__ import annotations

import uuid

from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response

from app.db.models import AuditLog
from app.core.database import AsyncSessionLocal


class AuditLogMiddleware(BaseHTTPMiddleware):
    """
    Middleware that writes an audit log entry for every incoming request.

    actor      -> user_id from request.state if available, else None
    action     -> "REQUEST"
    resource_type -> endpoint path
    metadata   -> {method, path, status_code}
    """

    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        response = await call_next(request)

        actor_id: uuid.UUID | None = None
        if hasattr(request.state, "user") and request.state.user:
            actor_id = request.state.user.id

        try:
            async with AsyncSessionLocal() as db:
                log = AuditLog(
                    user_id=actor_id,
                    action="REQUEST",
                    resource_type=request.url.path,
                    resource_id=None,
                    ip_address=request.client.host if request.client else None,
                    user_agent=request.headers.get("user-agent"),
                    audit_metadata={
                        "method": request.method,
                        "path": request.url.path,
                        "status_code": response.status_code,
                    },
                )
                db.add(log)
                await db.commit()
        except Exception:
            pass

        return response
