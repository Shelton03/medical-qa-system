"""add ai message type

Revision ID: 20260715_add_ai_message_type
Revises: 20260715_add_ai_assessment_fields
Create Date: 2026-07-15

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '20260715_add_ai_message_type'
down_revision: Union[str, None] = '20260715_add_ai_assessment_fields'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('ai_messages', sa.Column('message_type', sa.String(length=50), nullable=True))


def downgrade() -> None:
    op.drop_column('ai_messages', 'message_type')
