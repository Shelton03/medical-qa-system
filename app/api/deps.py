from app.db.mongodb import get_database
from app.db.repositories import SessionRepository, MessageRepository
from app.services.orchestrator import Orchestrator
from fastapi import Depends

def get_session_repo(db = Depends(get_database)) -> SessionRepository:
    return SessionRepository(db)

def get_message_repo(db = Depends(get_database)) -> MessageRepository:
    return MessageRepository(db)

def get_orchestrator(
    session_repo: SessionRepository = Depends(get_session_repo),
    message_repo: MessageRepository = Depends(get_message_repo)
) -> Orchestrator:
    return Orchestrator(session_repo, message_repo)
