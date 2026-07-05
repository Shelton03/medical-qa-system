from __future__ import annotations

from pydantic import BaseModel, ConfigDict


class TokenPair(BaseModel):
    """Response model issued on successful authentication."""

    model_config = ConfigDict(strict=True)
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int
    role: str
    demo_mode: bool = False
