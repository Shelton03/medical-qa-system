/**
 * Mirage API Types — Aligned with actual backend snake_case Envelope schemas
 */

// ------------------------------------------------------------------
// Standard Response Envelope
// ------------------------------------------------------------------

export interface ApiErrorDetail {
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
  errors: ApiErrorDetail[];
  meta: ApiMeta;
}

// ------------------------------------------------------------------
// Authentication
// ------------------------------------------------------------------

export type UserRole = "doctor" | "patient" | "admin";

export interface UserProfile {
  id: string;
  role: UserRole;
  first_name: string;
  last_name: string;
  email: string;
  avatar_url: string | null;
}

export interface TokenPair {
  access_token: string;
  refresh_token: string;
  token_type: string;
  expires_in: number;
  role: string;
  demo_mode: boolean;
}

// ------------------------------------------------------------------
// Patient
// ------------------------------------------------------------------

export interface PatientResponse {
  id: string;
  user_id: string;
  medical_record_number: string;
  national_identifier: string;
  date_of_birth: string;
  gender: string;
  blood_type: string | null;
  emergency_contact_name: string | null;
  emergency_contact_phone: string | null;
  created_at: string;
  updated_at: string;
  first_name?: string;
  last_name?: string;
  phone?: string;
  email?: string;
}

export interface MedicalRecordSummaryResponse {
  id: string;
  patient_id: string;
  allergies: AllergySummary[];
  chronic_conditions: ChronicConditionSummary[];
  medications: MedicationSummary[];
}

export interface AllergySummary {
  id: string;
  allergen: string;
  severity: string;
  reaction: string | null;
}

export interface ChronicConditionSummary {
  id: string;
  condition_name: string;
  icd10_code: string | null;
  status: string;
  diagnosed_date: string | null;
}

export interface MedicationSummary {
  id: string;
  name: string;
  dosage: string | null;
  frequency: string | null;
  status: string;
}

export interface PatientFullProfileResponse extends PatientResponse {
  medical_record: MedicalRecordSummaryResponse | null;
}

// ------------------------------------------------------------------
// Consent
// ------------------------------------------------------------------

export type ConsentStatus = "pending" | "approved" | "declined" | "expired" | "revoked";

export interface ConsentRequestResponse {
  id: string;
  doctor_id: string;
  patient_id: string;
  doctor_name: string | null;
  status: ConsentStatus;
  purpose: string | null;
  shared_data: string[] | null;
  created_at: string;
  expiry_date: string | null;
  approved_at: string | null;
  declined_at: string | null;
}

export interface ConsentListResponse {
  items: ConsentRequestResponse[];
  meta: {
    total: number;
    limit: number;
    offset: number;
  };
}

export interface CreateConsentPayload {
  doctor_id: string;
  patient_id: string;
  purpose: string;
  shared_data: string[];
  expiry_hours: number;
}

// ------------------------------------------------------------------
// Consultation (Visit)
// ------------------------------------------------------------------

export type VisitStatus = "scheduled" | "in_progress" | "completed" | "cancelled";

export interface VisitResponse {
  id: string;
  patient_id: string | null;
  doctor_id: string;
  facility_id: string | null;
  visit_date: string;
  status: VisitStatus;
  reason: string | null;
  chief_complaint: string | null;
  summary: string | null;
  ai_summary: string | null;
  follow_up_required: boolean;
  created_at: string;
  updated_at: string;
}

export interface ClinicalNoteResponse {
  id: string;
  visit_id: string;
  doctor_id: string;
  subjective: string | null;
  objective: string | null;
  assessment: string | null;
  plan: string | null;
  note_type?: "subjective" | "objective" | "assessment" | "plan" | null;
  content?: string | null;
  is_finalized: boolean;
  created_at: string;
  updated_at: string;
}

export interface DiagnosisResponse {
  id: string;
  visit_id: string;
  diagnosis_name: string;
  icd10_code: string | null;
  confidence: string | null;
  primary_diagnosis: boolean;
  notes: string | null;
  created_at: string;
}

export interface MedicationResponse {
  id: string;
  visit_id: string | null;
  name: string;
  dosage: string | null;
  frequency: string | null;
  duration: string | null;
  instructions: string | null;
  status: string | null;
  start_date: string | null;
  end_date: string | null;
  created_at: string;
}

export interface VisitWithDetailsResponse extends VisitResponse {
  clinical_notes: ClinicalNoteResponse[];
  diagnoses: DiagnosisResponse[];
  medications: MedicationResponse[];
  ai_sessions: AISessionBriefResponse[];
}

export interface AISessionBriefResponse {
  id: string;
  provider_name: string | null;
  status: string;
  started_at: string;
}

export interface VisitCreatePayload {
  patient_id: string;
  chief_complaint?: string;
  reason?: string;
  facility_id?: string;
}

export interface ClinicalNoteCreatePayload {
  note_type: "subjective" | "objective" | "assessment" | "plan";
  content: string;
}

export interface DiagnosisCreatePayload {
  diagnosis_name: string;
  icd10_code?: string;
  type?: "primary" | "secondary";
  status?: "confirmed" | "suspected" | "ruled_out";
  notes?: string;
}

export interface MedicationCreatePayload {
  name: string;
  dosage?: string;
  frequency?: string;
  duration?: string;
  instructions?: string;
  start_date?: string;
  end_date?: string;
}

// ------------------------------------------------------------------
// AI Session
// ------------------------------------------------------------------

export interface AISessionResponse {
  id: string;
  doctor_id: string;
  patient_id: string | null;
  provider_name: string | null;
  status: string;
  started_at: string;
  ended_at: string | null;
}

export interface AIMessageResponse {
  id: string;
  session_id: string;
  role: string;
  content: string;
  model_name: string | null;
  token_count: number | null;
  created_at: string;
}

export interface AISessionWithMessagesResponse extends AISessionResponse {
  messages: AIMessageResponse[];
}

export interface AISessionCreatePayload {
  patient_id?: string;
}

export interface AIMessageCreatePayload {
  content: string;
}

// ------------------------------------------------------------------
// Notification
// ------------------------------------------------------------------

export interface NotificationResponse {
  id: string;
  type: string;
  title: string;
  body: string | null;
  is_read: boolean;
  created_at: string;
}

export interface NotificationListResponse {
  items: NotificationResponse[];
  total: number;
  limit: number;
  offset: number;
}

export interface UnreadCountResponse {
  count: number;
}

export interface CountResponse {
  count: number;
}

// ------------------------------------------------------------------
// WebSocket
// ------------------------------------------------------------------

export interface WsEvent {
  type: string;
  payload: Record<string, unknown>;
  timestamp: string;
}

// ------------------------------------------------------------------
// AI — Differential Diagnosis
// ------------------------------------------------------------------

export interface DifferentialDiagnosis {
  id: string;
  diagnosis_name: string;
  icd10_code: string | null;
  probability: number;
  confidence: string | null;
  reasoning: string | null;
  supporting_evidence: string[];
  contradictory_evidence: string[];
  suggested_investigations: string[];
  medication_risks: string[];
  status: "suggested" | "confirmed" | "ignored";
}

// ------------------------------------------------------------------
// AI — Clinical Summary (SOAP)
// ------------------------------------------------------------------

export interface ClinicalSummary {
  subjective: string;
  objective: string;
  assessment: string;
  plan: string;
}

// ------------------------------------------------------------------
// Audit / Access History
// ------------------------------------------------------------------

export interface AuditLogEntry {
  id: string;
  patient_name: string;
  patient_id: string;
  facility: string;
  access_time: string;
  purpose: string;
  duration_minutes: number;
  outcome: string;
}
