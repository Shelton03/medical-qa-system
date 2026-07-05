from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List, Literal
from datetime import datetime
import uuid

class Message(BaseModel):
    session_id: str
    role: Literal["user", "assistant"]
    content: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    message_type: Literal["question", "answer", "initial"]

    model_config = ConfigDict(from_attributes=True)

class Session(BaseModel):
    session_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: Optional[int] = None
    first_message: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    # State flags
    assessment_done: bool = False
    confidence: float = 0.0
    gaps_remaining: int = 0
    
    # Assessment Data
    candidate_domains: List[str] = Field(default_factory=list)
    key_symptoms: List[str] = Field(default_factory=list)
    missing_info: List[str] = Field(default_factory=list)
    answered_info: List[str] = Field(default_factory=list)
    risk_flags: List[str] = Field(default_factory=list)

    model_config = ConfigDict(from_attributes=True)
