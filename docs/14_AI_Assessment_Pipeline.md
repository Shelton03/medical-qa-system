# AI Clinical Assessment Pipeline

## Overview

The AI Clinical Assessment Pipeline replaces the legacy mock provider introduced in earlier versions. Its purpose is to perform structured clinical triage using a local large language model (LLM), guiding patients through a conversational symptom checker and producing a preliminary assessment for clinical review.

The pipeline follows a state-machine-driven flow: each user message is processed, assessed, and either generates a follow-up question or produces a final preliminary answer.

---

## Architecture Diagram

```
User Message
      │
      ▼
┌─────────────────┐
│  InputProcessor │ ← Extracts structured data from free text
└────────┬────────┘
         │ dict with symptoms, duration, severity, entities
         ▼
┌──────────────────┐
│ AssessmentService│ ← Runs initial triage once per session
└────────┬─────────┘
         │ full assessment state
         ▼
┌──────────────────┐
│  DecisionEngine  │ ← 3× LLM self-consistency vote
│   (3 runs)       │
└────────┬─────────┘
         │ decision: ASK or ANSWER
    ┌────┴────┐
    ▼         ▼
[  ASK  ]  [ ANSWER ]
    │         │
    ▼         ▼
┌──────────┐  ┌─────────────┐
│Question  │  │Answer       │
│Generator │  │Generator    │
└──────────┘  └─────────────┘
```

---

## Services

### 1. InputProcessor

**Purpose**
Extract structured clinical data from free-text user messages.

**Implementation**
- Sends the raw message to the local LLM with a prompt that asks for a strictly formatted JSON response.
- Prompt fields requested:
  - `symptoms`: list of reported symptoms
  - `duration`: how long symptoms have been present
  - `severity`: patient-reported severity level
  - `entities`: additional clinical entities mentioned (e.g., medications, triggers)

**Output**
A Python `dict` consumed by the `AssessmentService`.

**File**
`backend/app/ai/assessment/input_processor.py`

---

### 2. AssessmentService

**Purpose**
Perform initial triage based on structured input and persist the result to the session.

**Implementation**
- Uses the structured input from `InputProcessor`.
- Prompts the LLM to return JSON with:
  - `candidate_domains`: possible clinical domains
  - `key_symptoms`: normalized list of key symptoms
  - `missing_info`: list of information still needed
  - `risk_flags`: any red flags or urgent indicators
- Guard: only executes once per session. Checks `if not session.assessment_done`.

**Persistence**
Updates the following `AISessionModel` columns:
- `candidate_domains`
- `key_symptoms`
- `missing_info`
- `risk_flags`
- `assessment_done`
- `gaps_remaining`

**File**
`backend/app/ai/assessment/assessment_service.py`

---

### 3. DecisionEngine

**Purpose**
Determine whether the pipeline should **ASK** (request more information) or **ANSWER** (generate a preliminary assessment), using a self-consistency voting mechanism.

**Algorithm (Self-Consistency)**

1. Build a prompt that includes the current assessment state (symptoms, risk flags, missing info, conversation history).
2. Run the LLM **3 times** (serialized by `asyncio.Semaphore`).
3. Parse each JSON response:
   ```json
   {
     "decision": "ASK|ANSWER",
     "confidence": 0.92,
     "rationale": " Critical red flag identified; enough data to proceed."
   }
   ```
4. Count votes: majority decision wins (ASK vs ANSWER).
5. Average `confidence` across all 3 runs.
6. Apply override rules:
   - If `avg_confidence < CONFIDENCE_THRESHOLD` (default `0.7`) → force **ASK**
   - If `gaps_remaining > 0` → force **ASK**

**Persistence**
- Stores the averaged confidence in `session.confidence`.

**File**
`backend/app/ai/assessment/decision_engine.py`

---

### 4. QuestionGenerator

**Purpose**
Generate a single, concise follow-up question when the `DecisionEngine` returns **ASK**.

**Implementation**
- Uses:
  - `session.missing_info`
  - `session.risk_flags`
  - existing conversation history
- Prompt instructs the LLM to “Generate ONE concise follow-up question...” targeting the most critical missing piece of information.

**Output**
A single question string returned to the user.

**File**
`backend/app/ai/assessment/question_generator.py`

---

### 5. AnswerGenerator

**Purpose**
Produce the final preliminary assessment when the `DecisionEngine` returns **ANSWER**.

**Implementation**
- Uses:
  - `risk_flags`
  - `session.confidence`
  - full conversation history
- Prompt asks the LLM for JSON with:
  - `content`: the assessment text
  - `explanation`: brief reasoning
  - `disclaimer`: mandatory medical disclaimer
  - `confidence_level`: high/medium/low

**Resilience**
- If JSON parsing fails, a structured **fallback answer** is returned that includes a strong medical disclaimer and advises the patient to consult a clinician.

**File**
`backend/app/ai/assessment/answer_generator.py`

---

## LLM Integration

### Local Model

| Property       | Value                                      |
|----------------|--------------------------------------------|
| Model          | Gemma 3 4B (Google)                        |
| Quantization   | Q4_K_M (~2.8 GB)                           |
| Path           | `/app/models/gemma-3-4b-it-Q4_K_M.gguf`    |
| Library        | llama-cpp via `local_ai_provider._get_llama()` |
| Context Window | 4096 tokens                                |

### Serialization

Inference is serialized to prevent concurrent model usage:
- `asyncio.Semaphore(1)` in `local_llm.py` ensures only one prompt runs at a time.
- `asyncio.to_thread()` executes llama-cpp inference in a thread pool, preventing event-loop blocking.

### Performance

| Step                  | Latency (CPU) |
|-----------------------|---------------|
| Single prompt         | ~1–2 s        |
| DecisionEngine (3×)   | ~3–6 s        |

The frontend displays **“Analyzing symptoms...”** during any pipeline step that invokes the LLM.

---

## Context Enrichment

### PatientClinicalProfile

A `PatientClinicalProfile` dataclass was added to `AIContext` to ground LLM decisions in real patient history.

**Fields**
- `demographics`
- `allergies`
- `chronic_conditions`
- `current_medications`
- `recent_visits`
- `previous_ai_sessions`

**Loading Strategy**
- Eagerly loaded via SQLAlchemy `joinedload` / `selectinload` in `context_builder.py`.
- **Patient mode**: full profile is always available (patient owns their data).
- **Doctor mode**: profile access is gated by `ConsentRequest.available_data` scopes. Only fields explicitly consented to are included in the context.

### Consent Model

| Scenario                            | Consent Required |
|-------------------------------------|------------------|
| Patient self-assessment (symptom checker) | **No**           |
| Doctor viewing patient AI sessions  | **Yes** — `check_record_access()` enforces an active consent record with `status="approved"` |
| Doctor AI context enrichment        | **Partial** — profile limited to consent scopes |

---

## Session-to-Appointment Linking

When a patient creates an AI session via the symptom checker, the system attempts to link the session to an upcoming appointment automatically.

**Linking Logic**
1. Query the `appointments` table for the earliest record where:
   - `patient_id = current_patient_id`
   - `status = "CONFIRMED"`
   - `appointment_date >= today`
2. If found:
   - `AISession.appointment_id` ← appointment UUID
   - `AISession.doctor_id` ← appointment’s physician

This linkage enables doctor endpoints to retrieve AI sessions for their own patients.

---

## Database Schema

### `ai_sessions` (existing + new columns)

| Column            | Type     | Description                                    |
|-------------------|----------|------------------------------------------------|
| `assessment_done` | boolean  | Whether initial triage has been performed      |
| `confidence`      | float    | Averaged decision confidence (0.0–1.0)         |
| `gaps_remaining`  | integer  | Number of missing-info gaps still open         |
| `candidate_domains`| JSONB   | List of possible clinical domains              |
| `key_symptoms`    | JSONB    | Normalized key symptoms                        |
| `missing_info`    | JSONB    | Information gaps identified by AssessmentService |
| `risk_flags`      | JSONB    | Detected red flags / urgent indicators         |
| `appointment_id`  | UUID FK  | → `appointments.id`                            |

### `ai_messages` (new column)

| Column        | Type        | Description                          |
|---------------|-------------|--------------------------------------|
| `message_type`| varchar, nullable | `"question"` or `"answer"`         |

---

## API Endpoints

### Patient

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/v1/patient/ai-sessions` | Create a new AI session (auto-links to upcoming appointment) |
| `POST` | `/api/v1/patient/ai-sessions/{id}/messages` | Send a message; triggers the full assessment pipeline |
| `GET`  | `/api/v1/patient/ai-sessions/{id}` | Retrieve session metadata and all messages |

### Doctor

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET`  | `/api/v1/doctor/patient/{patient_id}/ai-sessions` | Returns all AI sessions for the patient, including full assessment details and messages. Access is consent-protected: active approved consent must exist between the doctor and the patient. |

---

## Frontend UX

### AIChatPanel Updates

The `AIChatPanel` component renders pipeline results with clear visual hierarchy:

- **Loading state**
  - Displays **“Analyzing symptoms...”** while any LLM call is in progress.

- **Question messages**
  - Rendered with a blue **“Follow-up Question”** badge to distinguish them from patient messages.

- **Answer messages**
  - **Confidence badge**: color-coded by level
    - Green → high confidence
    - Yellow → medium confidence
    - Red → low confidence
  - **Risk flags**: displayed in a red alert box if any red flags were detected
  - **Explanation**: collapsible section with the model’s reasoning
  - **Disclaimer**: shown in muted text beneath the assessment content

---

## Files

### Backend — Pipeline Core

- `backend/app/ai/local_llm.py`
- `backend/app/ai/assessment/__init__.py`
- `backend/app/ai/assessment/input_processor.py`
- `backend/app/ai/assessment/assessment_service.py`
- `backend/app/ai/assessment/decision_engine.py`
- `backend/app/ai/assessment/question_generator.py`
- `backend/app/ai/assessment/answer_generator.py`

### Backend — Context & Routing

- `backend/app/ai/context_builder.py`
- `backend/app/ai/chat_engine.py`
- `backend/app/ai/router.py`
- `backend/app/ai/factory.py`
- `backend/app/ai/local_llm_provider.py`

### Backend — Doctor Endpoint

- `backend/app/doctor/router.py`

### Backend — Database & Migrations

- `backend/app/db/models.py`
- `backend/alembic/versions/20260715_add_ai_assessment_fields.py`
- `backend/alembic/versions/20260715_add_ai_message_type.py`

### Frontend

- `frontend/components/doctor/AIChatPanel.tsx`
- `frontend/lib/types.ts`
