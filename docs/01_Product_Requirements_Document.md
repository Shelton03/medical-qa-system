# Mirage
# Product Requirements Document (PRD)

**Version:** 1.0

**Project Name:** Mirage

**Project Type:**
AI-Assisted National Patient Record Platform

**Technology Stack**
- Frontend: Next.js
- Backend: FastAPI (Python)
- Database: PostgreSQL
- Cache: Redis
- Deployment: Docker Compose
- Authentication: JWT + Demo Authentication Mode
- AI Layer: Provider Abstraction Interfaces
- Real-time Communication: WebSockets

---

# 1. Executive Summary

Mirage is an AI-assisted digital health platform designed to modernize patient record management by placing ownership and control of medical records in the hands of patients while enabling verified healthcare practitioners to securely request, access, and update those records with explicit patient consent.

Unlike traditional Electronic Health Record (EHR) systems that are fragmented across healthcare providers, Mirage creates a longitudinal patient record that follows the patient instead of remaining locked inside individual institutions.

The system combines:

- National patient records
- Practitioner verification
- Consent-based access
- AI-assisted symptom assessment
- AI-assisted clinical documentation
- Structured consultation workflows
- Real-time patient notifications
- Comprehensive audit logging

The Healthathon demonstration focuses on a narrow but complete clinical workflow rather than attempting to build an entire national healthcare system.

The MVP demonstrates how patient-controlled records, artificial intelligence, and secure access controls can improve continuity of care without replacing clinical decision making.

---

# 2. Problem Statement

Healthcare information in Zimbabwe remains fragmented across hospitals, clinics, and private practices.

Patients frequently carry paper records between facilities.

Medical histories are often incomplete.

Laboratory results may be unavailable during consultations.

Medication histories can be difficult to retrieve.

Previous diagnoses are frequently inaccessible.

When providers cannot access historical information they often:

- repeat laboratory tests
- repeat imaging
- prescribe medications without complete allergy information
- spend consultation time reconstructing medical history
- lose continuity of care

These issues contribute to increased healthcare costs, longer waiting times, poorer patient experiences, and greater clinical risk.

Mirage addresses these problems by creating a secure, consent-driven national patient record that follows the patient regardless of where care is delivered.

---

# 3. Vision

Create a future where every patient owns a lifelong medical record that is instantly accessible—with consent—to any verified healthcare professional, regardless of institution.

The platform should improve:

- patient safety
- continuity of care
- healthcare efficiency
- clinical documentation
- public health reporting
- patient trust

while ensuring clinicians remain responsible for all final medical decisions.

Artificial Intelligence assists clinicians.

It never replaces them.

---

# 4. Product Goals

The MVP has six primary goals.

## Goal 1

Demonstrate patient-controlled medical records.

Patients—not hospitals—control who accesses their health information.

---

## Goal 2

Demonstrate secure practitioner verification.

Only registered clinicians may request access to patient records.

---

## Goal 3

Demonstrate explicit patient consent.

Every access request requires patient approval unless future emergency access rules are introduced.

---

## Goal 4

Demonstrate AI-assisted clinical workflows.

Artificial Intelligence should:

- ask structured questions
- summarize conversations
- draft consultation notes
- generate ranked differential diagnoses

The clinician remains responsible for every diagnosis and every record update.

---

## Goal 5

Demonstrate longitudinal health records.

Medical history should appear as one continuous timeline regardless of where treatment occurred.

---

## Goal 6

Demonstrate a realistic production-ready architecture.

Although the Healthathon focuses on an MVP, the architecture should be scalable enough to evolve into a national platform without requiring fundamental redesign.

---

# 5. Non-Goals

The MVP intentionally excludes:

- Appointment scheduling
- Billing
- Insurance claims
- Pharmacy inventory
- Laboratory management
- Radiology PACS
- Hospital administration
- Emergency override workflows
- National identity management
- Offline synchronization
- Multi-language support
- Wearable integrations

These features may be introduced in future phases.

---

# 6. Product Philosophy

The system should embody five principles.

## 6.1 Patient Ownership

Patients own their records.

Healthcare providers become trusted contributors rather than record owners.

---

## 6.2 Consent First

Every access request should be transparent.

Patients always know:

- who requested access
- why
- when
- from which facility

---

## 6.3 AI Assists

Artificial Intelligence never writes directly into permanent records.

Every AI-generated output requires clinician review.

Nothing reaches the medical record without practitioner approval.

---

## 6.4 Modular Architecture

Every major subsystem must be replaceable.

Examples include:

- authentication provider
- symptom checker
- transcription engine
- diagnosis engine
- summarization engine
- notification provider

The application should depend on interfaces rather than implementations.

---

## 6.5 Transparency

Every action should be logged.

Patients should always be able to review:

- who viewed their records
- who requested access
- when records changed
- which clinician approved updates

---

# 7. Target Users

The MVP supports four user types.

## Patient

Primary owner of medical information.

Responsibilities include:

- reviewing records
- approving access requests
- completing AI symptom assessments
- reviewing access history
- managing profile information

---

## Doctor

Licensed medical practitioner.

Responsibilities include:

- searching for patients
- requesting record access
- reviewing records
- conducting consultations
- interacting with AI assistance
- approving documentation
- updating patient records

---

## System Administrator

Administrative role used only for development and testing.

Can:

- manage facilities
- manage practitioner registry
- monitor system health

This role is not part of the demonstration flow.

---

## AI Providers

The AI layer is treated as an external service.

Providers are interchangeable.

Examples include:

- Existing Symptom Checker
- OpenAI
- Azure OpenAI
- Ollama
- Anthropic
- Future custom models

The backend communicates with provider interfaces only.

---

# 8. User Stories

## Patient

As a patient,

I want to approve requests for my records,

so that I remain in control of my health information.

---

As a patient,

I want my complete history available regardless of hospital,

so I never have to remember every diagnosis myself.

---

As a patient,

I want allergies displayed prominently,

so clinicians immediately see critical safety information.

---

As a patient,

I want to complete an AI symptom assessment before my visit,

so my consultation begins with relevant clinical context.

---

## Doctor

As a doctor,

I want to search for patients quickly,

so consultations begin without unnecessary delay.

---

As a doctor,

I want immediate access after consent,

so I don't waste consultation time.

---

As a doctor,

I want AI assistance during consultations,

so documentation takes less time.

---

As a doctor,

I want to review every AI suggestion before saving,

so I remain responsible for clinical decisions.

---

# 9. Success Metrics

The MVP will be considered successful if judges can complete the following demonstration without assistance:

✓ Doctor logs in.

✓ Doctor searches patient.

✓ Patient found.

✓ Doctor requests access.

✓ Patient immediately receives request.

✓ Patient approves.

✓ Doctor gains access.

✓ Doctor reviews patient history.

✓ AI assists consultation.

✓ AI produces structured differential diagnosis.

✓ Doctor confirms diagnosis.

✓ Consultation note generated.

✓ Doctor approves note.

✓ Record updated.

✓ Patient immediately sees updated record.

This complete workflow should require less than five minutes during demonstration.

---

# 10. Design Principles

The system should feel:

- modern
- trustworthy
- lightweight
- responsive
- clinically safe
- patient-centered

The patient experience should resemble a premium mobile application.

The clinician experience should resemble a professional clinical dashboard optimized for speed and clarity.

Both interfaces should feel like two views into the same real-time healthcare platform rather than separate applications.

---

# 11. High-Level Functional Scope

The MVP consists of two applications sharing one backend.

## Patient Application

Built in Next.js but rendered inside a simulated mobile device frame.

Features:

- Login
- Home Dashboard
- Medical Record
- AI Symptom Check
- Consent Requests
- Notifications
- Access Log
- Health Timeline
- Medical ID
- Profile

---

## Doctor Portal

Desktop-oriented responsive web application.

Features:

- Login
- Dashboard
- Patient Search
- Consent Requests
- Patient Record
- AI Consultation
- Diagnosis Review
- Clinical Notes
- Record Update
- Access History

# 12. Functional Requirements

The following functional requirements define the complete MVP that will be implemented for the Healthathon demonstration.

---

# FR-1 Authentication

## Objectives

Provide both rapid demonstration access and production-ready authentication.

### Functional Requirements

The system shall support two authentication modes.

### Demo Mode

Designed for rapid demonstrations and development.

Users can enter the application with one click.

Available demo accounts include:

- Demo Patient
- Demo Doctor
- Demo Administrator

No passwords are required.

No JWT validation occurs.

Demo Mode is enabled through configuration.

```env
DEMO_MODE=true
```

---

### Production Mode

Production mode enables:

- JWT Authentication
- Refresh Tokens
- Password Hashing
- Secure Sessions
- Role-Based Authorization

Users authenticate using email and password.

JWT expiration should be configurable.

Refresh tokens should be securely stored.

Authentication providers must remain replaceable.

---

# FR-2 Patient Management

The system shall maintain a longitudinal patient profile.

Each patient contains:

- Unique Medical Record Number
- National ID
- Name
- Date of Birth
- Gender
- Blood Group
- Emergency Contact
- Contact Details
- Allergies
- Chronic Conditions
- Medical Timeline
- Previous Consultations
- Current Medications

Patients cannot directly modify clinical records.

Patients may update:

- phone number
- address
- emergency contacts

---

# FR-3 Practitioner Registry

The system shall maintain a verified practitioner registry.

Each practitioner contains:

- Name
- Registration Number
- Facility
- Role
- Speciality
- Verification Status

Only verified practitioners may request patient records.

Inactive practitioners cannot log in.

---

# FR-4 Consent Management

Consent is the foundation of Mirage.

No patient records are released without patient approval.

Exception handling for emergency override is intentionally excluded from the MVP.

Each consent request includes:

Requester

Facility

Registration Number

Reason

Scope

Expiry Time

Timestamp

Status

Possible statuses:

Pending

Approved

Denied

Expired

Cancelled

---

Patient approval immediately unlocks records.

Patient denial immediately closes the request.

Expired requests automatically revoke access.

---

# FR-5 Access Control

Access permissions are temporary.

Doctors do not permanently gain access.

Permission expires after the consultation.

Every permission must include:

Patient

Doctor

Facility

Time Granted

Expiry

Reason

Approval Source

---

# FR-6 Medical Record Management

Medical records form one continuous timeline.

Each visit contains:

Visit Date

Facility

Doctor

Diagnosis

Symptoms

Vitals

Prescriptions

Notes

Investigations

Attachments

AI Summary

Every update generates an immutable audit log.

No records are deleted.

Corrections generate new versions.

---

# FR-7 Allergy Management

Allergy information is treated as critical safety information.

Allergy warnings appear:

Patient Home

Patient Record

Doctor Record

AI Diagnosis

Clinical Notes

Prescription Screen

Critical allergies must never scroll off-screen.

Pinned warnings remain visible.

---

# FR-8 Patient Timeline

The patient timeline presents the complete health history chronologically.

Timeline entries include:

Admissions

Outpatient Visits

Diagnoses

Vaccinations

Lab Results

Procedures

Medications

Notes

AI Assessments

Each entry opens detailed information.

Timeline is read-only for patients.

---

# FR-9 AI Symptom Assessment

The AI Symptom Assessment exists as an independent provider.

The application never depends on a specific implementation.

Instead it communicates through:

SymptomAssessmentProvider

Responsibilities:

Start Session

Load Patient Context

Submit Patient Response

Receive Next Question

End Assessment

Store Conversation

The provider implementation may change without affecting application code.

Examples:

Current QA System

OpenAI

Azure

Anthropic

Local LLM

---

The AI receives:

Known allergies

Previous diagnoses

Age

Gender

Medical history

Current medications

The provider returns:

Question

Clinical reasoning metadata

Conversation state

Completion status

---

# FR-10 AI Diagnostic Assistant

The doctor portal includes AI assistance.

Responsibilities include:

Generate differential diagnosis

Suggest additional questions

Recommend investigations

Highlight risks

Reference previous history

Display confidence estimates

AI outputs are suggestions only.

Doctors remain responsible for:

Diagnosis

Treatment

Documentation

Approval

---

# FR-11 AI Clinical Summary

The consultation summary provider creates structured documentation.

Input:

Conversation

Patient history

Symptoms

Doctor observations

Output:

Chief Complaint

History of Present Illness

Clinical Findings

Assessment

Plan

Recommendations

Doctors may edit every field.

Nothing is automatically committed.

---

# FR-12 AI Transcription

Consultations may optionally be transcribed.

The transcription provider remains abstract.

Possible providers include:

Whisper

Azure Speech

Deepgram

AssemblyAI

Future Provider

The backend communicates only through:

TranscriptionProvider

---

# FR-13 Notifications

Notifications appear in real time.

Patient notifications include:

Consent Requests

Record Updated

Access Granted

Access Expired

Doctor notifications include:

Consent Approved

Consent Denied

Patient Updated

AI Complete

Notifications should use WebSockets.

Fallback polling should exist.

---

# FR-14 Search

Doctors can search patients using:

Medical Record Number

National ID

Full Name

Partial Name

Search should tolerate spelling errors.

Results appear instantly.

---

# FR-15 Audit Logging

Every important action generates an audit entry.

Examples include:

Login

Logout

Consent Requested

Consent Approved

Consent Denied

Record Viewed

Record Updated

AI Started

AI Completed

Diagnosis Confirmed

Audit logs are immutable.

---

# 13. Patient Journey

The patient application is designed as a simulated mobile application running inside the browser.

The experience should feel indistinguishable from a native application.

---

## Step 1

Patient launches Mirage.

If Demo Mode is enabled,

the patient can enter immediately.

Otherwise authentication occurs.

---

## Step 2

Patient lands on Home Dashboard.

Dashboard contains:

Greeting

Profile Summary

Medical Record Summary

Upcoming Notifications

Quick Actions

Recent Visit

Critical Allergy Banner

Medical ID Shortcut

---

## Step 3

Patient views complete medical history.

History is presented chronologically.

Each visit expands.

Patient may view:

Diagnosis

Facility

Doctor

Prescriptions

Notes

Attachments

---

## Step 4

Patient receives doctor access request.

A notification appears instantly.

The request clearly displays:

Doctor

Facility

Registration Number

Purpose

Requested Scope

Expiration

Patient selects:

Approve

or

Deny

---

## Step 5

Doctor immediately receives response.

If approved,

the patient sees:

Access Active

Doctor Name

Expiration Time

---

## Step 6

Patient completes AI symptom assessment.

The conversation resembles a modern messaging application.

The AI should:

Reference previous history

Avoid asking redundant questions

Remember previous answers

Guide the conversation naturally

---

## Step 7

Assessment completes.

Patient receives confirmation.

Conversation becomes available to the doctor.

---

## Step 8

Following consultation,

the patient immediately sees:

Updated diagnosis

New consultation

Updated medications

New notes

Latest recommendations

Recent activity

The updated visit appears at the top of the timeline.

---

# 14. Patient Screens

The MVP includes the following screens.

Authentication

Home Dashboard

Medical Timeline

Visit Details

Consent Request

Consent History

Notifications

AI Symptom Assessment

Medical ID

Profile

Settings

Access Log

Emergency Information

About Mirage

Each screen must support:

Loading State

Empty State

Error State

Offline Placeholder

Animated Transitions

Responsive Layout

Accessibility

# 15. Doctor Journey

The Doctor Portal is designed to provide healthcare practitioners with a fast, intuitive, and clinically safe workflow. Unlike the patient application, which prioritizes transparency and patient ownership, the doctor portal prioritizes efficiency, clarity, and rapid decision support while ensuring that every clinical action remains under physician control.

The complete demonstration should resemble a realistic consultation from beginning to end.

---

## Step 1 — Doctor Authentication

The doctor accesses the Mirage Doctor Portal.

If Demo Mode is enabled:

- One-click login as Demo Doctor.

If Production Mode is enabled:

- Email
- Password
- JWT Authentication
- Role Validation

Successful authentication loads:

- Today's Dashboard
- Patient Queue
- Recent Activity
- Notifications

---

## Step 2 — Dashboard

The Doctor Dashboard acts as the landing page.

Displayed information includes:

### Today's Queue

Patients currently waiting.

Each card displays:

- Patient Name
- Appointment Time
- Consultation Status

---

### Recent Patients

Recently accessed patients.

Allows clinicians to resume interrupted consultations.

---

### Pending Consent Requests

Displays requests awaiting patient approval.

Status examples:

Pending

Approved

Denied

Expired

---

### Notifications

Examples:

Patient approved request

AI assessment completed

Record updated

System announcements

---

### Quick Actions

Search Patient

New Consultation

Review AI Sessions

View Recent Records

---

## Step 3 — Search Patient

The clinician searches using:

Medical Record Number

National ID

Full Name

Partial Name

Autocomplete should begin after two characters.

Search results display:

Patient Name

Date of Birth

Medical Record Number

Blood Group

Verification Status

Current Consent Status

The clinician can immediately determine whether:

Patient exists

Consent exists

Access is active

---

## Step 4 — Request Record Access

If access is unavailable:

Doctor presses

Request Record Access

Immediately:

Backend validates practitioner.

Consent request created.

Notification pushed to patient.

Doctor sees:

Waiting for patient approval...

The interface remains responsive.

No manual refresh required.

---

## Step 5 — Patient Approval

Once approval occurs:

Dashboard updates instantly.

Patient record unlocks.

Visual confirmation displayed.

Doctor proceeds directly into consultation.

---

## Step 6 — Review Patient Record

The clinician first sees a concise summary.

Pinned information:

Critical Allergies

Active Conditions

Current Medication

Recent Visits

Previous Diagnoses

Medical Timeline

Nothing important should require scrolling before consultation begins.

---

## Step 7 — Begin AI Consultation

The clinician launches the AI assistant.

The assistant already knows:

Patient demographics

Medical history

Known allergies

Current medications

Past diagnoses

Recent symptom assessment

The doctor does not manually load context.

---

## Step 8 — AI Conversation

The AI guides the consultation.

The clinician remains in control.

The AI may:

Ask targeted questions.

Highlight missing information.

Reference previous illnesses.

Suggest investigations.

Raise safety alerts.

The doctor may:

Accept

Ignore

Skip

Modify

Any recommendation.

---

## Step 9 — Differential Diagnosis

Following sufficient questioning,

the AI generates:

Ranked differential diagnoses.

Each includes:

Probability

Reasoning Summary

Supporting Evidence

Contradictory Evidence

Suggested Investigations

Potential Risks

Medication Warnings

Doctors may expand each diagnosis.

No diagnosis is automatically accepted.

---

## Step 10 — Clinical Documentation

The AI generates a structured consultation note.

Sections include:

Chief Complaint

History of Present Illness

Review of Systems

Assessment

Differential

Plan

Prescriptions

Follow-up

Doctors may edit any field.

---

## Step 11 — Record Confirmation

Nothing is written until confirmation.

Confirmation screen displays:

Original Patient Record

Proposed Changes

Diagnosis

Medications

Clinical Notes

AI Summary

Doctor presses:

Confirm & Update Record

Backend:

Creates new record version.

Updates patient timeline.

Creates audit log.

Notifies patient.

---

## Step 12 — Consultation Complete

Doctor returns to dashboard.

Patient immediately receives:

Updated timeline

New consultation

Medication

Recommendations

Notification

---

# 16. Doctor Portal Screens

The Doctor Portal includes the following pages.

---

## Authentication

Purpose:

Authenticate practitioners.

Functions:

Login

Forgot Password (future)

Demo Login

Session Management

---

## Dashboard

Purpose:

Daily overview.

Widgets:

Today's Queue

Recent Patients

Notifications

Pending Requests

Quick Actions

System Status

---

## Patient Search

Purpose:

Locate patient records.

Capabilities:

Search

Filters

Sorting

Recent Searches

Suggestions

---

## Consent Waiting Screen

Purpose:

Display pending approval.

Shows:

Patient Name

Elapsed Time

Status

Cancel Request

Retry Notification

---

## Patient Overview

Purpose:

Clinical summary before consultation.

Sections:

Demographics

Allergies

Conditions

Medication

Timeline

Recent Notes

---

## Medical Timeline

Purpose:

Chronological history.

Each entry expands.

Supports:

Diagnosis

Medication

Attachments

Notes

Lab Results

---

## Visit Details

Purpose:

Review historical encounters.

Contains:

Facility

Doctor

Diagnosis

Investigations

Treatment

Prescriptions

Notes

---

## AI Consultation

Purpose:

Interactive consultation.

Contains:

Conversation

Suggested Questions

Clinical Context

Current Assessment

History Panel

---

## Differential Review

Purpose:

Present AI recommendations.

Displays:

Diagnosis Ranking

Confidence

Evidence

Risks

Next Steps

Clinician Notes

---

## Documentation Review

Purpose:

Approve generated documentation.

Editable fields:

SOAP Note

Assessment

Plan

Diagnosis

Medication

Instructions

---

## Confirmation

Purpose:

Final review.

Actions:

Confirm

Cancel

Return to Edit

---

## Access History

Purpose:

Review previous patient access.

Shows:

Patient

Facility

Time

Purpose

Duration

Outcome

---

## Notifications

Purpose:

Review alerts.

Categories:

Consent

Patient Updates

AI Events

System

---

## Settings

Purpose:

Personal preferences.

Contains:

Profile

Notification Preferences

Theme

Accessibility

Security

---

# 17. Real-Time Consent Workflow

Mirage demonstrates patient-controlled healthcare through a real-time consent workflow.

This interaction is the centrepiece of the demonstration.

---

Doctor searches patient.

↓

Patient located.

↓

Doctor requests access.

↓

Backend validates practitioner.

↓

Consent request created.

↓

WebSocket event emitted.

↓

Patient immediately receives notification.

↓

Patient reviews request.

↓

Approve or Deny.

↓

Backend records decision.

↓

Access token generated.

↓

Doctor interface unlocks instantly.

↓

Consultation begins.

↓

Consultation ends.

↓

Access expires automatically.

↓

Audit log written.

↓

Patient Access History updated.

---

# 18. AI Workflow

Artificial Intelligence exists as a supporting clinical tool.

It never makes autonomous clinical decisions.

The workflow is:

Patient completes symptom assessment.

↓

Assessment stored.

↓

Doctor requests consultation.

↓

Patient context loaded.

↓

AI receives:

History

Medications

Allergies

Previous diagnoses

Symptoms

↓

AI asks structured questions.

↓

Doctor enters responses.

↓

AI produces:

Differential diagnosis

Clinical summary

Suggested investigations

Suggested documentation

↓

Doctor reviews.

↓

Doctor edits.

↓

Doctor approves.

↓

Backend updates medical record.

---

# AI Provider Architecture

The backend must never directly call vendor APIs.

Instead, it communicates through provider interfaces.

Required interfaces include:

SymptomAssessmentProvider

DiagnosisProvider

TranscriptionProvider

ClinicalSummaryProvider

NotificationProvider

Future providers should be replaceable without changing application code.

Dependency Injection should be used throughout the backend.

---

# 19. Notification Workflow

Notifications should be event-driven.

Events include:

Consent Requested

Consent Approved

Consent Denied

Consultation Started

Consultation Completed

Record Updated

Medication Added

Diagnosis Added

Access Expired

System Message

Patients receive only notifications relevant to them.

Doctors receive only notifications relevant to their consultations.

Notifications should synchronize across multiple browser sessions.

Unread counts update in real time.

# 20. Non-Functional Requirements

The Mirage platform must be designed as though it will eventually support a national healthcare system, even though the MVP targets a Healthathon demonstration.

The architecture should prioritize maintainability, scalability, modularity, security, and developer experience.

---

## Performance

The application should feel responsive throughout the demonstration.

Target performance:

- Initial application load: < 3 seconds
- Dashboard navigation: < 500ms
- Patient search: < 300ms
- Consent notification delivery: < 2 seconds
- AI provider response indicator: immediate loading feedback
- Record updates visible to the patient: < 2 seconds after doctor confirmation

Perceived responsiveness is more important than raw speed.

Skeleton loaders, optimistic UI, and progressive rendering should be used where appropriate.

---

## Reliability

The system should degrade gracefully.

Examples:

- AI unavailable
- WebSocket disconnected
- Database temporarily unavailable
- Notification delivery delayed

Core clinical workflows should never crash because an AI provider fails.

Provider failures should surface as recoverable application errors.

---

## Scalability

Although the MVP is single-instance, the architecture should support future scaling.

Backend services should be stateless wherever possible.

Future scaling targets include:

- Multiple FastAPI instances
- Separate worker processes
- Distributed AI providers
- Horizontal database read replicas
- Object storage for attachments

---

## Maintainability

The project should prioritize readability over cleverness.

Requirements:

- Clear module boundaries
- Dependency Injection
- Service interfaces
- Repository pattern
- Comprehensive documentation
- Type hints throughout backend
- Strict TypeScript on frontend

Business logic should never live inside UI components.

---

# 21. Accessibility Requirements

Healthcare software must be usable by as many people as possible.

Minimum accessibility goals include:

- Keyboard navigation
- Visible focus indicators
- Screen reader labels
- Color contrast compliance
- Responsive text sizing
- Semantic HTML
- Reduced motion support
- Touch-friendly controls

Animations should never block interaction.

---

# 22. Security & Privacy

Although the MVP uses mock data, the architecture should reflect healthcare-grade security practices.

## Authentication

Support:

- JWT Authentication
- Refresh Tokens
- Secure Password Hashing
- Role-Based Authorization

---

## Authorization

Permissions should be enforced server-side.

Frontend permissions are for user experience only.

The backend is the source of truth.

---

## Data Privacy

Patients own their medical records.

Medical records must never be exposed without authorization.

Every access event should be recorded.

---

## Auditability

The following actions must always generate audit entries:

- Login
- Logout
- Record Viewed
- Record Updated
- Consent Requested
- Consent Approved
- Consent Denied
- Diagnosis Confirmed
- AI Consultation Started
- AI Consultation Completed

Audit logs should be immutable.

---

## Secrets

Secrets should never be committed.

Configuration should use:

- Environment variables
- Docker secrets (future)
- Configuration providers

---

# 23. Error Handling

The application should fail gracefully.

Every feature should define:

Loading State

Empty State

Error State

Retry State

Recovery State

Example:

Patient search fails.

↓

Display error.

↓

Allow retry.

↓

Preserve entered search.

Never discard user work.

---

# 24. Acceptance Criteria

The MVP is complete when the following workflow succeeds without manual intervention.

## Authentication

✓ Doctor logs in.

✓ Patient logs in.

---

## Patient Search

✓ Doctor finds patient.

✓ Patient profile displayed.

---

## Consent

✓ Doctor requests access.

✓ Patient immediately receives notification.

✓ Patient approves request.

✓ Doctor gains temporary access.

---

## Medical Record

✓ Doctor reviews longitudinal history.

✓ Allergy warning always visible.

✓ Previous visits displayed chronologically.

---

## AI Consultation

✓ Existing symptom assessment is available to the clinician.

✓ AI continues the consultation using historical context.

✓ Suggested differential generated.

✓ Suggested documentation generated.

---

## Clinical Approval

✓ Doctor edits diagnosis if necessary.

✓ Doctor confirms documentation.

✓ Record updated.

---

## Patient Synchronization

✓ Patient immediately sees updated consultation.

✓ Notification received.

✓ Timeline updated.

✓ Access history updated.

---

## Audit

✓ Record access logged.

✓ Record modification logged.

✓ Consent decision logged.

---

# 25. Edge Cases

The system should correctly handle common failure scenarios.

## Consent expires before approval

Doctor must request access again.

---

## Patient denies access

Doctor receives immediate notification.

Consultation cannot continue.

---

## Doctor closes browser

Consultation state should be recoverable.

---

## AI provider unavailable

Consultation continues manually.

Doctors can complete documentation without AI.

---

## Notification delivery fails

Polling fallback should synchronize pending events.

---

## Duplicate patient names

Search results should clearly distinguish patients using:

- Medical Record Number
- Date of Birth
- National ID

---

## Multiple simultaneous requests

Patients should see each request independently.

Doctors should not gain unintended access.

---

## Expired sessions

JWT should refresh automatically.

If refresh fails:

Return user to login.

---

# 26. Future Roadmap

The MVP intentionally limits scope.

Future phases may include:

## Phase 2

Emergency access workflows

Biometric authentication

Appointment scheduling

Facility administration

Laboratory integration

Radiology integration

Prescription management

Insurance verification

Offline synchronization

QR Code patient identification

---

## Phase 3

National interoperability

FHIR support

HL7 messaging

Government registry integration

Insurance APIs

Public health reporting

Disease surveillance

Analytics dashboards

Clinical quality metrics

---

## Phase 4

Predictive AI

Population health analytics

Clinical decision support

Medication interaction engine

Risk prediction

Remote monitoring

Wearable integration

Telemedicine

---

# 27. Technical Assumptions

The following assumptions guide implementation.

Frontend:

- Next.js
- TypeScript
- TailwindCSS
- Framer Motion

Backend:

- FastAPI
- Python
- SQLAlchemy
- Alembic
- PostgreSQL
- Redis

Infrastructure:

- Docker Compose
- Environment-based configuration

Communication:

- REST APIs
- WebSockets

Authentication:

- Demo Mode
- JWT Mode

AI:

Provider abstraction only.

Implementations remain replaceable.

---

# 28. Definition of Done

The Mirage MVP is complete when:

- Every patient wireframe has been implemented.
- Every doctor wireframe has been implemented.
- All core user journeys function correctly.
- Docker launches the complete stack with a single command.
- Demo Mode and JWT Mode both function.
- AI providers are abstracted behind interfaces.
- PostgreSQL stores all application data.
- Seed data creates a realistic demonstration environment.
- Real-time consent workflow functions end-to-end.
- Documentation is sufficient for another engineer to understand the system without external explanation.

---

# End of Product Requirements Document