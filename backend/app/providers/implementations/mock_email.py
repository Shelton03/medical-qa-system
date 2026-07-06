"""MockEmailProvider — logs to stdout."""

from __future__ import annotations

import logging
from typing import Any

from app.providers.interfaces.email import EmailProvider

logger = logging.getLogger(__name__)


class MockEmailProvider(EmailProvider):
    """Synthetic email provider that logs messages to stdout for local development."""

    async def initialize(self) -> None:
        """No-op initialization."""

    async def validate(self, **params: Any) -> bool:
        return True

    async def execute(self, **params: Any) -> dict[str, Any]:
        return params

    async def send_email(
        self,
        to: str,
        subject: str,
        body_text: str,
        body_html: str | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        logger.info(
            "[MockEmail] to=%s subject=%s text=%s html=%s meta=%s",
            to,
            subject,
            body_text,
            body_html,
            metadata,
        )
        return {
            "success": True,
            "to": to,
            "subject": subject,
            "message_id": f"mock-{hash(to + subject) & 0xFFFFFFFF}",
        }
