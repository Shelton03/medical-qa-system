# Mirage Real-Time Transcription

Version: 1.0

---

# Overview

The real-time transcription feature allows doctors to record and transcribe patient consultations using speech-to-text technology. The transcript is streamed live into the AI consultation interface, automatically sent as a message to the AI assistant, and persisted to the visit record for future reference.

---

# Architecture

## Backend

- **WebSocket Endpoint:** `/ws/transcription`
  - Accepts binary audio chunks (webm/opus format)
  - Buffers chunks, flushes to faster-whisper for transcription
  - Streams partial (`is_final: false`) and final (`is_final: true`) transcripts
  - Auth via JWT in query parameter

- **Provider:** `LocalTranscriptionProvider` using `faster-whisper` (tiny model on CPU)
  - Lazy model loading from `/app/models`
  - Supports English by default
  - Runs in background thread to avoid blocking WebSocket

- **REST Endpoint:** `PATCH /doctor/{visit_id}/transcript`
  - Persists the full transcript to the `Visit.transcript` column
  - Checks that the requesting doctor owns the visit

- **Configuration:**
  - `TRANSCRIPTION_PROVIDER=local` (or `mock` for testing)
  - `NEXT_PUBLIC_WS_URL` — frontend WebSocket base URL

## Frontend

- **Custom Hook:** `useVoiceRecorder()`
  - Manages MediaRecorder lifecycle
  - Connects to `/ws/transcription?token=JWT`
  - Returns `{ recording, liveText, finalText, startRecording, stopRecording }`
  - Calls `onTranscript(text)` callback when `is_final: true`

- **Integration:** `AIChatPanel.tsx`
  - Mic button (left of text input)
  - Red pulsing icon + animated waveform bars while recording
  - Live text shown in textarea as it's transcribed
  - Full transcript auto-sent as a doctor message when recording stops
  - Transcript persisted via `PATCH /doctor/{visit_id}/transcript`

---

# User Flow

1. **Doctor clicks mic icon** in AI consultation chat panel.
2. **Browser requests microphone permission** and starts MediaRecorder (100ms chunks).
3. **WebSocket opens** to `/ws/transcription?token=<JWT>`.
4. **Doctor speaks** — audio chunks stream to backend.
5. **Interim transcripts** appear live in the text input field.
6. **Doctor clicks mic again** to stop recording.
7. **Final transcript** is auto-sent as a chat message to the AI assistant.
8. **Transcript is saved** to `Visit.transcript` via PATCH endpoint.
9. **AI responds** to the transcript content.

---

# Data Flow

```
Doctor (browser)
  → getUserMedia({ audio: true })
  → MediaRecorder.start(100ms)
  → WebSocket binary chunks → /ws/transcription
  
Backend (faster-whisper)
  → Buffer chunks
  → Transcribe audio
  → JSON { text, is_final } → WebSocket
  
Frontend (AIChatPanel)
  → onTranscript(finalText)
  → auto-send to aiApi.sendMessageStream()
  → PATCH /doctor/{visit_id}/transcript (persist)
```

---

# Database Schema

### Visit Table (updated)

```
transcript: TEXT (nullable)
```

Stores the complete consultation transcript. Populated when a doctor records and stops voice input during an AI consultation.

---

# API Endpoints

| Method | Path | Auth | Description |
|---|---|---|---|
| WS | `/ws/transcription` | JWT query param | Real-time streaming transcription |
| PATCH | `/doctor/{visitId}/transcript` | Doctor JWT | Save transcript to visit record |

---

# Configuration

### Environment Variables

| Variable | Default | Description |
|---|---|---|
|`NEXT_PUBLIC_WS_URL`|`ws://localhost:8000/ws`|Frontend WebSocket base URL|
|`TRANSCRIPTION_PROVIDER`|`mock`|Backend provider: `local` (Whisper) or `mock` (synthetic)|

### WebSocket URL Resolution

Frontend determines the WebSocket URL at runtime:

```typescript
function getWsBase(): string {
  if (process.env.NEXT_PUBLIC_WS_URL) return process.env.NEXT_PUBLIC_WS_URL;
  const protocol = window.location.protocol === "https:" ? "wss:" : "ws:";
  return `${protocol}//${window.location.host}`;
}
```

For transcription: `${getWsBase()}/transcription?token=<JWT>`

---

# Implementation Notes

- **No pause detection** — recording stops only when the doctor manually clicks the mic icon again.
- **Real-time display** — interim transcripts update the text input, but messages are only sent on final transcript.
- **Error resilience** — WebSocket errors are logged; recording cleanup happens on unmount.
- **SSR safe** — `window` access is guarded with `typeof window !== "undefined"` checks.

---

# Files Modified/Created

- `backend/app/db/models.py` — Added `transcript` column to Visit
- `backend/alembic/versions/20260711_add_visit_transcript.py` — Migration
- `backend/app/doctor/repository.py` — `update_visit_transcript()`
- `backend/app/doctor/service.py` — `update_visit_transcript()` with ownership check
- `backend/app/doctor/router.py` — `PATCH /doctor/{visit_id}/transcript`
- `frontend/hooks/useVoiceRecorder.ts` — New custom hook
- `frontend/components/doctor/AIChatPanel.tsx` — Mic button + transcription integration
- `frontend/app/doctor/ai-consultation/AIConsultationContent.tsx` — Pass `visitId`
- `frontend/providers/WebSocketProvider.tsx` — Runtime WS URL resolution
- `frontend/lib/api.ts` — `doctorApi.updateVisitTranscript()`

---

# Security Considerations

- Audio data never leaves the server — local Whisper model processes everything.
- JWT token is transmitted in the WebSocket URL query parameter (browser limitation — custom headers not supported for WS handshake).
- Transcript is only accessible to the assigned doctor via ownership check.
