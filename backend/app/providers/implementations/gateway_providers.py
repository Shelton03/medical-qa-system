"""Gateway provider implementations that route all model calls through ccaimex."""

from __future__ import annotations

import json
import logging
import tempfile
from typing import Any

import httpx

from app.ai.gateway_provider import GatewayAIProvider
from app.ai.provider import AIContext, AIMessage
from app.core.config import settings
from app.providers.interfaces.diagnosis import DiagnosisProvider
from app.providers.interfaces.summary import ClinicalSummaryProvider
from app.providers.interfaces.transcription import TranscriptionProvider

logger = logging.getLogger(__name__)


from datetime import datetime, timezone


def _now() -> datetime:
    return datetime.now(timezone.utc)


class _GatewayChatMixin:
    """Reusable gateway chat client for diagnosis/summary providers."""

    def __init__(self) -> None:
        self._chat = GatewayAIProvider()

    async def _complete(self, prompt: str, max_tokens: int = 1024, temperature: float = 0.2) -> str:
        message = AIMessage(role="user", content=prompt, timestamp=_now())
        return await self._chat.generate_response([message], AIContext())


class GatewayDiagnosisProvider(DiagnosisProvider, _GatewayChatMixin):
    """Differential-diagnosis provider backed by the ccaimex gateway."""

    async def initialize(self) -> None:
        pass

    async def validate(self, **params: Any) -> bool:
        return True

    async def execute(self, **params: Any) -> dict[str, Any]:
        symptoms = params.get("symptoms", [])
        context = params.get("patient_context")
        diagnoses = await self.generate_differential(symptoms, context)
        return {"diagnoses": diagnoses}

    async def generate_differential(
        self,
        symptoms: list[str],
        patient_context: dict[str, Any] | None = None,
    ) -> list[dict[str, Any]]:
        patient_context = patient_context or {}
        age = patient_context.get("age", "unknown")
        gender = patient_context.get("gender", "unknown")
        prompt = (
            "You are a clinical decision support tool. A patient presents with the following symptoms: "
            f"{', '.join(symptoms)}. "
            f"Demographics: {age}y/o {gender}. "
            "Return a ranked differential diagnosis as a JSON array of objects with keys: "
            "name, confidence (0.0-1.0), reasoning, recommended_investigations (array of strings), "
            "medication_warnings (array of strings). "
            "Do not include any commentary outside the JSON."
        )
        raw = await self._complete(prompt, max_tokens=1024, temperature=0.2)
        raw = raw.strip().strip("`").replace("json", "", 1).strip()
        try:
            parsed = json.loads(raw)
            if isinstance(parsed, list):
                return [
                    {
                        "name": str(item.get("name", "Unknown")),
                        "confidence": max(0.0, min(1.0, float(item.get("confidence", 0.5)))),
                        "reasoning": str(item.get("reasoning", "")),
                        "recommended_investigations": list(item.get("recommended_investigations", [])),
                        "medication_warnings": list(item.get("medication_warnings", [])),
                    }
                    for item in parsed
                    if isinstance(item, dict)
                ]
        except (json.JSONDecodeError, ValueError) as exc:
            logger.warning("GatewayDiagnosisProvider failed to parse JSON: %s", exc)
        return [
            {
                "name": "Unspecified diagnosis",
                "confidence": 0.5,
                "reasoning": raw,
                "recommended_investigations": [],
                "medication_warnings": [],
            }
        ]


class GatewaySummaryProvider(ClinicalSummaryProvider, _GatewayChatMixin):
    """Clinical-summary/SOAP provider backed by the ccaimex gateway."""

    async def initialize(self) -> None:
        pass

    async def validate(self, **params: Any) -> bool:
        return True

    async def execute(self, **params: Any) -> dict[str, Any]:
        return await self.generate_soap_note(
            transcript=params.get("transcript"),
            symptoms=params.get("symptoms"),
            diagnoses=params.get("diagnoses"),
        )

    async def generate_soap_note(
        self,
        transcript: str | None = None,
        symptoms: list[str] | None = None,
        diagnoses: list[dict[str, Any]] | None = None,
    ) -> dict[str, Any]:
        symptoms_str = ", ".join(symptoms) if symptoms else "None provided"
        diagnoses_str = json.dumps(diagnoses, indent=2) if diagnoses else "None provided"
        prompt = (
            "You are a clinical documentation assistant. Generate a concise SOAP note from the following data.\n\n"
            f"Transcript: {transcript or 'N/A'}\n"
            f"Symptoms: {symptoms_str}\n"
            f"Diagnoses: {diagnoses_str}\n\n"
            "Return the SOAP note as a JSON object with keys: subjective, objective, assessment, plan. "
            "Do not include commentary outside the JSON."
        )
        raw = await self._complete(prompt, max_tokens=1024, temperature=0.2)
        raw = raw.strip().strip("`").replace("json", "", 1).strip()
        sections = {"subjective": "", "objective": "", "assessment": "", "plan": ""}
        try:
            parsed = json.loads(raw)
            if isinstance(parsed, dict):
                for key in sections:
                    sections[key] = str(parsed.get(key, "")).strip()
        except (json.JSONDecodeError, ValueError) as exc:
            logger.warning("GatewaySummaryProvider failed to parse JSON: %s", exc)
            sections["subjective"] = raw
        return {"soap": sections, "diagnoses": diagnoses or [], "symptoms": symptoms or []}


class GatewayTranscriptionProvider(TranscriptionProvider):
    """Transcription provider backed by the ccaimex gateway audio endpoint."""

    def __init__(self) -> None:
        self._http: httpx.AsyncClient | None = None
        self._sessions: dict[str, bytearray] = {}

    def _client(self) -> httpx.AsyncClient:
        if self._http is None:
            if not settings.llm_gateway_url:
                raise RuntimeError("LLM_GATEWAY_URL is not configured")
            headers = {}
            if settings.llm_gateway_api_key:
                headers["Authorization"] = f"Bearer {settings.llm_gateway_api_key}"
            self._http = httpx.AsyncClient(
                base_url=settings.llm_gateway_url.rstrip("/"),
                headers=headers,
                timeout=120.0,
            )
        return self._http

    async def initialize(self) -> None:
        pass

    async def validate(self, **params: Any) -> bool:
        return True

    async def execute(self, **params: Any) -> dict[str, Any]:
        audio = params.get("audio")
        language = params.get("language", "en")
        if audio is None:
            return {"success": False, "error": "Missing audio parameter."}
        text = await self.transcribe(audio, language)
        return {"success": True, "text": text}

    async def transcribe(self, audio_path_or_bytes: str | bytes, language: str = "en") -> str:
        if isinstance(audio_path_or_bytes, str):
            with open(audio_path_or_bytes, "rb") as f:
                audio_bytes = f.read()
        else:
            audio_bytes = audio_path_or_bytes

        fd, tmp_path = tempfile.mkstemp(suffix=".webm")
        try:
            with open(fd, "wb") as f:
                f.write(audio_bytes)
            with open(tmp_path, "rb") as f:
                files = {"file": ("audio.webm", f, "audio/webm")}
                data = {"model": settings.transcription_model, "language": language}
                resp = await self._client().post("/v1/audio/transcriptions", files=files, data=data)
            resp.raise_for_status()
            return resp.json().get("text", "").strip()
        except Exception as exc:
            logger.error("Gateway transcription failed: %s", exc)
            return ""
        finally:
            import os
            try:
                os.unlink(tmp_path)
            except OSError:
                pass

    async def start_session(self) -> str:
        session_id = __import__("uuid").uuid4().hex
        self._sessions[session_id] = bytearray()
        return session_id

    async def send_audio(self, session_id: str, audio_chunk: bytes) -> None:
        buf = self._sessions.get(session_id)
        if buf is None:
            raise ValueError("Session not found.")
        buf.extend(audio_chunk)

    async def stop_session(self, session_id: str) -> dict[str, Any]:
        buf = self._sessions.pop(session_id, bytearray())
        text = await self.transcribe(bytes(buf))
        return {
            "session_id": session_id,
            "status": "completed",
            "text": text,
            "segments": [{"speaker": "Unknown", "text": text, "timestamp": ""}],
        }

    async def stream_transcript(self, session_id: str):
        buf = self._sessions.get(session_id)
        if not buf or len(buf) == 0:
            return
        text = await self.transcribe(bytes(buf))
        if text:
            yield {"speaker": "Unknown", "text": text, "timestamp": ""}
