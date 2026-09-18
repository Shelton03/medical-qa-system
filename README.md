# Mirage

<p align="center">
  <img src="assets/logo-light.svg" alt="Mirage — Clarity in Healthcare" width="320">
</p>

**Mirage** is a healthcare platform designed to improve patient-doctor interactions through secure, real-time collaboration and AI-assisted clinical workflows. Built as a Healthathon demonstration platform, Mirage showcases a production-quality architecture ready for future expansion.

---

## Architecture Overview

Mirage follows a clean five-layer architecture:

```
┌──────────────────────────────────────┐
│         Next.js 14+ Frontend         │
│  Patient App (PhoneFrame) │ Doctor   │
│  Portal (Desktop-first)              │
└──────────────────────────────────────┘
                  │ REST + WebSockets
                  ▼
┌──────────────────────────────────────┐
│         FastAPI Backend (Python)     │
│  Auth │ API │ Services │ AI Layer (Local Gemma 3 4B)  │
└──────────────────────────────────────┘
                  │
     ┌────────────┴────────────┐
     ▼                         ▼
  PostgreSQL                 Redis
  (UUID PKs, UTC)      (Cache / Events)
```

- **Patient Application** — Mobile-first web app rendered inside a realistic `PhoneFrame` simulator.
- **Doctor Portal** — Desktop-first clinical dashboard with responsive layouts.
- **Split-screen Demo Mode** — Side-by-side patient and doctor views for live demonstrations.
- **AI Clinical Assessment Pipeline** — 5-service architecture (InputProcessor, AssessmentService, DecisionEngine with 3-run self-consistency, QuestionGenerator, AnswerGenerator) powered by local Gemma 3 4B via llama-cpp. Replaces mock provider. Symptom checking with structured triage and risk-flag detection.
- **Consent-Gated Clinical Data Access** — Doctor AI context is enriched with `PatientClinicalProfile` (allergies, conditions, medications, visits) only after patient consent is approved via `ConsentRequest` record.

---

## Services & Ports

| Service   | Port | Description                           |
|-----------|------|---------------------------------------|
| Frontend  | 3000 | Static chat UI (nginx)                |
| Backend   | 8001 | FastAPI server (auto-reload)          |
| PostgreSQL| 5433 | Persistent database (`mirage_dev`)    |
| Redis     | 6379 | Cache, Pub/Sub, event broker          |
| MinIO     | 9000 | S3-compatible object storage          |

---

## Quick Start

```bash
# 1. Clone & configure
cp .env.example .env

# 2. Build & launch
make build && make up

# 3. (Optional) Run migrations
make migrate
```

The application will be available at:
- **Frontend** → http://localhost:3000
- **Backend API** → http://localhost:8001
- **API Docs** → http://localhost:8001/docs

---

## AI Assessment Pipeline

Mirage v1.1.0 replaces the mock AI provider with a real local LLM-powered clinical assessment pipeline.

### Architecture

The pipeline runs through 5 services in sequence:

1. **InputProcessor** — Extracts structured symptoms, duration, severity from free-text patient messages.
2. **AssessmentService** — Runs initial triage via LLM prompt, populates `candidate_domains`, `key_symptoms`, `missing_info`, `risk_flags`.
3. **DecisionEngine** — 3-run self-consistency loop (majority vote) decides "ASK" or "ANSWER". Override: confidence < 0.7 = ASK, gaps_remaining > 0 = ASK.
4. **QuestionGenerator** — Generates one follow-up question targeting gaps or risk flags.
5. **AnswerGenerator** — Produces preliminary assessment with content, explanation, disclaimer, and confidence level.

### Constraints

- **Local Gemma 3 4B** (`gemma-3-4b-it-Q4_K_M.gguf`, 2.8GB) loaded via `llama-cpp`
- **Inference is CPU-only** — serialized via `asyncio.Semaphore(1)`, ~1-2s per call
- **Self-consistency adds ~3-6s** on first assessment (3 sequential runs)
- **Medical disclaimer required** on all generated answers

---

## Common Commands

| Command           | Description                            |
|-------------------|----------------------------------------|
| `make build`      | Build all Docker images                |
| `make up`         | Start the full stack                   |
| `make down`       | Stop and remove containers             |
| `make logs`       | Follow container logs                  |
| `make migrate`    | Run Alembic migrations (`upgrade head`)|
| `make shell-backend` | Open a shell in the backend container |
| `make test`       | Run the migration smoke test           |

---

## Technology Stack

- **Backend:** Python 3.12+, FastAPI, SQLAlchemy 2.x, Alembic, asyncpg, Pydantic
- **Frontend:** HTML5 / vanilla JavaScript served by nginx
- **Database:** PostgreSQL 16+
- **Object Storage:** MinIO (S3-compatible)
- **Cache / Events:** Redis 7
- **Authentication:** JWT
- **Infrastructure:** Docker, Docker Compose

---

## Development Notes

- PostgreSQL is the only database — no MongoDB references anywhere.
- All Python code requires strict type hints.
- UUID v4 is used for every primary key.
- Timestamps are stored in UTC.
- Environment variables live in `.env` (never commit secrets).

---

## Demonstration Context

This repository was built as part of a **Healthathon** event to demonstrate modern healthcare software architecture, real-time consent workflows, AI-assisted clinical tools, and responsive mobile simulation. While functional, it is intended as a foundation for future production expansion.
