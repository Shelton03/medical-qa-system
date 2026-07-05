from __future__ import annotations

from pydantic import BaseModel, ConfigDict


class UserResponse(BaseModel):
    """Public representation of an authenticated user."""

    model_config = ConfigDict(strict=True)
    id: str
    role: str
    first_name: str
    last_name: str
    email: str
    avatar_url: str | None = None
