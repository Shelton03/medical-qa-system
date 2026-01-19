from pydantic import BaseModel
from typing import Optional

# --- API Request ---
class UserQueryRequest(BaseModel):
    session_id: Optional[str] = None
    message: str