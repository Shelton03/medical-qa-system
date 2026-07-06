"""NotificationProvider interface."""

from __future__ import annotations

import abc
from typing import Any

from app.providers.interfaces.base import BaseProvider


class NotificationProvider(BaseProvider, abc.ABC):
    """
    Interface for push / real-time notification delivery providers.

    Responsibilities:
    - Send a notification payload to a user or channel.
    """

    @abc.abstractmethod
    async def send(
        self,
        recipient_id: str,
        title: str,
        body: str,
        metadata: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Deliver a notification and return a delivery result."""
