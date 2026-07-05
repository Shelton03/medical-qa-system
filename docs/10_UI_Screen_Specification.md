# Mirage
# UI Screen Specification

Version: 2.0

---

# Purpose

This document defines every user interface within Mirage.

Unlike the Design System, which specifies visual language and reusable components, this document specifies the application's concrete screens exactly as they appear in the approved wireframes.

It is the implementation guide for the frontend.

---

# Primary Source of Truth

The canonical reference for every screen is:

docs/wireframes.html

The HTML wireframes represent the approved MVP design.

They define:

- Screen order
- Navigation
- Layout
- Information hierarchy
- Component placement
- User interaction flow
- Demo presentation

This document extends those wireframes by defining:

- React component hierarchy
- API dependencies
- Backend integration
- State management
- Real-time synchronization
- Loading states
- Empty states
- Error handling
- Accessibility requirements
- Acceptance criteria

If this document conflicts with the wireframes regarding visual layout, the wireframes take precedence.

---

# Relationship to Other Documentation

This document should be read after:

01_Product_Requirements_Document.md

02_Technical_Architecture.md

03_Design_System.md

05_API_Contract.md

06_Database_Schema.md

The responsibilities are divided as follows:

Product Requirements

Defines WHAT the product should accomplish.

Technical Architecture

Defines HOW the system is implemented.

Design System

Defines HOW components should look and behave.

Wireframes

Define WHERE everything appears.

This document

Defines HOW every screen should be implemented.

---

# Screen Fidelity Requirements

The generated application should closely match the supplied wireframes.

The coding assistant may improve:

✓ Typography

✓ Iconography

✓ Animation quality

✓ Spacing consistency

✓ Accessibility

✓ Responsiveness

✓ Component reuse

The coding assistant must NOT change:

✗ Screen order

✗ Navigation

✗ Information hierarchy

✗ User workflow

✗ Screen purpose

✗ Core interaction patterns

---

# Demo Layout

The primary demonstration environment consists of two synchronized applications.

Left Panel

Patient Application

Rendered inside the PhoneFrame component.

Right Panel

Doctor Portal

Desktop dashboard.

The applications should communicate exclusively through the backend using WebSockets.

The frontend should never directly synchronize state between the two panels.

---

# Patient Application

The patient application is a mobile-first web experience.

Every patient screen must render inside the PhoneFrame described in:

03_Design_System.md

The application should never detect browser width.

Instead, the PhoneFrame provides a fixed viewport that scales appropriately.

---

# Doctor Portal

The doctor portal is desktop-first.

Unlike the patient application, it should maximize information density.

The doctor portal should support:

• Multi-column layouts

• Keyboard navigation

• Large datasets

• Simultaneous patient context

---

# Navigation Model

Patient Navigation

The wireframes define the canonical navigation sequence.

Screens should appear in the exact order shown in:

docs/wireframes.html

Additional navigation should only exist where required for implementation.

---

Doctor Navigation

Primary navigation should remain persistent.

Recommended sections:

• Dashboard

• Patients

• Consultation

• Notifications

• Settings

Navigation should never interrupt an active consultation.

---

# Shared Component Library

Every screen should reuse components whenever possible.

Examples include:

PatientCard

MedicalRecordCard

ConsentCard

NotificationCard

TimelineEvent

DiagnosisCard

VitalSignsCard

PrescriptionCard

BottomNavigation

TopAppBar

SearchInput

PrimaryButton

SecondaryButton

StatusBadge

LoadingSkeleton

EmptyState

ErrorState

ConfirmationDialog

BottomSheet

These components should be implemented once and reused throughout the application.

---

# API Integration Principles

No React component should call the backend directly.

Communication should follow this pattern:

Screen

↓

Feature Hook

↓

Service Layer

↓

Typed API Client

↓

FastAPI Backend

↓

Repository

↓

Database

All API requests should use React Query.

---

# Real-Time Updates

Real-time communication should occur exclusively through WebSockets.

The UI should subscribe to events rather than poll for updates.

Expected events include:

Consent Requested

Consent Approved

Consent Denied

Consultation Started

Consultation Completed

Timeline Updated

Medical Record Updated

Notification Created

Notification Read

---

# Standard Screen Template

Every screen described in this document follows the same specification.

Each screen includes:

1. Purpose

2. Wireframe Reference

3. Layout

4. Component Hierarchy

5. API Dependencies

6. WebSocket Events

7. User Actions

8. Loading Behaviour

9. Empty State

10. Error State

11. Accessibility

12. Acceptance Criteria

Every implementation should satisfy every acceptance criterion before the screen is considered complete.

---

# Screen Numbering

Screens are documented in the exact order presented by the wireframes.

Patient Application

P1

P2

P3

...

Doctor Portal

D1

D2

D3

...

This numbering should be preserved throughout implementation, testing, and future documentation.

---

# Implementation Philosophy

The frontend should be viewed as an implementation of the approved wireframes rather than a reinterpretation of them.

Where implementation decisions are required, choose the option that best preserves the intent of the supplied prototype while maintaining consistency with the project's architecture and design system.

# End of Part 1
# Patient Application

The patient application is the mobile-facing experience of Mirage.

All patient screens must:

- Render inside the PhoneFrame component.
- Follow the layouts defined in `docs/wireframes.html`.
- Reuse components from the Design System.
- Consume backend data exclusively through the typed API layer.
- Synchronize with the backend through WebSockets where applicable.

---

# P1 — Home Dashboard

## Wireframe Reference

Source:

docs/wireframes.html

Screen:

Patient Application → Home Dashboard

This is the default landing page after authentication.

---

## Purpose

The Home Dashboard gives patients immediate visibility into:

- Current health status
- Recent consultations
- Outstanding actions
- Quick access to core features

This screen should minimize cognitive load while surfacing the most important information first.

---

## Layout

The implementation should preserve the visual hierarchy defined in the wireframe.

Top to bottom:

1. Greeting & Profile Summary
2. Health Summary Card
3. Quick Actions
4. Recent Consultation Card
5. Active Consent Requests (if any)
6. Recent Notifications Preview
7. Bottom Navigation

The order should not change.

---

## Component Hierarchy

```
PatientHomeScreen

├── AppHeader
│   ├── Greeting
│   ├── ProfileAvatar
│   └── NotificationButton
│
├── HealthSummaryCard
│
├── QuickActionsGrid
│   ├── AI Symptom Check
│   ├── My Health Record
│   ├── Notifications
│   └── Profile
│
├── RecentVisitCard
│
├── ActiveConsentCard
│
├── NotificationPreviewList
│
└── BottomNavigation
```

Every section should be independently reusable.

---

## API Dependencies

GET /patients/me

GET /patients/me/summary

GET /consultations/recent

GET /consent/active

GET /notifications

---

## WebSocket Events

Subscribe:

NotificationCreated

ConsentRequested

ConsultationCompleted

MedicalRecordUpdated

TimelineUpdated

These events should update only the affected widgets.

The entire page should not reload.

---

## User Actions

Available interactions include:

- Open AI Symptom Checker
- View Health Record
- Open Consultation History
- Review Consent Request
- Open Notifications
- Navigate to Profile

Every card should be tappable.

---

## Loading Behaviour

Display:

- Skeleton header
- Skeleton summary card
- Skeleton quick actions
- Skeleton cards for consultations and notifications

Navigation should remain available while content loads.

---

## Empty State

Recent consultations:

"No consultations yet."

Notifications:

"You're all caught up."

Consent:

"No active consent requests."

---

## Error State

If a widget fails to load:

Display an inline error with:

- Retry button

Do not fail the entire dashboard because one widget fails.

---

## Accessibility

Support:

- Screen readers
- Minimum 44px touch targets
- VoiceOver labels
- Keyboard navigation (desktop demo)
- Dynamic text scaling where practical

---

## Acceptance Criteria

✓ Dashboard matches the wireframe layout.

✓ Widgets update independently.

✓ Notification badge updates in real time.

✓ Active consent appears immediately after doctor request.

✓ No full-page refresh required.

---

# P2 — Consent Request

## Wireframe Reference

Source:

docs/wireframes.html

Screen:

Patient Application → Consent Request

---

## Purpose

Allow the patient to review and respond to a doctor's request for access to their medical information.

This is the most security-sensitive interaction in the patient application.

The patient must clearly understand:

- Who is requesting access
- Why access is requested
- What information will be shared
- How long access remains valid

---

## Layout

Follow the supplied wireframe.

Expected sections:

1. Doctor Information
2. Facility Information
3. Consultation Reason
4. Requested Data Categories
5. Expiration Time
6. Approve Button
7. Decline Button

Buttons should remain fixed near the bottom of the viewport.

---

## Component Hierarchy

```
ConsentScreen

├── Header
│
├── DoctorCard
│
├── FacilityCard
│
├── ConsentSummary
│
├── SharedDataList
│
├── ExpirationBanner
│
├── ConsentActions
│   ├── ApproveButton
│   └── DeclineButton
│
└── BottomNavigation
```

---

## API Dependencies

GET /consent/{id}

POST /consent/{id}/approve

POST /consent/{id}/deny

---

## WebSocket Events

Receive:

ConsentRequested

Send:

ConsentApproved

ConsentDenied

The doctor's dashboard should update immediately after approval or denial.

---

## User Actions

Patient may:

- Read consent details
- Expand shared data categories
- Approve request
- Decline request

Approval should require explicit confirmation before submission.

---

## Loading Behaviour

Display skeletons for:

- Doctor information
- Facility information
- Requested data
- Action buttons (disabled)

---

## Empty State

If the consent has expired before opening:

"This request has expired."

Provide a button to return to the dashboard.

---

## Error State

If approval fails:

Display:

"We couldn't submit your decision."

Allow retry without losing context.

---

## Accessibility

Consent text should support:

- Screen readers
- Logical heading hierarchy
- Focus management
- Large touch targets

Approval and denial buttons must be visually distinct and not rely on colour alone.

---

## Acceptance Criteria

✓ Matches the approved wireframe.

✓ Approval updates doctor dashboard in real time.

✓ Denial updates doctor dashboard in real time.

✓ Expired requests cannot be approved.

✓ Audit event recorded.

✓ User receives confirmation after submission.

# P3 — My Health Record

## Wireframe Reference

Source:

docs/wireframes.html

Screen:

Patient Application → My Health Record

---

## Purpose

This screen provides patients with a chronological view of their personal medical information.

It should become the patient's primary location for reviewing healthcare history while maintaining a clean, understandable presentation for non-clinical users.

Unlike the doctor's record view, this interface is designed for readability rather than clinical density.

---

## Layout

Follow the approved wireframe.

Expected hierarchy:

1. Screen Header
2. Patient Summary
3. Timeline Filters
4. Medical Timeline
5. Recent Diagnoses
6. Prescriptions
7. Visit History

Scrolling should affect only the content area.

The header remains fixed.

---

## Component Hierarchy

```
HealthRecordScreen

├── AppHeader
│
├── PatientSummaryCard
│
├── TimelineFilters
│
├── MedicalTimeline
│   ├── TimelineEvent
│   ├── TimelineEvent
│   └── TimelineEvent
│
├── DiagnosisSection
│
├── PrescriptionSection
│
├── VisitHistorySection
│
└── BottomNavigation
```

---

## API Dependencies

GET /patients/me

GET /timeline

GET /medical-records

GET /diagnoses

GET /prescriptions

GET /consultations/history

---

## WebSocket Events

Subscribe:

TimelineUpdated

MedicalRecordUpdated

DiagnosisCreated

ConsultationCompleted

Updates should insert or modify only affected timeline entries.

---

## User Actions

Patient may:

- Scroll medical history
- Expand timeline events
- View diagnoses
- View prescriptions
- Open consultation summaries
- Filter timeline

No editing is permitted.

---

## Loading Behaviour

Skeletons:

- Timeline cards
- Diagnosis cards
- Prescription cards

Progressive loading is preferred.

---

## Empty State

Display:

"No medical history is available yet."

Offer:

"Complete your first consultation to begin building your medical record."

---

## Error State

Inline retry component.

Existing cached data should remain visible whenever possible.

---

## Accessibility

Timeline should remain fully screen-reader compatible.

Dates should be announced clearly.

Icons require accessible labels.

---

## Acceptance Criteria

✓ Timeline ordered newest first.

✓ New consultations appear automatically.

✓ Record matches backend chronology.

✓ No editing actions available.

✓ Matches approved wireframe.

---

# P4 — AI Symptom Check

## Wireframe Reference

Source:

docs/wireframes.html

Screen:

Patient Application → AI Symptom Check

---

## Purpose

This screen integrates the existing symptom checker into Mirage.

Mirage does not implement symptom analysis itself.

Instead, this interface consumes the existing symptom checker through the SymptomCheckerProvider abstraction defined in the Technical Architecture.

The UI should make this interaction feel native to Mirage.

---

## Layout

The visual structure must follow the approved wireframe.

Expected regions:

1. Introduction
2. Current Question
3. Conversation History
4. Suggested Answers
5. Free Text Input
6. Continue Button

Conversation should expand vertically.

Input remains anchored to the bottom.

---

## Component Hierarchy

```
SymptomCheckScreen

├── Header
│
├── SessionProgress
│
├── ConversationList
│   ├── AIMessage
│   ├── UserMessage
│   └── SuggestedResponses
│
├── TextInput
│
├── ContinueButton
│
└── BottomNavigation
```

---

## API Dependencies

POST /symptom-check/start

POST /symptom-check/message

GET /symptom-check/{session}

POST /symptom-check/complete

---

## WebSocket Events

None required.

Conversation remains request/response based.

---

## User Actions

Patient may:

- Answer AI questions
- Enter free text
- Select suggested responses
- Review previous answers
- Complete session

Patients may not modify completed sessions.

---

## Provider Integration

This screen communicates only with:

SymptomCheckerProvider

The frontend must never know which provider implementation is active.

Supported implementations:

- Existing Symptom Checker
- Mock Provider
- Future providers

---

## Loading Behaviour

Typing indicator.

Animated AI placeholder.

Disable input while awaiting provider response.

---

## Empty State

Initial screen should display onboarding guidance explaining how symptom assessment works.

---

## Error State

If provider unavailable:

"We're having trouble connecting to the symptom assessment service."

Retry available.

---

## Accessibility

Conversation should announce newly received messages.

Suggested answers must be keyboard accessible.

---

## Acceptance Criteria

✓ Existing symptom checker integrated through provider abstraction.

✓ Conversation persists.

✓ Responses saved.

✓ Completion returns structured summary.

✓ Matches supplied wireframe.

---

# Shared Patient Navigation

The patient application's bottom navigation should exactly match the navigation model shown in the approved wireframes.

Primary destinations include:

- Home
- Health Record
- AI Symptom Check
- Notifications
- Profile

Navigation transitions should use Framer Motion according to the Design System.

Navigation state should survive page refreshes where appropriate.

---

# Patient Notification Behaviour

Notifications may originate from:

- Consent requests
- Consultation updates
- Medical record changes
- AI session completion
- System announcements

Unread counts should update in real time through WebSockets.

---

# Patient Offline Behaviour

If connectivity is lost:

- Existing cached records remain readable.
- Navigation remains functional.
- Mutating actions are disabled.
- User receives connectivity warning.
- Automatic reconnection occurs when available.

No clinical data should be lost because of temporary network interruption.

---

# Patient Acceptance Criteria

The Patient Application is considered complete when:

✓ Every screen matches the approved wireframes.

✓ PhoneFrame behaviour matches Design System.

✓ Existing symptom checker integrates correctly.

✓ Consent workflow functions.

✓ Medical timeline updates live.

✓ Notifications synchronize.

✓ All loading, empty and error states implemented.

✓ Accessibility requirements satisfied.

✓ All API interactions occur through typed service layers.

✓ No duplicated UI components exist.

# Part 4 — Doctor Portal

The Doctor Portal is the primary clinical workspace for healthcare providers.

Unlike the Patient Application, the Doctor Portal prioritizes information density, rapid navigation, and efficient decision-making while maintaining a clean and approachable interface.

The Doctor Portal shown in `docs/wireframes.html` is the canonical layout.

---

# D1 — Doctor Dashboard

## Wireframe Reference

Source:

docs/wireframes.html

Screen:

Doctor Portal → Dashboard

---

## Purpose

The Dashboard serves as the doctor's landing page and provides an overview of current clinical activity.

It should immediately surface:

- Today's consultations
- Recently viewed patients
- Pending consent requests
- Active AI-assisted consultations
- Notifications
- Quick patient search

The dashboard should minimize unnecessary clicks while avoiding information overload.

---

## Layout

The layout must match the approved wireframe.

Expected regions:

• Top Navigation Bar

• Search

• Today's Schedule

• Recent Patients

• Pending Consents

• Active Consultation Widget

• Notification Panel

---

## Component Hierarchy

```
DoctorDashboard

├── TopNavigation
│
├── SearchBar
│
├── DashboardGrid
│   ├── ScheduleWidget
│   ├── RecentPatientsWidget
│   ├── PendingConsentWidget
│   ├── ActiveConsultationWidget
│   └── NotificationWidget
│
└── UserMenu
```

---

## API Dependencies

GET /doctor/dashboard

GET /consultations/today

GET /consent/pending

GET /patients/recent

GET /notifications

---

## WebSocket Events

Subscribe:

ConsentApproved

ConsentDenied

ConsultationStarted

ConsultationCompleted

NotificationCreated

Widgets should refresh individually.

---

## User Actions

Doctor may:

- Search patient
- Open consultation
- Review consent
- Open notifications
- Continue active consultation

---

## Loading Behaviour

Dashboard widgets load independently.

Skeleton placeholders should appear for each widget.

---

## Empty State

If no consultations:

"No consultations scheduled."

If no pending consent:

"No pending consent requests."

---

## Error State

Widget-level retry.

Dashboard should never completely fail because one service is unavailable.

---

## Accessibility

Dashboard must support:

- Keyboard navigation

- Landmark regions

- ARIA labels

- Screen readers

---

## Acceptance Criteria

✓ Matches wireframe

✓ Widgets update independently

✓ Dashboard responds to WebSocket events

✓ Search available immediately

---

# D2 — Patient Search

## Wireframe Reference

Doctor Portal → Patient Search

---

## Purpose

Locate patients quickly using multiple search criteria.

The search experience should remain responsive even with large datasets.

---

## Layout

Expected sections:

Search Input

Search Filters

Search Results

Recent Searches

---

## Component Hierarchy

```
PatientSearchPage

├── SearchInput

├── SearchFilters

├── ResultsTable

│   └── PatientRow

├── Pagination

└── EmptyState
```

---

## API Dependencies

GET /patients/search

---

## Search Behaviour

Support:

- Name

- National ID

- Phone Number

- Medical Record Number

- Date of Birth

Debounce:

300ms

---

## User Actions

Doctor may:

- Open patient profile

- Begin consultation

- Request consent

- View previous visits

---

## Loading Behaviour

Results table displays skeleton rows.

---

## Empty State

"No patients found."

---

## Error State

Retry search.

---

## Acceptance Criteria

✓ Fast search

✓ Keyboard accessible

✓ Pagination supported

✓ Matches wireframe

---

# D3 — Patient Record

## Wireframe Reference

Doctor Portal → Patient Record

---

## Purpose

Provide clinicians with a complete view of the patient's medical history after consent has been granted.

This screen is information-rich and optimized for clinical review.

---

## Layout

Expected regions:

Patient Header

Medical Timeline

Diagnoses

Prescriptions

Vitals

Previous Visits

AI Summary Panel

---

## Component Hierarchy

```
PatientRecordPage

├── PatientHeader

├── TimelinePanel

├── DiagnosisPanel

├── MedicationPanel

├── VitalsPanel

├── ConsultationHistory

└── AISummaryCard
```

---

## API Dependencies

GET /patients/{id}

GET /timeline/{id}

GET /diagnoses/{id}

GET /prescriptions/{id}

GET /consultations/{id}

---

## WebSocket Events

MedicalRecordUpdated

TimelineUpdated

ConsultationCompleted

---

## User Actions

Doctor may:

- Review history

- Expand records

- Filter timeline

- Open consultation

- Launch AI assistant

---

## Loading Behaviour

Progressive loading by section.

---

## Empty State

"No historical records available."

---

## Acceptance Criteria

✓ Record updates after consent approval

✓ Timeline synchronized

✓ Matches wireframe

---

# D4 — Consent Request Workflow

## Wireframe Reference

Doctor Portal → Request Consent

---

## Purpose

Initiate secure patient authorization before viewing protected records.

Consent should be simple, transparent, and legally auditable.

---

## Layout

Patient Summary

Consent Explanation

Requested Information

Expiry

Send Request Button

---

## API Dependencies

POST /consent/request

GET /consent/{id}

---

## WebSocket Events

ConsentApproved

ConsentDenied

ConsentExpired

---

## User Actions

Doctor may:

- Send request

- Cancel request

- Monitor status

---

## Loading Behaviour

Disable submit while sending.

---

## Acceptance Criteria

✓ Request immediately appears on patient device

✓ Live status updates

✓ Audit event created

---

# D5 — AI Consultation Workspace

## Wireframe Reference

Doctor Portal → Consultation

---

## Purpose

Provide the doctor's primary workspace during a consultation.

This screen combines:

- Patient information

- Live transcription

- AI diagnostic suggestions

- Clinical notes

The consultation experience should feel cohesive rather than fragmented.

---

## Layout

The layout should follow the approved wireframe.

Expected regions:

Patient Context

Consultation Transcript

AI Diagnostic Suggestions

Clinical Notes Editor

Recommended Questions

Consultation Controls

---

## Component Hierarchy

```
ConsultationWorkspace

├── PatientContext

├── TranscriptPanel

├── AIAssistantPanel

├── NotesEditor

├── SuggestedQuestions

├── ConsultationControls

└── StatusBar
```

---

## Provider Dependencies

The workspace must interact exclusively through provider abstractions.

TranscriptProvider

DiagnosisProvider

ClinicalNoteProvider

Each provider should be replaceable without modifying the UI.

---

## API Dependencies

POST /consultation/start

POST /consultation/end

GET /consultation/{id}

POST /notes/generate

POST /diagnosis/suggest

POST /transcription/start

---

## WebSocket Events

TranscriptUpdated

AISuggestionReady

ConsultationCompleted

MedicalRecordUpdated

---

## User Actions

Doctor may:

- Start consultation

- Pause transcription

- Accept AI suggestion

- Reject AI suggestion

- Edit notes

- Finalize consultation

---

## Loading Behaviour

Each AI widget loads independently.

The consultation interface must remain usable while AI processing occurs.

---

## Error State

Provider failures should only disable the affected panel.

Doctors should always be able to continue manually.

---

## Acceptance Criteria

✓ Provider abstraction maintained

✓ Consultation never blocked by AI

✓ Clinical notes editable

✓ Matches approved wireframe

---

# Doctor Portal Acceptance Criteria

The Doctor Portal is complete when:

✓ Every screen matches the approved wireframes.

✓ Patient search performs efficiently.

✓ Consent requests synchronize in real time.

✓ Patient records remain read-only until consent is granted.

✓ AI providers integrate exclusively through abstraction interfaces.

✓ Clinical notes support manual editing.

✓ All widgets implement loading, empty, and error states.

✓ Accessibility requirements are satisfied.

✓ WebSocket synchronization functions across all supported workflows.

# End of Part 4

# Part 5 — Cross-Screen Behaviour & Global Interface Standards

This section defines application-wide behaviour that applies to every screen in both the Patient Application and Doctor Portal.

These requirements supplement the wireframes and ensure a consistent implementation.

---

# Navigation Behaviour

## Patient Application

Navigation follows the order defined in `docs/wireframes.html`.

Navigation should feel identical to a native mobile application.

Requirements:

- Animated page transitions
- Preserved scroll position where appropriate
- Persistent bottom navigation
- Current page indicator
- Swipe-back support where appropriate (future)

The browser should never expose traditional desktop navigation patterns while inside the PhoneFrame.

---

## Doctor Portal

Navigation should remain persistent throughout the session.

The sidebar should not reload when switching pages.

Breadcrumbs should be shown whenever the doctor is deeper than one navigation level.

Example

Dashboard

↓

Patients

↓

John Smith

↓

Consultation

---

# Screen Transition Behaviour

Patient transitions should use the spring animations defined in:

03_Design_System.md

Recommended transitions

Push Navigation

Slide Left

Back Navigation

Slide Right

Bottom Sheet

Slide Up

Dialog

Fade + Scale

Notifications

Slide Down + Fade

Loading

Skeleton fade

Animations should communicate state changes rather than act as decoration.

---

# Global Notification System

Notifications should appear consistently throughout the application.

Types

Information

Success

Warning

Error

Clinical

Each notification should include

- Icon
- Title
- Description
- Timestamp
- Read status
- Action (optional)

---

# Notification Sources

Notifications may originate from

Patient

- Consent request
- Consultation complete
- Record updated
- New diagnosis
- Prescription issued

Doctor

- Consent approved
- Consent denied
- Patient joined
- AI suggestion available
- Consultation reminder

System

- Maintenance
- Connectivity
- Version updates
- Provider unavailable

Notifications should synchronize through WebSockets.

---

# Loading Behaviour

Every asynchronous operation must define an explicit loading state.

Preferred hierarchy

Level 1

Skeleton Components

Level 2

Progress Indicators

Level 3

Full-screen Loader

Full-screen blocking loaders should only be used during:

- Application initialization
- Authentication validation
- Critical route changes

---

# Empty States

Every collection-based component should define an empty state.

Examples

Timeline

"No medical events available."

Notifications

"No notifications."

Patients

"No matching patients."

Consultations

"No consultations found."

Consent

"No active requests."

Each empty state should explain the absence of information and, where appropriate, suggest the next action.

---

# Error Behaviour

Errors should never expose internal implementation details.

Every recoverable error should provide:

- Friendly explanation
- Retry action
- Return option (where appropriate)

Global application failures should display a dedicated error page with retry capability.

---

# Offline Behaviour

Patient Application

If connectivity is lost

- Cached medical records remain readable
- Timeline remains accessible
- Navigation continues functioning
- Mutating actions disabled
- Banner displayed indicating offline status

Doctor Portal

If connectivity is lost

- Existing patient information remains visible
- Editing disabled where synchronization is required
- Consultation controls indicate degraded mode

Automatic reconnection should occur when connectivity returns.

---

# Real-Time Synchronization

The frontend must never poll for state that is already available through WebSockets.

Expected synchronized events include

Consent

Consultation

Medical Record

Timeline

Notifications

AI Processing Status

Transcript Updates

Connection state should be visible only when necessary.

---

# Global Search Behaviour

Search should remain consistent across the application.

Requirements

- Debounced requests
- Keyboard shortcuts (Doctor Portal)
- Accessible labels
- Recent searches
- Clear button
- Loading indicator

Future enhancements may include fuzzy search and semantic search.

---

# Accessibility Standards

Every screen must satisfy WCAG 2.2 AA where practical.

Requirements

✓ Semantic HTML

✓ Keyboard accessibility

✓ Screen reader compatibility

✓ Logical heading structure

✓ Visible focus indicators

✓ High contrast support

✓ Accessible form validation

✓ Touch targets ≥44px

Clinical safety must always take precedence over visual aesthetics.

---

# Demo Behaviour

The demonstration environment renders both applications simultaneously.

Desktop Layout

```
+---------------------------------------------------------------+

 Patient Phone              Doctor Portal

+-------------------+    +--------------------------------------+

|                   |    |                                      |

|                   |    |                                      |

|                   |    |                                      |

+-------------------+    +--------------------------------------+
```

Both applications communicate only through the backend.

The frontend should never synchronize state directly between windows.

All synchronization must occur through:

Frontend

↓

FastAPI

↓

PostgreSQL / Redis

↓

WebSockets

↓

Other Client

This ensures the demonstration accurately reflects production behaviour.

---

# Developer Guidelines

When implementing a new screen:

1.

Locate the corresponding wireframe.

2.

Reuse existing components.

3.

Connect through the Service Layer.

4.

Use React Query.

5.

Implement loading state.

6.

Implement empty state.

7.

Implement error state.

8.

Implement accessibility.

9.

Add WebSocket subscriptions where required.

10.

Verify acceptance criteria.

No screen should bypass these steps.

---

# Traceability Matrix

Every screen should trace back to the project documentation.

| Concern | Primary Reference |
|----------|-------------------|
| Product Behaviour | 01_Product_Requirements_Document.md |
| System Architecture | 02_Technical_Architecture.md |
| Visual Design | 03_Design_System.md |
| Development Sequence | 04_Implementation_Plan.md |
| Backend Endpoints | 05_API_Contract.md |
| Data Model | 06_Database_Schema.md |
| Coding Conventions | 08_Coding_Standards.md |
| Deployment Constraints | 09_Deployment_Guide.md |
| Screen Layout & Navigation | docs/wireframes.html |

When implementation decisions are required, these references should be consulted in the order above.

---

# Definition of Completion

The UI implementation is considered complete when:

✓ Every screen defined in `docs/wireframes.html` has been implemented.

✓ All layouts match the approved wireframes.

✓ Every screen consumes backend data exclusively through typed service layers.

✓ Every AI capability is accessed through provider abstractions.

✓ Every screen defines loading, empty, and error states.

✓ WebSocket synchronization functions correctly.

✓ Patient and Doctor applications remain synchronized.

✓ Accessibility requirements are satisfied.

✓ Shared components are reused throughout the application.

✓ No duplicate implementations exist for common UI elements.

✓ All acceptance criteria defined within this document have been satisfied.

---

# Final Notes

This document intentionally extends, rather than replaces, the approved wireframes.

The wireframes define the visual and interaction design.

This specification defines the engineering implementation required to faithfully reproduce those designs within the Mirage architecture.

Future changes to the user interface should begin by updating `docs/wireframes.html`, followed by corresponding updates to this specification to maintain alignment.

# End of 10_UI_Screen_Specification.md