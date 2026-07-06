# Mirage
# User Flows and State Machines

Version: 1.0

---

# Purpose

This document defines every workflow implemented by Mirage.

Where `10_UI_Screen_Specification.md` describes what users see, this document describes how the application behaves.

Every workflow should be deterministic.

Given the same state and the same event, the application should always transition to the same next state.

No business logic should exist outside these workflows.

---

# Relationship to Other Documentation

This document complements:

01_Product_Requirements_Document.md

Defines product behaviour.

02_Technical_Architecture.md

Defines implementation.

05_API_Contract.md

Defines communication.

06_Database_Schema.md

Defines persistence.

10_UI_Screen_Specification.md

Defines presentation.

This document defines behaviour.

---

# Workflow Design Principles

Every workflow should satisfy:

• Predictable

• Recoverable

• Observable

• Auditable

• Idempotent

• Testable

Clinical workflows should never rely on implicit state.

Every state transition must be explicit.

---

# State Machine Standard

Each workflow follows the same specification.

Purpose

Actors

Entry Conditions

State Diagram

States

Transitions

API Calls

WebSocket Events

Audit Events

Failure Recovery

Acceptance Criteria

---

# Event Naming Convention

Events should use the format:

Entity.Action

Examples

Consent.Requested

Consent.Approved

Consultation.Started

Consultation.Completed

Timeline.Updated

Notification.Created

Diagnosis.Generated

Transcript.Updated

Authentication.LoggedIn

Authentication.LoggedOut

---

# Workflow Categories

Patient

Authentication

Home Dashboard

Medical Record

Symptom Assessment

Consent

Notifications

Doctor

Authentication

Dashboard

Patient Search

Patient Review

Consultation

Diagnosis

Clinical Notes

System

Notifications

WebSockets

Provider Integrations

Background Jobs

Synchronization

---

# Global State Rules

State belongs to one owner.

Examples

Authentication State

Owned by Auth Service.

Consultation State

Owned by Consultation Service.

Consent State

Owned by Consent Service.

Medical Record

Owned by Medical Record Service.

The frontend should never invent state.

---

# API Rule

Every state transition requiring persistence must pass through the backend.

Frontend

↓

FastAPI

↓

Database

↓

WebSocket

↓

Clients

Direct client-to-client communication is prohibited.

---

# WebSocket Rule

WebSockets should communicate state changes only.

Business logic must remain on the backend.

Clients should react to events rather than determine state independently.

---

# Provider Rule

AI providers never change workflow behaviour.

Regardless of implementation:

Mock

Existing Symptom Checker

Azure OpenAI

OpenAI

Anthropic

Future Provider

The workflow remains identical.

Only provider outputs differ.

---

# Recovery Rule

Every workflow must define recovery paths.

Recoverable failures should never require restarting the application.

Whenever possible:

Retry

Reconnect

Resume

Continue

Rather than restart.

---

# Audit Rule

Every clinically significant action should generate an immutable audit event.

Examples

Consent approved

Diagnosis confirmed

Record viewed

Record updated

Consultation completed

Prescription issued

Authentication success

Authentication failure

Audit logs should never be editable.

---

# State Diagram Notation

Notation used throughout this document

```

State

↓

Event

↓

Next State

```

Conditional transitions use:

```

State

↓

Condition?

↓

Yes → Next State

↓

No → Alternate State

```

All subsequent workflows follow this notation.

# End of Part 1

# Part 2 — Authentication State Machines

Authentication supports two distinct operating modes.

Development Mode

- Mock Login
- Instant role switching
- No credential validation
- No JWT enforcement
- Intended only for local development

Production Mode

- JWT Authentication
- Refresh Tokens
- Password validation
- Role-based authorization

The UI should behave identically in both modes.

Only the authentication backend changes.

---

# Workflow A1 — Development Login

## Purpose

Allow developers to rapidly enter either application without repeatedly authenticating.

This workflow exists exclusively to improve development speed.

It must be disabled in production.

---

## Actors

- Developer

---

## Entry Conditions

Application running with

```
DEMO_MODE=true
```

---

## State Diagram

```
Application Started

↓

Demo Login Screen

↓

Select Role

↓

Patient
        \
         \
          → Authenticated
         /
Doctor
```

---

## States

Idle

↓

Role Selection

↓

Authenticated

---

## API Calls

None required.

A mock identity is generated locally.

---

## Stored Session

```
user_id

role

demo_mode

expires_at
```

---

## Exit Conditions

Logout

↓

Return to Demo Login

---

## Audit Event

```
Authentication.DemoLogin
```

---

## Acceptance Criteria

✓ One click login

✓ Switch between Doctor and Patient instantly

✓ No backend dependency

✓ Disabled automatically in production

---

# Workflow A2 — JWT Authentication

## Purpose

Authenticate real users securely.

---

## Actors

Patient

Doctor

---

## Entry Conditions

Application started

Production mode

---

## State Diagram

```
Unauthenticated

↓

Submit Credentials

↓

Valid?

↓

Yes

↓

Generate JWT

↓

Authenticated

↓

Refresh Loop

↓

Logout

↓

Unauthenticated

------------------------

Invalid Credentials

↓

Authentication Failed

↓

Retry
```

---

## States

Unauthenticated

Authenticating

Authenticated

Refresh Pending

Expired

Logged Out

---

## API Calls

POST /auth/login

POST /auth/refresh

POST /auth/logout

GET /auth/me

---

## WebSocket Events

Authenticate socket after JWT validation.

Disconnect immediately after logout.

---

## Failure Recovery

Invalid credentials

↓

Display validation message

↓

Remain on login screen

---

Expired token

↓

Attempt refresh

↓

Refresh successful

↓

Continue session

---

Refresh failed

↓

Return to login

---

## Audit Events

Authentication.Login

Authentication.Logout

Authentication.Refresh

Authentication.Failed

---

## Acceptance Criteria

✓ JWT stored securely

✓ Refresh automatic

✓ Logout invalidates refresh token

✓ Socket reconnects automatically

---

# Workflow A3 — Session Restoration

## Purpose

Restore authenticated users after browser refresh.

---

## State Diagram

```
Application Starts

↓

Existing Token?

↓

No

↓

Login Screen

----------------------

Yes

↓

Validate Token

↓

Valid?

↓

Yes

↓

Restore Session

↓

Dashboard

----------------------

No

↓

Attempt Refresh

↓

Success?

↓

Yes

↓

Dashboard

↓

No

↓

Login
```

---

## API Calls

GET /auth/me

POST /auth/refresh

---

## Acceptance Criteria

✓ Refresh survives browser reload

✓ Expired sessions handled gracefully

✓ No unnecessary login prompts

---

# Workflow A4 — Role Switching (Development)

## Purpose

Rapidly switch between Patient and Doctor applications during demonstrations.

---

## Entry Conditions

Demo Mode enabled.

---

## State Diagram

```
Patient

↓

Switch Role

↓

Doctor

↓

Switch Role

↓

Patient
```

---

## Requirements

Switching roles should

- Preserve application state where appropriate
- Disconnect old WebSocket
- Establish new authenticated socket
- Reload role-specific navigation
- Reload permissions

---

## Audit Event

```
Authentication.RoleSwitched
```

---

## Acceptance Criteria

✓ Role switch <1 second

✓ No page reload required

✓ New permissions applied immediately

---

# Workflow A5 — Logout

## Purpose

Terminate authenticated session safely.

---

## State Diagram

```
Authenticated

↓

Logout Requested

↓

Invalidate Refresh Token

↓

Disconnect Socket

↓

Clear Local Storage

↓

Login Screen
```

---

## API Calls

POST /auth/logout

---

## Cleanup

Remove

- JWT

- Refresh Token

- Cached User

- Active Consultation Cache

- Temporary AI Sessions

---

## Acceptance Criteria

✓ Session destroyed

✓ Socket disconnected

✓ Tokens removed

✓ Cannot navigate using browser history into protected pages

---

# Global Authentication Rules

Authentication state is owned exclusively by the Authentication Service.

React components should consume authentication through:

```
Auth Context

↓

Auth Hook

↓

API Client

↓

FastAPI
```

Components should never inspect JWT contents directly.

Authorization decisions always belong to the backend.

---

# Authentication Failure Matrix

| Failure | Recovery |
|----------|----------|
| Wrong Password | Retry |
| Expired JWT | Refresh |
| Expired Refresh | Login |
| Network Failure | Retry |
| Backend Offline | Offline Screen |
| Demo Login | Always succeeds |

# End of Part 2

# Part 3 — Consent Lifecycle State Machine

The Consent Workflow is the foundation of Mirage.

No protected medical information may be accessed until an active consent grant exists.

Consent must always be:

- Explicit
- Time-limited
- Auditable
- Revocable
- Observable in real time

The backend is the source of truth.

---

# Workflow C1 — Doctor Requests Consent

## Purpose

Allow a clinician to request temporary access to a patient's protected medical information before consultation.

---

## Actors

Doctor

Patient

Consent Service

Notification Service

WebSocket Gateway

---

## Entry Conditions

Doctor is authenticated.

Patient exists.

No active consent currently grants the requested permissions.

---

## State Diagram

```
Patient Selected

↓

Create Consent Request

↓

Consent Created

↓

Patient Notified

↓

Waiting For Response
```

---

## States

Idle

↓

Creating Request

↓

Pending

↓

Delivered

↓

Awaiting Response

---

## API Calls

POST /consent/request

GET /consent/{id}

---

## Backend Actions

Generate Consent Record

↓

Store Expiry Timestamp

↓

Create Notification

↓

Publish WebSocket Event

↓

Return Pending Status

---

## WebSocket Events

Publish

Consent.Requested

Notification.Created

Patient receives the request immediately.

---

## Audit Events

Consent.Requested

Notification.Created

---

## Acceptance Criteria

✓ Consent stored.

✓ Patient notified.

✓ Dashboard immediately shows Pending.

✓ Request visible in audit history.

---

# Workflow C2 — Patient Reviews Consent

## Purpose

Present the patient with sufficient information to make an informed decision.

---

## State Diagram

```
Notification Opened

↓

Load Consent

↓

Consent Displayed

↓

Review Information
```

---

## Information Presented

Doctor Name

Facility

Reason

Requested Information

Expiry

Privacy Notice

---

## API Calls

GET /consent/{id}

---

## Acceptance Criteria

✓ Patient understands exactly what will be shared.

✓ Consent cannot be approved without loading complete details.

---

# Workflow C3 — Patient Approves Consent

## Purpose

Grant temporary access to requested medical records.

---

## State Diagram

```
Pending

↓

Approve

↓

Consent Active

↓

Doctor Notified

↓

Medical Records Unlocked
```

---

## States

Pending

Approved

Active

Expired

---

## API Calls

POST /consent/{id}/approve

---

## Backend Actions

Update Consent

↓

Create Audit Event

↓

Publish WebSocket

↓

Enable Record Access

---

## WebSocket Events

Consent.Approved

MedicalRecord.AccessGranted

Notification.Created

---

## Acceptance Criteria

✓ Doctor immediately gains access.

✓ Patient receives confirmation.

✓ Audit recorded.

✓ Timeline updated.

---

# Workflow C4 — Patient Denies Consent

## Purpose

Reject access request.

---

## State Diagram

```
Pending

↓

Decline

↓

Denied

↓

Doctor Notified

↓

Request Closed
```

---

## API Calls

POST /consent/{id}/deny

---

## Backend Actions

Update Status

↓

Publish Notification

↓

Audit Log

---

## WebSocket Events

Consent.Denied

Notification.Created

---

## Acceptance Criteria

✓ Doctor loses ability to access records.

✓ Patient confirmation displayed.

✓ Request closed.

---

# Workflow C5 — Consent Expiration

## Purpose

Automatically revoke access after the approved duration.

No manual action should be required.

---

## State Diagram

```
Active

↓

Expiry Time Reached

↓

Expired

↓

Access Revoked

↓

Notification Sent
```

---

## Trigger

Background Scheduler

---

## Backend Actions

Update Consent

↓

Revoke Access

↓

Publish Events

↓

Audit

---

## WebSocket Events

Consent.Expired

MedicalRecord.AccessRevoked

---

## Acceptance Criteria

✓ Automatic.

✓ Immediate.

✓ Logged.

---

# Workflow C6 — Consent Revocation

## Purpose

Allow patients to revoke previously granted consent before expiry.

---

## State Diagram

```
Active

↓

Patient Revokes

↓

Revoked

↓

Access Removed

↓

Doctor Updated
```

---

## API Calls

POST /consent/{id}/revoke

---

## WebSocket Events

Consent.Revoked

MedicalRecord.AccessRevoked

---

## Audit Events

Consent.Revoked

---

## Acceptance Criteria

✓ Access removed immediately.

✓ Doctor informed.

✓ Timeline updated.

---

# Permission Matrix

| Consent Status | Doctor Access |
|----------------|--------------|
| Pending | None |
| Approved | Granted |
| Active | Granted |
| Expired | None |
| Denied | None |
| Revoked | None |

---

# Failure Recovery

## Patient Offline

Notification queued.

Delivered when reconnecting.

---

## Doctor Offline

Dashboard updated after reconnect.

---

## Duplicate Approval

Ignored.

Return existing Active consent.

---

## Expired Before Approval

Return

```
409 Conflict
```

Display

"This consent request has expired."

---

## Network Failure

Remain on current screen.

Retry available.

No duplicate requests should be created.

---

# Security Rules

Consent tokens must be:

- Unpredictable
- Time limited
- Single authoritative record
- Audit logged

Medical data access must always validate consent at request time.

Never trust cached permissions.

---

# Audit Trail

Every transition records

Timestamp

Actor

Consent ID

Patient ID

Doctor ID

Old State

New State

IP Address (future)

Device Information (future)

Audit entries are immutable.

---

# Acceptance Criteria

✓ Entire workflow matches PRD.

✓ Doctor and Patient remain synchronized.

✓ Expiry automatic.

✓ Revocation immediate.

✓ Every transition audited.

✓ WebSocket events emitted correctly.

✓ Permission checks enforced on every protected endpoint.

# End of Part 3

# Part 4 — Consultation Lifecycle State Machine

The Consultation Workflow is the primary clinical workflow within Mirage.

It orchestrates multiple independent services into a single seamless experience while maintaining provider abstraction.

The consultation workflow coordinates:

- Authentication
- Patient Context
- Active Consent Validation
- Existing Symptom Checker
- Live Transcription
- AI Clinical Suggestions
- Clinical Notes
- Diagnosis
- Medical Record Updates
- Timeline Events
- Notifications

The consultation workflow is owned by the Consultation Service.

---

# Workflow CL1 — Consultation Initialization

## Purpose

Initialize a consultation after patient selection and successful consent verification.

No consultation may begin unless consent validation succeeds.

---

## Actors

Doctor

Patient

Consultation Service

Consent Service

Medical Record Service

Notification Service

---

## Entry Conditions

✓ Doctor authenticated

✓ Patient selected

✓ Active consent exists

✓ Patient record accessible

---

## State Diagram

```
Patient Selected

↓

Validate Consent

↓

Consent Valid?

↓

Yes

↓

Create Consultation

↓

Load Patient Context

↓

Consultation Ready

----------------------------

No

↓

Access Denied

↓

Request Consent
```

---

## API Calls

POST /consultations/start

GET /consultations/{id}

GET /patients/{id}

GET /timeline/{id}

GET /medical-records/{id}

---

## Backend Actions

Create consultation

↓

Load patient context

↓

Initialize AI session

↓

Initialize transcription session

↓

Publish Consultation.Started

---

## WebSocket Events

Consultation.Started

Notification.Created

---

## Acceptance Criteria

✓ Consultation cannot begin without consent

✓ Patient context loads automatically

✓ AI services initialize in background

✓ Dashboard updates immediately

---

# Workflow CL2 — Existing Symptom Checker Integration

## Purpose

Display structured symptom assessment generated by the existing symptom checker.

Mirage does not implement diagnostic questioning itself.

Instead it consumes an external provider through the SymptomCheckerProvider interface.

---

## Provider Architecture

```
Consultation

↓

SymptomCheckerProvider

↓

Current Provider

↓

Structured Assessment
```

Future providers should be interchangeable without modifying consultation logic.

---

## State Diagram

```
Consultation Ready

↓

Request Assessment

↓

Assessment Running

↓

Assessment Complete

↓

Structured Summary Available
```

---

## API Calls

POST /symptom-check/start

POST /symptom-check/message

POST /symptom-check/complete

GET /symptom-check/{session}

---

## Backend Actions

Retrieve assessment

↓

Normalize provider response

↓

Store structured output

↓

Attach to consultation

---

## Acceptance Criteria

✓ Existing symptom checker integrated

✓ Provider abstraction maintained

✓ Structured assessment attached to consultation

---

# Workflow CL3 — Live Transcription

## Purpose

Capture clinician-patient conversation during consultation.

Transcription should be optional.

Consultation must continue if transcription becomes unavailable.

---

## Provider Architecture

```
TranscriptProvider

↓

Azure

↓

Deepgram

↓

Whisper

↓

Future Provider
```

---

## State Diagram

```
Consultation Active

↓

Start Transcription

↓

Streaming

↓

Transcript Updated

↓

Stop

↓

Transcript Finalized
```

---

## API Calls

POST /transcription/start

POST /transcription/stop

GET /transcription/{id}

---

## WebSocket Events

Transcript.Updated

Transcript.Completed

---

## Failure Recovery

Provider unavailable

↓

Pause transcription

↓

Continue consultation

↓

Doctor continues manually

---

## Acceptance Criteria

✓ Consultation independent from transcription

✓ Partial transcript retained

✓ Provider abstraction preserved

---

# Workflow CL4 — AI Diagnostic Suggestions

## Purpose

Generate non-authoritative clinical suggestions.

AI recommendations assist the clinician but never replace clinical judgement.

---

## Provider Architecture

```
DiagnosisProvider

↓

OpenAI

↓

Azure OpenAI

↓

Anthropic

↓

Mock Provider
```

---

## State Diagram

```
Consultation Active

↓

Generate Suggestions

↓

Processing

↓

Suggestions Ready

↓

Doctor Reviews

↓

Accept

or

Reject
```

---

## API Calls

POST /diagnosis/suggest

GET /diagnosis/{id}

---

## Backend Actions

Collect consultation context

↓

Invoke provider

↓

Normalize response

↓

Store suggestions

↓

Notify frontend

---

## WebSocket Events

Diagnosis.Generated

---

## Acceptance Criteria

✓ Suggestions editable

✓ Suggestions optional

✓ Doctor remains decision maker

---

# Workflow CL5 — Clinical Notes Generation

## Purpose

Generate an editable consultation summary.

AI produces a draft only.

Doctors retain complete editorial control.

---

## State Diagram

```
Transcript Ready

↓

Generate Draft

↓

Draft Ready

↓

Doctor Edits

↓

Final Notes
```

---

## Provider Architecture

```
ClinicalNoteProvider

↓

OpenAI

↓

Azure OpenAI

↓

Local Provider

↓

Mock Provider
```

---

## API Calls

POST /notes/generate

PUT /notes/{id}

GET /notes/{id}

---

## Acceptance Criteria

✓ Draft editable

✓ AI never overwrites manual edits

✓ Manual notes always preserved

---

# Workflow CL6 — Diagnosis Confirmation

## Purpose

Record the clinician's final diagnosis.

The diagnosis becomes part of the permanent medical record.

---

## State Diagram

```
Consultation Active

↓

Doctor Reviews

↓

Diagnosis Confirmed

↓

Record Updated

↓

Timeline Updated

↓

Patient Notified
```

---

## API Calls

POST /diagnoses

PUT /consultations/{id}/complete

---

## Backend Actions

Persist diagnosis

↓

Update medical record

↓

Append timeline

↓

Generate notification

↓

Audit event

---

## WebSocket Events

Diagnosis.Confirmed

Timeline.Updated

MedicalRecord.Updated

Notification.Created

---

## Acceptance Criteria

✓ Medical record updated

✓ Timeline updated

✓ Patient receives notification

✓ Audit recorded

---

# Workflow CL7 — Consultation Completion

## Purpose

Safely close the consultation while ensuring all generated clinical information has been persisted.

---

## State Diagram

```
Consultation Active

↓

Finalize

↓

Persist Remaining Data

↓

Generate Timeline Event

↓

Close Consultation

↓

Completed
```

---

## Backend Actions

Save notes

↓

Save diagnosis

↓

Save transcript

↓

Save AI outputs

↓

Close consultation

↓

Publish events

---

## WebSocket Events

Consultation.Completed

Timeline.Updated

MedicalRecord.Updated

Notification.Created

---

## Audit Events

Consultation.Started

Consultation.Completed

Diagnosis.Confirmed

Notes.Finalized

Transcript.Completed

---

# Failure Recovery

## AI Failure

Disable AI panels.

Consultation continues.

---

## Transcription Failure

Continue consultation.

Allow manual notes.

---

## Database Failure

Prevent completion.

Display retry.

Do not lose entered notes.

---

## WebSocket Failure

Reconnect automatically.

Synchronize latest consultation state after reconnection.

---

## Browser Refresh

Restore consultation if still active.

Reload:

- Patient context
- Notes
- Transcript
- AI suggestions

---

# Consultation State Matrix

| State | Description |
|---------|-------------|
| Initializing | Consultation being created |
| Ready | Patient context loaded |
| Active | Consultation in progress |
| Transcribing | Audio capture active |
| AI Processing | AI generating output |
| Reviewing | Doctor validating outputs |
| Completing | Persisting data |
| Completed | Consultation closed |
| Failed | Recoverable failure |

---

# Global Consultation Rules

The consultation workflow orchestrates provider services but never depends on a specific implementation.

Every AI capability must communicate through its corresponding abstraction:

- SymptomCheckerProvider
- TranscriptProvider
- DiagnosisProvider
- ClinicalNoteProvider

Replacing one provider must never require changes to business logic, UI workflows, API contracts, or database schemas.

The doctor always retains final authority over diagnoses, notes, and treatment decisions.

AI outputs are advisory and must remain clearly distinguishable from clinician-authored content.

---

# Acceptance Criteria

✓ Consultation lifecycle follows the approved workflow.

✓ Existing Symptom Checker integrates through abstraction.

✓ Live transcription is optional and recoverable.

✓ AI suggestions are advisory only.

✓ Clinical notes remain editable.

✓ Diagnosis confirmation updates the medical record.

✓ Timeline events generated automatically.

✓ Patient notified of completed consultation.

✓ Every significant action audited.

✓ Provider abstraction maintained throughout the workflow.

# End of Part 4

# Part 5 — Medical Record, Timeline & Notification State Machines

This section defines how clinical information becomes part of the permanent patient record.

Unlike AI outputs, these workflows produce authoritative medical data that persists beyond the consultation.

All state changes described here are considered clinically significant and must be auditable.

---

# Workflow MR1 — Medical Record Update

## Purpose

Persist finalized clinical information to the patient's longitudinal medical record.

Only finalized clinician-approved information may be written to the permanent record.

---

## Actors

Doctor

Medical Record Service

Consultation Service

Timeline Service

Notification Service

---

## Entry Conditions

✓ Consultation completed

✓ Diagnosis confirmed

✓ Clinical notes finalized

✓ Doctor has appropriate permissions

---

## State Diagram

```
Consultation Completed

↓

Validate Clinical Data

↓

Valid?

↓

Yes

↓

Persist Medical Record

↓

Generate Timeline Event

↓

Notify Patient

↓

Completed

------------------------

No

↓

Validation Failed

↓

Return To Consultation
```

---

## States

Pending

↓

Validating

↓

Persisting

↓

Completed

↓

Failed

---

## API Calls

POST /medical-records

PUT /medical-records/{id}

GET /medical-records/{patientId}

---

## Backend Actions

Validate diagnosis

↓

Validate consultation

↓

Store record

↓

Generate timeline event

↓

Generate notification

↓

Publish WebSocket events

---

## WebSocket Events

MedicalRecord.Created

MedicalRecord.Updated

Timeline.Updated

Notification.Created

---

## Audit Events

MedicalRecord.Created

MedicalRecord.Updated

---

## Acceptance Criteria

✓ Permanent record updated

✓ Timeline automatically updated

✓ Patient notified

✓ Audit created

---

# Workflow MR2 — Timeline Generation

## Purpose

Generate a chronological history of significant patient events.

The timeline serves as the canonical longitudinal view of the patient's healthcare journey.

---

## Timeline Event Types

Consultation

Diagnosis

Prescription

Consent Granted

Consent Revoked

Medical Record Updated

Laboratory Result

Imaging Result

Referral

Future integrations may extend this list.

---

## State Diagram

```
Clinical Event

↓

Create Timeline Entry

↓

Persist Timeline

↓

Publish Update

↓

Visible To Users
```

---

## API Calls

POST /timeline

GET /timeline/{patientId}

---

## Backend Actions

Normalize event

↓

Assign timestamp

↓

Persist

↓

Publish update

---

## Acceptance Criteria

✓ Events ordered chronologically

✓ Immutable timestamps

✓ Visible immediately

---

# Workflow MR3 — Diagnosis Lifecycle

## Purpose

Track the progression of a diagnosis from AI suggestion through clinician confirmation.

AI suggestions are never considered diagnoses until confirmed by a clinician.

---

## State Diagram

```
AI Suggestion

↓

Doctor Reviews

↓

Accept?

↓

Yes

↓

Diagnosis Confirmed

↓

Medical Record Updated

-----------------------

No

↓

Discard Suggestion
```

---

## States

Suggested

↓

Under Review

↓

Confirmed

↓

Rejected

---

## API Calls

POST /diagnoses

PUT /diagnoses/{id}

GET /diagnoses/{patientId}

---

## Acceptance Criteria

✓ AI suggestions remain separate

✓ Only confirmed diagnoses persisted

✓ Audit maintained

---

# Workflow MR4 — Prescription Lifecycle

## Purpose

Record medications prescribed during consultation.

---

## State Diagram

```
Doctor Creates Prescription

↓

Validate

↓

Persist

↓

Medical Record Updated

↓

Patient Notified
```

---

## API Calls

POST /prescriptions

GET /prescriptions/{patientId}

---

## Acceptance Criteria

✓ Prescription stored

✓ Patient notified

✓ Timeline updated

---

# Workflow N1 — Notification Lifecycle

## Purpose

Provide real-time awareness of important system events.

Notifications are informational and never replace the underlying clinical data.

---

## Notification Sources

Consent

Consultation

Medical Record

Diagnosis

Prescription

System

Authentication

Future Integrations

---

## State Diagram

```
Business Event

↓

Notification Generated

↓

Persisted

↓

Published

↓

Delivered

↓

Read

↓

Archived
```

---

## States

Created

↓

Queued

↓

Delivered

↓

Read

↓

Archived

---

## API Calls

GET /notifications

PUT /notifications/{id}/read

PUT /notifications/read-all

---

## WebSocket Events

Notification.Created

Notification.Read

Notification.Archived

---

## Acceptance Criteria

✓ Notifications delivered instantly

✓ Badge counts synchronized

✓ Read state synchronized

---

# Workflow N2 — Real-Time Synchronization

## Purpose

Keep every connected client synchronized without polling.

---

## State Diagram

```
Backend Event

↓

Publish WebSocket

↓

Client Receives

↓

Update Local Cache

↓

Refresh UI
```

---

## Synchronization Events

Consent

Consultation

Timeline

Medical Record

Diagnosis

Notification

Authentication

Provider Status

---

## Cache Strategy

React Query remains the source of cached frontend data.

WebSocket events should invalidate or patch cached queries rather than trigger full page reloads.

---

## Acceptance Criteria

✓ No polling

✓ Minimal UI updates

✓ Cache consistency maintained

---

# Workflow N3 — Notification Read Synchronization

## Purpose

Ensure notification state remains consistent across multiple open sessions.

---

## Example

Patient has:

Desktop browser

+

Mobile browser

Notification opened on desktop.

↓

Notification.Read published.

↓

Mobile immediately removes unread badge.

---

## Acceptance Criteria

✓ Multi-session consistency

✓ WebSocket synchronized

---

# Global Persistence Rules

The following entities are authoritative records:

Medical Record

Diagnosis

Prescription

Timeline

Consent

Consultation

Authentication Audit

Notifications are derived records and may be regenerated if necessary.

---

# Failure Recovery

## Notification Service Offline

Persist notifications.

Deliver after recovery.

---

## Timeline Failure

Medical record persists.

Retry timeline generation asynchronously.

---

## Medical Record Failure

Consultation remains open.

Completion blocked until persistence succeeds.

---

## Duplicate Events

Idempotency keys prevent duplicate:

Timeline entries

Medical records

Notifications

Audit events

---

# Audit Matrix

| Workflow | Audit Event |
|----------|-------------|
| Medical Record | MedicalRecord.Created |
| Timeline | Timeline.Created |
| Diagnosis | Diagnosis.Confirmed |
| Prescription | Prescription.Created |
| Notification | Notification.Created |

---

# Acceptance Criteria

✓ Medical record remains authoritative.

✓ Timeline generated automatically.

✓ Notifications synchronized in real time.

✓ AI outputs remain distinct from clinician-authored data.

✓ Duplicate writes prevented.

✓ Every clinically significant action audited.

# End of Part 5

# Part 6 — System Orchestration, Provider Lifecycle & Platform State Machines

This section defines the behavior of the Mirage platform itself.

Unlike previous workflows, these state machines describe how infrastructure, AI providers, background services, and inter-service communication behave.

These workflows should remain independent of the user interface.

---

# Workflow S1 — AI Provider Orchestration

## Purpose

Provide a single abstraction layer for all AI capabilities.

Business logic must never communicate directly with vendor SDKs.

Instead, every AI interaction passes through a provider interface.

---

## Supported Provider Interfaces

```
SymptomCheckerProvider

TranscriptProvider

DiagnosisProvider

ClinicalNoteProvider
```

Each provider interface may have multiple implementations.

Example

```
DiagnosisProvider

↓

OpenAI

Azure OpenAI

Anthropic

Mock Provider

Future Provider
```

---

## State Diagram

```
Request Received

↓

Resolve Active Provider

↓

Provider Available?

↓

Yes

↓

Execute Request

↓

Normalize Response

↓

Return Result

----------------------------

No

↓

Fallback Provider

↓

Available?

↓

Yes

↓

Execute

↓

Return Result

----------------------------

No

↓

Provider Failure
```

---

## Requirements

Providers must expose identical interfaces regardless of implementation.

No UI component should know which provider is active.

Provider selection should be configurable through environment variables.

---

## Acceptance Criteria

✓ Provider swapping requires configuration only.

✓ Business logic unchanged.

✓ Frontend unchanged.

---

# Workflow S2 — Provider Health Monitoring

## Purpose

Continuously monitor external provider availability.

---

## State Diagram

```
Healthy

↓

Health Check

↓

Healthy?

↓

Yes

↓

Remain Healthy

---------------------

No

↓

Degraded

↓

Retry

↓

Recovered?

↓

Yes

↓

Healthy

----------------------

No

↓

Unavailable
```

---

## Health Checks

Each provider should expose

```
health()

ready()

latency()

version()
```

---

## Dashboard Indicators

Healthy

Warning

Unavailable

These indicators should appear only within administrative tooling, not patient-facing interfaces.

---

## Acceptance Criteria

✓ Provider failures detected automatically.

✓ Recovery automatic.

✓ Metrics recorded.

---

# Workflow S3 — Background Job Lifecycle

## Purpose

Coordinate scheduled and asynchronous work.

Background jobs should never block user interactions.

---

## Example Jobs

Consent Expiration

Notification Delivery

Timeline Generation

Audit Export

Provider Health Checks

Database Cleanup

Future Analytics

---

## State Diagram

```
Job Scheduled

↓

Queued

↓

Running

↓

Completed

↓

Archived
```

---

## Failure Recovery

Failed

↓

Retry

↓

Retry Limit?

↓

No

↓

Retry

---------------------

Yes

↓

Dead Letter Queue

---

## Acceptance Criteria

✓ Retry supported.

✓ Jobs idempotent.

✓ Dead-letter queue implemented.

---

# Workflow S4 — WebSocket Connection Lifecycle

## Purpose

Maintain reliable real-time communication between frontend and backend.

---

## State Diagram

```
Application Starts

↓

Authenticate

↓

Connect

↓

Connected

↓

Heartbeat

↓

Disconnected?

↓

No

↓

Connected

-----------------------

Yes

↓

Reconnect

↓

Connected
```

---

## Connection Events

Socket.Connected

Socket.Disconnected

Socket.Reconnecting

Socket.Authenticated

Socket.Error

---

## Reconnection Strategy

Attempt

1 second

↓

2 seconds

↓

5 seconds

↓

10 seconds

↓

30 seconds

Continue until connection restored.

---

## Acceptance Criteria

✓ Automatic reconnect.

✓ JWT revalidated.

✓ Event subscriptions restored.

---

# Workflow S5 — Docker Platform Startup

## Purpose

Ensure every service starts in the correct dependency order.

---

## Startup Sequence

```
Docker Compose

↓

PostgreSQL

↓

Redis

↓

Database Migration

↓

FastAPI

↓

Background Worker

↓

WebSocket Gateway

↓

Next.js

↓

Ready
```

---

## Health Dependencies

FastAPI must wait for:

PostgreSQL

Redis

Completed migrations

Next.js should wait until FastAPI is healthy.

---

## Acceptance Criteria

✓ One-command startup.

✓ Deterministic service order.

✓ Health checks enforced.

---

# Workflow S6 — System Health Monitoring

## Purpose

Expose overall platform status.

---

## Components

Database

Redis

API

WebSocket

AI Providers

Background Workers

Storage

---

## Overall State

Healthy

↓

Warning

↓

Degraded

↓

Critical

---

## Health Endpoint

```
GET /health

GET /ready

GET /live
```

---

## Acceptance Criteria

✓ Kubernetes-ready.

✓ Docker-ready.

✓ Machine-readable responses.

---

# Workflow S7 — Application Recovery

## Purpose

Recover safely after crashes or unexpected shutdowns.

---

## State Diagram

```
Unexpected Failure

↓

Restart

↓

Restore Services

↓

Restore Sessions

↓

Resume Jobs

↓

Healthy
```

---

## Recovery Rules

Restore

Queued jobs

Active consultations

Open WebSocket subscriptions

Cached state

Provider sessions where supported

---

## Acceptance Criteria

✓ Recovery automatic.

✓ No database corruption.

✓ No duplicate jobs.

---

# Workflow S8 — Global State Ownership

Every mutable state has a single owner.

| State | Owner |
|---------|-------|
| Authentication | Auth Service |
| Consultation | Consultation Service |
| Consent | Consent Service |
| Medical Record | Medical Record Service |
| Timeline | Timeline Service |
| Notification | Notification Service |
| Diagnosis | Diagnosis Service |
| Clinical Notes | Consultation Service |
| Transcription | Transcript Provider |
| Symptom Assessment | Symptom Provider |

Frontend components consume state but never own business state.

---

# Workflow S9 — End-to-End Consultation Overview

This summarizes the complete Mirage workflow.

```
Doctor Login

↓

Patient Search

↓

Request Consent

↓

Patient Approves

↓

Medical Record Accessible

↓

Consultation Starts

↓

Existing Symptom Checker

↓

Live Transcription

↓

AI Suggestions

↓

Clinical Notes

↓

Diagnosis Confirmed

↓

Medical Record Updated

↓

Timeline Updated

↓

Patient Notified

↓

Consultation Closed
```

Every transition shown above is fully defined elsewhere in this document.

---

# Cross-Cutting System Rules

## Idempotency

The following operations must be idempotent:

- Consent approval
- Consent denial
- Consultation completion
- Timeline generation
- Notification creation
- Medical record persistence

Repeated requests must never create duplicate records.

---

## Observability

Every service should expose:

Structured logs

Metrics

Health endpoints

Correlation IDs

Request tracing

Future OpenTelemetry support should require minimal changes.

---

## Security

Protected endpoints require JWT authentication.

Authorization is validated on every request.

Consent is validated on every protected medical record request.

Sensitive information must never appear in logs.

Secrets must be supplied through environment variables or Docker secrets.

---

## Performance Targets

Patient Dashboard

< 2 seconds

Doctor Dashboard

< 2 seconds

Patient Search

< 500 ms

Medical Record Loading

< 2 seconds

Consent Synchronization

< 1 second

Notification Delivery

< 1 second

WebSocket Reconnection

< 10 seconds

These targets apply to the demo environment and should remain achievable as the platform evolves.

---

# Document Traceability

This document implements the behavioral requirements defined by:

- `00_Project_Index.md`
- `01_Product_Requirements_Document.md`
- `02_Technical_Architecture.md`
- `03_Design_System.md`
- `04_Implementation_Plan.md`
- `05_API_Contract.md`
- `06_Database_Schema.md`
- `08_Coding_Standards.md`
- `09_Deployment_Guide.md`
- `10_UI_Screen_Specification.md`
- `docs/wireframes.html`

Future workflow modifications should update this document before implementation begins.

---

# Definition of Completion

The platform implementation is considered complete when:

✓ Every workflow defined in this document is implemented.

✓ Every state transition is deterministic.

✓ Every clinically significant action is auditable.

✓ Every provider is accessed exclusively through abstraction interfaces.

✓ All frontend clients synchronize through WebSockets.

✓ Background jobs execute independently of user interactions.

✓ Docker startup is deterministic.

✓ Recovery paths exist for every critical workflow.

✓ Performance targets are met.

✓ The implemented behavior matches the Product Requirements Document, UI Specification, and approved wireframes.

---

# End of 11_User_Flows_and_State_Machines.md