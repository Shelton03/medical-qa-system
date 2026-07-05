#!/usr/bin/env python3
"""Mirage Patient API router."""

from __future__ import annotations

import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.auth.dependencies import get_current_user, get_current_doctor
from app.models import User
from app.schemas.envelope import Envelope
from app.patient import service
from app.patient.schemas import (
    PatientCreate,
    PatientResponse,
    PatientUpdate,
    PatientFullProfileResponse,
    MedicalRecordSummaryResponse,
)

router = APIRouter()


@router.get(
    "",
    response_model=Envelope[list[PatientResponse]],
    summary="List and search patients",
    description="Search patients by name, national ID, or phone. Doctor and admin only.",
)
async def list_patients(
    q: Annotated[str | None, Query(None, description="Search query")] = None,
    limit: Annotated[int, Query(20, ge=1, le=100)] = 20,
    offset: Annotated[int, Query(0, ge=0)] = 0,
    db: AsyncSession = Depends(get_db),
    current_user: User = get_current_doctor,
) -> Envelope[list[PatientResponse]]:
    query = q or ""
    patients, _total = await service.search_patients(db, query, limit, offset, current_user)
    return Envelope.ok(patients)


@router.get(
    "/{patient_id}",
    response_model=Envelope[PatientFullProfileResponse],
    summary="Get patient profile",
    description="Retrieve full patient profile with medical record summary.",
)
async def get_patient(
    patient_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Envelope[PatientFullProfileResponse]:
    profile = await service.get_patient_profile(db, patient_id, current_user)
    return Envelope.ok(profile)


@router.post(
    "",
    response_model=Envelope[PatientResponse],
    summary="Register a new patient",
    description="Create a patient record and linked medical record. Doctor and admin only.",
    status_code=201,
)
async def register_patient(
    data: PatientCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = get_current_doctor,
) -> Envelope[PatientResponse]:
    patient = await service.register_patient(db, data)
    return Envelope.ok(patient)


@router.put(
    "/{patient_id}",
    response_model=Envelope[PatientResponse],
    summary="Update patient record",
    description="Update patient demographics and emergency contacts. Doctor and admin only.",
)
async def update_patient(
    patient_id: uuid.UUID,
    data: PatientUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = get_current_doctor,
) -> Envelope[PatientResponse]:
    patient = await service.update_patient_record(db, patient_id, data, current_user)
    return Envelope.ok(patient)


@router.get(
    "/{patient_id}/records",
    response_model=Envelope[MedicalRecordSummaryResponse],
    summary="Get medical record summary",
    description="Return the medical record for a patient, including allergies, conditions, and medications.",
)
async def get_patient_records(
    patient_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Envelope[MedicalRecordSummaryResponse]:
    record = await service.get_patient_records_summary(db, patient_id, current_user)
    return Envelope.ok(record)
