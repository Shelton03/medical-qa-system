"""SQLAlchemy models for the Medical QA System (PostgreSQL persistence).

MongoDB has been removed: chat sessions, messages and contacts are now
relational tables. Uploaded images/files live in MinIO (S3-compatible object
storage); this schema keeps only their metadata, indexed by ``object_key``.
"""
from datetime import datetime
from typing import List, Optional

from sqlalchemy import (
    ForeignKey,
    Index,
    String,
    Text,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.postgres import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    password_hash: Mapped[str] = mapped_column(String(255))
    salt: Mapped[str] = mapped_column(String(255))
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    last_login: Mapped[Optional[datetime]] = mapped_column(nullable=True)

    sessions: Mapped[List["Session"]] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )

    __table_args__ = (
        Index("idx_users_email", "email"),
    )


class Session(Base):
    """Auth/session tokens (pre-existing table)."""
    __tablename__ = "sessions"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
    )
    token: Mapped[str] = mapped_column(String(512), unique=True, index=True)
    expires_at: Mapped[datetime]
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)

    user: Mapped["User"] = relationship(back_populates="sessions")

    __table_args__ = (
        Index("idx_sessions_token", "token"),
        Index("idx_sessions_user_id", "user_id"),
        Index("idx_sessions_expires_at", "expires_at"),
    )


class ChatSession(Base):
    """A conversational QA session (was MongoDB collection ``sessions``)."""
    __tablename__ = "chat_sessions"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    session_id: Mapped[str] = mapped_column(String(64), unique=True, index=True)
    user_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=True,
        index=True,
    )
    first_message: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)

    # State flags
    assessment_done: Mapped[bool] = mapped_column(default=False)
    confidence: Mapped[float] = mapped_column(default=0.0)
    gaps_remaining: Mapped[int] = mapped_column(default=0)

    # Assessment data (was embedded document arrays in Mongo)
    candidate_domains: Mapped[str] = mapped_column(Text, default="")
    key_symptoms: Mapped[str] = mapped_column(Text, default="")
    missing_info: Mapped[str] = mapped_column(Text, default="")
    answered_info: Mapped[str] = mapped_column(Text, default="")
    risk_flags: Mapped[str] = mapped_column(Text, default="")

    messages: Mapped[List["ChatMessage"]] = relationship(
        back_populates="chat_session",
        cascade="all, delete-orphan",
        foreign_keys="ChatMessage.chat_session_id",
    )

    __table_args__ = (
        Index("idx_chat_sessions_session_id", "session_id"),
        Index("idx_chat_sessions_user_id", "user_id"),
        Index("idx_chat_sessions_user_updated", "user_id", "updated_at"),
    )


class ChatMessage(Base):
    """One turn in a chat session (was MongoDB collection ``messages``)."""
    __tablename__ = "chat_messages"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    chat_session_id: Mapped[int] = mapped_column(
        ForeignKey("chat_sessions.id", ondelete="CASCADE"),
    )
    session_id: Mapped[str] = mapped_column(String(64), index=True)
    role: Mapped[str] = mapped_column(String(16))
    content: Mapped[str] = mapped_column(Text)
    message_type: Mapped[str] = mapped_column(String(16))
    timestamp: Mapped[datetime] = mapped_column(default=datetime.utcnow)

    chat_session: Mapped["ChatSession"] = relationship(
        back_populates="messages",
        foreign_keys=[chat_session_id],
    )

    __table_args__ = (
        Index("idx_chat_messages_session_ts", "session_id", "timestamp"),
        Index("idx_chat_messages_chat_session_id", "chat_session_id"),
    )


class ContactMessage(Base):
    """Contact-form submissions (was MongoDB collection ``contacts``)."""
    __tablename__ = "contact_messages"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(255))
    email: Mapped[str] = mapped_column(String(255), index=True)
    message: Mapped[str] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)

    __table_args__ = (
        Index("idx_contact_messages_created", "created_at"),
    )


class Attachment(Base):
    """Metadata for a file stored in MinIO object storage.

    Bytes live in the bucket at ``object_key``; this row is the index.
    ``object_key`` is unique and indexed so lookups by storage key are exact.
    """
    __tablename__ = "attachments"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    object_key: Mapped[str] = mapped_column(String(512), unique=True, index=True)
    bucket: Mapped[str] = mapped_column(String(255))
    filename: Mapped[Optional[str]] = mapped_column(String(512), nullable=True)
    content_type: Mapped[str] = mapped_column(
        String(128),
        default="application/octet-stream",
    )
    size_bytes: Mapped[int] = mapped_column(default=0)
    uploaded_by: Mapped[Optional[int]] = mapped_column(
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    session_id: Mapped[Optional[str]] = mapped_column(
        String(64),
        nullable=True,
        index=True,
    )
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)

    __table_args__ = (
        Index("idx_attachments_object_key", "object_key"),
        Index("idx_attachments_session", "session_id"),
        Index("idx_attachments_uploaded_by", "uploaded_by"),
    )
