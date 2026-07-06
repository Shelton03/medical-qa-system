import pytest
from sqlalchemy import func, select

from app.db.models import (
    User,
    Patient,
    Doctor,
    Visit,
    Medication,
    Diagnosis,
    Allergy,
    ChronicCondition,
    LaboratoryResult,
    ImagingResult,
    ConsentRequest,
    Notification,
    AuditLog,
    AISession,
)
from app.db.seeder import seed_demo_data


@pytest.mark.asyncio
async def test_seed_data_creates_expected_counts(db_session):
    await seed_demo_data(db_session)

    counts = {}
    counts["users"] = (
        await db_session.execute(select(func.count(User.id)))
    ).scalar()
    counts["patients"] = (
        await db_session.execute(select(func.count(Patient.id)))
    ).scalar()
    counts["doctors"] = (
        await db_session.execute(select(func.count(Doctor.id)))
    ).scalar()
    counts["visits"] = (
        await db_session.execute(select(func.count(Visit.id)))
    ).scalar()
    counts["medications"] = (
        await db_session.execute(select(func.count(Medication.id)))
    ).scalar()
    counts["diagnoses"] = (
        await db_session.execute(select(func.count(Diagnosis.id)))
    ).scalar()
    counts["allergies"] = (
        await db_session.execute(select(func.count(Allergy.id)))
    ).scalar()
    counts["conditions"] = (
        await db_session.execute(select(func.count(ChronicCondition.id)))
    ).scalar()
    counts["labs"] = (
        await db_session.execute(select(func.count(LaboratoryResult.id)))
    ).scalar()
    counts["imaging"] = (
        await db_session.execute(select(func.count(ImagingResult.id)))
    ).scalar()
    counts["consents"] = (
        await db_session.execute(select(func.count(ConsentRequest.id)))
    ).scalar()
    counts["notifications"] = (
        await db_session.execute(select(func.count(Notification.id)))
    ).scalar()
    counts["ai_sessions"] = (
        await db_session.execute(select(func.count(AISession.id)))
    ).scalar()
    counts["audit_logs"] = (
        await db_session.execute(select(func.count(AuditLog.id)))
    ).scalar()

    assert counts["users"] >= 10 + 5  # 10 patients + 5 doctors
    assert counts["patients"] >= 10
    assert counts["doctors"] >= 5
    assert counts["visits"] >= 50
    assert counts["medications"] >= 150
    assert counts["diagnoses"] >= 120
    assert counts["allergies"] >= 20
    assert counts["conditions"] >= 20
    assert counts["labs"] >= 50
    assert counts["imaging"] >= 10
    assert counts["consents"] >= 20
    assert counts["notifications"] >= 100
    assert counts["ai_sessions"] >= 15
    assert counts["audit_logs"] >= 500
