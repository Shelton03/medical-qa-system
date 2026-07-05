/**
 * Mirage API Types
 *
 * Shared type definitions for the frontend API layer.
 * Mirror the backend Envelope format and domain models.
 */

// ------------------------------------------------------------------
// Standard Response Envelope
// ------------------------------------------------------------------

export interface ApiError {
  code: string;
  message: string;
  field?: string;
}

export interface ApiMeta {
  requestId: string;
  timestamp: string;
  page?: number;
  pageSize?: number;
  total?: number;
  totalPages?: number;
}

export interface ApiEnvelope<T> {
  success: boolean;
  data: T | null;
  errors: ApiError[];
  meta: ApiMeta;
}

// ------------------------------------------------------------------
// Authentication
// ------------------------------------------------------------------

export type UserRole = "doctor" | "patient" | "admin";

export interface UserProfile {
  id: string;
  role: UserRole;
  firstName: string;
  lastName: string;
  email: string;
  avatarUrl: string | null;
}

export interface LoginResponse {
  accessToken: string;
  refreshToken: string;
  expiresIn: number;
  user: UserProfile;
}

export interface DoctorProfile extends UserProfile {
  role: "doctor";
  registrationNumber: string;
  specialty: string;
  facilityId: string;
}

export interface PatientProfile extends UserProfile {
  role: "patient";
  medicalRecordNumber: string;
  dateOfBirth: string;
  gender: string;
}

// ------------------------------------------------------------------
// Patient
// ------------------------------------------------------------------

export interface PatientSearchResult {
  patientId: string;
  medicalRecordNumber: string;
  fullName: string;
  dateOfBirth: string;
  gender: string;
}

export interface PatientOverview {
  id: string;
  medicalRecordNumber: string;
  firstName: string;
  lastName: string;
  gender: string;
  dateOfBirth: string;
  bloodType?: string;
  allergies: string[];
  conditions: string[];
  medications: string[];
}

// ------------------------------------------------------------------
// Consent
// ------------------------------------------------------------------

export type ConsentStatus = "PENDING" | "APPROVED" | "DENIED" | "EXPIRED" | "CANCELLED" | "REVOKED";

export interface ConsentRequest {
  id: string;
  patientId: string;
  doctorId: string;
  purpose: string;
  scope: string[];
  status: ConsentStatus;
  expiresAt: string;
  createdAt: string;
}

export interface CreateConsentPayload {
  patientId: string;
  purpose: string;
  scope: string[];
  expiresInMinutes: number;
}

// ------------------------------------------------------------------
// Consultation
// ------------------------------------------------------------------

export type ConsultationStatus = "CREATED" | "ACTIVE" | "PAUSED" | "COMPLETED" | "CANCELLED";

export interface Consultation {
  id: string;
  patientId: string;
  doctorId: string;
  reason: string;
  status: ConsultationStatus;
  createdAt: string;
  updatedAt: string;
}

export interface StartConsultationPayload {
  patientId: string;
  reason: string;
}

export interface AddNotePayload {
  content: string;
}

export interface AddDiagnosisPayload {
  diagnosis: string;
  icd10Code?: string;
  notes?: string;
}

export interface AddMedicationPayload {
  name: string;
  dosage: string;
  frequency: string;
  duration: string;
}

// ------------------------------------------------------------------
// AI Session
// ------------------------------------------------------------------

export type AiSessionStatus = "CREATED" | "ACTIVE" | "PROCESSING" | "COMPLETED" | "FAILED";

export interface AiSession {
  id: string;
  patientId?: string;
  consultationId?: string;
  provider: string;
  status: AiSessionStatus;
  createdAt: string;
}

export interface AiMessage {
  id: string;
  role: "user" | "assistant";
  content: string;
  suggestedQuestions?: string[];
  citations?: string[];
  complete?: boolean;
  createdAt: string;
}

export interface SendMessagePayload {
  message: string;
}

// ------------------------------------------------------------------
// Notification
// ------------------------------------------------------------------

export type NotificationType = "CONSENT" | "MEDICAL_RECORD" | "CONSULTATION" | "REMINDER" | "SYSTEM" | "AI";

export interface Notification {
  id: string;
  type: NotificationType;
  title: string;
  body: string;
  read: boolean;
  createdAt: string;
  actionUrl?: string;
}

// ------------------------------------------------------------------
// Timeline
// ------------------------------------------------------------------

export interface TimelineEvent {
  eventId: string;
  eventType: string;
  date: string;
  facility: {
    id: string;
    name: string;
  };
  doctor: {
    id: string;
    firstName: string;
    lastName: string;
  };
  summary: string;
  attachments: string[];
  status: string;
}

// ------------------------------------------------------------------
// WebSocket
// ------------------------------------------------------------------

export interface WsEvent {
  type: string;
  timestamp: string;
  payload: Record<string, unknown>;
}

export interface ConsentRequestedPayload {
  consentId: string;
  doctorId: string;
  patientId: string;
}

export interface ConsentStatusPayload {
  consentId: string;
}

export type WsMessageHandler = (event: WsEvent) => void;
