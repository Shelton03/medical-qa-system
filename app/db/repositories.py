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

class MessageRepository:
    def __init__(self, db):
        self.collection = db["messages"]

    async def add_message(self, message: Message):
        await self.collection.insert_one(message.model_dump())

    async def get_session_history(self, session_id: str) -> List[Message]:
        cursor = self.collection.find({"session_id": session_id}).sort("timestamp", 1)
        messages = await cursor.to_list(length=None)
        return [Message(**msg) for msg in messages]
