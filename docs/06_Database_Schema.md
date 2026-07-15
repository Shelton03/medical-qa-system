# Mirage
# Database Schema Specification

Version: 1.0

---

# Purpose

This document defines the relational database schema for Mirage.

It is the single source of truth for:

- PostgreSQL schema
- SQLAlchemy models
- Alembic migrations
- Repository implementations
- Seed data
- Foreign key relationships

The database should follow normalization principles while remaining practical for healthcare workloads.

---

# Database Technology

Database

PostgreSQL 16+

ORM

SQLAlchemy 2.x

Migration Tool

Alembic

Driver

psycopg

---

# General Rules

Primary keys

UUID v4

Public identifiers

UUID only

Timestamps

UTC

Soft deletion

Supported where appropriate

Audit logging

Immutable

Foreign keys

Explicitly declared

Indexes

Added to commonly queried fields

---

# Common Columns

Nearly every table should include:

```
id UUID PRIMARY KEY

created_at TIMESTAMP WITH TIME ZONE

updated_at TIMESTAMP WITH TIME ZONE

created_by UUID NULL

updated_by UUID NULL
```

Optional

```
deleted_at TIMESTAMP NULL
```

Soft deletion should be avoided for clinical events that require permanent history.

---

# Enumerations

## UserRole

```
PATIENT

DOCTOR

ADMIN
```

---

## ConsentStatus

```
PENDING

APPROVED

DENIED

EXPIRED

CANCELLED
```

---

## VisitStatus

```
SCHEDULED

IN_PROGRESS

COMPLETED

CANCELLED
```

---

## NotificationType

```
CONSENT

VISIT

REMINDER

SYSTEM

AI

MEDICAL_RECORD
```

---

## AISessionStatus

```
CREATED

ACTIVE

PROCESSING

COMPLETED

FAILED
```

---

# Entity Relationship Overview

```
User
│
├── Patient
│     │
│     ├── MedicalRecord
│     │       │
│     │       ├── Visit
│     │       │       │
│     │       │       ├── Diagnosis
│     │       │       ├── Medication
│     │       │       └── LabResult
│     │       │
│     │       ├── Allergy
│     │       ├── ChronicCondition
│     │       └── Document
│     │
│     ├── Notification
│     ├── ConsentRequest
│     └── AISession
│
└── Doctor
      │
      ├── Consultation
      ├── ClinicalNote
      └── Facility
```

---

# users

Purpose

Authentication and identity.

Columns

```
id

email

password_hash

role

first_name

last_name

avatar_url

phone_number

is_active

last_login_at

created_at

updated_at
```

Indexes

```
email UNIQUE

role

is_active
```

---

# patients

Purpose

Patient demographic profile.

Relationship

One-to-one with User.

Columns

```
id

user_id

medical_record_number

national_identifier

date_of_birth

gender

blood_type

address

emergency_contact_name

emergency_contact_phone

preferred_language
```

Indexes

```
medical_record_number UNIQUE

national_identifier

date_of_birth
```

---

# doctors

Purpose

Doctor profile.

Columns

```
id

user_id

registration_number

specialty

facility_id

department

license_expiry

years_experience
```

Indexes

```
registration_number UNIQUE

facility_id

specialty
```

---

# facilities

Columns

```
id

name

address

phone

email

city

country

timezone
```

Indexes

```
name

city
```

---

# medical_records

Purpose

Root clinical record.

One record per patient.

Columns

```
id

patient_id

primary_physician_id

record_status

created_at

updated_at
```

Indexes

```
patient_id UNIQUE
```

---

# visits

Purpose

Every clinical encounter.

Columns

```
id

medical_record_id

doctor_id

facility_id

visit_date

status

reason

chief_complaint

summary

ai_summary

follow_up_required
```

- transcript

  The full text transcript of the consultation, generated via real-time speech-to-text. Stored as plain text. Nullable.

Indexes

```
visit_date

doctor_id

facility_id

status
```

Visits are immutable after finalization except through versioned amendments.

---

# diagnoses

Columns

```
id

visit_id

diagnosis_name

icd10_code

confidence

primary_diagnosis

notes
```

Indexes

```
visit_id

icd10_code
```

Multiple diagnoses per visit supported.

---

# medications

Columns

```
id

visit_id

name

dosage

frequency

duration

instructions

start_date

end_date
```

Indexes

```
visit_id

name
```

---

# allergies

Columns

```
id

medical_record_id

allergen

reaction

severity

notes
```

Indexes

```
medical_record_id

severity
```

---

# chronic_conditions

Purpose

Long-term medical history.

Columns

```
id

medical_record_id

condition_name

diagnosed_date

status

notes
```

---

# laboratory_results

Columns

```
id

visit_id

test_name

result

reference_range

status

performed_at
```

Indexes

```
performed_at

visit_id
```

---

# imaging_results

Columns

```
id

visit_id

modality

study_name

report

performed_at
```

Examples

X-Ray

CT

MRI

Ultrasound

---

# clinical_documents

Purpose

Uploaded PDFs, referrals, discharge summaries, reports, and attachments.

Columns

```
id

medical_record_id

storage_key

filename

mime_type

uploaded_by

uploaded_at
```

The storage provider determines where the file is physically stored (local, S3, Azure Blob, etc.), keeping the database independent of storage implementation.

---

# Relationship Rules

User → Patient

One-to-one

User → Doctor

One-to-one

Patient → MedicalRecord

One-to-one

MedicalRecord → Visits

One-to-many

Visit → Diagnoses

One-to-many

Visit → Medications

One-to-many

MedicalRecord → Allergies

One-to-many

MedicalRecord → ChronicConditions

One-to-many

Visit → LaboratoryResults

One-to-many

Visit → ImagingResults

One-to-many

MedicalRecord → ClinicalDocuments

One-to-many

Foreign key constraints should enforce referential integrity. Cascading deletes should generally be avoided for clinical data; instead, records should be retained or archived in accordance with audit and retention requirements.

# consent_requests

Purpose

Represents a doctor's request to access a patient's medical information.

Consent is explicit, time-bound, and fully auditable.

Columns

```
id

patient_id

doctor_id

facility_id

purpose

scope

status

requested_at

approved_at

expires_at

denied_reason

cancelled_at
```

Scope should be stored as a JSON array for flexibility.

Example

```json
[
  "medical_record",
  "timeline",
  "lab_results"
]
```

Indexes

```
patient_id

doctor_id

status

expires_at
```

Rules

- Only one ACTIVE/PENDING consent request per doctor-patient pair.
- Expired consent must not grant access.
- Historical consent records are immutable.

---

# ai_sessions

Purpose

Tracks AI-assisted consultations.

Columns

```
id

patient_id

doctor_id

consultation_id

provider_name

status

started_at

completed_at

provider_metadata

conversation_summary
```

Indexes

```
patient_id

doctor_id

status

started_at
```

provider_metadata should be stored as JSONB.

---

# ai_messages

Purpose

Stores conversation history for AI consultations.

Columns

```
id

session_id

role

content

token_count

created_at
```

Role values

```
SYSTEM

USER

ASSISTANT
```

Indexes

```
session_id

created_at
```

Messages should never be edited after creation.

---

# clinical_notes

Purpose

Doctor-authored consultation notes.

Columns

```
id

visit_id

doctor_id

subjective

objective

assessment

plan

is_finalized

created_at

updated_at
```

Rules

Notes remain editable until finalized.

Finalized notes create a new version instead of overwriting.

---

# notifications

Purpose

Stores all in-app notifications.

Columns

```
id

recipient_user_id

type

title

body

payload

priority

is_read

read_at

created_at
```

Payload stored as JSONB.

Example

```json
{
  "consentId": "uuid",
  "patientId": "uuid"
}
```

Indexes

```
recipient_user_id

is_read

type

created_at
```

---

# refresh_tokens

Purpose

Supports secure JWT refresh token rotation.

Columns

```
id

user_id

token_hash

expires_at

revoked_at

created_at

last_used_at
```

Rules

Store only hashed refresh tokens.

Never store raw refresh tokens.

---

# audit_logs

Purpose

Immutable record of every sensitive action.

Columns

```
id

user_id

action

resource_type

resource_id

ip_address

user_agent

metadata

created_at
```

Metadata stored as JSONB.

Examples of actions

```
LOGIN

LOGOUT

CONSENT_REQUESTED

CONSENT_APPROVED

CONSENT_DENIED

PATIENT_RECORD_VIEWED

PATIENT_RECORD_UPDATED

AI_SESSION_STARTED

AI_SUMMARY_GENERATED

PROFILE_UPDATED
```

Indexes

```
user_id

resource_type

resource_id

created_at

action
```

Audit logs must never be updated or deleted.

---

# websocket_connections (Optional)

Purpose

Track active WebSocket connections.

Useful for scaling to multiple backend instances.

Columns

```
id

user_id

connection_id

connected_at

last_seen_at

server_instance
```

This table may be omitted in MVP if connection state is maintained in memory.

---

# background_jobs (Optional)

Purpose

Track long-running asynchronous work.

Columns

```
id

job_type

status

payload

result

created_at

started_at

completed_at

error_message
```

Status

```
QUEUED

RUNNING

COMPLETED

FAILED
```

This is optional if Redis-based queues already provide sufficient tracking.

---

# medical_record_versions

Purpose

Maintain version history for patient records.

Columns

```
id

medical_record_id

version_number

changed_by

change_summary

snapshot

created_at
```

Snapshot stored as JSONB.

Supports:

- Rollback
- Audit
- Historical comparison

Medical records should never lose historical state.

---

# Database Constraints

Required unique constraints

Users

```
email
```

Patients

```
medical_record_number
```

Doctors

```
registration_number
```

Medical Records

```
patient_id
```

Refresh Tokens

```
token_hash
```

---

# Foreign Key Rules

Every foreign key should specify explicit actions.

Preferred defaults

```
ON UPDATE CASCADE

ON DELETE RESTRICT
```

Clinical information should not be deleted automatically.

---

# JSONB Usage

Use JSONB only for semi-structured data.

Examples

AI metadata

Notification payloads

Consent scope

Audit metadata

Medical record snapshots

Avoid storing structured relational data in JSONB.

---

# Indexing Strategy

Indexes should exist for:

Primary keys

Foreign keys

Search fields

Frequently filtered timestamps

Status columns

Medical Record Number

Registration Number

Notification recipient

Consent status

Visit date

Avoid unnecessary indexes that slow writes.

---

# Soft Deletion Strategy

Soft deletion (`deleted_at`) may be used for:

User accounts

Notifications

Draft consultations

Do NOT soft-delete:

Medical records

Visits

Diagnoses

Clinical notes

Audit logs

Consent history

Clinical history should remain permanently traceable.

---

# Alembic Migration Strategy

Migration rules

- One migration per logical change.
- Never edit an existing migration after it has been committed.
- Use descriptive migration names.
- Test upgrades and downgrades locally.
- Seed data should not be embedded inside schema migrations.

Example

```
001_create_users.py

002_create_patients.py

003_create_medical_records.py

004_create_visits.py

005_create_consent_requests.py
```

---

# Seed Data Relationships

Initial seed data should create a realistic ecosystem.

Minimum dataset

```
10 Users (Patients)

5 Users (Doctors)

3 Facilities

10 Medical Records

50 Visits

120 Diagnoses

150 Medications

40 Allergies

30 Chronic Conditions

75 Laboratory Results

25 Imaging Reports

100 Notifications

20 Consent Requests

15 AI Sessions

500 Audit Log Entries
```

Seeded data should maintain referential integrity and realistic timelines.

---

# Database Definition of Done

The database layer is complete when:

- Every entity required by the Product Requirements Document exists.
- Relationships are normalized and enforce referential integrity.
- UUIDs are used consistently as public identifiers.
- Audit logs are immutable.
- Medical history is preserved through versioning.
- Provider-specific data remains abstracted via JSONB where appropriate.
- Alembic migrations can create the schema from an empty database.
- Seed data produces a realistic demonstration environment without manual intervention.

# End of Database Schema Specification