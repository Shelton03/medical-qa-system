from motor.motor_asyncio import AsyncIOMotorClient
from app.models.domain import Session, Message
from app.core.logger import logger
from datetime import datetime
from typing import List, Optional

class SessionRepository:
    def __init__(self, db):
        self.collection = db["sessions"]

    async def create_session(self, session: Session) -> Session:
        await self.collection.insert_one(session.model_dump())
        return session

    async def get_session(self, session_id: str) -> Optional[Session]:
        data = await self.collection.find_one({"session_id": session_id})
        if data:
            return Session(**data)
        return None

    async def update_session(self, session: Session):
        session.updated_at = datetime.utcnow()
        await self.collection.replace_one(
            {"session_id": session.session_id},
            session.model_dump()
        )

    async def get_user_sessions(self, user_id: int) -> List[Session]:
        cursor = self.collection.find({"user_id": user_id}).sort("updated_at", -1)
        sessions = await cursor.to_list(length=None)
        return [Session(**s) for s in sessions]

    async def delete_session(self, session_id: str):
        await self.collection.delete_one({"session_id": session_id})

class MessageRepository:
    def __init__(self, db):
        self.collection = db["messages"]

    async def add_message(self, message: Message):
        await self.collection.insert_one(message.model_dump())

    async def get_session_history(self, session_id: str) -> List[Message]:
        cursor = self.collection.find({"session_id": session_id}).sort("timestamp", 1)
        messages = await cursor.to_list(length=None)
        return [Message(**msg) for msg in messages]

    async def get_first_user_message(self, session_id: str) -> Optional[str]:
        doc = await self.collection.find_one(
            {"session_id": session_id, "role": "user"},
            sort=[("timestamp", 1)]
        )
        return doc["content"] if doc else None
