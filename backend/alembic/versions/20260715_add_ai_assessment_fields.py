"""add ai assessment fields

Revision ID: 20260715_add_ai_assessment_fields
Revises: 20260711_add_visit_transcript
Create Date: 2026-07-15

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '20260715_add_ai_assessment_fields'
down_revision: Union[str, None] = '20260711_add_visit_transcript'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('ai_sessions', sa.Column('assessment_done', sa.Boolean(), nullable=False, server_default='false'))
    op.add_column('ai_sessions', sa.Column('confidence', sa.Float(), nullable=False, server_default='0.0'))
    op.add_column('ai_sessions', sa.Column('gaps_remaining', sa.Integer(), nullable=False, server_default='0'))
    op.add_column('ai_sessions', sa.Column('candidate_domains', postgresql.JSONB(astext_type=sa.Text()), nullable=True))
    op.add_column('ai_sessions', sa.Column('key_symptoms', postgresql.JSONB(astext_type=sa.Text()), nullable=True))
    op.add_column('ai_sessions', sa.Column('missing_info', postgresql.JSONB(astext_type=sa.Text()), nullable=True))
    op.add_column('ai_sessions', sa.Column('risk_flags', postgresql.JSONB(astext_type=sa.Text()), nullable=True))
    op.add_column('ai_sessions', sa.Column('appointment_id', sa.UUID(), nullable=True))
    op.create_foreign_key(
        'fk_ai_sessions_appointment_id_appointments',
        'ai_sessions',
        'appointments',
        ['appointment_id'],
        ['id'],
        ondelete='SET NULL',
    )


def downgrade() -> None:
    op.drop_constraint('fk_ai_sessions_appointment_id_appointments', 'ai_sessions', type_='foreignkey')
    op.drop_column('ai_sessions', 'appointment_id')
    op.drop_column('ai_sessions', 'risk_flags')
    op.drop_column('ai_sessions', 'missing_info')
    op.drop_column('ai_sessions', 'key_symptoms')
    op.drop_column('ai_sessions', 'candidate_domains')
    op.drop_column('ai_sessions', 'gaps_remaining')
    op.drop_column('ai_sessions', 'confidence')
    op.drop_column('ai_sessions', 'assessment_done')
