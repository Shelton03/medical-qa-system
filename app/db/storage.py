"""S3-compatible object storage client (MinIO).

Bytes live in the bucket; PostgreSQL keeps only metadata (``attachments``
table, indexed by ``object_key``). Configure via Settings: S3_ENDPOINT,
S3_ACCESS_KEY, S3_SECRET_KEY, S3_BUCKET, S3_REGION.
"""
from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.core.config import Settings

from app.core.logger import logger


class StorageError(Exception):
    def __init__(self, code: str, message: str):
        self.code = code
        self.message = message
        super().__init__(message)


class StorageClient:
    """Thin boto3 wrapper. Callers only use put/get/delete/ensure_bucket."""

    def __init__(self, settings: "Settings"):
        self.settings = settings
        self._client = None

    def _get_client(self):
        if self._client is not None:
            return self._client
        try:
            import boto3
            from botocore.config import Config
        except ImportError as exc:  # pragma: no cover
            raise StorageError("storage_not_configured", "boto3 is not installed") from exc

        endpoint = self.settings.S3_ENDPOINT
        if not endpoint:
            raise StorageError(
                "storage_not_configured",
                "S3_ENDPOINT is not configured; refusing to fall back to AWS S3",
            )
        region = self.settings.S3_REGION or None
        config = Config(
            # MinIO needs path-style addressing
            s3={"addressing_style": "path" if "minio" in endpoint.lower() else "auto"},
            retries={"max_attempts": 3, "mode": "standard"},
        )
        self._client = boto3.client(
            "s3",
            endpoint_url=endpoint,
            aws_access_key_id=self.settings.S3_ACCESS_KEY or None,
            aws_secret_access_key=self.settings.S3_SECRET_KEY or None,
            region_name=region,
            config=config,
        )
        return self._client

    def ensure_bucket(self) -> None:
        """Create the bucket if missing. Fail soft when storage is not configured."""
        if not self.settings.S3_ENDPOINT:
            return
        try:
            client = self._get_client()
        except StorageError as exc:
            logger.warning("Object storage not available: %s", exc.message)
            return
        try:
            client.head_bucket(Bucket=self.settings.S3_BUCKET)
        except Exception:
            try:
                client.create_bucket(Bucket=self.settings.S3_BUCKET)
                logger.info("Created object storage bucket: %s", self.settings.S3_BUCKET)
            except Exception as exc:  # pragma: no cover
                logger.warning("Could not create bucket %s: %s", self.settings.S3_BUCKET, exc)

    def put(self, key: str, data: bytes, content_type: str = "application/octet-stream") -> None:
        try:
            self._get_client().put_object(
                Bucket=self.settings.S3_BUCKET,
                Key=key,
                Body=data,
                ContentType=content_type,
            )
        except Exception as exc:
            raise StorageError("upload_failed", str(exc)) from exc

    def get(self, key: str) -> bytes:
        try:
            resp = self._get_client().get_object(Bucket=self.settings.S3_BUCKET, Key=key)
            return resp["Body"].read()
        except Exception as exc:
            raise StorageError("download_failed", str(exc)) from exc

    def delete(self, key: str) -> None:
        try:
            self._get_client().delete_object(Bucket=self.settings.S3_BUCKET, Key=key)
        except Exception as exc:
            raise StorageError("delete_failed", str(exc)) from exc

    def presigned_url(self, key: str, expires_seconds: int = 3600) -> str:
        """Presigned GET URL so clients can fetch the object directly."""
        try:
            return self._get_client().generate_presigned_url(
                "get_object",
                Params={"Bucket": self.settings.S3_BUCKET, "Key": key},
                ExpiresIn=expires_seconds,
            )
        except Exception as exc:
            raise StorageError("presign_failed", str(exc)) from exc


def get_storage_client(settings: "Settings") -> StorageClient:
    return StorageClient(settings)
