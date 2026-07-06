"""MockNotificationProvider — no-op or logs notifications."""

from __future__ import annotations

import logging
from typing import Any

from app.providers.interfaces.notification import NotificationProvider

logger = logging.getLogger(__name__)


class MockNotificationProvider(NotificationProvider):
    """Synthetic notification provider that logs to stdout for local development."""

    async def initialize(self) -> None:
        """No-op initialization."""

    async def validate(self, **params: Any) -> bool:
        return True

    async def execute(self, **params: Any) -> dict[str, Any]:
        return params

    async def send(
        self,
        recipient_id: str,
        title: str,
        body: str,
        metadata: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        logger.info(
            "[MockNotification] to=%s title=%s body=%s meta=%s",
            recipient_id,
            title,
            body,
            metadata,
        )
        return {
            "success": True,
            "recipient_id": recipient_id,
            "title": title,
            "delivery_id": "mock",
        }
