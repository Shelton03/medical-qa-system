# Mirage
# Technical Architecture Specification

Version: 1.0

---

# 1. Architecture Philosophy

Mirage is designed as a modular healthcare platform rather than a monolithic web application.

Every subsystem should be independently replaceable.

Business logic must never depend directly on infrastructure implementations.

Instead, every external dependency is accessed through interfaces.

Examples include:

- Authentication
- AI Providers
- Notifications
- Storage
- Email
- Speech-to-Text
- Clinical Summarization

This allows Mirage to evolve from a Healthathon MVP into a production healthcare platform without requiring large architectural rewrites.

---

# 2. High-Level Architecture

Mirage consists of five major layers.

┌──────────────────────────────────────┐
│           Next.js Frontend           │
│                                      │
│  Patient App     Doctor Portal       │
└──────────────────────────────────────┘
                 │
                 │ REST + WebSockets
                 ▼
┌──────────────────────────────────────┐
│           FastAPI Backend            │
│                                      │
│ Authentication                       │
│ API                                  │
│ Services                             │
│ Domain Logic                         │
│ AI Interfaces                        │
└──────────────────────────────────────┘
                 │
        ┌────────┴────────┐
        ▼                 ▼
 PostgreSQL           Redis
 Database          Cache / Events
        │
        ▼
 AI Provider Interfaces

- Symptom Checker
- Diagnosis
- Summary
- Transcription
- Notifications

---

# 3. Design Principles

The architecture follows several principles.

## Separation of Concerns

Presentation

↓

Application

↓

Domain

↓

Infrastructure

No UI code should contain business logic.

---

## Dependency Inversion

High-level services depend only on interfaces.

Never concrete implementations.

For example:

PatientService

depends on

PatientRepository

not

SQLAlchemyPatientRepository

---

## Single Responsibility

Each module performs one responsibility.

Authentication should never contain patient logic.

Patient services should never perform notification delivery.

---

## Event Driven

Important system events should be emitted rather than tightly coupling services.

Examples:

ConsentApproved

↓

Notification Service

↓

Audit Service

↓

WebSocket Service

↓

Analytics

---

# 4. Repository Structure

mirage/

│

├── frontend/

│   ├── app/

│   ├── components/

│   ├── features/

│   ├── hooks/

│   ├── providers/

│   ├── services/

│   ├── lib/

│   ├── styles/

│   ├── types/

│   └── utils/

│

├── backend/

│

│   ├── api/

│   ├── core/

│   ├── domain/

│   ├── repositories/

│   ├── services/

│   ├── interfaces/

│   ├── infrastructure/

│   ├── websocket/

│   ├── auth/

│   ├── workers/

│   ├── models/

│   ├── migrations/

│   ├── tests/

│   └── main.py

│

├── docker/

│

├── docs/

│

├── scripts/

│

├── seed/

│

└── docker-compose.yml

---

# 5. Backend Folder Structure

backend/

api/

Contains all HTTP routes.

No business logic.

Controllers only.

---

services/

Business logic.

Examples:

PatientService

DoctorService

ConsentService

NotificationService

RecordService

ConsultationService

DiagnosisService

TimelineService

AuditService

---

repositories/

Database access.

Examples:

PatientRepository

VisitRepository

ConsentRepository

DoctorRepository

AuditRepository

MedicationRepository

NotificationRepository

Repositories communicate with SQLAlchemy.

Services never do.

---

interfaces/

Contains contracts.

Examples:

SymptomCheckerProvider

DiagnosisProvider

SummaryProvider

NotificationProvider

TranscriptionProvider

StorageProvider

EmailProvider

---

infrastructure/

Concrete implementations.

OpenAIProvider

RedisNotificationProvider

WebSocketProvider

PostgresRepositories

Future providers belong here.

---

models/

SQLAlchemy models.

Contains only persistence definitions.

---

domain/

Pure business objects.

No framework dependencies.

---

core/

Configuration.

Dependency Injection.

Logging.

Environment variables.

Application startup.

---

auth/

JWT

Password Hashing

Roles

Permissions

Session management

---

websocket/

Real-time event handling.

---

workers/

Background jobs.

Future AI processing.

Notification delivery.

Long-running tasks.

---

# 6. Frontend Structure

The frontend follows feature-first organization.

components/

Reusable UI.

Buttons

Cards

Inputs

Sheets

PhoneFrame

Timeline

Dialogs

Tables

Navigation

---

features/

Patient

Doctor

Authentication

Notifications

Consent

Timeline

AI Consultation

Medical Records

Each feature contains:

components/

hooks/

services/

types/

utils/

---

app/

Next.js routing.

Should remain thin.

Pages compose features.

---

providers/

Global providers.

Theme

Authentication

WebSocket

React Query

Motion

---

hooks/

Shared hooks.

Examples:

useAuth()

usePatient()

useDoctor()

useTimeline()

useConsent()

useNotification()

---

services/

REST API.

WebSocket Client.

Caching.

---

lib/

Shared utilities.

Date formatting.

Validation.

Constants.

Helpers.

---

# 7. Docker Architecture

The project must launch with a single command.

docker compose up

Required containers:

frontend

backend

postgres

redis

worker

Optional:

adminer

pgadmin

mailhog

The frontend communicates only with the backend.

The backend owns all database communication.

No frontend code accesses PostgreSQL directly.

---

# 8. Environment Configuration

Each service should expose configuration using environment variables.

Frontend

NEXT_PUBLIC_API_URL

NEXT_PUBLIC_WS_URL

DEMO_MODE

Backend

DATABASE_URL

REDIS_URL

JWT_SECRET

JWT_EXPIRATION

REFRESH_SECRET

OPENAI_KEY

SYMPTOM_PROVIDER

SUMMARY_PROVIDER

TRANSCRIPTION_PROVIDER

LOG_LEVEL

All configuration should be injectable.

No secrets should exist inside source code.

---

# 9. Coding Standards

Backend

Python 3.12+

Type hints everywhere.

Black

Ruff

Pytest

SQLAlchemy 2.x

Alembic

Frontend

TypeScript Strict Mode

ESLint

Prettier

TailwindCSS

Framer Motion

React Query

No `any` types unless absolutely unavoidable.

# 10. Domain-Driven Design

Mirage should follow a Domain-Driven Design (DDD) inspired architecture.

The application should be organized around business concepts rather than infrastructure.

Primary Domains:

- Authentication
- Patient Management
- Practitioner Registry
- Medical Records
- Consultations
- Consent Management
- AI Services
- Notifications
- Audit Logging

Each domain owns:

- Models
- Services
- Repositories
- Events
- DTOs
- Validation

Cross-domain communication should occur through service interfaces or events, never by directly manipulating another domain's persistence layer.

---

# 11. Database Architecture

Database Engine

PostgreSQL

ORM

SQLAlchemy 2.x

Migration Tool

Alembic

Database Naming Convention

snake_case

Primary Keys

UUID

Foreign Keys

UUID

Soft Deletes

Not initially.

Instead use immutable history and audit logs.

Created At

Every table.

Updated At

Every mutable table.

---

# 12. Core Database Entities

The following entities form the foundation of Mirage.

Users

Roles

Patients

Doctors

Facilities

Practitioner Registry

Medical Records

Visits

Diagnoses

Medications

Allergies

Conditions

Lab Results

Clinical Notes

Consent Requests

Consent Sessions

Notifications

Audit Logs

Access Logs

AI Sessions

AI Messages

Attachments

Refresh Tokens

---

# 13. Entity Relationships

User

↓

Patient Profile

or

Doctor Profile

↓

Consultation

↓

Visit

↓

Medical Record

↓

Timeline

Doctors belong to Facilities.

Patients own Medical Records.

Medical Records contain Visits.

Visits contain:

Diagnoses

Notes

Medication

Attachments

AI Sessions

Lab Results

Consent links Patient and Doctor.

Audit logs reference every important entity.

---

# 14. Users Table

Purpose

Authentication.

Columns

id

email

password_hash

role

status

is_demo

created_at

updated_at

Relationships

One Patient

or

One Doctor

Future Admin

---

# 15. Patients Table

Columns

id

medical_record_number

national_id

first_name

last_name

date_of_birth

gender

blood_group

phone

email

address

emergency_contact

created_at

updated_at

Relationships

One Medical Record

Many Visits

Many Notifications

Many Consent Requests

Many Access Logs

---

# 16. Doctors Table

Columns

id

user_id

registration_number

facility_id

speciality

verification_status

phone

email

created_at

Relationships

Many Consultations

Many Consent Requests

Many Clinical Notes

Many AI Sessions

---

# 17. Facilities

Columns

id

name

province

district

facility_type

address

contact_number

status

Relationships

Many Doctors

Many Visits

Many Notifications

---

# 18. Medical Records

Every patient owns exactly one longitudinal record.

Columns

id

patient_id

created_at

updated_at

Relationships

Many Visits

Many Allergies

Many Conditions

Many Medications

Many Attachments

---

# 19. Visits

Visits represent consultations.

Columns

id

medical_record_id

facility_id

doctor_id

visit_date

chief_complaint

status

created_at

Relationships

Diagnoses

Clinical Notes

Medication

Investigations

Lab Results

AI Session

---

# 20. Diagnoses

Columns

id

visit_id

diagnosis

confidence

confirmed

notes

created_at

Only confirmed diagnoses become part of permanent history.

---

# 21. Medications

Columns

id

visit_id

drug_name

strength

frequency

duration

instructions

---

# 22. Allergies

Critical safety information.

Columns

id

patient_id

substance

reaction

severity

status

Critical allergies should be surfaced throughout the application.

---

# 23. Clinical Notes

AI generated.

Doctor reviewed.

Columns

id

visit_id

subjective

objective

assessment

plan

doctor_modified

approved

approved_by

approved_at

---

# 24. Consent Requests

Columns

id

patient_id

doctor_id

facility_id

status

requested_at

approved_at

expires_at

reason

scope

Every consultation requires a consent request.

---

# 25. Consent Sessions

Tracks active permissions.

Columns

id

consent_request_id

started_at

expires_at

active

Automatically expires.

---

# 26. Notifications

Columns

id

recipient_id

type

title

message

read

created_at

Notification types

Consent

Consultation

Medical Record

AI

System

---

# 27. Access Logs

Every record view generates an access log.

Columns

id

patient_id

doctor_id

facility_id

purpose

access_time

duration

ip_address

user_agent

---

# 28. Audit Logs

Immutable.

Never edited.

Columns

id

actor

action

entity

entity_id

timestamp

metadata

Audit logs form the legal record of system activity.

---

# 29. AI Sessions

Represents a consultation with AI assistance.

Columns

id

visit_id

provider

started_at

completed_at

status

summary

Relationships

Many Messages

Generated Diagnosis

Generated Summary

---

# 30. AI Messages

Conversation history.

Columns

id

session_id

role

content

timestamp

Messages remain immutable.

---

# 31. Attachments

Future compatible.

Examples

Lab Reports

Scans

Images

Documents

Columns

id

visit_id

filename

mime_type

storage_key

uploaded_at

---

# 32. Refresh Tokens

Production mode only.

Columns

id

user_id

token_hash

expires_at

revoked

created_at

---

# 33. Repository Pattern

Every database table should expose a repository.

PatientRepository

DoctorRepository

VisitRepository

ConsentRepository

DiagnosisRepository

MedicationRepository

TimelineRepository

NotificationRepository

AuditRepository

Repositories perform persistence only.

No business logic.

---

# 34. Service Layer

Business rules belong here.

PatientService

DoctorService

ConsentService

TimelineService

RecordService

ConsultationService

DiagnosisService

AuthenticationService

NotificationService

AuditService

AISessionService

These services coordinate repositories and providers.

---

# 35. Transaction Boundaries

Each business operation should execute within a transaction.

Example:

Doctor confirms consultation

↓

Save diagnosis

↓

Save notes

↓

Update timeline

↓

Create audit log

↓

Create notification

↓

Commit

If any step fails:

Rollback entire transaction.

Never leave partially written medical records.

---

# 36. Dependency Injection

FastAPI dependency injection should be used throughout.

Example flow

API Route

↓

Service

↓

Repository

↓

Database

External providers

↓

Interfaces

↓

Concrete implementations

No service should instantiate dependencies directly.

All dependencies should be injected.

This enables testing, mocking, and provider replacement.

# 37. Backend Application Architecture

The FastAPI backend follows a layered architecture.

```
HTTP Request
      │
      ▼
API Router
      │
      ▼
Request Validation (Pydantic)
      │
      ▼
Application Service
      │
      ▼
Repository + Domain Services
      │
      ▼
Database / AI Provider / Notification Provider
      │
      ▼
Response DTO
      │
      ▼
HTTP Response
```

Routes should never contain business logic.

Business rules belong inside Services.

Repositories only perform persistence.

---

# 38. REST API Design

The backend exposes a versioned REST API.

```
/api/v1/
```

Future breaking changes become:

```
/api/v2/
```

---

# 39. Authentication Endpoints

## Demo Login

```
POST /api/v1/auth/demo-login
```

Request

```
{
    "role": "patient"
}
```

or

```
{
    "role": "doctor"
}
```

Returns

JWT (optional)

User profile

Permissions

Demo flag

---

## Production Login

```
POST /api/v1/auth/login
```

Returns

Access Token

Refresh Token

Profile

Permissions

---

## Refresh Token

```
POST /api/v1/auth/refresh
```

---

## Logout

```
POST /api/v1/auth/logout
```

Revokes refresh token.

---

# 40. Patient Endpoints

```
GET /patients/me
```

Returns patient profile.

---

```
GET /patients/me/timeline
```

Returns longitudinal timeline.

---

```
GET /patients/me/notifications
```

---

```
GET /patients/me/access-history
```

---

```
GET /patients/me/medical-record
```

---

```
GET /patients/me/visits
```

---

```
GET /patients/me/visit/{id}
```

---

```
PUT /patients/me/profile
```

Patient-editable information only.

---

# 41. Doctor Endpoints

```
GET /doctor/dashboard
```

---

```
GET /doctor/recent-patients
```

---

```
GET /doctor/pending-consent
```

---

```
POST /doctor/search
```

---

```
GET /doctor/patient/{id}
```

---

```
GET /doctor/patient/{id}/timeline
```

---

```
POST /doctor/patient/{id}/consultation
```

Creates a consultation session.

---

# 42. Consent API

Request Access

```
POST /consent/request
```

Approve

```
POST /consent/approve
```

Reject

```
POST /consent/reject
```

Cancel

```
POST /consent/cancel
```

Status

```
GET /consent/{id}
```

History

```
GET /consent/history
```

---

# 43. Medical Record API

Retrieve record

```
GET /records/{id}
```

Retrieve visit

```
GET /visits/{id}
```

Update record

```
POST /records/update
```

Only after doctor approval.

---

# 44. AI Session API

Create AI Session

```
POST /ai/session
```

Returns

Session ID

Provider

Patient Context Loaded

---

Continue Session

```
POST /ai/session/{id}/message
```

Returns

AI Response

Suggested Questions

Updated Context

---

Generate Differential

```
POST /ai/session/{id}/diagnosis
```

---

Generate Summary

```
POST /ai/session/{id}/summary
```

---

Close Session

```
POST /ai/session/{id}/complete
```

---

# 45. Notification API

```
GET /notifications
```

```
PUT /notifications/read
```

```
DELETE /notifications/{id}
```

---

# 46. WebSocket Architecture

Real-time communication should use WebSockets.

Endpoint

```
/ws
```

Authenticated using JWT.

Clients subscribe after login.

---

Supported Events

Consent Requested

Consent Approved

Consent Denied

Consultation Started

Consultation Completed

Record Updated

Notification Created

Patient Timeline Updated

Doctor Dashboard Updated

AI Response Ready

---

WebSocket payloads should be lightweight.

Heavy data should still be retrieved using REST.

---

# 47. Redis Event Bus

Redis should act as the application's event broker.

Example

Doctor requests consent

↓

Consent Event

↓

Redis

↓

Notification Worker

↓

WebSocket

↓

Patient receives request

Multiple workers should be able to subscribe independently.

---

# 48. AI Provider Architecture

The application must never call OpenAI (or any provider) directly from business logic.

Instead:

```
Application Service

↓

DiagnosisProvider Interface

↓

Concrete Provider

↓

Vendor API
```

---

Required Provider Interfaces

SymptomCheckerProvider

DiagnosisProvider

ClinicalSummaryProvider

TranscriptionProvider

NotificationProvider

FutureProvider

---

Every provider should implement a common lifecycle:

Initialize

Validate

Execute

Handle Errors

Return Standardized Response

---

# 49. Symptom Checker Integration

The existing symptom checker is an external dependency.

The backend must treat it as a provider.

It is NOT implemented inside Mirage.

Responsibilities:

Load patient context.

Begin session.

Receive patient answers.

Return next question.

Return completion state.

Mirage owns:

Session storage.

Conversation history.

Authentication.

Patient linking.

Audit logging.

The symptom engine owns only diagnostic questioning.

---

# 50. Diagnosis Provider

Receives

Patient History

Consultation

Symptoms

Previous Conditions

Allergies

Current Medications

Returns

Differential Diagnoses

Confidence Scores

Suggested Investigations

Clinical Reasoning

Medication Warnings

---

# 51. Clinical Summary Provider

Produces structured documentation.

Input

Conversation

History

Doctor Notes

Output

SOAP Note

Assessment

Plan

Recommendations

Doctor Approval Required

---

# 52. Transcription Provider

Accepts

Audio Stream

Returns

Timestamped Transcript

Speaker Separation

Confidence

Providers may include:

Whisper

Azure Speech

Deepgram

AssemblyAI

Custom Provider

---

# 53. Notification Provider

Responsible for:

Push Notifications

Email

SMS

WebSocket

Future Mobile Notifications

Application services communicate only through the interface.

---

# 54. Background Workers

Long-running operations should execute asynchronously.

Examples:

AI Requests

Notification Delivery

Summary Generation

Email

Future Analytics

Worker Queue

Redis

Future Migration

Celery

RQ

Dramatiq

All workers should be replaceable.

---

# 55. Error Handling Strategy

Every API returns a consistent structure.

```
{
    "success": true,
    "data": {},
    "errors": [],
    "metadata": {}
}
```

Failures

```
{
    "success": false,
    "errors": [
        {
            "code": "CONSENT_DENIED",
            "message": "...",
            "details": {}
        }
    ]
}
```

Never expose stack traces.

Internal errors are logged.

User receives safe messages.

---

# 56. API Documentation

FastAPI automatically generates

Swagger UI

```
/docs
```

ReDoc

```
/redoc
```

Every endpoint must include:

Summary

Description

Tags

Request Example

Response Example

Possible Errors

Permission Requirements

---

# 57. Logging Strategy

Structured logging only.

Every request includes:

Request ID

User ID

Endpoint

Latency

Response Status

Errors

Logs should be JSON formatted.

Future integrations should support:

OpenTelemetry

Grafana

Prometheus

ELK Stack

---

# 58. Health Checks

Required endpoints

```
GET /health
```

```
GET /ready
```

```
GET /live
```

Docker should use these for container health monitoring.

---

# 59. Seed Data

The repository should include realistic seed data.

Minimum:

10 Patients

5 Doctors

3 Facilities

50 Visits

100 Notifications

Multiple AI Sessions

Consent Requests

Medication History

Chronic Conditions

Lab Results

The demonstration should feel like a real healthcare system rather than an empty application.

 # 60. Frontend Architecture

The frontend is implemented as a single Next.js application that provides two distinct user experiences:

- Patient Application (mobile simulation)
- Doctor Portal (desktop-first)

Both applications share:

- Authentication
- API client
- Component library
- Theme
- Design tokens
- State management
- Notification system
- WebSocket client

The frontend should feel like two products powered by the same platform, not two unrelated applications.

---

# 61. Application Routing

Next.js App Router should be used.

Suggested route structure:

```
/

├── login

├── patient
│   ├── dashboard
│   ├── timeline
│   ├── record
│   ├── symptoms
│   ├── notifications
│   ├── access
│   ├── profile
│   ├── settings
│   └── medical-id

├── doctor
│   ├── dashboard
│   ├── search
│   ├── patient
│   ├── consultation
│   ├── diagnosis
│   ├── notes
│   ├── notifications
│   ├── access-history
│   └── settings

└── admin (future)
```

Protected routes should automatically redirect unauthenticated users.

---

# 62. Layout Strategy

The application should expose two layout systems.

## Patient Layout

Uses the reusable `PhoneFrame` component.

Every patient screen renders inside the simulated mobile device.

```
<AppLayout>
    <PhoneFrame>
        <PatientScreen />
    </PhoneFrame>
</AppLayout>
```

The browser is only the container.

The patient application always believes it is running on a phone.

---

## Doctor Layout

Traditional responsive dashboard.

Structure:

```
Sidebar

Header

Content

Right Panel (optional)
```

Responsive behaviour:

Desktop

Tablet

Laptop

Large monitors

No mobile simulation is used.

---

# 63. Demo Modes

The frontend supports three viewing modes.

## Patient Mode

Only PhoneFrame visible.

Ideal for demonstrating patient workflows.

---

## Doctor Mode

Only doctor portal visible.

Ideal for clinician demonstrations.

---

## Split Screen Mode

This is the preferred Healthathon demonstration mode.

```
---------------------------------------------------------

Patient Phone         Doctor Portal

|               |     |                           |
|               |     |                           |
|               |     |                           |
|               |     |                           |
|               |     |                           |

---------------------------------------------------------
```

The patient phone remains fixed.

The doctor interface occupies remaining space.

Real-time interactions become immediately visible.

Examples:

Doctor requests consent.

↓

Patient phone immediately updates.

↓

Patient approves.

↓

Doctor portal unlocks.

This dramatically improves demonstrations.

---

# 64. PhoneFrame Component

PhoneFrame is the foundation of the patient experience.

Responsibilities:

Render realistic device.

Maintain fixed viewport.

Prevent browser resizing from affecting layouts.

Expose a consistent mobile canvas.

Target viewport:

370 × 800

Fallback:

350 × 760

The component should include:

Rounded bezel

Device shadow

Status bar

Dynamic safe area

Camera notch

Glass reflections

Optional home indicator

The PhoneFrame should be reusable and configurable.

---

# 65. Patient Navigation

Primary navigation uses a bottom navigation bar.

Suggested tabs:

Home

Timeline

Symptoms

Notifications

Profile

Navigation should remain persistent across screens.

Animated active indicator.

Glassmorphism styling.

---

# 66. Doctor Navigation

Sidebar navigation.

Primary sections:

Dashboard

Patients

Consultations

Notifications

Settings

Profile

The sidebar should collapse on smaller screens.

---

# 67. State Management

Global state should remain minimal.

Recommended tools:

React Query

Authentication Context

Theme Context

WebSocket Context

Everything else should remain local.

Avoid unnecessary global state.

---

# 68. React Query

Server state should use React Query.

Examples:

Patient Record

Timeline

Notifications

Dashboard

Consent Requests

Visits

Benefits:

Caching

Refetching

Invalidation

Optimistic Updates

Retry Logic

---

# 69. WebSocket Client

The frontend establishes a single persistent WebSocket connection after authentication.

Responsibilities:

Receive notifications.

Receive consent events.

Receive timeline updates.

Receive AI completion events.

Reconnect automatically after connection loss.

---

# 70. API Client

The frontend communicates exclusively with the FastAPI backend.

A centralized API client should handle:

JWT attachment

Refresh token flow

Error handling

Request cancellation

Retry logic

Response normalization

No component should call `fetch()` directly.

---

# 71. Feature Modules

Each feature should be isolated.

Example:

```
features/

patient/

doctor/

consultation/

consent/

timeline/

notifications/

authentication/

symptoms/
```

Each feature contains:

```
components/

hooks/

services/

types/

utils/
```

Features should avoid importing one another directly unless absolutely necessary.

---

# 72. Design Tokens

The design system should expose reusable tokens.

Colors

Typography

Spacing

Elevation

Border Radius

Animation

Breakpoints

Shadows

Glass styles

Never hardcode design values inside components.

---

# 73. Loading Strategy

Every asynchronous screen should define:

Skeleton Loading

Partial Loading

Error State

Retry State

Empty State

Example:

Timeline

↓

Skeleton cards

↓

Timeline appears

rather than

Blank screen

↓

Data

---

# 74. Error Boundaries

React Error Boundaries should isolate failures.

If:

Timeline crashes

Symptoms page crashes

Notifications fail

The entire application should not crash.

Only the affected section.

---

# 75. Offline Behaviour

Although true offline support is outside MVP scope, the UI should gracefully detect connection loss.

Examples:

Banner

"Connection Lost"

Retry Button

Cached Timeline

Read-only state

Never display broken interfaces.

---

# 76. Accessibility

Components should include:

ARIA labels

Keyboard navigation

Focus states

Reduced motion support

Semantic HTML

Screen reader support

Healthcare software must prioritize usability.

---

# 77. Responsive Behaviour

Patient application

Never changes dimensions.

Always renders inside PhoneFrame.

Doctor application

Responsive across:

1280+

1024

768

Mobile support is optional but should not break the interface.

---

# 78. Frontend Testing Strategy

Recommended testing:

Vitest

React Testing Library

Playwright (future)

Critical flows to test:

Authentication

Consent approval

Patient search

Record updates

Notification rendering

PhoneFrame layout

AI consultation

Focus on behaviour over implementation details.

---

# 79. Shared Utilities

Centralized utility modules should include:

Date formatting

Age calculation

Medical Record formatting

Validation

Status helpers

Permission helpers

Notification formatting

Avoid duplicating utility functions across features.

---

# 80. Definition of Frontend Done

The frontend is considered complete when:

- Patient application fully matches the wireframe flows while using the mobile simulation framework.
- Doctor portal implements every required consultation workflow.
- Split-screen mode demonstrates real-time interaction.
- Authentication supports Demo Mode and JWT Mode.
- Every screen includes loading, error, and empty states.
- Components are reusable and documented.
- No business logic resides inside UI components.
- API interactions are centralized.
- State management remains predictable and maintainable.