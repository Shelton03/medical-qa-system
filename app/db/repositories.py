"""Async SQLAlchemy repositories (replacing the Motor/MongoDB repositories).

ChatSession/ChatMessage persist to PostgreSQL; uploaded files go to MinIO via
``app.db.storage`` with only their metadata kept in the ``attachments`` table.
"""
import json
import re
import uuid
from datetime import datetime
from typing import List, Optional

from sqlalchemy import select, delete, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import ChatSession, ChatMessage, ContactMessage, Attachment
from app.db.storage import StorageClient


# ---------------------------------------------------------------------------
# Domain <-> row helpers (list fields stored as JSON text columns)
# ---------------------------------------------------------------------------

_LIST_FIELDS = (
    "candidate_domains", "key_symptoms", "missing_info", "answered_info", "risk_flags",
)


def _domain_to_row(session) -> ChatSession:
    """Convert a Pydantic domain Session into a ChatSession row."""
    row = ChatSession(
        session_id=session.session_id,
        user_id=session.user_id,
        first_message=session.first_message,
        created_at=session.created_at,
        updated_at=session.updated_at,
        assessment_done=session.assessment_done,
        confidence=session.confidence,
        gaps_remaining=session.gaps_remaining,
    )
    for f in _LIST_FIELDS:
        value = getattr(session, f) or []
        if not isinstance(value, list):
            value = []
        setattr(row, f, json.dumps(value))
    return row


def _update_row_from_domain(row: ChatSession, session) -> None:
    row.session_id = session.session_id
    row.user_id = session.user_id
    row.first_message = session.first_message
    row.updated_at = datetime.utcnow()
    row.assessment_done = session.assessment_done
    row.confidence = session.confidence
    row.gaps_remaining = session.gaps_remaining
    for f in _LIST_FIELDS:
        value = getattr(session, f) or []
        if not isinstance(value, list):
            value = []
        setattr(row, f, json.dumps(value))


def _row_to_domain(row: ChatSession):
    """Rebuild the Pydantic domain Session from a ChatSession row."""
    from app.models.domain import Session as DomainSession

    kwargs = {
        "session_id": row.session_id,
        "user_id": row.user_id,
        "first_message": row.first_message,
        "created_at": row.created_at,
        "updated_at": row.updated_at,
        "assessment_done": row.assessment_done,
        "confidence": row.confidence,
        "gaps_remaining": row.gaps_remaining,
    }
    for f in _LIST_FIELDS:
        raw = getattr(row, f) or "[]"
        try:
            kwargs[f] = json.loads(raw)
        except (ValueError, TypeError):
            kwargs[f] = []
    return DomainSession(**kwargs)


# ---------------------------------------------------------------------------
# Session repository
# ---------------------------------------------------------------------------

class SessionRepository:
    """Chat-session persistence (was MongoDB ``sessions`` collection)."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_session(self, session) -> None:
        row = _domain_to_row(session)
        self.db.add(row)
        await self.db.flush()

    async def get_session(self, session_id: str):
        result = await self.db.execute(
            select(ChatSession).where(ChatSession.session_id == session_id)
        )
        row = result.scalar_one_or_none()
        return _row_to_domain(row) if row else None

    async def update_session(self, session) -> None:
        result = await self.db.execute(
            select(ChatSession).where(ChatSession.session_id == session.session_id)
        )
        row = result.scalar_one_or_none()
        if row:
            _update_row_from_domain(row, session)
            await self.db.flush()

    async def get_user_sessions(self, user_id: int) -> List:
        result = await self.db.execute(
            select(ChatSession)
            .where(ChatSession.user_id == user_id)
            .order_by(ChatSession.updated_at.desc())
        )
        return [_row_to_domain(r) for r in result.scalars().all()]

    async def delete_session(self, session_id: str) -> None:
        await self.db.execute(
            delete(ChatSession).where(ChatSession.session_id == session_id)
        )


# ---------------------------------------------------------------------------
# Message repository
# ---------------------------------------------------------------------------

class MessageRepository:
    """Chat-message persistence (was MongoDB ``messages`` collection)."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def add_message(self, message) -> None:
        row = ChatMessage(
            session_id=message.session_id,
            role=message.role,
            content=message.content,
            message_type=message.message_type,
            timestamp=message.timestamp,
        )
        # Link to the parent chat_sessions row via its integer PK.
        result = await self.db.execute(
            select(ChatSession.id).where(ChatSession.session_id == message.session_id)
        )
        parent_id = result.scalar_one_or_none()
        if not parent_id:
            raise ValueError(f"Chat session {message.session_id} not found")
        row.chat_session_id = parent_id
        self.db.add(row)
        await self.db.flush()

    async def get_session_history(self, session_id: str) -> List:
        result = await self.db.execute(
            select(ChatMessage)
            .where(ChatMessage.session_id == session_id)
            .order_by(ChatMessage.timestamp.asc())
        )
        rows = result.scalars().all()
        from app.models.domain import Message as DomainMessage

        return [
            DomainMessage(
                session_id=r.session_id,
                role=r.role,
                content=r.content,
                timestamp=r.timestamp,
                message_type=r.message_type,
            )
            for r in rows
        ]

    async def get_first_user_message(self, session_id: str) -> Optional[str]:
        result = await self.db.execute(
            select(ChatMessage.content)
            .where(ChatMessage.session_id == session_id, ChatMessage.role == "user")
            .order_by(ChatMessage.timestamp.asc())
            .limit(1)
        )
        return result.scalar_one_or_none()

    async def delete_session_messages(self, session_id: str) -> None:
        await self.db.execute(
            delete(ChatMessage).where(ChatMessage.session_id == session_id)
        )


# ---------------------------------------------------------------------------
# Contact repository (was MongoDB ``contacts`` collection)
# ---------------------------------------------------------------------------

class ContactRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def add_contact(self, name: str, email: str, message: str) -> int:
        row = ContactMessage(name=name, email=email, message=message)
        self.db.add(row)
        await self.db.flush()
        return row.id


# ---------------------------------------------------------------------------
# Attachment repository (MinIO metadata index)
# ---------------------------------------------------------------------------

_SAFE_NAME_RE = re.compile(r"[^A-Za-z0-9._-]+")


def safe_filename(filename: str) -> str:
    """Path-traversal-safe filename: strip slashes, dots-segments, controls."""
    name = filename.replace("\\", "/").split("/")[-1]
    name = name.replace("..", "")
    name = _SAFE_NAME_RE.sub("_", name).strip("._") or "file"
    return name[:200]


def build_object_key(category: str, filename: str) -> str:
    """Deterministic storage key: <year>/<category>/<uuid>_<safe_filename>."""
    year = datetime.utcnow().strftime("%Y")
    return f"{year}/{category}/{uuid.uuid4().hex}_{safe_filename(filename)}"


class AttachmentRepository:
    """Metadata index for objects stored in MinIO."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_attachment(
        self,
        object_key: str,
        bucket: str,
        content_type: str,
        size_bytes: int,
        filename: Optional[str] = None,
        uploaded_by: Optional[int] = None,
        session_id: Optional[str] = None,
    ) -> Attachment:
        row = Attachment(
            object_key=object_key,
            bucket=bucket,
            filename=filename,
            content_type=content_type,
            size_bytes=size_bytes,
            uploaded_by=uploaded_by,
            session_id=session_id,
        )
        self.db.add(row)
        await self.db.flush()
        return row

    async def get_by_object_key(self, object_key: str) -> Optional[Attachment]:
        result = await self.db.execute(
            select(Attachment).where(Attachment.object_key == object_key)
        )
        return result.scalar_one_or_none()

    async def get_by_id(self, attachment_id: int) -> Optional[Attachment]:
        result = await self.db.execute(
            select(Attachment).where(Attachment.id == attachment_id)
        )
        return result.scalar_one_or_none()

    async def list_by_session(self, session_id: str) -> List[Attachment]:
        result = await self.db.execute(
            select(Attachment)
            .where(Attachment.session_id == session_id)
            .order_by(Attachment.created_at.desc())
        )
        return list(result.scalars().all())

    async def list_by_user(self, user_id: int) -> List[Attachment]:
        result = await self.db.execute(
            select(Attachment)
            .where(Attachment.uploaded_by == user_id)
            .order_by(Attachment.created_at.desc())
        )
        return list(result.scalars().all())

    async def delete_attachment(
        self,
        attachment_id: int,
        storage: Optional[StorageClient] = None,
    ) -> Optional[Attachment]:
        result = await self.db.execute(
            select(Attachment).where(Attachment.id == attachment_id)
        )
        row = result.scalar_one_or_none()
        if row:
            if storage is not None:
                try:
                    storage.delete(row.object_key)
                except Exception:
                    pass  # metadata deletion must not fail if object is already gone
            await self.db.delete(row)
        return row

    async def delete_by_session_id(
        self,
        session_id: str,
        storage: Optional[StorageClient] = None,
    ) -> int:
        rows = await self.list_by_session(session_id)
        for row in rows:
            if storage is not None:
                try:
                    storage.delete(row.object_key)
                except Exception:
                    pass
            await self.db.delete(row)
        return len(rows)
