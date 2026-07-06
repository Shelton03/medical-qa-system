"""MockStorageProvider — saves to local filesystem in /tmp/."""

from __future__ import annotations

import logging
import os
from typing import Any

from app.providers.interfaces.storage import StorageProvider

logger = logging.getLogger(__name__)


class MockStorageProvider(StorageProvider):
    """Synthetic file storage provider that persists to ``/tmp/mirage_storage/``."""

    BASE_DIR = "/tmp/mirage_storage"

    async def initialize(self) -> None:
        os.makedirs(self.BASE_DIR, exist_ok=True)

    async def validate(self, **params: Any) -> bool:
        return True

    async def execute(self, **params: Any) -> dict[str, Any]:
        return params

    async def upload(self, key: str, data: bytes, mime_type: str | None = None) -> dict[str, Any]:
        await self.initialize()
        safe_key = key.replace("..", "").lstrip("/")
        full_path = os.path.join(self.BASE_DIR, safe_key)
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        with open(full_path, "wb") as fh:
            fh.write(data)
        logger.info("[MockStorage] Uploaded %s (%d bytes)", full_path, len(data))
        return {
            "success": True,
            "key": safe_key,
            "size": len(data),
            "mime_type": mime_type,
        }

    async def download(self, key: str) -> bytes:
        safe_key = key.replace("..", "").lstrip("/")
        full_path = os.path.join(self.BASE_DIR, safe_key)
        with open(full_path, "rb") as fh:
            return fh.read()

    async def delete(self, key: str) -> dict[str, Any]:
        safe_key = key.replace("..", "").lstrip("/")
        full_path = os.path.join(self.BASE_DIR, safe_key)
        if os.path.exists(full_path):
            os.remove(full_path)
            logger.info("[MockStorage] Deleted %s", full_path)
        return {"success": True, "key": safe_key}
