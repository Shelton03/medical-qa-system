"""Add visit transcript column

Revision ID: 20260711_add_visit_transcript
Revises: 20260709_add_appointment_booking
Create Date: 2026-07-11

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '20260711_add_visit_transcript'
down_revision = '20260709_add_appointment_booking'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('visits', sa.Column('transcript', sa.Text(), nullable=True))


def downgrade() -> None:
    op.drop_column('visits', 'transcript')
