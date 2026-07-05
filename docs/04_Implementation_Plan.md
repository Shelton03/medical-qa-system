# Mirage
# Implementation Plan

Version 1.0

---

# Purpose

This document defines the recommended implementation order for Mirage.

The coding assistant should complete one phase at a time.

Each phase should compile successfully before beginning the next.

No placeholder implementations should remain unless explicitly documented.

Every phase should leave the repository in a runnable state.

---

## Prerequisites

Before implementation begins, the AI assistant must
read every document in docs/.

No implementation should begin until the
UI Screen Specification and User Flow Specification
have also been loaded into context.

---

# Guiding Principles

The coding assistant should:

- Prefer incremental delivery over large batches.
- Keep the application runnable after every phase.
- Avoid speculative abstractions.
- Follow the Technical Architecture document.
- Follow the Design System document.
- Never bypass provider interfaces.
- Never embed business logic inside UI components.
- Never hardcode provider implementations.

---

# Phase 1 — Repository Bootstrap

## Goal

Create the complete repository structure.

Nothing functional yet.

Only scaffolding.

---

Deliverables

```
mirage/

frontend/

backend/

docker/

docs/

seed/

scripts/

.github/

docker-compose.yml

README.md

.env.example

.gitignore
```

---

Backend folders

```
api/

auth/

core/

domain/

interfaces/

models/

repositories/

services/

workers/

websocket/

tests/

migrations/
```

---

Frontend folders

```
app/

components/

features/

providers/

hooks/

services/

types/

utils/

styles/
```

---

Acceptance Criteria

✓ Repository builds.

✓ Docker folders exist.

✓ Folder naming follows architecture.

✓ README explains project.

---

# Phase 2 — Docker Environment

## Goal

Launch the entire stack with one command.

```
docker compose up
```

---

Containers

Frontend

Backend

PostgreSQL

Redis

Worker

Optional

Adminer

Mailhog

---

Networking

Internal Docker network.

Backend communicates with:

Postgres

Redis

Frontend communicates only with backend.

---

Acceptance Criteria

✓ Every container starts.

✓ Health checks pass.

✓ Logs are readable.

✓ Volumes persist.

---

# Phase 3 — Backend Bootstrap

Goal

Create FastAPI application.

Implement:

Application startup

Configuration

Dependency Injection

Logging

Health endpoints

Swagger

ReDoc

---

Routes

```
/health

/live

/ready
```

---

Acceptance Criteria

Backend starts.

Swagger available.

Health endpoints operational.

---

# Phase 4 — Database

Goal

Configure PostgreSQL.

Install:

SQLAlchemy

Alembic

Create:

Base Model

Session Factory

Migration configuration

Connection pooling

---

Acceptance Criteria

Database connects.

Migration executes.

Tables created.

---

# Phase 5 — Authentication Foundation

Goal

Implement authentication.

Features

JWT

Refresh Tokens

Password Hashing

Roles

Permissions

Demo Mode

---

Demo Accounts

Patient

Doctor

Administrator

Demo mode should be switchable using:

```
DEMO_MODE=true
```

---

Acceptance Criteria

Demo login works.

JWT login works.

Protected routes function.

Role authorization functions.

---

# Phase 6 — Core Database Models

Implement every SQLAlchemy model.

Minimum

Users

Patients

Doctors

Facilities

Medical Records

Visits

Diagnoses

Allergies

Medications

Consent Requests

Notifications

Audit Logs

AI Sessions

Refresh Tokens

---

Acceptance Criteria

Alembic migration succeeds.

Relationships valid.

No circular imports.

---

# Phase 7 — Repository Layer

Create repositories.

Each repository includes:

Create

Retrieve

Update

Delete (where appropriate)

Pagination

Filtering

Searching

Repositories contain no business logic.

---

Acceptance Criteria

Repositories tested.

No service accesses SQLAlchemy directly.

---

# Phase 8 — Service Layer

Implement:

PatientService

DoctorService

ConsentService

TimelineService

RecordService

NotificationService

AuditService

AuthenticationService

ConsultationService

AISessionService

---

Acceptance Criteria

Business logic isolated.

Dependency Injection used.

Repositories injected.

No direct database access from routes.

# Phase 9 — REST API

## Goal

Implement the complete REST API described in the Technical Architecture document.

Modules:

Authentication

Patients

Doctors

Medical Records

Timeline

Visits

Consent

Notifications

AI Sessions

Audit Logs

Settings

---

Every endpoint should include:

Request validation

Response DTOs

Permission validation

Structured errors

OpenAPI documentation

Pagination where appropriate

Filtering

Sorting

---

Acceptance Criteria

✓ Swagger fully documents every endpoint.

✓ Endpoints return standardized responses.

✓ Error handling is consistent.

✓ Authorization enforced server-side.

---

# Phase 10 — WebSocket Infrastructure

## Goal

Implement real-time communication.

WebSocket endpoint:

```
/ws
```

Events:

Consent Requested

Consent Approved

Consent Denied

Timeline Updated

Notification Created

Consultation Started

Consultation Completed

AI Response Ready

Dashboard Updated

---

Requirements

JWT Authentication

Automatic reconnect

Heartbeat

Graceful disconnect

Subscription model

---

Acceptance Criteria

Real-time updates function.

Browser refresh reconnects correctly.

No duplicate subscriptions.

---

# Phase 11 — Provider Interfaces

## Goal

Implement abstraction layers for every external dependency.

Interfaces:

SymptomCheckerProvider

DiagnosisProvider

ClinicalSummaryProvider

TranscriptionProvider

NotificationProvider

StorageProvider

EmailProvider

---

Initially implement mock providers for all services.

The existing symptom checker should be wrapped behind the SymptomCheckerProvider interface rather than called directly.

Acceptance Criteria

✓ Business logic depends only on interfaces.

✓ Swapping providers requires configuration only.

---

# Phase 12 — Seed Data

Generate realistic demonstration data.

Minimum:

10 Patients

5 Doctors

3 Facilities

50 Historical Visits

20 Consent Requests

100 Notifications

20 AI Sessions

100 Clinical Notes

Medication History

Allergies

Chronic Conditions

Lab Results

---

Data should appear realistic.

Avoid placeholder values such as:

John Doe

Test Patient

Lorem Ipsum

Use geographically and culturally appropriate mock data for the intended demonstration region where possible.

---

Acceptance Criteria

Application appears populated immediately after setup.

---

# Phase 13 — Patient Application

Implement every patient screen.

Required screens:

Authentication

Dashboard

Timeline

Visit Details

Medical Record

Notifications

Consent Requests

Consent History

Profile

Settings

Medical ID

AI Symptom Assessment

Access History

About

---

Every screen includes:

Loading State

Error State

Empty State

Success Feedback

Transitions

---

Acceptance Criteria

Entire patient journey functions.

---

# Phase 14 — Doctor Portal

Implement:

Dashboard

Patient Search

Patient Overview

Timeline

Visit Details

AI Consultation

Differential Diagnosis

Clinical Summary

Notifications

Access History

Settings

---

Acceptance Criteria

Complete consultation workflow operational.

---

# Phase 15 — Mobile Simulation

Implement PhoneFrame.

Features:

Fixed viewport

Status bar

Safe areas

Notch

Glass bezel

Rounded display

Bottom navigation

Responsive scaling

Motion

No browser scrollbars inside the simulated device.

---

Acceptance Criteria

Patient application visually resembles a native mobile application.

---

# Phase 16 — Split-Screen Demonstration

Create dedicated demonstration mode.

Layout:

```
---------------------------------------------------------

Patient Phone

Doctor Portal

---------------------------------------------------------
```

Synchronization:

Doctor requests consent.

↓

Patient notification appears.

↓

Patient approves.

↓

Doctor portal unlocks.

↓

Consultation proceeds.

↓

Patient timeline updates.

---

Acceptance Criteria

Entire demonstration completes without refreshing either side.

---

# Phase 17 — AI Consultation

Integrate provider interfaces.

Workflow:

Patient assessment.

↓

Doctor consultation.

↓

Differential diagnosis.

↓

Clinical summary.

↓

Doctor edits.

↓

Confirmation.

---

Streaming responses preferred.

Fallback to standard responses if unsupported.

---

Acceptance Criteria

Entire AI workflow functions through provider abstractions.

---

# Phase 18 — Audit Logging

Every important action should create an immutable audit record.

Events include:

Authentication

Consent

Medical Record Access

Medical Record Updates

AI Sessions

Notifications

Settings Changes

---

Acceptance Criteria

Audit trail visible and complete.

---

# Phase 19 — Notification System

Implement:

In-app notifications

Unread count

Toast notifications

Real-time delivery

Notification history

Mark read

Delete

---

Acceptance Criteria

Notifications synchronize across browser tabs and active sessions.

---

# Phase 20 — Authentication Completion

Finalize authentication.

Verify:

Demo Mode

JWT Mode

Refresh Tokens

Logout

Permission Guards

Route Protection

Session Recovery

---

Acceptance Criteria

Application can switch between Demo Mode and Production Mode via configuration only.

---

# Phase 21 — Testing

Backend:

Pytest

Repository tests

Service tests

API tests

Authentication tests

---

Frontend:

Vitest

React Testing Library

Critical user flow tests

---

Integration:

Consent workflow

Timeline updates

Notifications

Authentication

AI provider mocks

---

Acceptance Criteria

Critical workflows covered by automated tests.

---

# Phase 22 — Documentation

Complete project documentation.

Required documents:

README

Architecture

Design System

API Guide

Environment Variables

Docker Setup

Development Guide

Testing Guide

Deployment Guide

Provider Integration Guide

---

README should allow a new developer to start the project within minutes.

---

# Phase 23 — Performance & Polish

Review the application for:

Animation consistency

Loading states

Accessibility

Responsive layouts

Keyboard navigation

Error handling

Empty states

Performance bottlenecks

Remove dead code.

Standardize naming.

Review component reuse.

---

Acceptance Criteria

Application feels production quality.

---

# Phase 24 — Final Demonstration

Execute the complete demonstration.

Scenario:

1. Launch Docker Compose.
2. Open split-screen mode.
3. Login as Demo Patient.
4. Login as Demo Doctor.
5. Doctor searches patient.
6. Doctor requests consent.
7. Patient receives notification.
8. Patient approves.
9. Doctor reviews medical history.
10. AI consultation begins.
11. Differential diagnosis generated.
12. Clinical summary generated.
13. Doctor edits notes.
14. Doctor confirms consultation.
15. Patient immediately receives updated timeline and notification.
16. Audit logs confirm every critical action.

The entire demonstration should complete without manual database edits, page refreshes, or developer intervention.

---

# Definition of Project Completion

Mirage is considered complete when:

- All Product Requirements are implemented.
- Technical Architecture is faithfully followed.
- Design System is consistently applied.
- Every implementation phase passes its acceptance criteria.
- The project starts with a single `docker compose up`.
- Demo Mode and JWT Mode are both fully operational.
- AI integrations are abstracted behind provider interfaces.
- Split-screen mode demonstrates the complete patient–doctor workflow.
- The repository is well documented, tested, and ready for future extension.

---

# End of Implementation Plan