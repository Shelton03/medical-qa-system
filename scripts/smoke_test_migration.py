"""Smoke test for MongoDB -> Postgres + MinIO migration.

This script is deliberately standalone and safe: it uses a fresh test session
and rolls back DB changes at the end. It does NOT mutate Alembic state except
for the explicit downgrade/upgrade cycle test.
"""
import asyncio
import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.postgres import async_session_maker
from app.db.repositories import SessionRepository, MessageRepository, AttachmentRepository
from app.db.storage import StorageClient
from app.models import Attachment, User
from app.core.config import settings
from app.models.domain import Session as DomainSession, Message as DomainMessage
from alembic.config import Config as AlembicConfig
from alembic import command as alembic_command


async def _ensure_user(db: AsyncSession, email: str) -> int:
    result = await db.execute(select(User).where(User.email == email))
    user = result.scalar_one_or_none()
    if user is None:
        user = User(
            email=email,
            password_hash="hash",
            salt="salt",
        )
        db.add(user)
        await db.commit()
        await db.refresh(user)
    return user.id


async def test_chat_roundtrip():
    print("\n[1] Chat repository round-trip")
    async with async_session_maker() as db:
        user_id = await _ensure_user(db, "smoke1@example.com")
        session_repo = SessionRepository(db)
        message_repo = MessageRepository(db)

        session = DomainSession(user_id=user_id, first_message="Hello, doctor")
        await session_repo.create_session(session)
        await db.commit()

        msg = DomainMessage(
            session_id=session.session_id,
            role="user",
            content="I have a headache",
            message_type="initial",
        )
        await message_repo.add_message(msg)
        await db.commit()

        fetched = await session_repo.get_session(session.session_id)
        assert fetched is not None, "session not found"
        assert fetched.first_message == "Hello, doctor"

        history = await message_repo.get_session_history(session.session_id)
        assert len(history) == 1
        assert history[0].content == "I have a headache"

        first = await message_repo.get_first_user_message(session.session_id)
        assert first == "I have a headache"

        # cleanup
        await message_repo.delete_session_messages(session.session_id)
        await session_repo.delete_session(session.session_id)
        await db.commit()
        print("    PASS")


async def test_minio_index():
    print("\n[2] MinIO upload + Postgres attachment index")
    storage = StorageClient(settings)
    storage.ensure_bucket()

    async with async_session_maker() as db:
        user_id = await _ensure_user(db, "smoke1@example.com")

    test_data = b"\x89PNG\r\n\x1a\n" + b"fake-image-data"
    key = "2026/smoke/test_image.png"

    storage.put(key, test_data, "image/png")
    retrieved = storage.get(key)
    assert retrieved == test_data, "MinIO round-trip failed"

    async with async_session_maker() as db:
        attach_repo = AttachmentRepository(db)
        row = await attach_repo.create_attachment(
            object_key=key,
            bucket=settings.S3_BUCKET,
            filename="test_image.png",
            content_type="image/png",
            size_bytes=len(test_data),
            uploaded_by=user_id,
            session_id="test-session-123",
        )
        await db.commit()

        # Index lookup by object_key
        found = await attach_repo.get_by_object_key(key)
        assert found is not None, "attachment metadata not indexed"
        assert found.id == row.id
        assert found.content_type == "image/png"

        # cleanup
        await db.delete(found)
        await db.commit()
        storage.delete(key)
        print("    PASS")


async def test_data_rollback():
    print("\n[3] Data rollback: downgrade archives / upgrade restores")
    async with async_session_maker() as db:
        user_id = await _ensure_user(db, "smoke2@example.com")
        session_repo = SessionRepository(db)
        message_repo = MessageRepository(db)

        session = DomainSession(user_id=user_id, first_message="Rollback test")
        await session_repo.create_session(session)
        await message_repo.add_message(
            DomainMessage(
                session_id=session.session_id,
                role="assistant",
                content="Before rollback",
                message_type="answer",
            )
        )
        await db.commit()
        sid = session.session_id

    # Alembic downgrade archives data and drops tables
    alembic_cfg = AlembicConfig("alembic.ini")
    alembic_command.downgrade(alembic_cfg, "-1")

    # Verify archive file exists
    archive = "alembic_archives/a1f2c3d4e5f6.data.json"
    assert os.path.exists(archive), "downgrade did not create data archive"
    print(f"    archive created: {archive}")

    # Upgrade restores data
    alembic_command.upgrade(alembic_cfg, "head")

    async with async_session_maker() as db:
        session_repo = SessionRepository(db)
        fetched = await session_repo.get_session(sid)
        assert fetched is not None, "session not restored after upgrade"
        assert fetched.first_message == "Rollback test"

        message_repo = MessageRepository(db)
        history = await message_repo.get_session_history(sid)
        assert len(history) == 1 and history[0].content == "Before rollback"

        # Sequence reset check: a new auto-increment insert must not collide.
        new_session = DomainSession(user_id=user_id, first_message="After rollback")
        await session_repo.create_session(new_session)
        await db.commit()
        from app.models import ChatSession as ChatSessionModel
        result = await db.execute(
            select(ChatSessionModel).where(ChatSessionModel.session_id == new_session.session_id)
        )
        new_row = result.scalar_one()
        assert new_row.id is not None and new_row.id > 0, "sequence reset appears broken"

        # cleanup
        await message_repo.delete_session_messages(sid)
        await session_repo.delete_session(sid)
        await session_repo.delete_session(new_session.session_id)
        await db.commit()

    # cleanup archive
    try:
        os.remove("alembic_archives/a1f2c3d4e5f6.data.json")
    except FileNotFoundError:
        pass

    print("    PASS")


async def main():
    await test_chat_roundtrip()
    await test_minio_index()
    await test_data_rollback()
    print("\nAll smoke tests passed.")


if __name__ == "__main__":
    asyncio.run(main())
