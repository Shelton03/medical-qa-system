from __future__ import annotations

# Re-exports: all legacy code should import from app.db.models directly.
# This module is kept only for backward compatibility.
from app.db.models import (
    User,
    Doctor,
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
