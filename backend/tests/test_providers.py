"""Tests for provider interfaces and mock implementations."""

from __future__ import annotations

import pytest

from app.providers.implementations.mock_symptom_checker import MockSymptomCheckerProvider
from app.providers.implementations.mock_diagnosis import MockDiagnosisProvider
from app.providers.implementations.mock_summary import MockClinicalSummaryProvider
from app.providers.implementations.mock_transcription import MockTranscriptionProvider
from app.providers.implementations.mock_notification import MockNotificationProvider
from app.providers.implementations.mock_storage import MockStorageProvider
from app.providers.implementations.mock_email import MockEmailProvider


# ---------------------------------------------------------------------------
# Symptom Checker
# ---------------------------------------------------------------------------
@pytest.mark.anyio
async def test_mock_symptom_checker_lifecycle():
    provider = MockSymptomCheckerProvider()
    await provider.initialize()
    assert await provider.validate()

    session_id = await provider.begin_session("patient-123")
    assert session_id

    result = await provider.submit_answer(session_id, "q1", "Yes")
    assert "next_question" in result or result.get("done") is not None

    assessment = await provider.get_assessment(session_id)
    assert assessment["triage_level"] in ("low", "medium", "high")
    assert "recommended_actions" in assessment


@pytest.mark.anyio
async def test_mock_symptom_checker_run():
    provider = MockSymptomCheckerProvider()
    result = await provider.run(patient_id="p1")
    assert result["success"] is True


# ---------------------------------------------------------------------------
# Diagnosis
# ---------------------------------------------------------------------------
@pytest.mark.anyio
async def test_mock_diagnosis_lifecycle():
    provider = MockDiagnosisProvider()
    await provider.initialize()
    assert await provider.validate()

    diagnoses = await provider.generate_differential(["fever", "cough"])
    assert 1 <= len(diagnoses) <= 5
    for d in diagnoses:
        assert "name" in d
        assert "confidence" in d
        assert 0 <= d["confidence"] <= 1


# ---------------------------------------------------------------------------
# Clinical Summary
# ---------------------------------------------------------------------------
@pytest.mark.anyio
async def test_mock_summary_lifecycle():
    provider = MockClinicalSummaryProvider()
    await provider.initialize()
    assert await provider.validate()

    soap = await provider.generate_soap_note(
        transcript="Patient complains of chest pain.",
        symptoms=["chest pain", "shortness of breath"],
    )
    assert "soap" in soap
    for section in ("subjective", "objective", "assessment", "plan"):
        assert section in soap["soap"]


# ---------------------------------------------------------------------------
# Transcription
# ---------------------------------------------------------------------------
@pytest.mark.anyio
async def test_mock_transcription_lifecycle():
    provider = MockTranscriptionProvider()
    await provider.initialize()
    assert await provider.validate()

    session_id = await provider.start_session()
    assert session_id

    await provider.send_audio(session_id, b"fake_audio_data")

    result = await provider.stop_session(session_id)
    assert result["status"] == "completed"
    assert len(result["segments"]) >= 1

    segments = [seg async for seg in provider.stream_transcript(session_id)]
    assert len(segments) == 2


# ---------------------------------------------------------------------------
# Notification
# ---------------------------------------------------------------------------
@pytest.mark.anyio
async def test_mock_notification_lifecycle():
    provider = MockNotificationProvider()
    await provider.initialize()
    assert await provider.validate()

    result = await provider.send(
        recipient_id="user-123",
        title="Test",
        body="Hello",
    )
    assert result["success"] is True
    assert result["recipient_id"] == "user-123"


# ---------------------------------------------------------------------------
# Storage
# ---------------------------------------------------------------------------
@pytest.mark.anyio
async def test_mock_storage_lifecycle():
    provider = MockStorageProvider()
    await provider.initialize()
    assert await provider.validate()

    upload_result = await provider.upload("test/file.txt", b"hello world", "text/plain")
    assert upload_result["success"] is True
    assert upload_result["size"] == 11

    data = await provider.download("test/file.txt")
    assert data == b"hello world"

    delete_result = await provider.delete("test/file.txt")
    assert delete_result["success"] is True


# ---------------------------------------------------------------------------
# Email
# ---------------------------------------------------------------------------
@pytest.mark.anyio
async def test_mock_email_lifecycle():
    provider = MockEmailProvider()
    await provider.initialize()
    assert await provider.validate()

    result = await provider.send_email(
        to="test@example.com",
        subject="Hello",
        body_text="Plain text body",
        body_html="<p>HTML body</p>",
    )
    assert result["success"] is True
    assert result["to"] == "test@example.com"


# ---------------------------------------------------------------------------
# Factory
# ---------------------------------------------------------------------------
def test_provider_factory_mock():
    from app.providers.factory import (
        get_ai_provider,
        get_symptom_checker_provider,
        get_summary_provider,
        get_transcription_provider,
        get_notification_provider,
        get_storage_provider,
        get_email_provider,
    )

    import os
    os.environ["AI_PROVIDER"] = "mock"
    os.environ["SYMPTOM_PROVIDER"] = "mock"
    os.environ["SUMMARY_PROVIDER"] = "mock"
    os.environ["TRANSCRIPTION_PROVIDER"] = "mock"
    os.environ["NOTIFICATION_PROVIDER"] = "mock"
    os.environ["STORAGE_PROVIDER"] = "mock"
    os.environ["EMAIL_PROVIDER"] = "mock"

    assert isinstance(get_ai_provider(), MockDiagnosisProvider)
    assert isinstance(get_symptom_checker_provider(), MockSymptomCheckerProvider)
    assert isinstance(get_summary_provider(), MockClinicalSummaryProvider)
    assert isinstance(get_transcription_provider(), MockTranscriptionProvider)
    assert isinstance(get_notification_provider(), MockNotificationProvider)
    assert isinstance(get_storage_provider(), MockStorageProvider)
    assert isinstance(get_email_provider(), MockEmailProvider)
