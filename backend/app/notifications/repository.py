"""NotificationRepository — persistence only, no business logic."""

from __future__ import annotations

import uuid
from datetime import datetime, timezone
from typing import Any

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import Notification


async def create_notification(
    db: AsyncSession,
    user_id: uuid.UUID,
    type: str,
    title: str,
    body: str,
    related_entity_type: str | None = None,
    related_entity_id: uuid.UUID | None = None,
) -> Notification:
    """Persist a new notification record."""
    payload: dict[str, Any] = {}
    if related_entity_type:
        payload["related_entity_type"] = related_entity_type
    if related_entity_id:
        payload["related_entity_id"] = str(related_entity_id)

    notification = Notification(
        recipient_user_id=user_id,
        type=type,
        title=title,
        body=body,
        payload=payload or None,
        is_read=False,
    )
    db.add(notification)
    await db.flush()
    await db.refresh(notification)
    return notification


async def get_notifications_for_user(
    db: AsyncSession,
    user_id: uuid.UUID,
    unread_only: bool = False,
    limit: int = 20,
    offset: int = 0,
) -> tuple[list[Notification], int]:
    """Return paginated notifications for a user ordered by newest first."""
    stmt = select(Notification).where(Notification.recipient_user_id == user_id)
    count_stmt = (
        select(func.count())
        .select_from(Notification)
        .where(Notification.recipient_user_id == user_id)
    )
    if unread_only:
        stmt = stmt.where(Notification.is_read.is_(False))
        count_stmt = count_stmt.where(Notification.is_read.is_(False))
    stmt = (
        stmt.order_by(Notification.created_at.desc())
        .offset(offset)
        .limit(limit)
    )
    result = await db.execute(stmt)
    total_result = await db.execute(count_stmt)
    return list(result.scalars().all()), total_result.scalar_one()


async def mark_notification_read(
    db: AsyncSession,
    notification_id: uuid.UUID,
) -> Notification | None:
    """Mark a single notification as read. Returns None if not found."""
    result = await db.execute(
        select(Notification).where(Notification.id == notification_id)
    )
    notification = result.scalar_one_or_none()
    if notification is None:
        return None
    if not notification.is_read:
        notification.is_read = True
        notification.read_at = datetime.now(timezone.utc)
        db.add(notification)
        await db.flush()
        await db.refresh(notification)
    return notification


async def mark_all_notifications_read(
    db: AsyncSession,
    user_id: uuid.UUID,
) -> int:
    """Mark every unread notification for the user as read. Returns count updated."""
    now = datetime.now(timezone.utc)
    result = await db.execute(
        Notification.__table__.update()
        .where(
            Notification.recipient_user_id == user_id,
            Notification.is_read.is_(False),
        )
        .values(is_read=True, read_at=now)
    )
    await db.flush()
    return result.rowcount if result.rowcount is not None else 0


async def get_unread_count(
    db: AsyncSession,
    user_id: uuid.UUID,
) -> int:
    """Return the number of unread notifications for a user."""
    result = await db.execute(
        select(func.count())
        .select_from(Notification)
        .where(
            Notification.recipient_user_id == user_id,
            Notification.is_read.is_(False),
        )
    )
    return result.scalar_one()


async def delete_notification(
    db: AsyncSession,
    notification_id: uuid.UUID,
) -> None:
    """Remove a notification record permanently."""
    result = await db.execute(
        select(Notification).where(Notification.id == notification_id)
    )
    notification = result.scalar_one_or_none()
    if notification:
        await db.delete(notification)
        await db.flush()
