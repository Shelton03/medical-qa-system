"""EmailProvider interface."""

from __future__ import annotations

import abc
from typing import Any

from app.providers.interfaces.base import BaseProvider


class EmailProvider(BaseProvider, abc.ABC):
    """
    Interface for email delivery providers.

    Responsibilities:
    - Send transactional email messages.
    """

    @abc.abstractmethod
    async def send_email(
        self,
        to: str,
        subject: str,
        body_text: str,
        body_html: str | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Send an email and return a delivery status."""
