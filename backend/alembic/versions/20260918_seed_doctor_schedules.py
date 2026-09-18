"""seed doctor schedules for appointment booking

Revision ID: 20260918_seed_doctor_schedules
Revises: e5f6a7b8c9d0
Create Date: 2026-09-18 18:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
from sqlalchemy import text


# revision identifiers, used by Alembic.
revision: str = "20260918_seed_doctor_schedules"
down_revision: Union[str, None] = "e5f6a7b8c9d0"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Seed weekday schedules for all doctors if none exist."""
    conn = op.get_bind()
    count = conn.execute(text("SELECT COUNT(*) FROM doctor_schedules")).scalar()
    if count and count > 0:
        return

    conn.execute(
        text(
            """
            INSERT INTO doctor_schedules (
                id, doctor_id, day_of_week, start_time, end_time,
                is_working_day, default_slot_duration, max_daily_appointments
            )
            SELECT
                gen_random_uuid(),
                d.id,
                dow.day_of_week,
                '08:00:00'::time,
                '17:00:00'::time,
                true,
                30,
                d.max_daily_appointments
            FROM doctors d
            CROSS JOIN (SELECT 0 AS day_of_week UNION ALL
                        SELECT 1 UNION ALL
                        SELECT 2 UNION ALL
                        SELECT 3 UNION ALL
                        SELECT 4) dow
            """
        )
    )


def downgrade() -> None:
    op.execute(text("DELETE FROM doctor_schedules"))
