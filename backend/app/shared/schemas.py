#!/usr/bin/env python3
"""Mirage Pydantic schemas for request validation and response serialization."""

from __future__ import annotations

from datetime import date, datetime
from decimal import Decimal
from typing import Generic, TypeVar
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

T = TypeVar("T")


# ---------------------------------------------------------------------------
# Base
# ---------------------------------------------------------------------------
class MirageBaseModel(BaseModel):
    """Base schema with ORM mode enabled for all descendants."""

    model_config = ConfigDict(from_attributes=True)


# ---------------------------------------------------------------------------
# Generic API envelope
# ---------------------------------------------------------------------------
class ErrorDetail(MirageBaseModel):
    code: str = Field(..., description="Machine-readable error code.")
    message: str = Field(..., description="Human-readable error message.")
    field: str | None = Field(None, description="Field associated with the error.")


class Meta(MirageBaseModel):
    request_id: UUID | None = Field(None, description="Correlation ID for tracing.")
    timestamp: datetime | None = Field(None, description="Response timestamp in UTC.")


class Envelope(MirageBaseModel, Generic[T]):
    """Standard API response envelope per the API Contract."""

    success: bool = Field(..., description="Whether the request succeeded.")
    data: T | None = Field(None, description="Payload for successful responses.")
    errors: list[ErrorDetail] = Field(default_factory=list, description="List of errors if any.")
    meta: Meta = Field(default_factory=Meta, description="Response metadata.")


# ---------------------------------------------------------------------------
# Pagination
# ---------------------------------------------------------------------------
class PaginationMeta(Meta):
    page: int = Field(1, ge=1)
    page_size: int = Field(20, ge=1, le=100)
    total: int = Field(0, ge=0)
    total_pages: int = Field(0, ge=0)


class PaginatedEnvelope(Envelope[T], Generic[T]):
    meta: PaginationMeta = Field(default_factory=PaginationMeta)


# ---------------------------------------------------------------------------
# User
# ---------------------------------------------------------------------------
class UserBase(MirageBaseModel):
    email: str = Field(..., max_length=255)
    role: str = Field(..., max_length=50)
    first_name: str | None = Field(None, max_length=255)
    last_name: str | None = Field(None, max_length=255)
    avatar_url: str | None = Field(None, max_length=500)
    phone_number: str | None = Field(None, max_length=50)
    is_active: bool = True


class UserCreate(UserBase):
    password: str | None = Field(None, max_length=255)


class UserUpdate(MirageBaseModel):
    first_name: str | None = Field(None, max_length=255)
    last_name: str | None = Field(None, max_length=255)
    phone_number: str | None = Field(None, max_length=50)
    avatar_url: str | None = Field(None, max_length=500)
    is_active: bool | None = None


class UserResponse(UserBase):
    id: UUID
    last_login_at: datetime | None = None
    created_at: datetime
    updated_at: datetime


class UserListResponse(MirageBaseModel):
    items: list[UserResponse]


# ---------------------------------------------------------------------------
# Patient
# ---------------------------------------------------------------------------
class PatientBase(MirageBaseModel):
    medical_record_number: str = Field(..., max_length=100)
    national_identifier: str | None = Field(None, max_length=100)
    date_of_birth: date | None = None
    gender: str | None = Field(None, max_length=50)
    blood_type: str | None = Field(None, max_length=10)
    address: str | None = None
    emergency_contact_name: str | None = Field(None, max_length=255)
    emergency_contact_phone: str | None = Field(None, max_length=50)
    preferred_language: str | None = Field(None, max_length=50)


class PatientCreate(PatientBase):
    user_id: UUID


class PatientUpdate(MirageBaseModel):
    address: str | None = None
    emergency_contact_name: str | None = Field(None, max_length=255)
    emergency_contact_phone: str | None = Field(None, max_length=50)
    preferred_language: str | None = Field(None, max_length=50)


class PatientResponse(PatientBase):
    id: UUID
    user_id: UUID
    created_at: datetime
    updated_at: datetime


class PatientListResponse(MirageBaseModel):
    items: list[PatientResponse]


# ---------------------------------------------------------------------------
# Doctor
# ---------------------------------------------------------------------------
class DoctorBase(MirageBaseModel):
    registration_number: str = Field(..., max_length=100)
    specialty: str | None = Field(None, max_length=255)
    facility_id: UUID | None = None
    department: str | None = Field(None, max_length=255)
    license_expiry: date | None = None
    years_experience: int | None = None


class DoctorCreate(DoctorBase):
    user_id: UUID


class DoctorUpdate(MirageBaseModel):
    specialty: str | None = Field(None, max_length=255)
    facility_id: UUID | None = None
    department: str | None = Field(None, max_length=255)
    license_expiry: date | None = None
    years_experience: int | None = None


class DoctorResponse(DoctorBase):
    id: UUID
    user_id: UUID
    created_at: datetime
    updated_at: datetime


class DoctorListResponse(MirageBaseModel):
    items: list[DoctorResponse]


# ---------------------------------------------------------------------------
# Facility
# ---------------------------------------------------------------------------
class FacilityBase(MirageBaseModel):
    name: str = Field(..., max_length=255)
    address: str | None = None
    phone: str | None = Field(None, max_length=50)
    email: str | None = Field(None, max_length=255)
    city: str | None = Field(None, max_length=255)
    country: str | None = Field(None, max_length=100)
    timezone: str | None = Field(None, max_length=100)


class FacilityCreate(FacilityBase):
    pass


class FacilityUpdate(MirageBaseModel):
    name: str | None = Field(None, max_length=255)
    address: str | None = None
    phone: str | None = Field(None, max_length=50)
    email: str | None = Field(None, max_length=255)
    city: str | None = Field(None, max_length=255)
    country: str | None = Field(None, max_length=100)
    timezone: str | None = Field(None, max_length=100)


class FacilityResponse(FacilityBase):
    id: UUID
    created_at: datetime
    updated_at: datetime


class FacilityListResponse(MirageBaseModel):
    items: list[FacilityResponse]


# ---------------------------------------------------------------------------
# Medical Record
# ---------------------------------------------------------------------------
class MedicalRecordBase(MirageBaseModel):
    patient_id: UUID
    primary_physician_id: UUID | None = None
    record_status: str | None = Field(None, max_length=50)


class MedicalRecordCreate(MedicalRecordBase):
    pass


class MedicalRecordUpdate(MirageBaseModel):
    primary_physician_id: UUID | None = None
    record_status: str | None = Field(None, max_length=50)


class MedicalRecordResponse(MedicalRecordBase):
    id: UUID
    created_at: datetime
    updated_at: datetime


class MedicalRecordListResponse(MirageBaseModel):
    items: list[MedicalRecordResponse]


# ---------------------------------------------------------------------------
# Visit
# ---------------------------------------------------------------------------
class VisitBase(MirageBaseModel):
    medical_record_id: UUID
    doctor_id: UUID
    facility_id: UUID | None = None
    visit_date: datetime
    status: str = Field(..., max_length=50)
    reason: str | None = None
    chief_complaint: str | None = None
    summary: str | None = None
    ai_summary: str | None = None
    follow_up_required: bool = False


class VisitCreate(VisitBase):
    pass


class VisitUpdate(MirageBaseModel):
    visit_date: datetime | None = None
    status: str | None = Field(None, max_length=50)
    reason: str | None = None
    chief_complaint: str | None = None
    summary: str | None = None
    ai_summary: str | None = None
    follow_up_required: bool | None = None


class VisitResponse(VisitBase):
    id: UUID
    created_at: datetime
    updated_at: datetime


class VisitListResponse(MirageBaseModel):
    items: list[VisitResponse]


# ---------------------------------------------------------------------------
# Diagnosis
# ---------------------------------------------------------------------------
class DiagnosisBase(MirageBaseModel):
    visit_id: UUID
    diagnosis_name: str = Field(..., max_length=500)
    icd10_code: str | None = Field(None, max_length=20)
    confidence: Decimal | None = None
    primary_diagnosis: bool = False
    notes: str | None = None


class DiagnosisCreate(DiagnosisBase):
    pass


class DiagnosisUpdate(MirageBaseModel):
    diagnosis_name: str | None = Field(None, max_length=500)
    icd10_code: str | None = Field(None, max_length=20)
    confidence: Decimal | None = None
    primary_diagnosis: bool | None = None
    notes: str | None = None


class DiagnosisResponse(DiagnosisBase):
    id: UUID
    created_at: datetime


class DiagnosisListResponse(MirageBaseModel):
    items: list[DiagnosisResponse]


# ---------------------------------------------------------------------------
# Medication
# ---------------------------------------------------------------------------
class MedicationBase(MirageBaseModel):
    medical_record_id: UUID
    name: str = Field(..., max_length=255)
    dosage: str | None = Field(None, max_length=255)
    frequency: str | None = Field(None, max_length=255)
    duration: str | None = Field(None, max_length=255)
    instructions: str | None = None
    start_date: date | None = None
    end_date: date | None = None


class MedicationCreate(MedicationBase):
    pass


class MedicationUpdate(MirageBaseModel):
    name: str | None = Field(None, max_length=255)
    dosage: str | None = Field(None, max_length=255)
    frequency: str | None = Field(None, max_length=255)
    duration: str | None = Field(None, max_length=255)
    instructions: str | None = None
    start_date: date | None = None
    end_date: date | None = None


class MedicationResponse(MedicationBase):
    id: UUID
    created_at: datetime


class MedicationListResponse(MirageBaseModel):
    items: list[MedicationResponse]


# ---------------------------------------------------------------------------
# Allergy
# ---------------------------------------------------------------------------
class AllergyBase(MirageBaseModel):
    medical_record_id: UUID
    allergen: str = Field(..., max_length=255)
    reaction: str | None = None
    severity: str | None = Field(None, max_length=50)
    notes: str | None = None


class AllergyCreate(AllergyBase):
    pass


class AllergyUpdate(MirageBaseModel):
    allergen: str | None = Field(None, max_length=255)
    reaction: str | None = None
    severity: str | None = Field(None, max_length=50)
    notes: str | None = None


class AllergyResponse(AllergyBase):
    id: UUID
    created_at: datetime


class AllergyListResponse(MirageBaseModel):
    items: list[AllergyResponse]


# ---------------------------------------------------------------------------
# Chronic Condition
# ---------------------------------------------------------------------------
class ChronicConditionBase(MirageBaseModel):
    medical_record_id: UUID
    condition_name: str = Field(..., max_length=255)
    diagnosed_date: date | None = None
    status: str | None = Field(None, max_length=50)
    notes: str | None = None


class ChronicConditionCreate(ChronicConditionBase):
    pass


class ChronicConditionUpdate(MirageBaseModel):
    condition_name: str | None = Field(None, max_length=255)
    diagnosed_date: date | None = None
    status: str | None = Field(None, max_length=50)
    notes: str | None = None


class ChronicConditionResponse(ChronicConditionBase):
    id: UUID
    created_at: datetime


class ChronicConditionListResponse(MirageBaseModel):
    items: list[ChronicConditionResponse]


# ---------------------------------------------------------------------------
# Laboratory Result
# ---------------------------------------------------------------------------
class LaboratoryResultBase(MirageBaseModel):
    visit_id: UUID
    test_name: str = Field(..., max_length=255)
    result: str | None = None
    reference_range: str | None = Field(None, max_length=255)
    status: str | None = Field(None, max_length=50)
    performed_at: datetime | None = None


class LaboratoryResultCreate(LaboratoryResultBase):
    pass


class LaboratoryResultUpdate(MirageBaseModel):
    result: str | None = None
    reference_range: str | None = Field(None, max_length=255)
    status: str | None = Field(None, max_length=50)
    performed_at: datetime | None = None


class LaboratoryResultResponse(LaboratoryResultBase):
    id: UUID
    created_at: datetime


class LaboratoryResultListResponse(MirageBaseModel):
    items: list[LaboratoryResultResponse]


# ---------------------------------------------------------------------------
# Imaging Result
# ---------------------------------------------------------------------------
class ImagingResultBase(MirageBaseModel):
    visit_id: UUID
    modality: str = Field(..., max_length=100)
    study_name: str | None = Field(None, max_length=255)
    report: str | None = None
    performed_at: datetime | None = None


class ImagingResultCreate(ImagingResultBase):
    pass


class ImagingResultUpdate(MirageBaseModel):
    modality: str | None = Field(None, max_length=100)
    study_name: str | None = Field(None, max_length=255)
    report: str | None = None
    performed_at: datetime | None = None


class ImagingResultResponse(ImagingResultBase):
    id: UUID
    created_at: datetime


class ImagingResultListResponse(MirageBaseModel):
    items: list[ImagingResultResponse]


# ---------------------------------------------------------------------------
# Clinical Document
# ---------------------------------------------------------------------------
class ClinicalDocumentBase(MirageBaseModel):
    medical_record_id: UUID
    storage_key: str = Field(..., max_length=500)
    filename: str = Field(..., max_length=500)
    mime_type: str = Field(..., max_length=100)
    uploaded_by: UUID | None = None


class ClinicalDocumentCreate(ClinicalDocumentBase):
    pass


class ClinicalDocumentResponse(ClinicalDocumentBase):
    id: UUID
    uploaded_at: datetime


class ClinicalDocumentListResponse(MirageBaseModel):
    items: list[ClinicalDocumentResponse]


# ---------------------------------------------------------------------------
# Consent Request
# ---------------------------------------------------------------------------
class ConsentRequestBase(MirageBaseModel):
    patient_id: UUID
    doctor_id: UUID
    facility_id: UUID | None = None
    purpose: str | None = None
    scope: list[str] | None = None
    status: str = Field(..., max_length=50)
    requested_at: datetime
    approved_at: datetime | None = None
    expires_at: datetime | None = None
    denied_reason: str | None = None
    cancelled_at: datetime | None = None


class ConsentRequestCreate(ConsentRequestBase):
    pass


class ConsentRequestUpdate(MirageBaseModel):
    status: str | None = Field(None, max_length=50)
    approved_at: datetime | None = None
    expires_at: datetime | None = None
    denied_reason: str | None = None
    cancelled_at: datetime | None = None


class ConsentRequestResponse(ConsentRequestBase):
    id: UUID


class ConsentRequestListResponse(MirageBaseModel):
    items: list[ConsentRequestResponse]


# ---------------------------------------------------------------------------
# AI Session
# ---------------------------------------------------------------------------
class AISessionBase(MirageBaseModel):
    patient_id: UUID
    doctor_id: UUID | None = None
    consultation_id: UUID | None = None
    provider_name: str | None = Field(None, max_length=100)
    status: str = Field(..., max_length=50)
    started_at: datetime
    completed_at: datetime | None = None
    provider_metadata: dict | None = None
    conversation_summary: str | None = None


class AISessionCreate(AISessionBase):
    pass


class AISessionUpdate(MirageBaseModel):
    status: str | None = Field(None, max_length=50)
    completed_at: datetime | None = None
    provider_metadata: dict | None = None
    conversation_summary: str | None = None


class AISessionResponse(AISessionBase):
    id: UUID


class AISessionListResponse(MirageBaseModel):
    items: list[AISessionResponse]


# ---------------------------------------------------------------------------
# AI Message
# ---------------------------------------------------------------------------
class AIMessageBase(MirageBaseModel):
    session_id: UUID
    role: str = Field(..., max_length=50)
    content: str
    token_count: int | None = None


class AIMessageCreate(AIMessageBase):
    pass


class AIMessageResponse(AIMessageBase):
    id: UUID
    created_at: datetime


class AIMessageListResponse(MirageBaseModel):
    items: list[AIMessageResponse]


# ---------------------------------------------------------------------------
# Clinical Note
# ---------------------------------------------------------------------------
class ClinicalNoteBase(MirageBaseModel):
    visit_id: UUID
    doctor_id: UUID
    subjective: str | None = None
    objective: str | None = None
    assessment: str | None = None
    plan: str | None = None
    is_finalized: bool = False


class ClinicalNoteCreate(ClinicalNoteBase):
    pass


class ClinicalNoteUpdate(MirageBaseModel):
    subjective: str | None = None
    objective: str | None = None
    assessment: str | None = None
    plan: str | None = None
    is_finalized: bool | None = None


class ClinicalNoteResponse(ClinicalNoteBase):
    id: UUID
    created_at: datetime
    updated_at: datetime


class ClinicalNoteListResponse(MirageBaseModel):
    items: list[ClinicalNoteResponse]


# ---------------------------------------------------------------------------
# Notification
# ---------------------------------------------------------------------------
class NotificationBase(MirageBaseModel):
    recipient_user_id: UUID
    type: str = Field(..., max_length=50)
    title: str = Field(..., max_length=255)
    body: str | None = None
    payload: dict | None = None
    priority: str | None = Field(None, max_length=50)
    is_read: bool = False
    read_at: datetime | None = None


class NotificationCreate(NotificationBase):
    pass


class NotificationUpdate(MirageBaseModel):
    is_read: bool | None = None
    read_at: datetime | None = None


class NotificationResponse(NotificationBase):
    id: UUID
    created_at: datetime


class NotificationListResponse(MirageBaseModel):
    items: list[NotificationResponse]


# ---------------------------------------------------------------------------
# Refresh Token
# ---------------------------------------------------------------------------
class RefreshTokenBase(MirageBaseModel):
    user_id: UUID
    token_hash: str = Field(..., max_length=255)
    expires_at: datetime
    revoked_at: datetime | None = None
    last_used_at: datetime | None = None


class RefreshTokenCreate(RefreshTokenBase):
    pass


class RefreshTokenResponse(RefreshTokenBase):
    id: UUID
    created_at: datetime


class RefreshTokenListResponse(MirageBaseModel):
    items: list[RefreshTokenResponse]


# ---------------------------------------------------------------------------
# Audit Log
# ---------------------------------------------------------------------------
class AuditLogBase(MirageBaseModel):
    user_id: UUID | None = None
    action: str = Field(..., max_length=100)
    resource_type: str | None = Field(None, max_length=100)
    resource_id: UUID | None = None
    ip_address: str | None = Field(None, max_length=45)
    user_agent: str | None = Field(None, max_length=500)
    audit_metadata: dict | None = None


class AuditLogCreate(AuditLogBase):
    pass


class AuditLogResponse(AuditLogBase):
    id: UUID
    created_at: datetime


class AuditLogListResponse(MirageBaseModel):
    items: list[AuditLogResponse]


# ---------------------------------------------------------------------------
# Medical Record Version
# ---------------------------------------------------------------------------
class MedicalRecordVersionBase(MirageBaseModel):
    medical_record_id: UUID
    version_number: int
    changed_by: UUID | None = None
    change_summary: str | None = None
    snapshot: dict | None = None


class MedicalRecordVersionCreate(MedicalRecordVersionBase):
    pass


class MedicalRecordVersionResponse(MedicalRecordVersionBase):
    id: UUID
    created_at: datetime


class MedicalRecordVersionListResponse(MirageBaseModel):
    items: list[MedicalRecordVersionResponse]
