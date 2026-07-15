# Changelog

All notable changes to the Mirage platform will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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
