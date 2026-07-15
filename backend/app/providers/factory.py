"""Provider factory — resolves concrete provider instances by env vars."""

from __future__ import annotations

import os
from typing import Any

from app.providers.interfaces import (
    SymptomCheckerProvider,
    DiagnosisProvider,
    ClinicalSummaryProvider,
    TranscriptionProvider,
    NotificationProvider,
    StorageProvider,
    EmailProvider,
)
from app.providers.implementations.mock_symptom_checker import MockSymptomCheckerProvider
from app.providers.implementations.mock_diagnosis import MockDiagnosisProvider
from app.providers.implementations.mock_summary import MockClinicalSummaryProvider
from app.providers.implementations.mock_transcription import MockTranscriptionProvider
from app.providers.implementations.mock_notification import MockNotificationProvider
from app.providers.implementations.mock_storage import MockStorageProvider
from app.providers.implementations.mock_email import MockEmailProvider
from app.providers.implementations.local_ai_provider import LocalDiagnosisProvider, LocalSummaryProvider
from app.providers.implementations.local_transcription_provider import LocalTranscriptionProvider

_registry: dict[str, Any] = {}


def _env_name(key: str, default: str = "mock") -> str:
    return os.getenv(key, default).lower().strip()


def get_ai_provider() -> DiagnosisProvider:
    """Return the configured AI diagnosis provider singleton."""
    name = _env_name("AI_PROVIDER", "mock")
    key = f"ai:{name}"
    if key not in _registry:
        if name == "mock":
            _registry[key] = MockDiagnosisProvider()
        elif name == "local":
            _registry[key] = LocalDiagnosisProvider()
        else:
            raise ValueError(f"Unsupported AI_PROVIDER: {name}")
    return _registry[key]


def get_symptom_checker_provider() -> SymptomCheckerProvider:
    """Return the configured symptom-checker provider singleton."""
    name = _env_name("SYMPTOM_PROVIDER", "mock")
    key = f"symptom:{name}"
    if key not in _registry:
        if name == "mock":
            _registry[key] = MockSymptomCheckerProvider()
        else:
            raise ValueError(f"Unsupported SYMPTOM_PROVIDER: {name}")
    return _registry[key]


def get_summary_provider() -> ClinicalSummaryProvider:
    """Return the configured clinical-summary provider singleton."""
    name = _env_name("SUMMARY_PROVIDER", "mock")
    key = f"summary:{name}"
    if key not in _registry:
        if name == "mock":
            _registry[key] = MockClinicalSummaryProvider()
        elif name == "local":
            _registry[key] = LocalSummaryProvider()
        else:
            raise ValueError(f"Unsupported SUMMARY_PROVIDER: {name}")
    return _registry[key]


def get_transcription_provider() -> TranscriptionProvider:
    """Return the configured transcription provider singleton."""
    name = _env_name("TRANSCRIPTION_PROVIDER", "mock")
    key = f"transcription:{name}"
    if key not in _registry:
        if name == "mock":
            _registry[key] = MockTranscriptionProvider()
        elif name == "local":
            _registry[key] = LocalTranscriptionProvider()
        else:
            raise ValueError(f"Unsupported TRANSCRIPTION_PROVIDER: {name}")
    return _registry[key]


def get_notification_provider() -> NotificationProvider:
    """Return the configured notification provider singleton."""
    name = _env_name("NOTIFICATION_PROVIDER", "mock")
    key = f"notification:{name}"
    if key not in _registry:
        if name == "mock":
            _registry[key] = MockNotificationProvider()
        else:
            raise ValueError(f"Unsupported NOTIFICATION_PROVIDER: {name}")
    return _registry[key]


def get_storage_provider() -> StorageProvider:
    """Return the configured storage provider singleton."""
    name = _env_name("STORAGE_PROVIDER", "mock")
    key = f"storage:{name}"
    if key not in _registry:
        if name == "mock":
            _registry[key] = MockStorageProvider()
        else:
            raise ValueError(f"Unsupported STORAGE_PROVIDER: {name}")
    return _registry[key]


def get_email_provider() -> EmailProvider:
    """Return the configured email provider singleton."""
    name = _env_name("EMAIL_PROVIDER", "mock")
    key = f"email:{name}"
    if key not in _registry:
        if name == "mock":
            _registry[key] = MockEmailProvider()
        else:
            raise ValueError(f"Unsupported EMAIL_PROVIDER: {name}")
    return _registry[key]
