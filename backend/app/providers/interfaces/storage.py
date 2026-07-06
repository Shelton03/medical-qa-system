"""StorageProvider interface."""

from __future__ import annotations

import abc
from typing import Any

from app.providers.interfaces.base import BaseProvider


class StorageProvider(BaseProvider, abc.ABC):
    """
    Interface for file / object storage providers.

    Responsibilities:
    - Upload files and return a storage key.
    - Retrieve files by key.
    - Delete files by key.
    """

    @abc.abstractmethod
    async def upload(self, key: str, data: bytes, mime_type: str | None = None) -> dict[str, Any]:
        """Persist *data* under *key* and return metadata."""

    @abc.abstractmethod
    async def download(self, key: str) -> bytes:
        """Retrieve the binary content for *key*."""

    @abc.abstractmethod
    async def delete(self, key: str) -> dict[str, Any]:
        """Remove the object at *key* and return a status."""
