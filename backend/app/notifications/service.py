"""NotificationService — coordinates persistence and real-time delivery."""

from __future__ import annotations

import json
import uuid
from datetime import datetime, timezone
from typing import Any

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import ConsentRequest, Doctor, Notification, Patient
from app.notifications.repository import (
    create_notification,
    get_notifications_for_user,
    get_unread_count,
    mark_all_notifications_read,
    mark_notification_read,
)
from app.shared.exceptions import ForbiddenException, NotFoundException
from app.shared.redis_client import get_redis


async def send_notification(
    db: AsyncSession,
    user_id: uuid.UUID,
    type: str,
    title: str,
    body: str,
    related_entity_type: str | None = None,
    related_entity_id: uuid.UUID | None = None,
) -> None:
    """Persist a notification and publish it to the user's Redis channel."""
    notification = await create_notification(
        db, user_id, type, title, body, related_entity_type, related_entity_id
    )
    redis = await get_redis()
    channel = f"notifications:user:{user_id}"
    message = {
        "type": "NOTIFICATION_CREATED",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "payload": {
            "id": str(notification.id),
            "type": notification.type,
            "title": notification.title,
            "body": notification.body,
            "read": notification.is_read,
            "created_at": (
                notification.created_at.isoformat()
                if notification.created_at
                else None
            ),
        },
    }
    await redis.publish(channel, json.dumps(message))


async def get_user_notifications(
    db: AsyncSession,
    user_id: uuid.UUID,
    filters: dict[str, Any],
) -> tuple[list[Notification], int]:
    """List notifications for a user with optional filtering and pagination."""
    unread_only = filters.get("unread_only", False)
    limit = filters.get("limit", 20)
    offset = filters.get("offset", 0)
    return await get_notifications_for_user(db, user_id, unread_only, limit, offset)


async def mark_read(
    db: AsyncSession,
    notification_id: uuid.UUID,
    user_id: uuid.UUID,
) -> Notification:
    """Verify ownership then mark a notification as read."""
    notification = await mark_notification_read(db, notification_id)
    if notification is None:
        raise NotFoundException("Notification not found.")
    if notification.recipient_user_id != user_id:
        raise ForbiddenException("You do not own this notification.")
    return notification


async def mark_all_read(
    db: AsyncSession,
    user_id: uuid.UUID,
) -> int:
    """Mark every unread notification for the user as read."""
    return await mark_all_notifications_read(db, user_id)


async def get_unread_count_for_user(
    db: AsyncSession,
    user_id: uuid.UUID,
) -> int:
    """Return the number of unread notifications for a user."""
    return await get_unread_count(db, user_id)


async def broadcast_consent_notification(
    db: AsyncSession,
    consent_request: ConsentRequest,
    event_type: str,
) -> None:
    """
    Helper called by ConsentService.

    Creates a Notification record and publishes a typed WebSocket event.
    Supported event types: CONSENT_REQUESTED, CONSENT_APPROVED,
    CONSENT_DECLINED, CONSENT_REVOKED.
    """
    if event_type == "CONSENT_REQUESTED":
        recipient_id = await _resolve_user_id_from_patient(
            db, consent_request.patient_id
        )
        title = "New Consent Request"
        body = "A doctor has requested access to your medical records."
    elif event_type == "CONSENT_APPROVED":
        recipient_id = await _resolve_user_id_from_doctor(
            db, consent_request.doctor_id
        )
        title = "Consent Approved"
        body = "The patient has approved your access request."
    elif event_type == "CONSENT_DECLINED":
        recipient_id = await _resolve_user_id_from_doctor(
            db, consent_request.doctor_id
        )
        title = "Consent Declined"
        body = "The patient has declined your access request."
    elif event_type == "CONSENT_REVOKED":
        recipient_id = await _resolve_user_id_from_doctor(
            db, consent_request.doctor_id
        )
        title = "Consent Revoked"
        body = "The patient has revoked your access to their medical records."
    else:
        return

    if recipient_id is None:
        return

    await send_notification(
        db,
        user_id=recipient_id,
        type="CONSENT",
        title=title,
        body=body,
        related_entity_type="ConsentRequest",
        related_entity_id=consent_request.id,
    )

    # Publish a dedicated typed event for real-time UI updates
    redis = await get_redis()
    channel = f"notifications:user:{recipient_id}"
    event_message = {
        "type": event_type,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "payload": {
            "consent_id": str(consent_request.id),
            "patient_id": str(consent_request.patient_id),
            "doctor_id": str(consent_request.doctor_id),
            "status": consent_request.status,
        },
    }
    await redis.publish(channel, json.dumps(event_message))


async def _resolve_user_id_from_patient(
    db: AsyncSession,
    patient_id: uuid.UUID,
) -> uuid.UUID | None:
    """Map a Patient.id to its linked User.id."""
    result = await db.execute(
        select(Patient.user_id).where(Patient.id == patient_id)
    )
    return result.scalar_one_or_none()


async def _resolve_user_id_from_doctor(
    db: AsyncSession,
    doctor_id: uuid.UUID,
) -> uuid.UUID | None:
    """Map a Doctor.id to its linked User.id."""
    result = await db.execute(
        select(Doctor.user_id).where(Doctor.id == doctor_id)
    )
    return result.scalar_one_or_none()
