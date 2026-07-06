# Mirage
# API Contract

Version: 1.0

---

# Purpose

This document defines every public API exposed by the Mirage backend.

The API contract is the single source of truth for communication between:

- Frontend
- Backend
- AI Providers
- Future Mobile Applications
- Third-party integrations

Implementation must conform to this specification.

---

# API Design Principles

The API should be:

- RESTful
- Predictable
- Versioned
- Typed
- Consistent
- Secure
- Documented

Every endpoint returns the same response envelope.

---

# Base URL

Development

```
http://localhost:8000/api/v1
```

Production

```
https://api.mirage.health/api/v1
```

---

# Versioning

All endpoints must be versioned.

```
/api/v1/
```

Breaking changes require a new version.

```
/api/v2/
```

Never silently change response structures.

---

# Authentication

Production authentication uses JWT.

Headers

```
Authorization: Bearer <access_token>
```

Access tokens should be short-lived.

Refresh tokens are stored securely and rotated on refresh.

---

# Demo Mode Authentication

When `DEMO_MODE=true`, the API exposes:

```
POST /auth/demo-login
```

Body

```json
{
  "role": "patient"
}
```

or

```json
{
  "role": "doctor"
}
```

Returns a valid JWT along with a demo user profile.

This endpoint must be disabled in production.

---

# Standard Response Envelope

Success

```json
{
  "success": true,
  "data": {},
  "errors": [],
  "meta": {
    "requestId": "uuid",
    "timestamp": "ISO-8601"
  }
}
```

Failure

```json
{
  "success": false,
  "data": null,
  "errors": [
    {
      "code": "VALIDATION_ERROR",
      "message": "Validation failed.",
      "field": "email"
    }
  ],
  "meta": {
    "requestId": "uuid",
    "timestamp": "ISO-8601"
  }
}
```

All endpoints must follow this structure.

---

# Pagination Standard

Collection endpoints should support:

```
?page=1
&pageSize=20
&sort=createdAt
&order=desc
```

Response

```json
{
  "success": true,
  "data": [...],
  "meta": {
    "page": 1,
    "pageSize": 20,
    "total": 247,
    "totalPages": 13
  }
}
```

---

# Filtering

Supported query parameters:

```
status

dateFrom

dateTo

doctorId

patientId

facilityId

search
```

Unknown filters should return HTTP 400.

---

# Sorting

Supported:

```
createdAt

updatedAt

date

lastName

firstName

status
```

---

# Standard Error Codes

Authentication

```
UNAUTHORIZED

TOKEN_EXPIRED

INVALID_TOKEN

FORBIDDEN
```

Validation

```
VALIDATION_ERROR

INVALID_REQUEST

MISSING_FIELD
```

Consent

```
CONSENT_REQUIRED

CONSENT_DENIED

CONSENT_EXPIRED
```

Medical Records

```
RECORD_NOT_FOUND

VISIT_NOT_FOUND

PATIENT_NOT_FOUND
```

AI

```
AI_PROVIDER_UNAVAILABLE

AI_TIMEOUT

AI_RESPONSE_INVALID
```

General

```
NOT_FOUND

INTERNAL_SERVER_ERROR

CONFLICT

RATE_LIMITED
```

Codes should remain stable across releases.

---

# Date Format

Always ISO-8601.

Example

```
2026-07-05T14:42:18Z
```

Never return locale-specific formats.

---

# UUID Format

Primary identifiers use UUID v4.

Example

```
8b9f13b4-f90b-41d9-b5e4-3a63cde2c87f
```

Integer IDs should not be exposed publicly.

---

# Common Objects

## User

```json
{
  "id": "uuid",
  "role": "doctor",
  "firstName": "Jane",
  "lastName": "Smith",
  "email": "jane@example.com",
  "avatarUrl": null
}
```

---

## Doctor

```json
{
  "id": "uuid",
  "registrationNumber": "MED12345",
  "specialty": "General Practice",
  "facilityId": "uuid"
}
```

---

## Patient

```json
{
  "id": "uuid",
  "medicalRecordNumber": "MRN-100234",
  "dateOfBirth": "1995-03-20",
  "gender": "Female"
}
```

---

## Facility

```json
{
  "id": "uuid",
  "name": "Harare Central Hospital",
  "address": "...",
  "phone": "..."
}
```

---

## Notification

```json
{
  "id": "uuid",
  "type": "CONSENT_REQUEST",
  "title": "Access Request",
  "body": "Dr. Smith has requested access.",
  "read": false,
  "createdAt": "..."
}
```

---

## Audit Entry

```json
{
  "id": "uuid",
  "userId": "uuid",
  "action": "CONSENT_APPROVED",
  "resource": "ConsentRequest",
  "resourceId": "uuid",
  "timestamp": "..."
}
```

---

# Idempotency

The following endpoints should accept an optional:

```
Idempotency-Key
```

Header.

Examples:

Create consultation

Submit AI request

Approve consent

Record update

Repeated requests with the same key should return the original response where appropriate.

---

# Rate Limiting

Authentication endpoints:

10 requests/minute

AI endpoints:

30 requests/minute

Search endpoints:

60 requests/minute

General API:

Configurable via environment variables.

Rate limit responses return HTTP 429.

---

# Correlation IDs

Every request receives a server-generated correlation ID.

Response header:

```
X-Request-ID
```

This value should also appear in structured logs to support tracing across services.

# Authentication API

---

## POST /auth/demo-login

Purpose

Authenticate instantly using predefined demonstration accounts.

Authentication

None

Request

```json
{
  "role": "patient"
}
```

Allowed values

```
patient

doctor

admin
```

Success

```json
{
  "success": true,
  "data": {
    "accessToken": "...",
    "refreshToken": "...",
    "expiresIn": 3600,
    "user": {
      "id": "uuid",
      "role": "patient",
      "firstName": "Alice",
      "lastName": "Ncube"
    }
  }
}
```

---

## POST /auth/login

Purpose

Authenticate using username/password.

Authentication

None

Request

```json
{
  "email": "doctor@example.com",
  "password": "password"
}
```

Response

Same structure as Demo Login.

Errors

```
INVALID_CREDENTIALS

ACCOUNT_DISABLED

ACCOUNT_LOCKED
```

---

## POST /auth/refresh

Request

```json
{
  "refreshToken": "..."
}
```

Returns

New access token.

Rotated refresh token.

---

## POST /auth/logout

Authentication

Required

Request

Empty

Response

204 No Content

Refresh token revoked.

---

## GET /auth/me

Returns

Current authenticated user.

---

# Patient API

---

## GET /patients/me

Returns

Patient profile.

Example

```json
{
  "success": true,
  "data": {
    "id": "uuid",
    "medicalRecordNumber": "MRN-0001",
    "firstName": "Alice",
    "lastName": "Ncube",
    "gender": "Female",
    "dateOfBirth": "1998-01-15",
    "bloodType": "O+",
    "allergies": [],
    "conditions": [],
    "medications": []
  }
}
```

---

## PUT /patients/me

Editable fields

Phone

Email

Emergency Contact

Address

Preferred Language

Notification Preferences

Immutable fields

MRN

Date of Birth

Legal Name

National Identifier

---

## GET /patients/me/timeline

Returns

Chronological medical history.

Response

```json
{
  "success": true,
  "data": [
    {
      "visitId": "uuid",
      "date": "...",
      "facility": "...",
      "doctor": "...",
      "summary": "...",
      "diagnosis": "...",
      "status": "completed"
    }
  ]
}
```

---

## GET /patients/me/visits

Paginated visit history.

Supports

Date filtering

Facility filtering

Search

---

## GET /patients/me/visit/{visitId}

Returns complete visit details.

Includes

Diagnoses

Medication

Clinical Notes

Attachments

Lab Results

AI Summary

Audit Metadata

---

## GET /patients/me/notifications

Returns notifications ordered by newest first.

Supports

Pagination

Unread filter

Category filter

---

## PUT /patients/me/notifications/{id}/read

Marks notification as read.

---

## GET /patients/me/access-history

Returns every healthcare professional that has viewed the patient's record.

Each record includes

Doctor

Facility

Purpose

Timestamp

Consent Reference

---

# Doctor API

---

## GET /doctor/dashboard

Returns

Today's appointments

Pending consent

Recent activity

Statistics

Notifications

AI tasks

---

## POST /doctor/search

Purpose

Search patients.

Request

```json
{
  "query": "Alice"
}
```

Response

```json
[
  {
    "patientId": "...",
    "medicalRecordNumber": "...",
    "fullName": "...",
    "dateOfBirth": "...",
    "gender": "..."
  }
]
```

---

Supports

Partial search

MRN

National ID

Phone

Email

Name

---

## GET /doctor/patient/{patientId}

Returns

Patient overview.

Requires

Approved consent.

Errors

```
CONSENT_REQUIRED

CONSENT_EXPIRED

PATIENT_NOT_FOUND
```

---

## GET /doctor/patient/{patientId}/timeline

Returns

Full timeline.

Requires

Valid consent.

---

## POST /doctor/patient/{patientId}/consultation

Creates consultation session.

Request

```json
{
  "reason": "Routine consultation"
}
```

Returns

```json
{
  "consultationId": "uuid",
  "status": "ACTIVE"
}
```

---

## POST /doctor/patient/{patientId}/notes

Creates clinician notes.

Notes remain editable until finalized.

---

## POST /doctor/patient/{patientId}/summary

Requests AI clinical summary.

Returns

Job ID.

---

# Consent API

---

## POST /consent/request

Purpose

Doctor requests patient access.

Request

```json
{
  "patientId": "...",
  "purpose": "Emergency consultation",
  "scope": [
    "medical_record",
    "timeline",
    "lab_results"
  ],
  "expiresInMinutes": 60
}
```

Returns

Consent request object.

Triggers

Notification

WebSocket event

Audit log

---

## GET /consent/{consentId}

Returns

Consent details.

Status

Pending

Approved

Denied

Expired

Cancelled

---

## POST /consent/{consentId}/approve

Authentication

Patient

Returns

Updated consent.

Triggers

Doctor notification

Dashboard refresh

Audit event

---

## POST /consent/{consentId}/deny

Authentication

Patient

Request

Optional reason.

Returns

Updated consent.

---

## POST /consent/{consentId}/cancel

Authentication

Doctor

Purpose

Withdraw request before approval.

---

## GET /consent/history

Returns

Historical consent requests.

Supports

Status filter

Date filter

Patient filter

Doctor filter

Pagination

---

# Permissions Matrix

| Endpoint | Patient | Doctor | Admin |
|-----------|:------:|:------:|:-----:|
| Demo Login | ✓ | ✓ | ✓ |
| Login | ✓ | ✓ | ✓ |
| Patient Profile | ✓ | ✗ | ✓ |
| Doctor Dashboard | ✗ | ✓ | ✓ |
| Patient Timeline | ✓ | ✓ (with consent) | ✓ |
| Request Consent | ✗ | ✓ | ✓ |
| Approve Consent | ✓ | ✗ | ✓ |
| Deny Consent | ✓ | ✗ | ✓ |
| Notifications | ✓ | ✓ | ✓ |
| AI Consultation | ✗ | ✓ | ✓ |

Permission enforcement must occur server-side regardless of any frontend restrictions.

---

# Authorization Rules

The backend is the ultimate authority for access control.

The frontend may hide unavailable actions for usability, but it must never be relied upon for security.

Every protected endpoint must verify:

- Authentication
- User role
- Consent status (where applicable)
- Resource ownership or authorization
- Token validity

Requests failing any of these checks should return the appropriate HTTP status code and standardized error response.

# Medical Record API

---

## GET /records/{recordId}

Purpose

Retrieve a patient's complete medical record.

Authentication

Doctor (with valid consent)

Patient (own record)

Admin

Response

```json
{
  "success": true,
  "data": {
    "patient": {},
    "conditions": [],
    "allergies": [],
    "medications": [],
    "vaccinations": [],
    "labResults": [],
    "imaging": [],
    "documents": []
  }
}
```

---

## PATCH /records/{recordId}

Purpose

Update patient record.

Authentication

Doctor

Restrictions

Changes remain in a draft state until the consultation is finalized.

Every update generates:

- Audit log
- Version history
- Updated timestamp

---

## GET /records/{recordId}/versions

Returns

Historical versions of the medical record.

Supports comparison between versions.

---

# Timeline API

---

## GET /timeline/{patientId}

Returns

Complete chronological timeline.

Each event includes:

```json
{
  "eventId": "uuid",
  "eventType": "VISIT",
  "date": "...",
  "facility": {},
  "doctor": {},
  "summary": "...",
  "attachments": [],
  "status": "COMPLETED"
}
```

Supported event types

- Visit
- Prescription
- Diagnosis
- Laboratory
- Imaging
- Surgery
- Vaccination
- Allergy Update
- Consent Event
- AI Consultation

---

## GET /timeline/event/{eventId}

Returns

Expanded timeline event.

---

# AI Session API

---

## POST /ai/session

Purpose

Create an AI consultation session.

Request

```json
{
  "patientId": "uuid",
  "consultationId": "uuid"
}
```

Response

```json
{
  "sessionId": "uuid",
  "provider": "mock",
  "status": "ACTIVE"
}
```

---

## POST /ai/session/{sessionId}/message

Purpose

Continue an AI conversation.

Request

```json
{
  "message": "The patient reports chest pain for three days."
}
```

Response

```json
{
  "messageId": "uuid",
  "role": "assistant",
  "content": "...",
  "suggestedQuestions": [],
  "citations": [],
  "complete": false
}
```

Streaming responses should be supported when the provider allows it.

---

## POST /ai/session/{sessionId}/diagnosis

Purpose

Generate differential diagnosis.

Returns

```json
{
  "diagnoses": [
    {
      "name": "Community-acquired pneumonia",
      "confidence": 0.83,
      "reasoning": "...",
      "recommendedInvestigations": [],
      "medicationWarnings": []
    }
  ]
}
```

AI responses remain advisory.

Nothing is persisted automatically.

---

## POST /ai/session/{sessionId}/summary

Purpose

Generate structured consultation notes.

Returns

```json
{
  "soap": {
    "subjective": "...",
    "objective": "...",
    "assessment": "...",
    "plan": "..."
  }
}
```

Doctors may edit every section before saving.

---

## POST /ai/session/{sessionId}/complete

Purpose

Close AI consultation.

Response

```json
{
  "status": "COMPLETED"
}
```

---

# Transcription API

---

## POST /transcription/start

Purpose

Begin live transcription.

Returns

Session identifier.

---

## POST /transcription/{sessionId}/audio

Purpose

Upload audio chunk.

Request

Binary stream or multipart upload.

---

## GET /transcription/{sessionId}

Returns

Current transcript.

```json
{
  "segments": [
    {
      "speaker": "Doctor",
      "text": "...",
      "timestamp": "..."
    }
  ]
}
```

---

## POST /transcription/{sessionId}/stop

Stops transcription.

Returns finalized transcript.

---

# Notification API

---

## GET /notifications

Supports

Pagination

Unread filter

Category filter

Priority filter

---

## GET /notifications/{notificationId}

Returns

Complete notification.

---

## PATCH /notifications/{notificationId}

Purpose

Update notification.

Examples

Mark read

Archive

Pin

---

## DELETE /notifications/{notificationId}

Soft delete only.

---

# Audit API

---

## GET /audit

Admin only.

Supports

User filter

Patient filter

Action filter

Date filter

---

## GET /audit/{auditId}

Returns complete audit event.

Includes

User

Timestamp

IP Address

User Agent

Affected Resource

Action

Metadata

Audit entries are immutable.

---

# WebSocket Contract

Endpoint

```
/ws
```

Authentication

Clients authenticate by sending an `auth` action message within 5 seconds of connection establishment. The JWT is not sent in the query string.

```json
{
  "action": "auth",
  "token": "<JWT>"
}
```

If authentication succeeds, the server responds with:

```json
{
  "type": "authenticated",
  "payload": {
    "user_id": "uuid"
  },
  "timestamp": "..."
}
```

If authentication fails or times out, the server responds with:

```json
{
  "type": "error",
  "payload": {
    "code": 4001,
    "message": "..."
  },
  "timestamp": "..."
}
```

then closes the connection with close code `4001`.

After authentication, the client subscribes to one or more channels.

Heartbeats

The client should send an `{"action": "ping"}` message every 30 seconds. The server acknowledges with `pong` and has a 45-second receive timeout.

Examples

```
patient:{patientId}

doctor:{doctorId}

notifications

consultations

dashboard
```

---

# WebSocket Event Envelope

Every event follows the same structure.

```json
{
  "type": "CONSENT_APPROVED",
  "timestamp": "...",
  "payload": {}
}
```

---

# Supported Events

## Consent Requested

```json
{
  "type": "CONSENT_REQUESTED",
  "payload": {
    "consentId": "uuid",
    "doctorId": "uuid",
    "patientId": "uuid"
  }
}
```

---

## Consent Approved

```json
{
  "type": "CONSENT_APPROVED",
  "payload": {
    "consentId": "uuid"
  }
}
```

---

## Consent Denied

---

## Consultation Started

---

## Consultation Completed

---

## Timeline Updated

---

## Medical Record Updated

---

## Notification Created

---

## AI Response Ready

---

## AI Streaming Token (optional)

```json
{
  "type": "AI_STREAM",
  "payload": {
    "sessionId": "uuid",
    "token": "partial text"
  }
}
```

The frontend should assemble streamed tokens into a complete message.

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

## ConsultationStatus

```
CREATED

ACTIVE

PAUSED

COMPLETED

CANCELLED
```

---

## NotificationType

```
CONSENT

MEDICAL_RECORD

CONSULTATION

REMINDER

SYSTEM

AI
```

---

## AI Session Status

```
CREATED

ACTIVE

PROCESSING

COMPLETED

FAILED
```

---

## Visit Status

```
SCHEDULED

IN_PROGRESS

COMPLETED

CANCELLED
```

---

# HTTP Status Code Usage

200 — Successful retrieval

201 — Resource created

202 — Accepted for asynchronous processing

204 — Successful operation with no content

400 — Invalid request

401 — Authentication required

403 — Authenticated but not authorized

404 — Resource not found

409 — Conflict

422 — Validation error

429 — Rate limit exceeded

500 — Internal server error

503 — External provider unavailable

Status codes should be used consistently across the API.

---

# API Definition of Done

The API contract is complete when:

- Every endpoint required by the Product Requirements Document is defined.
- Every request and response is explicitly specified.
- Standard response envelopes are used throughout.
- Authentication and authorization rules are documented.
- Error codes are stable and documented.
- WebSocket payloads are standardized.
- AI interactions remain provider-agnostic.
- The contract is sufficient for frontend and backend teams to work independently without additional clarification.

# End of API Contract