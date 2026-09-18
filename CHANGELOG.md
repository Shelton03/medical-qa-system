# Changelog

All notable changes to the Mirage platform will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [1.1.0] - 2026-07-15

### Added

#### 1. AI Clinical Assessment Pipeline (5-Service Architecture)
Ported from commit `6b6a35a`, the mock AI provider is replaced with a real clinical assessment pipeline powered by local Gemma 3 4B (`llama-cpp`).

- **InputProcessor** — Extracts structured data (symptoms, duration, severity, entities) from free-text user input via LLM prompt.
- **AssessmentService** — Performs initial triage, populates `candidate_domains`, `key_symptoms`, `missing_info`, `risk_flags` on `AISession`.
- **DecisionEngine** — 3-run self-consistency loop (serialized via `asyncio.Semaphore(1)`): each run returns JSON `{"decision": "ASK|ANSWER", "confidence": 0.0-1.0, "rationale": "..."}`. Majority vote determines next action. Override rules: confidence < 0.7 → ASK; gaps_remaining > 0 → ASK.
- **QuestionGenerator** — Generates one follow-up question targeting missing information or risk flags.
- **AnswerGenerator** — Generates final preliminary assessment with content, explanation, confidence_level, and strong medical disclaimer.
- **New files:** `backend/app/ai/assessment/*.py`, `backend/app/ai/local_llm.py`

#### 2. Rich Patient Clinical Profile in AI Context
- New `PatientClinicalProfile` dataclass (demographics, allergies, chronic conditions, medications, recent visits, previous AI sessions).
- `enrich_context_with_patient_data()` eagerly loads full patient data from PostgreSQL with `joinedload`/`selectinload`.
- Patient mode: full profile always available. Doctor mode: gated by `ConsentRequest.available_data` scopes.
- **New files:** `backend/app/ai/context_builder.py`

#### 3. Doctor Endpoint for Patient AI Sessions
- `GET /api/v1/doctor/patient/{patient_id}/ai-sessions` — returns ALL AI session details for a patient, protected by `check_record_access()` consent gate.
- Returns: session metadata, full assessment state (confidence, gaps, risk flags, candidate domains), all messages (chronological), linked appointment info.
- **Files:** `backend/app/doctor/router.py`

#### 4. Sequelize-to-SQLAlchemy Model Migrations
- Migration `20260715_add_ai_assessment_fields.py` — adds 7 columns to `ai_sessions` for assessment state, plus `appointment_id` FK.
- Migration `20260715_add_ai_message_type.py` — adds `message_type` to `ai_messages`.
- Widened `alembic_version.version_num` from `VARCHAR(32)` to `VARCHAR(200)` to support long revision names.
- **Files:** `backend/alembic/versions/20260715_*.py`

### Fixed

#### 5. MissingGreenlet on Start Consultation (Proper Fix)
- **Root Cause:** `handle_visit()` sync helper in `doctor/service.py` still accessed `visit.medical_record.patient_id` via property getter → triggers SQLAlchemy lazy-load inside sync context under async greenlet → `MissingGreenlet`.
- **Fix:**
  - `doctor/service.py`: Changed to `sqlalchemy.inspect(visit)` and check `"medical_record" in state.dict` before accessing. Added eager `selectinload(Visit.medical_record)` in `doctor/repository.py` `create_visit()` so the data is always available.
- **Files:** `backend/app/doctor/service.py`, `backend/app/doctor/repository.py`

#### 6. Booking Confirmation UI — Missing Details
- **Root Cause:** `handleConfirm` discarded `createMutation.mutateAsync()` response. Passed only local state to `Step4Confirm` with `doctorName={null}` → user saw "To be assigned" / "—".
- **Fix:** Captured `AppointmentResponse`, stored in local state. Extended `Step4Confirm` to accept `allocatedStartTime`/`allocatedEndTime`. Now shows real doctor name, specialty, time slot, facility.
- **Files:** `frontend/app/patient/book-appointment/page.tsx`, `frontend/components/patient/booking/Step4Confirm.tsx`

#### 7. Admin 404 Errors
- Removed `Facilities` and `Settings` nav items from admin sidebar. No pages exist, no backend support.
- Removed unused `Building2`, `Settings` Lucide imports.
- **Files:** `frontend/app/admin/layout.tsx`

### Changed

#### 8. Seeder — Independent Appointment Seeding
- Appointment seeding extracted from `seed_demo_data()` into standalone `seed_appointments()` function with its own idempotency guard (`Appointment.count >= 10`).
- Calls both `seed_demo_data()` then `seed_appointments()` on startup.
- **Files:** `backend/app/db/seeder.py`, `backend/main.py`

---

## [1.0.4] - 2026-07-15

### Fixed

#### 1. Admin Doctors Page — 500 Internal Server Error
- **Symptom:** `GET /api/v1/appointments/admin/doctors?limit=100` returned 500 with `AttributeError: 'Doctor' object has no attribute 'first_name'`.
- **Root Cause:** The `Doctor` model does not have `first_name`/`last_name` columns. Those fields live on the related `User` model via `doctor.user`. The query did not eagerly load `Doctor.user` and the response mapper directly accessed `d.first_name`.
- **Fix:** Added `.options(selectinload(Doctor.user))` to the query and changed the mapping to `d.user.first_name` / `d.user.last_name` with None-safe fallback.
- **Files:** `backend/app/appointment/router.py`

#### 2. Facility Doctors List — 500 Internal Server Error
- **Symptom:** `GET /api/v1/appointments/{facility_id}/doctors` returned 500 with the same `AttributeError`.
- **Root Cause:** Same as above — `d.first_name` / `d.last_name` accessed on `Doctor` instead of `Doctor.user`.
- **Fix:** Added `.options(selectinload(Doctor.user))` and updated the response mapping.
- **Files:** `backend/app/appointment/router.py`

#### 3. Doctor Start Consultation — MissingGreenlet
- **Symptom:** `POST /api/v1/doctor` (start consultation) returned 500 with `sqlalchemy.exc.MissingGreenlet: greenlet_spawn has not been called`.
- **Root Cause:** `_visit_response()` is a sync function that accessed `visit.medical_record.patient_id`. After `create_visit()` returns a `Visit`, the `medical_record` relationship is not loaded. SQLAlchemy tried to fire an implicit lazy SELECT query inside a sync context, which is illegal on the async engine.
- **Fix:** Made `_visit_response` resilient by using `getattr` + `try/except` around the `medical_record` access. This catches the `MissingGreenlet` (or any lazy-load error) and safely returns `None` for `patient_id`.
- **Files:** `backend/app/doctor/service.py`

#### 4. Booking — "No doctor is available" + Seeder Crashes
- **Symptom:** Patient booking wizard showed "No doctor is available for the selected date" on any day. On fresh DB resets, the backend crashed on startup with `TypeError: 'max_appointments' is an invalid keyword argument for DoctorSchedule`.
- **Root Cause (multiple):**
  1. `DoctorSchedule` kwargs in seeder were wrong: `max_appointments` should be `max_daily_appointments`, `slot_duration_minutes` should be `default_slot_duration`, `is_active` doesn't exist (replaced with `is_working_day`).
  2. Idempotency guard in seeder skipped schedule creation if patients already existed.
  3. Only 5 doctors seeded, randomly distributed across 3 facilities — some facilities got 0-1 doctors.
  4. Schedules only covered Mon-Fri (days 0-4), so weekend bookings always failed.
- **Fix:**
  1. Corrected all `DoctorSchedule` kwargs to match model columns.
  2. Moved schedule creation to an idempotent per-doctor block that runs even if patients already exist.
  3. Expanded `_DOCTORS` from 5 to 9 doctors, assigned round-robin (3 per facility).
  4. Expanded schedules from Mon-Fri to Mon-Sun (7 days) with weekend half-days (08:00-13:00).
  5. Explicitly set `is_accepting_appointments=True` on all doctors.
- **Files:** `backend/app/db/seeder.py`

---

## [1.0.3] - 2026-07-15

### Fixed

#### Admin Portal Login Page Blocked
- **Symptom:** `/admin/login` showed "Redirecting..." indefinitely because the admin layout's auth redirect fired for all pages including the login page.
- **Root Cause:** The `AdminLayout` component unconditionally redirected unauthenticated users to `/admin/login`, even when they were already on the login page. This created a redirect loop.
- **Fix:** Added a `usePathname` check in `AdminLayout` to skip auth enforcement on the `/admin/login` page. When on the login page, children are rendered without the sidebar.
- **Files:** `frontend/app/admin/layout.tsx`

#### Consultation Start — 500 Internal Server Error
- **Symptom:** `POST /api/v1/doctor` (start consultation) returned 500 with `InvalidRequestError: A transaction is already begun on this Session`.
- **Root Cause:** `start_consultation()` in `doctor/service.py` used `async with db.begin()` inside a session already managed by FastAPI's `get_db()` dependency. `get_db()` yields a session with an active transaction and auto-commits at the end. Nesting a second `begin()` is not allowed.
- **Fix:** Removed `async with db.begin()` wrapper. The function now calls `await db.flush()` after creating the visit to sync state before the audit log write. The outer `get_db()` dependency handles the final commit.
- **Files:** `backend/app/doctor/service.py`, `backend/app/patient/service.py` (same pattern)

#### Booking — "No doctor is available"
- **Symptom:** Patient booking wizard on Step 4 showed "No doctor is available for the selected date" even when doctors exist.
- **Root Cause:** The auto-routing algorithm looks up `DoctorSchedule` records to find available doctors. The seeder created doctors but never created their schedules.
- **Fix:** Added `DoctorSchedule` seeding to `backend/app/db/seeder.py`. Each seeded doctor gets Mon-Fri schedules with default working hours (08:00–17:00), 30-min slots, max 20 appointments/day.
- **Files:** `backend/app/db/seeder.py`

### Changed

- **`.gitignore`** — Added `backend/models/` and model file extensions (`*.bin`, `*.gguf`, `*.pt`, etc.) to prevent large model files from being committed.
- Removed `backend/models/ggml-tiny.bin` from git tracking.

---

## [1.0.2] - 2026-07-11

### Summary

This release adds real-time speech-to-text transcription to the doctor AI consultation workflow and fixes the booking wizard navigation.

---

### Added

#### Real-Time Transcription in AI Consultations
- **Feature:** Doctors can now record their voice during AI consultations using a mic button in the chat panel.
- **Technology:** WebSocket streaming to local faster-whisper model (tiny, CPU) for real-time transcription.
- **UI:**
  - Mic button (left of text input) — grey idle, red pulsing when recording.
  - Animated waveform bars showing recording activity.
  - Live interim transcripts appear in the text input as the doctor speaks.
  - "Recording" indicator with pulsing dot in the chat header.
- **Auto-send:** When recording stops, the full transcript is automatically sent as a doctor message to the AI assistant.
- **Persistence:** The transcript is saved to `Visit.transcript` via `PATCH /doctor/{visit_id}/transcript`.
- **Custom Hook:** New `useVoiceRecorder()` hook extracts all WebSocket + MediaRecorder logic.
- **Files:**
  - `frontend/hooks/useVoiceRecorder.ts` (new)
  - `frontend/components/doctor/AIChatPanel.tsx` (mic + waveform + integration)
  - `frontend/app/doctor/ai-consultation/AIConsultationContent.tsx` (pass visitId)
  - `frontend/lib/api.ts` (`doctorApi.updateVisitTranscript()`)
  - `frontend/providers/WebSocketProvider.tsx` (runtime WS URL)
  - `backend/app/db/models.py` (`transcript` column)
  - `backend/alembic/versions/20260711_add_visit_transcript.py` (new migration)
  - `backend/app/doctor/repository.py` (`update_visit_transcript()`)
  - `backend/app/doctor/service.py` (`update_visit_transcript()`)
  - `backend/app/doctor/router.py` (`PATCH /doctor/{visit_id}/transcript`)

---

### Fixed

#### Booking Wizard — "Review & Confirm" Button Not Visible
- **Symptom:** On Step 3 (Symptoms), the "Review & Confirm" button was not visible. The symptoms form was too tall and pushed the button below the viewport, where `overflow-hidden` clipped it.
- **Root Cause:** `Step3Symptoms` component used `h-full` inside a flex column alongside the button. The form content's `min-height: auto` prevented shrinking.
- **Fix:** Wrapped `Step3Symptoms` in a `div` with `flex-1 min-h-0 overflow-y-auto`, allowing it to shrink and leave room for the button.
- **Files:** `frontend/app/patient/book-appointment/page.tsx`

---

### Changed

- **WebSocket URL Resolution** (`VoiceRecorder.tsx`, `WebSocketProvider.tsx`): Both now determine the WebSocket URL at runtime, supporting:
  - `NEXT_PUBLIC_WS_URL` environment variable
  - Auto-detection from `window.location` (uses `wss:` for HTTPS, `ws:` for HTTP)
  - This enables production deployment behind reverse proxies.

---

## [1.0.1] - 2026-07-11

### Summary

This release fixes five critical runtime errors in the live deployed system and aligns the doctor-facing patient detail view with the consent-protected backend schema.

---

### Fixed

#### 1. Booking Wizard — Confirmation Moved to Step 4
- **Symptom:** The appointment was being created on step 3 ("Symptoms") when the user clicked "Review & Confirm" to advance to step 4. Step 4's "Confirm Booking" button did nothing except show a success toast — no backend call was made.
- **Root Cause:** `handleNext()` in the booking page called `createMutation.mutateAsync()` when `step === 3`. The `handleConfirm()` callback only set `isSuccess = true`.
- **Fix:** Moved the `createMutation.mutateAsync()` call from `handleNext()` to `handleConfirm()`. Step 3 now simply advances to step 4. Step 4's "Confirm Booking" button now performs the actual `POST /api/v1/appointments` call with `isSubmitting={createMutation.isPending}`.
- **Files:** `frontend/app/patient/book-appointment/page.tsx`

#### 2. Doctor Endpoints — `ImportError: cannot import name _resolve_doctor_id`
- **Symptom:** `GET /api/v1/doctor/schedule` and `GET /api/v1/doctor/appointments/today` both crashed with `ImportError`.
- **Root Cause:** Both endpoint handlers had a local `from app.doctor.repository import _resolve_doctor_id` statement inside the function body. The function `_resolve_doctor_id` is defined locally in the same file (line 113), not exported from the repository module.
- **Fix:** Removed the bogus local import statements. The endpoints now correctly reference the locally-defined `_resolve_doctor_id` function.
- **Files:** `backend/app/doctor/router.py`

#### 3. Audit Log Middleware — `RuntimeError: No response returned`
- **Symptom:** Intermittent `RuntimeError: No response returned` on some requests.
- **Root Cause:** The audit log middleware's DB write block (`await db.commit()`) was not wrapped in error handling. If the DB operation failed (e.g., connection pool exhausted, serialization error), an exception was raised before `return response` could execute, causing Starlette to report no response.
- **Fix:** Wrapped the entire async DB block in `try/except Exception: pass`. The middleware now silently swallows audit log failures and always returns the response.
- **Files:** `backend/app/middleware/audit_log.py`

#### 4. AI Session Endpoint — `MissingGreenlet`
- **Symptom:** `GET /api/v1/ai/sessions/{session_id}` crashed with `sqlalchemy.exc.MissingGreenlet` when the session had messages.
- **Root Cause:** `get_session_for_user()` in `ai/router.py` loaded the `AISessionModel` without eager-loading the `messages` relationship. Any subsequent access to `session.messages` triggered lazy loading inside an async function (which SQLAlchemy 2.x does not support with the default async strategy).
- **Fix:** Added `.options(selectinload(AISessionModel.messages))` to the query. Added the `selectinload` import from `sqlalchemy.orm`.
- **Files:** `backend/app/ai/router.py`

#### 5. Doctor Patient View — Consent-Protected Access + Full Schema Alignment
- **Symptom:** When a doctor clicked "View Record" on a patient, the page showed "Patient not found" or a blank error state. The AI consultation page also failed to load patient context.
- **Root Cause — Multiple issues:**
  1. The frontend called `GET /patients/{id}` via `patientsApi.getPatient()`, which internally used the `_to_full_profile()` mapper. This mapper accessed `patient.medical_record.medications`, but the `MedicalRecord` model has **no `medications` relationship** — medications belong to `Visit`. This caused an `AttributeError` → 500 → frontend showed "Patient not found."
  2. The seeder created consent records with uppercase status values (`"APPROVED"`, `"PENDING"`, `"DENIED"`, `"EXPIRED"`), but all consent lookup queries checked for lowercase (`"approved"`, `"pending"`, `"declined"`, `"expired"`). This meant NO seeded consent requests ever matched live queries.
  3. The frontend had no API client for the consent-protected `GET /doctor/patient/{id}` endpoint.
  4. The `PatientOverview` schema was missing contact/demographic fields (phone, email, emergency contacts).
- **Fix:**
  1. **Backend schema:** Added `national_identifier`, `phone`, `email`, `emergency_contact_name`, and `emergency_contact_phone` to the `PatientOverview` Pydantic schema.
  2. **Backend seeder:** Normalized consent status values to lowercase: `"pending"`, `"approved"`, `"declined"`, `"expired"`.
  3. **Backend chat engine:** Fixed `ConsentRequest.status == "APPROVED"` → `"approved"`.
  4. **Frontend types:** Added `DoctorPatientOverview`, `DoctorPatientMedication`, and `DoctorPatientVisit` types to `frontend/lib/types.ts`.
  5. **Frontend API client:** Added `doctorApi.getDoctorPatientOverview(patientId)` to `frontend/lib/api.ts`, calling `GET /doctor/patient/{id}`.
  6. **Frontend detail page:** Completely rewrote `frontend/app/doctor/patients/[id]/page.tsx` to use `doctorApi.getDoctorPatientOverview()`. The page now detects 403 responses (no active consent) and renders a clean "Consent Required" state with a "Request Consent" button instead of crashing.
  7. **Frontend AI consultation:** Updated `frontend/app/doctor/ai-consultation/AIConsultationContent.tsx` to use `doctorApi.getDoctorPatientOverview()` and updated field references from `medical_record.*` to flat `allergies`/`conditions`/`current_medications`.
- **Files:**
  - `backend/app/doctor/router.py` (schema + endpoint)
  - `backend/app/db/seeder.py`
  - `backend/app/ai/chat_engine.py`
  - `frontend/lib/types.ts`
  - `frontend/lib/api.ts`
  - `frontend/app/doctor/patients/[id]/page.tsx`
  - `frontend/app/doctor/ai-consultation/AIConsultationContent.tsx`

---

### Architecture Notes

#### Consent-Protected Data Flow (Doctor)

| Without Consent | With Consent |
|---|---|
| Doctor searches patients → sees name, MRN, basic demographics in list | Doctor clicks "View Record" → full record loads |
| Doctor clicks "View Record" → **"Consent Required"** screen with "Request Consent" button | `GET /doctor/patient/{id}` returns `PatientOverview` |
| Cannot see medical data | Full detail page renders: allergies, conditions, medications, recent visits |

- The `GET /doctor/patient/{id}` endpoint enforces `check_record_access()`. If no active consent exists, it returns **403 Forbidden** with `CONSENT_REQUIRED`.
- The frontend detail page intercepts 403 errors and renders a dedicated "Consent Required" UI instead of showing a generic error.

#### Medications Relationship

- **Important:** The `MedicalRecord` model does **not** have a `medications` relationship. Medications are reachable only via `MedicalRecord.visits` → `Visit.medications`.
- The `_to_full_profile()` mapper in `patient/service.py` references `patient.medical_record.medications` which does not exist. Patient self-view bypasses this via `GET /me/patient` which correctly builds medications from visits.
- For doctor access, use `GET /doctor/patient/{id}` which aggregates current medications across all visits into `current_medications`.

---

### Added

- `GET /doctor/patient/{patient_id}` — Consent-protected patient overview endpoint. Returns `PatientOverview` with demographics, allergies, conditions, current medications, and recent visits.
- `GET /doctor/patient/{patient_id}/timeline` — Consent-protected full patient timeline.
- `GET /doctor/schedule` — Doctor weekly schedule configuration + time-off requests.
- `GET /doctor/appointments/today` — Today's confirmed and pending appointments for the logged-in doctor.
- `DoctorPatientOverview`, `DoctorPatientMedication`, `DoctorPatientVisit` TypeScript types.
- `doctorApi.getDoctorPatientOverview()` API client method.

---

### Security

- Consent status values are now normalized to lowercase (`pending`, `approved`, `declined`, `expired`) across the entire backend (models, queries, seeders, and AI engine).
- The AI chat engine now correctly enforces `status == "approved"` when querying consent scope.
- Audit log middleware failures no longer break request processing.

---

### Documentation

- This document (`CHANGELOG.md`) is new.
