"""make ai_sessions patient_id nullable

Revision ID: e5f6a7b8c9d0
Revises: d9478b961bc5
Create Date: 2026-09-18 11:45:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "e5f6a7b8c9d0"
down_revision: Union[str, None] = "d9478b961bc5"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column("ai_sessions", "patient_id", existing_type=sa.UUID(), nullable=True)


def downgrade() -> None:
    op.alter_column("ai_sessions", "patient_id", existing_type=sa.UUID(), nullable=False)
