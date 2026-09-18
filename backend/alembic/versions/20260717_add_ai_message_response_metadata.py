"""persist structured AI response metadata.

Revision ID: 20260717_add_ai_message_response_metadata
Revises: 20260715_add_system_config
Create Date: 2026-07-17
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision: str = "20260717_add_ai_message_response_metadata"
down_revision: Union[str, None] = "20260715_add_system_config"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Add durable metadata for structured assessment answers."""
    op.add_column(
        "ai_messages",
        sa.Column("response_metadata", postgresql.JSONB(astext_type=sa.Text()), nullable=True),
    )


def downgrade() -> None:
    """Remove structured assessment response metadata."""
    op.drop_column("ai_messages", "response_metadata")
