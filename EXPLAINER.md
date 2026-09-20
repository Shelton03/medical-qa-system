# EXPLAINER.md

A plain-language guide to what this repository is, what it's trying to achieve, and how its parts fit together.

## What this repo is

`medical-qa-system` is **Mirage** — a full healthcare platform built for a **Healthathon** demonstration: patient-controlled medical records with consent-based doctor access, schedule-driven appointment booking, an admin console, AI-assisted clinical workflows, and real-time updates. The platform lives in `backend/` + `frontend/` + `docs/`.

The system started life as the medical QA chatbot the repo is named for: an AI symptom-triage engine that decides at each turn whether to ASK clarifying questions or ANSWER with advice, using LLM self-consistency voting with a safety bias. Mirage is that idea grown up — the triage DNA became the platform's AI layer (symptom check, assessment, diagnosis drafting), and the original engine is preserved at `app/` as the first generation of the codebase.

The repo lives at `github.com/Shelton03/medical-qa-system`, forked from `github.com/NyashaEysenck/medical-qa-system` (added as `upstream`).

## What Mirage is trying to achieve

Per `docs/01_Product_Requirements_Document.md`: healthcare information in Zimbabwe is fragmented across institutions — patients carry paper records, histories are incomplete, tests get repeated, allergies get missed. Mirage is an MVP demonstration of an alternative model:

- **Patients own their records**, not hospitals. Records follow the patient across facilities.
- **Consent first**: a doctor must request access; the patient approves or denies on their phone; access is temporary and expires. No consent, no records.
- **AI assists, never decides**: AI drafts differential diagnoses, SOAP-style clinical summaries, and symptom assessments — but nothing enters the permanent record without clinician review and approval.
- **Bookable, not just walk-in**: patients book appointments against real doctor schedules; confirmed appointments open an AI pre-assessment that feeds the consultation.
- **Transparency**: every view, edit, consent, and access is audit-logged; patients can see who viewed their records.
- **One 5-minute demo path** (the success metric): doctor logs in → searches patient → requests access → patient approves in real time → doctor reviews history → AI assists consultation → doctor confirms diagnosis and note → record updates → patient sees it instantly.

## How the AI is wired

Per the PRD (FR-9), the AI symptom assessment "exists as an independent provider" — with examples including "Current QA System, OpenAI, Azure, Anthropic, Local LLM". The code mirrors that:

```
backend/app/providers/interfaces/       <- abstract contracts (SymptomCheckerProvider,
                                           DiagnosisProvider, ClinicalSummaryProvider,
                                           TranscriptionProvider, NotificationProvider,
                                           StorageProvider, EmailProvider)
backend/app/providers/implementations/  <- mock_*, gateway_*, local_* implementations
backend/app/providers/factory.py        <- resolves provider by env (SYMPTOM_PROVIDER,
                                           SUMMARY_PROVIDER, TRANSCRIPTION_PROVIDER)
backend/app/ai/factory.py               <- resolves the chat AIProvider by AI_PROVIDER
```

Every model slot resolves the same three ways: `mock` (canned demo data), `gateway`/`ccaimex` (real models through the ccaimex OpenAI-compatible gateway configured via `LLM_GATEWAY_URL` + `LLM_GATEWAY_API_KEY`/`LLM_API_KEY`), or `local` (a locally hosted LLM). `backend/app/ai/gateway_provider.py` (`GatewayAIProvider`) handles chat, streaming, and record analysis; `gateway_providers.py` reuses it for diagnosis, summary, and transcription. Business logic only ever sees the abstract interfaces — swapping a vendor never touches routers or services.

Patient-facing AI output is cleaned server-side before it reaches the UI: generated questions and JSON payloads pass through strippers (`QuestionGenerator._clean_question`, `app/ai/local_llm.clean_json_response`) that remove reasoning traces and formatting artifacts, so model internals never leak to patients.

## The original triage engine (`app/`)

This is where the system began — the first-generation ASK/ANSWER triage engine, preserved at `app/`. Its decision machinery is the design ancestor of the platform's AI assessment pipeline.

FastAPI + PostgreSQL (SQLAlchemy 2 async) + MinIO for uploaded files, entry `app/main.py`, mounted at `/api` with sub-routers for auth/sessions/contact plus the main `POST /api/query`. Sessions, messages, and contact requests persist to PostgreSQL (`app/db/repositories.py`); uploaded files go to a MinIO bucket (`app/db/storage.py`) with only metadata in an `attachments` table. Pipeline in `app/services/orchestrator.py`:

- `InputProcessor` — extracts entities/symptoms/severity via LLM (stand-in for MedSpaCy/BioBERT)
- `AssessmentService`, `GapAnalysisService` — track missing info and risk flags per session
- `DecisionEngine` (`app/services/decision_engine.py`) — the interesting part: runs the same decision prompt `SELF_CONSISTENCY_RUNS` times (default 3) in parallel, majority-votes ASK vs ANSWER, averages confidence, and **overrides to ASK** if confidence < `CONFIDENCE_THRESHOLD` (0.7) or any high-risk flag exists — i.e. abstention-by-default under uncertainty
- `QuestionGenerator` / `AnswerGenerator` — produce the next question or the advice
- `ConversationSummarizer` — wraps up the session, with escalation to a doctor after >15 user turns

It runs standalone with `POSTGRES_URL`/`POSTGRES_PASSWORD`, MinIO `S3_*`, and `LLM_BASE_URL`/`LLM_API_KEY`/`LLM_MODEL` env vars. Note that `backend/app/` is the platform backend; the engine above predates it.

## Mirage backend (`backend/`)

FastAPI, Python 3.12, SQLAlchemy 2 async + asyncpg, Alembic, Redis pub/sub, JWT auth. Entry: `backend/main.py`, which wires the routers, CORS plus correlation-ID / rate-limit / audit-log middlewares, and startup tasks.

**Routers** (all under `/api/v1` per the API contract):

| Router | Purpose |
|---|---|
| `auth/` | demo-login (one-click), doctor/patient login (national ID + PIN for patients), refresh, logout, me |
| `patient/` + `patient/me_router` | patient search (doctor-facing), registration, own profile/timeline/visits |
| `doctor/` | dashboard aggregate, patient search, consultations with notes/diagnoses/medications |
| `consent/` | create / list / approve / decline / revoke consent requests |
| `records/` | consent-gated medical record get/patch + version history |
| `timeline/` | chronological health timeline + per-event detail |
| `ai/` | AI sessions, messages, streaming responses (SSE), diagnosis + summary generation |
| `appointment/` | booking, my-appointments, doctor schedule, facilities lookup, admin dashboard/doctors/schedules/time-off, confirm/cancel, start-consultation |
| `admin/` | admin console API: facilities CRUD + system settings (`system_configs`) |
| `notifications/` | notification list/unread-count/mark-read + `/ws/notifications` WebSocket |
| `transcription/` | consultation transcription (provider-abstracted) |
| `audit/` | immutable audit log queries |
| `websocket/` | generic `/ws` endpoint, event types, Redis listener/publisher |

**Real-time flow**: domain events (`WSEventType` — CONSENT_REQUESTED/APPROVED/DECLINED/REVOKED, RECORD_UPDATED, AI_RESPONSE_READY, TIMELINE_UPDATED, APPOINTMENT_CREATED/CONFIRMED/CANCELLED/REMINDER, EMERGENCY_APPOINTMENT, CONSULTATION_READY, etc.) are published to Redis (`mirage:ws:{channel}` via `websocket/publisher.py`); background listeners started in `main.py`'s lifespan subscribe to the Redis patterns and push to connected WebSocket clients per-user (`notifications:user:{id}`) or broadcast (`notifications:all`). This is what makes the patient's phone update the moment the doctor acts, and vice versa.

**Auth**: JWT (access 60 min / refresh 30 days), role-gated dependencies (`require_role` factory), role-aware token keys (`mirage_patient_access_token`, `mirage_doctor_access_token`, ...) kept in sync between `localStorage` and HTTP cookies so Next.js middleware can gate routes. Demo mode (`DEMO_MODE=true`) enables one-click login for patient/doctor/admin using deterministic synthetic accounts.

**Data model** — 26 SQLAlchemy tables in `backend/app/db/models.py` (UUID PKs, UTC): users, patients, doctors, facilities, system_configs, medical_records (+ medical_record_versions — corrections create new versions, nothing is deleted), visits, diagnoses, medications, allergies, chronic_conditions, laboratory_results, imaging_results, clinical_documents, clinical_notes, consent_requests, appointments (+ doctor_schedules, doctor_time_offs, appointment_slot_allocations), ai_sessions, ai_messages, notifications, refresh_tokens, audit_logs. This models the core idea: the record belongs to the patient, consent links patient and doctor, appointments live on real doctor schedules, and every change leaves history.

**Appointment booking**: `backend/app/appointment/` (router/service/schemas/enums) — patients book with `desired_duration_minutes` and `is_emergency` against seeded doctor schedules; doctors confirm, cancel, or start the consultation; slots are allocated from `doctor_schedules`/`appointment_slot_allocations`. Booking requires schedule rows, so weekday schedules are seeded idempotently by Alembic migration when empty. Each appointment carries an AI pre-assessment that is available to the doctor at consultation time.

**Demo seeding**: `backend/app/db/seeder.py` populates a full demo world on startup when `DEMO_MODE=true` — a demo doctor, a demo patient, their conditions, allergies, medications, and roughly 50 realistic visits with timeline events — so dashboards and the whole workflow can be demonstrated without real or zeroed-out data.

**Tests**: 13 test modules in `backend/tests/` (auth, consent, patients, doctor, records, ai, audit, middleware, migrations, providers, seeder, websocket, db connection) — run with `make test`.

## Mirage frontend (`frontend/`)

Next.js 14 App Router + TypeScript + Tailwind + Framer Motion + React Query, with three apps plus demo mode in one codebase:

- **`/patient/*`** — mobile-first patient app: home dashboard, records, AI symptom check (chat-style), appointment booking (`book-appointment`) and appointment list, consent approvals, notifications, health timeline, medical ID, profile, visits. Login with national ID + PIN.
- **`/doctor/*`** — desktop clinical portal: dashboard, patient search, schedule, consent management, consultations with `AIChatPanel` (streaming AI responses), `SOAPEditor` (editable AI-drafted summary sections: Chief Complaint / HPI / Findings / Assessment / Plan), `DifferentialList`, `PrescriptionCard`, AI consultation page, access history, audit views.
- **`/admin/*`** — admin console: dashboard, appointments, doctors, facilities, schedules, reports, settings (backed by the `/api/v1/admin` + appointment admin endpoints).
- **`/demo`** — split-screen demo mode: doctor portal in a sandboxed `<iframe>` on the left, the patient app in a second iframe **wrapped in a realistic `PhoneFrame`** (CSS-simulated smartphone) on the right, with a scripted 10-step Healthathon walkthrough (Introduction → logins → Search Patient → Request Consent → patient receives/approves → doctor sees approval → AI-Assisted Consultation → Patient Sees Updated Record) with keyboard shortcuts, per-step auto-advance timers, and a collapsible narration panel. This exists so the full patient-doctor story can be shown on one screen, no second device needed.

**State**: `providers/` — `AuthProvider` (JWT access+refresh tokens, auto-refresh), `WebSocketProvider` (live notifications, reconnect + heartbeat, consent/appointment-event handling), `QueryProvider` (React Query caching), `ToastProvider`. `middleware.ts` gates `/doctor/*` and `/patient/*` routes. `lib/api.ts` is a fully typed API client with a relative base URL `/api/v1` — requests are proxied through Next.js rewrites to the FastAPI backend, unwrapping the `{success, data, errors}` envelope and handling 401s with refresh-and-retry (browser-facing URLs never expose internal Docker hostnames).

**Tests**: Vitest + React Testing Library (`__tests__/`) covering PhoneFrame, StatusBadge, doctor dashboard, and the AI consultation page — run with `npm test` (vitest).

## Design docs (`docs/`)

15 numbered documents — this repo was spec-first, so the docs describe intent in depth. Read in order: 00 Project Index → 01 PRD → 02 Technical Architecture → 03 Design System (color/typography tokens) → 04 Implementation Plan → 05 API Contract (envelope responses, versioning) → 06 Database Schema → 07 Master Generation Prompt → 08 Coding Standards → 09 Deployment Guide → 10 UI Screen Spec → 11 User Flows & State Machines (+ `wireframes.html`) → 12 Appointment Booking System → 13 Real-Time Transcription → 14 AI Assessment Pipeline. The Project Index defines the precedence if documents conflict: PRD wins over architecture, which wins over the API contract, and so on.

## Running it

```bash
cp .env.example .env      # then fill LLM_GATEWAY_URL/LLM_API_KEY and POSTGRES_PASSWORD
make build && make up     # host ports: frontend 3001, backend 8002, postgres 5433, redis 6380
make migrate              # alembic upgrade head
make test                 # backend pytest suite
```

- Frontend http://localhost:3001 · API http://localhost:8002 · Swagger http://localhost:8002/docs
- Docker Compose is the single way to start services (`make up` / `make down` / `make logs`; `shell-backend` / `shell-frontend` for shells).
- With `DEMO_MODE=true` the app seeds a realistic demo world and offers one-click login, so the full consent → consult → record-update story works out of the box.
- Model providers resolve by env: `mock` by default; set `AI_PROVIDER` / `SYMPTOM_PROVIDER` / `SUMMARY_PROVIDER` / `TRANSCRIPTION_PROVIDER` to `gateway` (or `ccaimex`) to route through the OpenAI-compatible gateway, or `local` for a locally hosted model. `SKIP_MODEL_DOWNLOAD=true` in compose keeps the backend from pulling large GGUF weights on every start.
- The dockerized stack is the platform; the original triage engine at `app/` remains from the first build and is not part of docker-compose.

## One-sentence summary

Mirage is a healthcare platform for patient-owned records, consent-based doctor access, schedule-driven appointment booking, and AI that assists but never decides — grown from a medical QA triage chatbot on a deliberately replaceable, vendor-agnostic AI architecture.
