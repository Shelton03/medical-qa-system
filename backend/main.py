"""Mirage FastAPI application entrypoint."""

from __future__ import annotations

import asyncio
import os
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

from app.core.config import settings
from app.core.database import init_db
from app.db.seeder import seed_demo_data
from app.auth import router as auth_router
from app.consent import router as consent_router
from app.ai import router as ai_router
from app.patient import router as patient_router
from app.patient.me_router import router as patient_me_router
from app.doctor import router as doctor_router
from app.records import router as records_router
from app.timeline import router as timeline_router
from app.transcription import router as transcription_router
from app.audit import router as audit_router
from app.notifications.router import router as notifications_router
from app.notifications.websocket_router import router as notifications_ws_router
from app.websocket.router import router as ws_router
from app.appointment import router as appointment_router
from app.middleware.correlation_id import CorrelationIdMiddleware
from app.middleware.rate_limit import RateLimitMiddleware
from app.middleware.audit_log import AuditLogMiddleware
from app.core.exceptions import (
    UnauthorizedException as CoreUnauthorizedException,
    ForbiddenException as CoreForbiddenException,
)
from app.shared.exceptions import (
    NotFoundException,
    ValidationException,
    UnauthorizedException as SharedUnauthorizedException,
    ForbiddenException as SharedForbiddenException,
    ConflictException,
)
from app.schemas.envelope import Envelope, ErrorDetail


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan: init DB, seed data, start Redis listener."""
    await init_db()
    if settings.demo_mode_enabled or os.getenv("DEMO_MODE", "false").lower() == "true":
        from app.core.database import AsyncSessionLocal

        async with AsyncSessionLocal() as db:
            await seed_demo_data(db)

    from app.websocket.redis_listener import listen_for_websocket_events
    from app.notifications.redis_listener import listen_for_notifications

    ws_listener_task = asyncio.create_task(listen_for_websocket_events())
    notifications_listener_task = asyncio.create_task(listen_for_notifications())

    yield

    # Shutdown
    ws_listener_task.cancel()
    notifications_listener_task.cancel()
    try:
        await ws_listener_task
    except asyncio.CancelledError:
        pass
    try:
        await notifications_listener_task
    except asyncio.CancelledError:
        pass


app = FastAPI(
    title="Mirage",
    description="Mirage healthcare platform API",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(CorrelationIdMiddleware)
app.add_middleware(RateLimitMiddleware)
app.add_middleware(AuditLogMiddleware)

app.include_router(auth_router, prefix="/api/v1/auth", tags=["Authentication"])
app.include_router(consent_router, prefix="/api/v1/consents", tags=["Consent"])
app.include_router(ai_router, prefix="/api/v1/ai", tags=["AI"])
app.include_router(patient_me_router, prefix="/api/v1/me/patient", tags=["Patient Me"])
app.include_router(patient_router, prefix="/api/v1/patients", tags=["Patients"])
app.include_router(doctor_router, prefix="/api/v1/doctor", tags=["Doctor"])
app.include_router(records_router, prefix="/api/v1/records", tags=["Records"])
app.include_router(timeline_router, prefix="/api/v1/timeline", tags=["Timeline"])
app.include_router(transcription_router, prefix="/api/v1/transcription", tags=["Transcription"])
app.include_router(audit_router, prefix="/api/v1/audit", tags=["Audit"])
app.include_router(
    appointment_router,
    prefix="/api/v1/appointments",
    tags=["Appointments"],
)
app.include_router(
    notifications_router,
    prefix="/api/v1/notifications",
    tags=["Notifications"],
)
app.include_router(notifications_ws_router)
app.include_router(ws_router)


def _build_error_response(status_code: int, error_code: str, message: str) -> JSONResponse:
    envelope = Envelope.fail(ErrorDetail(code=error_code, message=message))
    return JSONResponse(status_code=status_code, content=envelope.model_dump())


@app.exception_handler(NotFoundException)
async def not_found_handler(request: Request, exc: NotFoundException) -> JSONResponse:
    return _build_error_response(404, exc.error_code or "NOT_FOUND", exc.message)


@app.exception_handler(ValidationException)
async def validation_exception_handler(request: Request, exc: ValidationException) -> JSONResponse:
    return _build_error_response(422, exc.error_code or "VALIDATION_ERROR", exc.message)


@app.exception_handler(SharedUnauthorizedException)
async def shared_unauthorized_handler(
    request: Request, exc: SharedUnauthorizedException
) -> JSONResponse:
    return _build_error_response(401, exc.error_code or "UNAUTHORIZED", exc.message)


@app.exception_handler(SharedForbiddenException)
async def shared_forbidden_handler(
    request: Request, exc: SharedForbiddenException
) -> JSONResponse:
    return _build_error_response(403, exc.error_code or "FORBIDDEN", exc.message)


@app.exception_handler(CoreUnauthorizedException)
async def core_unauthorized_handler(
    request: Request, exc: CoreUnauthorizedException
) -> JSONResponse:
    return _build_error_response(401, "UNAUTHORIZED", str(exc))


@app.exception_handler(CoreForbiddenException)
async def core_forbidden_handler(
    request: Request, exc: CoreForbiddenException
) -> JSONResponse:
    return _build_error_response(403, "FORBIDDEN", str(exc))


@app.exception_handler(ConflictException)
async def conflict_handler(request: Request, exc: ConflictException) -> JSONResponse:
    return _build_error_response(409, exc.error_code or "CONFLICT", exc.message)


@app.exception_handler(RequestValidationError)
async def request_validation_handler(
    request: Request, exc: RequestValidationError
) -> JSONResponse:
    errors = [
        ErrorDetail(
            code="VALIDATION_ERROR",
            message=err.get("msg", "Invalid value."),
            field=err.get("loc", [None])[-1],
        )
        for err in exc.errors()
    ]
    envelope = Envelope.fail(*errors)
    return JSONResponse(status_code=422, content=envelope.model_dump())


@app.get("/health", tags=["Health"])
async def health_check() -> dict[str, str]:
    """Service health check."""
    return {"status": "ok", "service": "mirage-backend"}
