"""Appointment booking system enums."""

from enum import Enum


class AppointmentStatus(str, Enum):
    PENDING = "PENDING"
    CONFIRMED = "CONFIRMED"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"
    NO_SHOW = "NO_SHOW"


class Priority(str, Enum):
    EMERGENCY = "EMERGENCY"
    URGENT = "URGENT"
    NORMAL = "NORMAL"
    LOW = "LOW"


class TimeOffType(str, Enum):
    LEAVE = "LEAVE"
    SICK = "SICK"
    TRAINING = "TRAINING"
    OTHER = "OTHER"


class TimeOffStatus(str, Enum):
    PENDING = "PENDING"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"


class CancellationBy(str, Enum):
    PATIENT = "PATIENT"
    DOCTOR = "DOCTOR"
    SYSTEM = "SYSTEM"
