"""Base provider interface with lifecycle hooks."""

from __future__ import annotations

import abc
import logging
from typing import Any

logger = logging.getLogger(__name__)


class BaseProvider(abc.ABC):
    """
    Abstract base for all pluggable providers.

    Lifecycle:
      1. initialize()
      2. validate(**params)
      3. execute(**params) -> StandardizedResponse
      4. handle_errors(exc) -> StandardizedResponse
    """

    @abc.abstractmethod
    async def initialize(self) -> None:
        """Perform any startup configuration or resource allocation."""

    @abc.abstractmethod
    async def validate(self, **params: Any) -> bool:
        """Validate input parameters before execution."""

    @abc.abstractmethod
    async def execute(self, **params: Any) -> dict[str, Any]:
        """Execute the primary provider logic and return a standardized result."""

    async def handle_errors(self, exc: Exception) -> dict[str, Any]:
        """Convert an exception into a safe standardized response."""
        logger.error("Provider %s error: %s", self.__class__.__name__, exc)
        return {
            "success": False,
            "error": str(exc),
            "provider": self.__class__.__name__,
        }

    async def run(self, **params: Any) -> dict[str, Any]:
        """Full lifecycle: initialize → validate → execute, with error handling."""
        try:
            await self.initialize()
            if not await self.validate(**params):
                return {
                    "success": False,
                    "error": "Validation failed.",
                    "provider": self.__class__.__name__,
                }
            result = await self.execute(**params)
            return {"success": True, **result}
        except Exception as exc:
            return await self.handle_errors(exc)
