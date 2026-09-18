# EXPLAINER.md

A plain-language guide to what this repository is, what it's trying to achieve, and how its parts fit together.

## What this repo is

`medical-qa-system` contains **two related but distinct systems**, and understanding the difference is the key to navigating the codebase:

1. **The Medical QA System** (`app/` at repo root) — the repo's namesake. A standalone AI symptom-triage chatbot: a FastAPI service that runs an interactive medical question-answering session, deciding at each turn whether to **ASK** more clarifying questions or **ANSWER** with advice, using LLM self-consistency voting with a safety bias. This is the original project.

2. **Mirage** (`backend/` + `frontend/` + `docs/`) — the larger, newer system and the bulk of the code. A full healthcare platform built for a **Healthathon** demonstration: patient-controlled medical records with consent-based doctor access, AI-assisted clinical workflows, and real-time updates. Its design explicitly treats the Medical QA System as the "Existing Symptom Checker" to be plugged in behind a provider interface (docs/01 PRD, FR-9).

The repo lives at `github.com/Shelton03/medical-qa-system`, forked from `github.com/NyashaEysenck/medical-qa-system` (added as `upstream`).

## What Mirage is trying to achieve

Per `docs/01_Product_Requirements_Document.md`: healthcare information in Zimbabwe is fragmented across institutions — patients carry paper records, histories are incomplete, tests get repeated, allergies get missed. Mirage is an MVP demonstration of an alternative model:

- **Patients own their records**, not hospitals. Records follow the patient across facilities.
- **Consent first**: a doctor must request access; the patient approves or denies on their phone; access is temporary and expires. No consent, no records.
- **AI assists, never decides**: AI drafts differential diagnoses, SOAP-style clinical summaries, and symptom assessments — but nothing enters the permanent record without clinician review and approval.
- **Transparency**: every view, edit, consent, and access is audit-logged; patients can see who viewed their records.
- **One 5-minute demo path** (the success metric): doctor logs in → searches patient → requests access → patient approves in real time → doctor reviews history → AI assists consultation → doctor confirms diagnosis and note → record updates → patient sees it instantly.

## How the two halves relate

The PRD (FR-9) defines the intended relationship: the AI symptom assessment "exists as an independent provider", with examples including "Current QA System, OpenAI, Azure, Anthropic, Local LLM". In code:

```
backend/app/providers/interfaces/       <- abstract contracts (SymptomCheckerProvider,
                                           DiagnosisProvider, ClinicalSummaryProvider,
                                           TranscriptionProvider, NotificationProvider,
                                           StorageProvider, EmailProvider)
backend/app/providers/implementations/  <- mock_* implementations selected via env vars
backend/app/providers/factory.py        <- resolves provider by env (AI_PROVIDER, SYMPTOM_PROVIDER...)
```

`backend/app/ai/provider.py` defines `AIProvider` (abstract) with `AIContext`/`AIMessage`, and `backend/app/ai/chat_engine.py` orchestrates AI sessions with consent-gated patient context. The default `MockAIProvider` (`backend/app/ai/mock_provider.py`) returns canned context-aware responses with the mandatory clinical disclaimer ("Final diagnoses... must be confirmed by the attending physician"). Swapping in the real Medical QA System — or any LLM vendor — means implementing these interfaces; business logic never imports a vendor SDK.

The root `app/` QA system is not yet wired in as a provider implementation — it sits alongside Mirage as a standalone service with its own `/api/query` endpoint. Building that adapter (implementing `SymptomCheckerProvider`/`AIProvider`) is the integration step the architecture anticipates.

## The Medical QA System (`app/`)

FastAPI + MongoDB (Motor async) + a parallel PostgreSQL engine, entry `app/main.py`, mounted at `/api` with sub-routers for auth/sessions/contact/chat plus the main `POST /api/query`. Pipeline in `app/services/orchestrator.py`:

- `InputProcessor` — extracts entities/symptoms/severity via LLM (stand-in for MedSpaCy/BioBERT)
- `AssessmentService`, `GapAnalysisService` — track missing info and risk flags per session
- `DecisionEngine` (`app/services/decision_engine.py`) — the interesting part: runs the same decision prompt `SELF_CONSISTENCY_RUNS` times (default 3) in parallel, majority-votes ASK vs ANSWER, averages confidence, and **overrides to ASK** if confidence < `CONFIDENCE_THRESHOLD` (0.7) or any high-risk flag exists — i.e. abstention-by-default under uncertainty
- `QuestionGenerator` / `AnswerGenerator` — produce the next question or the advice
- `ConversationSummarizer` — wraps up the session, with escalation to a doctor after >15 user turns

Sessions persist to MongoDB via motor repositories; it needs `MONGODB_URI` and `LLM_BASE_URL/API_KEY/MODEL` env vars. It is a separate FastAPI app from Mirage's backend — do not confuse the two `app/` packages; only `backend/app/` is the Mirage backend.

## Mirage backend (`backend/`)

FastAPI, Python 3.12, SQLAlchemy 2 async + asyncpg, Alembic, Redis pub/sub, JWT auth. Entry: `backend/main.py`, which wires the routers, three middlewares, and startup tasks.

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
| `notifications/` | notification list/unread-count/mark-read + `/ws/notifications` WebSocket |
| `transcription/` | consultation transcription (provider-abstracted) |
| `audit/` | immutable audit log queries |
| `websocket/` | generic `/ws` endpoint, event types, Redis listener/publisher |

**Real-time flow**: domain events (`WSEventType` — CONSENT_REQUESTED/APPROVED/DECLINED/REVOKED, RECORD_UPDATED, AI_RESPONSE_READY, TIMELINE_UPDATED, etc.) are published to Redis (`mirage:ws:{channel}` via `websocket/publisher.py`); background listeners started in `main.py`'s lifespan subscribe to the Redis patterns and push to connected WebSocket clients per-user (`notifications:user:{id}`) or broadcast (`notifications:all`). This is what makes the patient's phone update the moment the doctor acts, and vice versa.

**Auth**: JWT (access 60 min / refresh 30 days), role-gated dependencies (`require_role` factory). Demo mode (`DEMO_MODE=true`) enables one-click login for patient/doctor/admin using deterministic synthetic accounts.

**Data model** — 21 SQLAlchemy tables in `backend/app/db/models.py` (UUID PKs, UTC): users, patients, doctors, facilities, medical_records (+ medical_record_versions — corrections create new versions, nothing is deleted), visits, diagnoses, medications, allergies, chronic_conditions, laboratory_results, imaging_results, clinical_documents, clinical_notes, consent_requests, ai_sessions, ai_messages, notifications, refresh_tokens, audit_logs. This models the core idea: the record belongs to the patient, consent links patient and doctor, and every change leaves history.

**Demo seeding**: `backend/app/db/seeder.py` populates a full demo world on startup when `DEMO_MODE=true` — a demo doctor, a demo patient, and their conditions, allergies, medications and visits — so the whole workflow can be demonstrated without real data.

**Tests**: 15 test files in `backend/tests/` (auth, consent, patients, records, ai, audit, middleware, migrations, providers, seeder, websocket, db connection) — run with `make test`.

## Mirage frontend (`frontend/`)

Next.js 14 App Router + TypeScript + Tailwind + Framer Motion + React Query, with two apps in one codebase:

- **`/patient/*`** — mobile-first patient app: home dashboard, records, AI symptom check (chat-style), consent approvals, notifications, health timeline, medical ID, profile. Login with national ID + PIN.
- **`/doctor/*`** — desktop clinical portal: dashboard, patient search, consent management, consultations with `AIChatPanel` (streaming AI responses), `SOAPEditor` (editable AI-drafted summary sections: Chief Complaint / HPI / Findings / Assessment / Plan), `DifferentialList`, `PrescriptionCard`, access history, audit views.
- **`/demo`** — split-screen demo mode: doctor portal in a sandboxed `<iframe>` on the left, the patient app in a second iframe **wrapped in a realistic `PhoneFrame`** (CSS-simulated smartphone) on the right, with a scripted 10-step Healthathon walkthrough (intro → logins → patient search → consent request → approve → AI consultation → record update) with keyboard shortcuts, per-step auto-advance timers, and a collapsible narration panel. This exists so the full patient-doctor story can be shown on one screen, no second device needed.

**State**: `providers/` — `AuthProvider` (JWT access+refresh tokens, auto-refresh), `WebSocketProvider` (live notifications, reconnect + heartbeat, consent-event handling), `QueryProvider` (React Query caching), `ToastProvider`. `middleware.ts` gates `/doctor/*` and `/patient/*` routes. `lib/api.ts` is a fully typed API client with a relative base URL `/api/v1` — requests are proxied through Next.js rewrites to the FastAPI backend, unwrapping the `{success, data, errors}` envelope and handling 401s with refresh-and-retry.

**Tests**: Vitest + React Testing Library (`__tests__/`) covering PhoneFrame, StatusBadge, doctor dashboard, and the AI consultation page.

## Design docs (`docs/`)

13 numbered documents — this repo was spec-first, so the docs describe intent in depth. Read in order: 00 Project Index → 01 PRD → 02 Technical Architecture → 03 Design System (color/typography tokens) → 04 Implementation Plan → 05 API Contract (envelope responses, versioning) → 06 Database Schema → 07 Master Generation Prompt → 08 Coding Standards → 09 Deployment Guide → 10 UI Screen Spec → 11 User Flows & State Machines (+ `wireframes.html`). The Project Index defines the precedence if documents conflict: PRD wins over architecture, which wins over the API contract, and so on.

## Running it

```bash
cp .env.example .env      # then fill LLM_* and POSTGRES_PASSWORD
make build && make up     # postgres:5432, redis:6379, backend:8000, frontend:3000
make migrate              # alembic upgrade head
make test                 # backend pytest suite
```

- Frontend http://localhost:3000 · API http://localhost:8000 · Swagger http://localhost:8000/docs
- With `DEMO_MODE=true` the app seeds demo data and offers one-click login, so the full consent → consult → record-update story works out of the box.
- The AI is mock-only by default: every provider (symptom checker, diagnosis, summary, transcription, notification, storage, email) resolves to a `mock_*` implementation until real vendor implementations are written and selected via env vars.
- The QA system (`app/`) is not part of docker-compose — it runs separately with its own MongoDB and LLM env vars.

## One-sentence summary

Mirage is a demo of patient-owned medical records with consent-based doctor access and AI that assists but never decides — built on a deliberately replaceable architecture where the repo's namesake Medical QA System is meant to plug in as one of those replaceable AI providers.
