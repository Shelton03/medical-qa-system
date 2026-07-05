from __future__ import annotations

from app.models.user import User
from app.models.doctor import Doctor
from app.models.patient_record import (
    Patient,
    MedicalRecord,
    Allergy,
    ChronicCondition,
    Medication,
)

__all__ = [
    "User",
    "Doctor",
    "Patient",
    "MedicalRecord",
    "Allergy",
    "ChronicCondition",
    "Medication",
]
