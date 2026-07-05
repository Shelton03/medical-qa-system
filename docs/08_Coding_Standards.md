# Mirage
# Coding Standards

Version: 1.0

---

# Purpose

This document defines the engineering standards for the Mirage codebase.

Its purpose is to ensure that every generated file follows the same conventions, regardless of which AI coding assistant or engineer creates it.

These standards take precedence over individual coding preferences.

---

# Engineering Philosophy

The codebase should prioritize:

- Readability
- Maintainability
- Explicitness
- Consistency
- Simplicity
- Extensibility
- Testability

Never sacrifice long-term maintainability for short-term convenience.

---

# General Principles

Prefer:

- Composition over inheritance
- Dependency Injection over service location
- Interfaces over concrete implementations
- Small focused modules
- Explicit dependencies
- Immutable data where practical

Avoid:

- Global mutable state
- Hidden side effects
- Circular dependencies
- Magic strings
- Hardcoded configuration
- Overly clever abstractions

---

# Repository Structure

Backend

```
backend/

app/
    api/
    core/
    db/
    models/
    repositories/
    services/
    providers/
    schemas/
    middleware/
    websocket/
    workers/
    tests/
```

Frontend

```
frontend/

app/
components/
features/
hooks/
lib/
providers/
services/
types/
styles/
```

Each directory should have a single responsibility.

---

# Python Version

Python 3.12+

All code should support strict type checking.

---

# Formatting

Use

Black

isort

Ruff

No custom formatting rules.

---

# Typing

Every function must include type hints.

Good

```python
def create_patient(patient: PatientCreate) -> Patient:
```

Avoid

```python
def create_patient(patient):
```

Return types are always required.

---

# Docstrings

Public modules, classes, and functions require docstrings.

Example

```python
class ConsentService:
    """
    Handles creation, approval, expiration,
    and auditing of patient consent requests.
    """
```

Avoid redundant docstrings that merely repeat the function name.

---

# Dependency Injection

Always inject dependencies.

Good

```python
class PatientService:

    def __init__(
        self,
        repository: PatientRepository,
        notifier: NotificationProvider
    ):
        ...
```

Avoid

```python
repo = PatientRepository()
```

inside services.

---

# Layered Architecture

Controllers (FastAPI Routes)

↓

Services

↓

Repositories

↓

Database

Controllers should contain almost no business logic.

Repositories should never contain business rules.

Business rules belong inside services.

---

# Repository Pattern

Repositories are responsible only for persistence.

Example

```python
PatientRepository

VisitRepository

ConsentRepository
```

Repositories should never:

- Send notifications
- Call AI providers
- Perform authorization
- Contain business workflows

---

# Service Layer

Services coordinate application behaviour.

Examples

```
ConsentService

ConsultationService

NotificationService

TimelineService

MedicalRecordService
```

Services may call multiple repositories and providers.

---

# Provider Pattern

External integrations must always be abstracted.

Example

```
DiagnosisProvider

EmailProvider

StorageProvider

NotificationProvider

SymptomCheckerProvider

TranscriptionProvider
```

Concrete implementations belong inside

```
providers/implementations/
```

Business logic imports interfaces only.

---

# Error Handling

Raise domain-specific exceptions.

Example

```
ConsentRequiredError

PatientNotFoundError

ProviderUnavailableError
```

Avoid generic Exception.

Errors should be translated into HTTP responses by middleware.

---

# Logging

Use structured logging.

Every log entry should include

```
request_id

user_id

action

duration

status
```

Avoid print statements.

---

# Configuration

Environment variables should be accessed only through a configuration module.

Good

```python
settings.jwt_secret
```

Avoid

```python
os.getenv(...)
```

throughout the application.

---

# Database Access

Use SQLAlchemy ORM.

Avoid raw SQL unless performance requires it.

Database sessions should be request-scoped.

Never expose ORM models directly through the API.

Always map models to Pydantic schemas.

---

# Transactions

Business operations involving multiple writes should execute inside a transaction.

Examples

- Consent approval
- Consultation completion
- Medical record updates

Partial failures should roll back automatically.

---

# Background Tasks

Long-running work should execute asynchronously.

Examples

- AI summaries
- Email delivery
- Notification fan-out
- File processing

Prefer Celery or RQ with Redis.

The application should remain responsive while background work executes.

---

# Security

Never log:

- Passwords
- JWTs
- Refresh tokens
- Medical information
- API keys

Sensitive configuration belongs in environment variables.

Passwords should always be hashed using Argon2 or bcrypt.

JWT signing keys must never be committed to source control.

---

# API Design

Every endpoint should:

- Validate input
- Authorize access
- Return standardized responses
- Use appropriate HTTP status codes
- Include OpenAPI documentation

Avoid inconsistent response formats.

---

# Database Migrations

Use Alembic exclusively.

Never modify an existing migration after it has been applied.

Each migration should represent one logical schema change.

---

# Testing Philosophy

Prefer behavioural testing over implementation testing.

Test:

- Public APIs
- Service behaviour
- Repository queries
- Permission checks
- Consent workflow
- AI provider abstraction

Avoid testing private helper methods directly.

# Frontend Standards

---

# Framework

The frontend should use:

- Next.js (App Router)
- TypeScript (strict mode)
- TailwindCSS
- Framer Motion
- React Query (TanStack Query)
- React Hook Form
- Zod

No page should depend directly on backend implementation details.

API communication should occur through dedicated service modules.

---

# Folder Organization

Feature-first architecture is preferred.

Example

```
features/

    authentication/

    consultation/

    consent/

    notifications/

    patient/

    doctor/

    timeline/
```

Each feature should contain:

```
components/

hooks/

services/

types/

utils/
```

Avoid placing unrelated components in a shared directory.

---

# Component Design

Components should have a single responsibility.

Prefer small composable components over large monolithic ones.

Good

```
PatientHeader

PatientSummaryCard

TimelineItem

ConsentBanner

VisitCard

NotificationList
```

Avoid

```
PatientDashboardEverything.tsx
```

---

# Props

Always define explicit interfaces.

Example

```typescript
interface VisitCardProps {
    visit: Visit
    onSelect: (visitId: string) => void
}
```

Avoid `any`.

---

# State Management

Use local state whenever possible.

Recommended order:

1. Local component state
2. React Context
3. React Query cache
4. URL state

Avoid introducing global state libraries unless there is a clear architectural benefit.

---

# Server State

All backend data should be managed through React Query.

Benefits:

- Caching
- Automatic refetching
- Background updates
- Retry policies
- Optimistic updates

Avoid manually managing server state with `useState`.

---

# Forms

All forms should use:

React Hook Form

Validation:

Zod

Validation logic should never be duplicated between frontend and backend.

---

# API Layer

Never call `fetch()` directly inside components.

Instead:

```
Component

↓

Hook

↓

API Client

↓

Backend
```

Example

```
usePatientTimeline()

↓

timelineService.getTimeline()

↓

ApiClient
```

This centralizes authentication, retries, error handling, and request logging.

---

# Styling

TailwindCSS only.

Avoid inline styles except for dynamically calculated values.

Use design tokens for:

- Colors
- Spacing
- Typography
- Border radius
- Shadows

Do not hardcode colors throughout the application.

---

# Mobile Patient Application

The patient application must always render inside the `PhoneFrame` component.

Patient screens should assume a fixed viewport.

Never implement responsive breakpoints inside patient-specific components.

The `PhoneFrame` is responsible for scaling.

---

# Doctor Portal

The doctor portal is desktop-first.

Focus on:

- Information density
- Readability
- Fast navigation
- Keyboard accessibility
- Multi-panel layouts

Avoid unnecessarily large spacing that reduces usable screen area.

---

# Animation Standards

Animations should communicate state changes, not decorate the interface.

Use Framer Motion for:

- Page transitions
- Bottom sheets
- Dialogs
- Loading states
- Shared element transitions

Preferred spring:

```typescript
const spring = {
    type: "spring",
    stiffness: 380,
    damping: 32
}
```

Avoid long or distracting animations.

---

# Loading States

Every asynchronous operation should expose a loading state.

Preferred patterns:

- Skeleton placeholders
- Spinner for short operations
- Progressive rendering
- Optimistic updates where appropriate

Avoid blank screens.

---

# Error States

Every API request should gracefully handle:

- Network failures
- Validation errors
- Authentication failures
- Provider outages

Users should always receive actionable feedback.

---

# Empty States

Every list should define an empty state.

Example

```
No consultations yet.

No notifications.

No medical history available.
```

Avoid rendering empty containers.

---

# Accessibility

Minimum requirements:

- Keyboard navigation
- Visible focus indicators
- Semantic HTML
- Accessible form labels
- ARIA attributes where appropriate
- Sufficient color contrast

Accessibility is required, not optional.

---

# Icons

Use Lucide React consistently.

Avoid mixing icon libraries.

---

# Testing Standards

Backend

pytest

Frontend

Vitest

React Testing Library

End-to-end

Playwright

Priority workflows:

- Login
- Demo mode
- Consent approval
- Consultation flow
- Timeline updates
- AI session
- Notifications
- Split-screen synchronization

---

# Git Conventions

Branch naming

```
feature/consent-workflow

feature/doctor-dashboard

fix/notification-refresh

refactor/provider-abstractions
```

Commit format

```
feat:

fix:

refactor:

docs:

test:

chore:
```

Examples

```
feat: implement consent approval workflow

fix: resolve timeline sorting issue

refactor: abstract transcription provider
```

---

# Code Review Checklist

Every pull request should answer:

- Does it follow the architecture?
- Does it introduce duplicate logic?
- Are interfaces respected?
- Are provider abstractions maintained?
- Are tests included?
- Is documentation updated?
- Are loading and error states handled?
- Is the feature accessible?
- Does it introduce unnecessary complexity?

Code should be easy to understand without external explanation.

---

# Performance Guidelines

Prefer:

- Lazy loading
- Code splitting
- Memoization when justified
- Pagination
- Incremental rendering
- Efficient database queries

Avoid premature optimization.

Profile before optimizing complex code paths.

---

# Security Guidelines

Validate all user input.

Escape rendered content where appropriate.

Protect all authenticated routes.

Never expose secrets in the frontend bundle.

Use HTTPS in production.

Sanitize uploaded file metadata.

Treat all client input as untrusted.

---

# Documentation Standards

Every major module should include:

- Purpose
- Responsibilities
- Extension points
- Dependencies

Complex business rules should explain *why* they exist.

Public APIs should include OpenAPI documentation and examples.

---

# Definition of Done

A feature is complete only when:

- Requirements from the Product Requirements Document are satisfied.
- Code follows the architecture.
- Unit tests pass.
- Integration tests pass (where applicable).
- Documentation is updated.
- Loading, empty, and error states are implemented.
- Accessibility requirements are met.
- Logging is in place for important operations.
- No TODOs or placeholder implementations remain.
- Code has been reviewed for consistency.

---

# Repository Quality Checklist

Before considering the repository production-ready, verify:

✓ Docker Compose starts the full stack.

✓ Backend passes health checks.

✓ Database migrations apply successfully.

✓ Seed data loads without errors.

✓ Demo Mode works.

✓ JWT authentication works.

✓ Patient application renders correctly inside the PhoneFrame.

✓ Doctor dashboard supports the complete consultation workflow.

✓ Real-time consent synchronization functions correctly.

✓ AI providers are fully abstracted.

✓ Existing Symptom Checker integrates through the provider interface.

✓ Notifications update in real time.

✓ Audit logs capture all sensitive operations.

✓ Test suite passes.

✓ Documentation is complete.

✓ Environment variables are documented.

✓ No placeholder code remains.

---

# Engineering Principle

Every line of code should make the repository easier to understand, easier to maintain, and easier to extend.

Optimize for the engineer who will read this code six months from now, not the engineer writing it today.

# End of Coding Standards