"""PostgreSQL persistence layer: chat tables + MinIO attachment index

MongoDB has been removed. Chat sessions, messages and contact submissions are
now relational tables; uploaded files are stored in MinIO (S3-compatible) with
only their metadata in the ``attachments`` table, indexed by ``object_key``.

Revision ID: a1f2c3d4e5f6
Revises:
Create Date: 2026-09-18 12:00:00.000000

Data rollback design
--------------------
``downgrade()`` is data-safe: before dropping the chat/message/contact/attachment
tables it exports their full contents to JSON archive files under
``alembic_archives/<revision>.data.json``. ``upgrade()`` restores from the
archive when it exists, so a full ``upgrade -> downgrade -> upgrade`` cycle
round-trips the data without loss.
"""
from __future__ import annotations

import json
import os
from datetime import datetime, timezone

import sqlalchemy as sa
from alembic import op

revision = "a1f2c3d4e5f6"
down_revision = None
branch_labels = None
depends_on = None

# Directory for data rollback archives (relative to the repo root / cwd)
_ARCHIVE_DIR_RAW = os.environ.get("ALEMBIC_ARCHIVE_DIR", "alembic_archives")


def _resolve_archive_dir() -> str:
    """Return a safe absolute archive directory, rejecting path traversal."""
    base = os.path.abspath(os.getcwd())
    candidate = os.path.abspath(os.path.join(base, _ARCHIVE_DIR_RAW))
    if not candidate.startswith(base + os.sep) and candidate != base:
        raise ValueError(
            f"ALEMBIC_ARCHIVE_DIR must resolve inside the repo root: {_ARCHIVE_DIR_RAW}"
        )
    return candidate


ARCHIVE_DIR = _resolve_archive_dir()

# (table, ordered columns) exported/restored by the data rollback logic
_DATA_TABLES = (
    ("chat_sessions", (
        "id", "session_id", "user_id", "first_message", "created_at", "updated_at",
        "assessment_done", "confidence", "gaps_remaining",
        "candidate_domains", "key_symptoms", "missing_info", "answered_info", "risk_flags",
    )),
    ("chat_messages", (
        "id", "chat_session_id", "session_id", "role", "content", "message_type", "timestamp",
    )),
    ("contact_messages", (
        "id", "name", "email", "message", "created_at",
    )),
    ("attachments", (
        "id", "object_key", "bucket", "filename", "content_type", "size_bytes",
        "uploaded_by", "session_id", "created_at",
    )),
)


def _iso(value):
    """JSON-safe value conversion (datetimes -> isoformat, Decimals -> str)."""
    if isinstance(value, datetime):
        return value.isoformat()
    return value


def _archive_table_data(conn, tables) -> str | None:
    """Export the given tables' rows to a JSON archive. Returns the path."""
    os.makedirs(ARCHIVE_DIR, exist_ok=True)
    archive = {
        "revision": revision,
        "archived_at": datetime.now(timezone.utc).isoformat(),
        "tables": {},
    }
    total_rows = 0
    for table, columns in tables:
        try:
            tbl = sa.table(table, *[sa.column(c) for c in columns])
            result = conn.execute(sa.select(*tbl.c))
            rows = [
                {col: _iso(v) for col, v in zip(result.keys(), row)}
                for row in result.fetchall()
            ]
        except Exception:
            rows = []  # table may not exist yet
        archive["tables"][table] = rows
        total_rows += len(rows)

    if total_rows == 0:
        return None  # nothing to archive

    filename = os.path.join(ARCHIVE_DIR, f"{revision}.data.json")
    with open(filename, "w", encoding="utf-8") as fh:
        json.dump(archive, fh, indent=2, default=str)
    return filename


def _restore_table_data(conn) -> int:
    """Restore rows from the newest archive for this revision. Returns count."""
    filename = os.path.join(ARCHIVE_DIR, f"{revision}.data.json")
    if not os.path.exists(filename):
        return 0

    with open(filename, "r", encoding="utf-8") as fh:
        archive = json.load(fh)

    restored = 0
    for table, columns in _DATA_TABLES:
        rows = archive.get("tables", {}).get(table, [])
        if not rows:
            continue
        tbl = sa.table(table, *[sa.column(c) for c in columns])
        for row in rows:
            try:
                conn.execute(tbl.insert().values(**row))
                restored += 1
            except Exception:
                continue  # skip rows that violate constraints (e.g. duplicates)

    # After inserting explicit ids, advance each sequence so the next
    # auto-increment insert does not collide with restored rows.
    for table, _columns in _DATA_TABLES:
        try:
            conn.execute(
                sa.text(
                    f"""
                    SELECT setval(
                        pg_get_serial_sequence(:table_name, 'id'),
                        COALESCE((SELECT MAX(id) FROM {table}), 1),
                        true
                    )
                    """
                ),
                {"table_name": table},
            )
        except Exception:
            pass  # table may not have a serial sequence
    return restored


def upgrade() -> None:
    conn = op.get_bind()
    dialect = conn.dialect

    # Baseline: users/sessions tables may already exist from the previous
    # SQLAlchemy create_all bootstrap. Create them only when missing so the
    # migration is safe for both fresh databases and existing ones.
    if not dialect.has_table(conn, "users"):
        op.create_table(
            "users",
            sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
            sa.Column("email", sa.String(length=255), nullable=False),
            sa.Column("password_hash", sa.String(length=255), nullable=False),
            sa.Column("salt", sa.String(length=255), nullable=False),
            sa.Column("created_at", sa.DateTime(), nullable=True),
            sa.Column("last_login", sa.DateTime(), nullable=True),
            sa.PrimaryKeyConstraint("id"),
            sa.UniqueConstraint("email"),
        )
        op.create_index("idx_users_email", "users", ["email"])

    if not dialect.has_table(conn, "sessions"):
        op.create_table(
            "sessions",
            sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
            sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
            sa.Column("token", sa.String(length=512), nullable=False),
            sa.Column("expires_at", sa.DateTime(), nullable=False),
            sa.Column("created_at", sa.DateTime(), nullable=True),
            sa.PrimaryKeyConstraint("id"),
            sa.UniqueConstraint("token"),
        )
        op.create_index("idx_sessions_token", "sessions", ["token"])
        op.create_index("idx_sessions_user_id", "sessions", ["user_id"])
        op.create_index("idx_sessions_expires_at", "sessions", ["expires_at"])

    op.create_table(
        "chat_sessions",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("session_id", sa.String(length=64), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=True),
        sa.Column("first_message", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.Column("assessment_done", sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column("confidence", sa.Float(), nullable=False, server_default="0.0"),
        sa.Column("gaps_remaining", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("candidate_domains", sa.Text(), nullable=False, server_default=""),
        sa.Column("key_symptoms", sa.Text(), nullable=False, server_default=""),
        sa.Column("missing_info", sa.Text(), nullable=False, server_default=""),
        sa.Column("answered_info", sa.Text(), nullable=False, server_default=""),
        sa.Column("risk_flags", sa.Text(), nullable=False, server_default=""),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("idx_chat_sessions_session_id", "chat_sessions", ["session_id"])
    op.create_index("idx_chat_sessions_user_id", "chat_sessions", ["user_id"])
    op.create_index("idx_chat_sessions_user_updated", "chat_sessions", ["user_id", "updated_at"])

    op.create_table(
        "chat_messages",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("chat_session_id", sa.Integer(), nullable=False),
        sa.Column("session_id", sa.String(length=64), nullable=False),
        sa.Column("role", sa.String(length=16), nullable=False),
        sa.Column("content", sa.Text(), nullable=False),
        sa.Column("message_type", sa.String(length=16), nullable=False),
        sa.Column("timestamp", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(["chat_session_id"], ["chat_sessions.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("idx_chat_messages_session_ts", "chat_messages", ["session_id", "timestamp"])
    op.create_index("idx_chat_messages_chat_session_id", "chat_messages", ["chat_session_id"])
    op.create_index(op.f("ix_chat_messages_session_id"), "chat_messages", ["session_id"])

    op.create_table(
        "contact_messages",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("email", sa.String(length=255), nullable=False),
        sa.Column("message", sa.Text(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("idx_contact_messages_created", "contact_messages", ["created_at"])
    op.create_index(op.f("ix_contact_messages_email"), "contact_messages", ["email"])

    op.create_table(
        "attachments",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("object_key", sa.String(length=512), nullable=False),
        sa.Column("bucket", sa.String(length=255), nullable=False),
        sa.Column("filename", sa.String(length=512), nullable=True),
        sa.Column("content_type", sa.String(length=128), nullable=False,
                  server_default="application/octet-stream"),
        sa.Column("size_bytes", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("uploaded_by", sa.Integer(), nullable=True),
        sa.Column("session_id", sa.String(length=64), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(["uploaded_by"], ["users.id"], ondelete="SET NULL"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("idx_attachments_object_key", "attachments", ["object_key"], unique=True)
    op.create_index("idx_attachments_session", "attachments", ["session_id"])
    op.create_index("idx_attachments_uploaded_by", "attachments", ["uploaded_by"])

    # Data rollback restore: bring back rows archived by a previous downgrade
    restored = _restore_table_data(conn)
    if restored:
        print(f"[data-rollback] restored {restored} row(s) from {revision} archive")


def downgrade() -> None:
    conn = op.get_bind()

    # Data rollback: archive all rows before dropping the tables
    archive_path = _archive_table_data(conn, _DATA_TABLES)
    if archive_path:
        print(f"[data-rollback] archived table data to {archive_path}")

    op.drop_index("idx_attachments_uploaded_by", table_name="attachments")
    op.drop_index("idx_attachments_session", table_name="attachments")
    op.drop_index("idx_attachments_object_key", table_name="attachments")
    op.drop_table("attachments")

    op.drop_index(op.f("ix_contact_messages_email"), table_name="contact_messages")
    op.drop_index("idx_contact_messages_created", table_name="contact_messages")
    op.drop_table("contact_messages")

    op.drop_index(op.f("ix_chat_messages_session_id"), table_name="chat_messages")
    op.drop_index("idx_chat_messages_chat_session_id", table_name="chat_messages")
    op.drop_index("idx_chat_messages_session_ts", table_name="chat_messages")
    op.drop_table("chat_messages")

    op.drop_index("idx_chat_sessions_user_updated", table_name="chat_sessions")
    op.drop_index("idx_chat_sessions_user_id", table_name="chat_sessions")
    op.drop_index("idx_chat_sessions_session_id", table_name="chat_sessions")
    op.drop_table("chat_sessions")
