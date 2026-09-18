/**
 * Mirage Typed API Client — Aligned with actual backend routers
 *
 * Backend routers (see main.py):
 *   /api/v1/auth       → Authentication
 *   /api/v1/patients   → Patients
 *   /api/v1/consents   → Consent
 *   /api/v1/consultations → Consultations
 *   /api/v1/ai         → AI
 *   /api/v1/notifications → Notifications
 */

import type {
  AIMessageCreatePayload,
  AIMessageResponse,
  AIMessageStreamChunk,
  AISessionCreatePayload,
  AISessionResponse,
  AISessionWithMessagesResponse,
  AdminFacilityItem,
  ApiEnvelope,
  AdminDashboardStats,
  AdminDoctorListItem,
  AppointmentAdminFilters,
  AppointmentAdminItem,
  AppointmentCreateRequest,
  AppointmentListResponse,
  AppointmentResponse,
  AppointmentStatus,
  AuditLogEntry,
  ClinicalNoteCreatePayload,
  ClinicalNoteResponse,
  ClinicalSummary,
  ConsentListResponse,
  ConsentRequestResponse,
  CountResponse,
  CreateConsentPayload,
  CreateFacilityPayload,
  DiagnosisCreatePayload,
  DiagnosisResponse,
  DifferentialDiagnosis,
  DoctorSchedule,
  DoctorScheduleResponse,
  DoctorScheduleView,
  Facility,
  MedicationCreatePayload,
  MedicationResponse,
  NotificationListResponse,
  NotificationResponse,
  PaginatedAdminAppointments,
  PatientFullProfileResponse,
  PatientResponse,
  ScheduleAppointment,
  ScheduleUpdateRequest,
  SystemConfigItem,
  TimeOffAdminRequest,
  TimeOffEntry,
  TimeOffRequest,
  TimeOffResponse,
  TimelineEvent,
  TokenPair,
  UnreadCountResponse,
  UpdateFacilityPayload,
  UpdateSystemConfigPayload,
  UserProfile,
  VisitCreatePayload,
  VisitResponse,
  VisitWithDetailsResponse,
  DoctorPatientOverview,
} from "./types";

const API_BASE = "/api/v1";

export const STORAGE_KEYS = {
  accessToken: "mirage_access_token",
  refreshToken: "mirage_refresh_token",
} as const;

/** Derive role-specific token keys from the current page path. */
function _detectRoleFromPath(): string {
  if (typeof window === "undefined") return "global";
  const path = window.location.pathname;
  if (path.startsWith("/doctor")) return "doctor";
  if (path.startsWith("/patient")) return "patient";
  if (path.startsWith("/admin")) return "admin";
  return "global";
}

function _tokenKey(role: string, suffix: string): string {
  return `mirage_${role}_${suffix}`;
}

function getCurrentRole(): string {
  if (typeof window === "undefined") return "global";
  // Try to infer from stored token, then fall back to path
  const path = window.location.pathname;
  if (path.startsWith("/doctor")) return "doctor";
  if (path.startsWith("/patient")) return "patient";
  if (path.startsWith("/admin")) return "admin";
  return "global";
}

export function getStoredAccessToken(): string | null {
  if (typeof window === "undefined") return null;
  const key = _tokenKey(getCurrentRole(), "access_token");
  return localStorage.getItem(key);
}

export function getStoredRefreshToken(): string | null {
  if (typeof window === "undefined") return null;
  const key = _tokenKey(getCurrentRole(), "refresh_token");
  return localStorage.getItem(key);
}

export function setStoredTokens(role: string, access: string, refresh: string): void {
  if (typeof window === "undefined") return;
  const accessKey = _tokenKey(role, "access_token");
  const refreshKey = _tokenKey(role, "refresh_token");
  localStorage.setItem(accessKey, access);
  localStorage.setItem(refreshKey, refresh);
  const expires = new Date(Date.now() + 7 * 24 * 60 * 60 * 1000).toUTCString();
  document.cookie = `access_token=${encodeURIComponent(access)}; path=/; expires=${expires}; SameSite=Lax`;
}

export function clearStoredTokensForRole(role: string): void {
  if (typeof window === "undefined") return;
  localStorage.removeItem(_tokenKey(role, "access_token"));
  localStorage.removeItem(_tokenKey(role, "refresh_token"));
}

export function clearStoredTokens(): void {
  if (typeof window === "undefined") return;
  for (const role of ["doctor", "patient", "admin", "global"]) {
    localStorage.removeItem(_tokenKey(role, "access_token"));
    localStorage.removeItem(_tokenKey(role, "refresh_token"));
  }
  document.cookie = "access_token=; path=/; expires=Thu, 01 Jan 1970 00:00:00 GMT; SameSite=Lax";
}

function redirectToLogin(): void {
  if (typeof window === "undefined") return;
  const path = window.location.pathname;
  if (path.startsWith("/doctor")) {
    window.location.href = "/doctor/login";
  } else if (path.startsWith("/patient")) {
    window.location.href = "/patient/login";
  } else if (path.startsWith("/admin")) {
    window.location.href = "/admin/login";
  } else {
    window.location.href = "/";
  }
}

// ------------------------------------------------------------------
// Core request wrapper
// ------------------------------------------------------------------

interface RequestOptions extends RequestInit {
  skipAuth?: boolean;
}

export class ApiError extends Error {
  code: string;
  field?: string;
  status?: number;

  constructor(code: string, message: string, field?: string, status?: number) {
    super(message);
    this.name = "ApiError";
    this.code = code;
    this.field = field;
    this.status = status;
  }

  static fromEnvelope<T>(envelope: ApiEnvelope<T> | null, status?: number): ApiError {
    if (!envelope || !envelope.errors || envelope.errors.length === 0) {
      return new ApiError("UNKNOWN", "An unknown error occurred.", undefined, status);
    }
    const first = envelope.errors[0];
    return new ApiError(first.code, first.message, first.field, status);
  }
}

async function request<T>(
  endpoint: string,
  options: RequestOptions = {}
): Promise<T> {
  const url = `${API_BASE}${endpoint}`;
  const headers = new Headers(options.headers);

  headers.set("Accept", "application/json");
  if (!options.body || !(options.body instanceof FormData)) {
    headers.set("Content-Type", "application/json");
  }

  if (!options.skipAuth) {
    const token = getStoredAccessToken();
    if (token) {
      headers.set("Authorization", `Bearer ${token}`);
    }
  }

  const response = await fetch(url, {
    ...options,
    headers,
  });

  if (response.status === 204) {
    return undefined as unknown as T;
  }

  let body: ApiEnvelope<T> | null = null;
  const contentType = response.headers.get("content-type");
  if (contentType && contentType.includes("application/json")) {
    body = (await response.json()) as ApiEnvelope<T>;
  }

  // Authentication endpoints intentionally return 401 for invalid credentials.
  // They must not invoke token refresh or navigate away from the login form.
  if (response.status === 401 && !options.skipAuth) {
    const refreshed = await attemptTokenRefresh();
    if (!refreshed) {
      clearStoredTokensForRole(getCurrentRole());
      redirectToLogin();
      throw new ApiError("UNAUTHORIZED", "Session expired. Please log in again.");
    }
    const retryHeaders = new Headers(options.headers);
    retryHeaders.set("Accept", "application/json");
    if (!options.body || !(options.body instanceof FormData)) {
      retryHeaders.set("Content-Type", "application/json");
    }
    const newToken = getStoredAccessToken();
    if (newToken) {
      retryHeaders.set("Authorization", `Bearer ${newToken}`);
    }

    const retryResponse = await fetch(url, {
      ...options,
      headers: retryHeaders,
    });

    if (retryResponse.status === 204) {
      return undefined as unknown as T;
    }

    const retryBody = (await retryResponse.json()) as ApiEnvelope<T>;
    if (!retryResponse.ok) {
      throw ApiError.fromEnvelope(retryBody, retryResponse.status);
    }
    return parseEnvelope(retryBody);
  }

  if (!response.ok) {
    throw ApiError.fromEnvelope(body, response.status);
  }

  if (!body) {
    throw new ApiError("UNKNOWN", "Empty response from server.");
  }

  return parseEnvelope(body);
}

function parseEnvelope<T>(envelope: ApiEnvelope<T>): T {
  if (!envelope.success) {
    throw ApiError.fromEnvelope(envelope);
  }
  if (envelope.data === null || envelope.data === undefined) {
    throw new ApiError("NO_DATA", "Response envelope contained no data.");
  }
  return envelope.data;
}

let isRefreshing = false;

async function attemptTokenRefresh(): Promise<boolean> {
  if (isRefreshing) return false;
  const refreshToken = getStoredRefreshToken();
  if (!refreshToken) return false;

  isRefreshing = true;
  try {
    const response = await fetch(`${API_BASE}/auth/refresh`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Accept: "application/json",
      },
      body: JSON.stringify({ refresh_token: refreshToken }),
    });

    if (!response.ok) return false;

    const envelope = (await response.json()) as ApiEnvelope<{
      access_token: string;
      token_type: string;
      expires_in: number;
    }>;

    if (!envelope.success || !envelope.data) return false;

    // Keep existing refresh token unless backend returns a new one
    setStoredTokens(getCurrentRole(), envelope.data.access_token, refreshToken);
    return true;
  } catch {
    return false;
  } finally {
    isRefreshing = false;
  }
}

// ------------------------------------------------------------------
// API Endpoint Groups
// ------------------------------------------------------------------

export const authApi = {
  loginDoctor: (email: string, password: string): Promise<TokenPair> =>
    request<TokenPair>("/auth/doctor/login", {
      method: "POST",
      body: JSON.stringify({ email, password }),
      skipAuth: true,
    }),

  loginAdmin: (email: string, password: string): Promise<TokenPair> =>
    request<TokenPair>("/auth/admin/login", {
      method: "POST",
      body: JSON.stringify({ email, password }),
      skipAuth: true,
    }),

  loginPatient: (national_id: string, pin: string): Promise<TokenPair> =>
    request<TokenPair>("/auth/patient/login", {
      method: "POST",
      body: JSON.stringify({ national_id, pin }),
      skipAuth: true,
    }),

  refreshToken: (refresh_token: string): Promise<{ access_token: string; token_type: string; expires_in: number }> =>
    request<{ access_token: string; token_type: string; expires_in: number }>("/auth/refresh", {
      method: "POST",
      body: JSON.stringify({ refresh_token }),
      skipAuth: true,
    }),

  logout: (): Promise<{ message: string }> =>
    request<{ message: string }>("/auth/logout", {
      method: "POST",
    }),

  getMe: (): Promise<UserProfile> =>
    request<UserProfile>("/auth/me", {
      method: "GET",
    }),
};

export const patientsApi = {
  searchPatients: (query: string, limit = 20, offset = 0): Promise<PatientResponse[]> =>
    request<PatientResponse[]>(
      `/patients?q=${encodeURIComponent(query)}&limit=${limit}&offset=${offset}`,
      { method: "GET" }
    ),

  getPatient: (patientId: string): Promise<PatientFullProfileResponse> =>
    request<PatientFullProfileResponse>(`/patients/${patientId}`, { method: "GET" }),

  getMyProfile: (): Promise<PatientFullProfileResponse> =>
    request<PatientFullProfileResponse>("/me/patient", { method: "GET" }),

  getMyTimeline: (): Promise<TimelineEvent[]> =>
    request<TimelineEvent[]>("/me/patient/timeline", { method: "GET" }),

  getMyVisit: (visitId: string): Promise<VisitWithDetailsResponse> =>
    request<VisitWithDetailsResponse>(`/me/patient/visit/${visitId}`, { method: "GET" }),

  getMyNotifications: (params?: { unread_only?: boolean; limit?: number; offset?: number }): Promise<NotificationListResponse> => {
    const search = new URLSearchParams();
    if (params?.unread_only !== undefined) search.set("unread_only", String(params.unread_only));
    if (params?.limit) search.set("limit", String(params.limit));
    if (params?.offset !== undefined) search.set("offset", String(params.offset));
    return request<NotificationListResponse>(`/me/patient/notifications?${search.toString()}`, { method: "GET" });
  },

  getMyAccessHistory: (): Promise<unknown> =>
    request<unknown>("/me/patient/access-history", { method: "GET" }),

  getPatientRecords: (patientId: string): Promise<unknown> =>
    request<unknown>(`/patients/${patientId}/records`, { method: "GET" }),

  registerPatient: (data: Record<string, unknown>): Promise<PatientResponse> =>
    request<PatientResponse>("/patients", {
      method: "POST",
      body: JSON.stringify(data),
    }),
};

export const doctorApi = {
  getDoctorPatientOverview: (patientId: string): Promise<DoctorPatientOverview> =>
    request<DoctorPatientOverview>(`/doctor/patient/${patientId}`, { method: "GET" }),

  updateVisitTranscript: (visitId: string, transcript: string): Promise<VisitResponse> =>
    request<VisitResponse>(`/doctor/${visitId}/transcript`, {
      method: "PATCH",
      body: JSON.stringify(transcript),
    }),
};

export const consentsApi = {
  createConsent: (data: CreateConsentPayload): Promise<ConsentRequestResponse> =>
    request<ConsentRequestResponse>("/consents", {
      method: "POST",
      body: JSON.stringify(data),
    }),

  listConsents: (params?: {
    status?: string;
    limit?: number;
    offset?: number;
  }): Promise<ConsentListResponse> => {
    const search = new URLSearchParams();
    if (params?.status) search.set("status", params.status);
    if (params?.limit) search.set("limit", String(params.limit));
    if (params?.offset !== undefined) search.set("offset", String(params.offset));
    return request<ConsentListResponse>(`/consents?${search.toString()}`, { method: "GET" });
  },

  getConsent: (consentId: string): Promise<ConsentRequestResponse> =>
    request<ConsentRequestResponse>(`/consents/${consentId}`, { method: "GET" }),

  approveConsent: (consentId: string): Promise<ConsentRequestResponse> =>
    request<ConsentRequestResponse>(`/consents/${consentId}/approve`, { method: "POST" }),

  declineConsent: (consentId: string): Promise<ConsentRequestResponse> =>
    request<ConsentRequestResponse>(`/consents/${consentId}/decline`, { method: "POST" }),

  revokeConsent: (consentId: string): Promise<ConsentRequestResponse> =>
    request<ConsentRequestResponse>(`/consents/${consentId}/revoke`, { method: "POST" }),
};

export const consultationsApi = {
  startConsultation: (data: VisitCreatePayload): Promise<VisitResponse> =>
    request<VisitResponse>("/doctor", {
      method: "POST",
      body: JSON.stringify(data),
    }),

  listConsultations: (params?: {
    status?: string;
    limit?: number;
    offset?: number;
  }): Promise<VisitResponse[]> => {
    const search = new URLSearchParams();
    if (params?.status) search.set("status", params.status);
    if (params?.limit) search.set("limit", String(params.limit));
    if (params?.offset !== undefined) search.set("offset", String(params.offset));
    return request<VisitResponse[]>(`/doctor?${search.toString()}`, { method: "GET" });
  },

  getConsultation: (visitId: string): Promise<VisitWithDetailsResponse> =>
    request<VisitWithDetailsResponse>(`/doctor/${visitId}`, { method: "GET" }),

  addNote: (visitId: string, data: ClinicalNoteCreatePayload): Promise<ClinicalNoteResponse> =>
    request<ClinicalNoteResponse>(`/doctor/${visitId}/notes`, {
      method: "POST",
      body: JSON.stringify(data),
    }),

  addDiagnosis: (visitId: string, data: DiagnosisCreatePayload): Promise<DiagnosisResponse> =>
    request<DiagnosisResponse>(`/doctor/${visitId}/diagnoses`, {
      method: "POST",
      body: JSON.stringify(data),
    }),

  addMedication: (visitId: string, data: MedicationCreatePayload): Promise<MedicationResponse> =>
    request<MedicationResponse>(`/doctor/${visitId}/medications`, {
      method: "POST",
      body: JSON.stringify(data),
    }),

  completeConsultation: (visitId: string): Promise<VisitResponse> =>
    request<VisitResponse>(`/doctor/${visitId}/complete`, { method: "POST", body: JSON.stringify({}) }),

  cancelConsultation: (visitId: string): Promise<VisitResponse> =>
    request<VisitResponse>(`/doctor/${visitId}/cancel`, { method: "POST", body: JSON.stringify({}) }),
};

export const aiApi = {
  createSession: (patientId?: string): Promise<AISessionResponse> =>
    request<AISessionResponse>("/ai/sessions", {
      method: "POST",
      body: JSON.stringify({ patient_id: patientId } as AISessionCreatePayload),
    }),

  listSessions: (page = 1, pageSize = 20): Promise<AISessionResponse[]> =>
    request<AISessionResponse[]>(`/ai/sessions?page=${page}&page_size=${pageSize}`, { method: "GET" }),

  getSession: (sessionId: string): Promise<AISessionWithMessagesResponse> =>
    request<AISessionWithMessagesResponse>(`/ai/sessions/${sessionId}`, { method: "GET" }),

  sendMessage: (sessionId: string, content: string): Promise<AIMessageResponse> =>
    request<AIMessageResponse>(`/ai/sessions/${sessionId}/messages`, {
      method: "POST",
      body: JSON.stringify({ content } as AIMessageCreatePayload),
    }),

  getDifferentialDiagnosis: (sessionId: string): Promise<DifferentialDiagnosis[]> =>
    request<DifferentialDiagnosis[]>(`/ai/sessions/${sessionId}/diagnosis`, {
      method: "POST",
      body: JSON.stringify({}),
    }),

  getClinicalSummary: (sessionId: string): Promise<ClinicalSummary> =>
    request<ClinicalSummary>(`/ai/sessions/${sessionId}/summary`, {
      method: "POST",
      body: JSON.stringify({}),
    }),

  sendMessageStream: async (
    sessionId: string,
    content: string,
    onChunk: (chunk: AIMessageStreamChunk) => void
  ): Promise<void> => {
    const token = getStoredAccessToken();
    const headers: Record<string, string> = {
      "Content-Type": "application/json",
      Accept: "text/event-stream",
    };
    if (token) {
      headers["Authorization"] = `Bearer ${token}`;
    }

    const response = await fetch(`${API_BASE}/ai/sessions/${sessionId}/messages/stream`, {
      method: "POST",
      headers,
      body: JSON.stringify({ content } as AIMessageCreatePayload),
    });

    if (!response.ok) {
      throw new ApiError("AI_STREAM_ERROR", "Failed to start AI message stream.");
    }

    const reader = response.body?.getReader();
    if (!reader) {
      throw new ApiError("AI_STREAM_ERROR", "Readable stream not supported.");
    }

    const decoder = new TextDecoder();
    let buffer = "";

    try {
      while (true) {
        const { done, value } = await reader.read();
        if (done) break;

        buffer += decoder.decode(value, { stream: true });
        const lines = buffer.split("\n");
        buffer = lines.pop() ?? "";

        for (const line of lines) {
          const trimmed = line.trim();
          if (trimmed.startsWith("data: ")) {
            const data = trimmed.slice(6);
            if (data === "[DONE]") return;
            try {
              const parsed = JSON.parse(data) as AIMessageStreamChunk;
              if (parsed.done) return;
              onChunk(parsed);
            } catch {
              // Ignore malformed JSON lines
            }
          }
        }
      }
    } finally {
      reader.releaseLock();
    }
  },
};

export const notificationsApi = {
  listNotifications: (params?: {
    unread_only?: boolean;
    limit?: number;
    offset?: number;
  }): Promise<NotificationListResponse> => {
    const search = new URLSearchParams();
    if (params?.unread_only !== undefined) search.set("unread_only", String(params.unread_only));
    if (params?.limit) search.set("limit", String(params.limit));
    if (params?.offset !== undefined) search.set("offset", String(params.offset));
    return request<NotificationListResponse>(`/notifications?${search.toString()}`, { method: "GET" });
  },

  getUnreadCount: (): Promise<UnreadCountResponse> =>
    request<UnreadCountResponse>("/notifications/unread-count", { method: "GET" }),

  markRead: (notificationId: string): Promise<NotificationResponse> =>
    request<NotificationResponse>(`/notifications/${notificationId}/read`, { method: "POST" }),

  markAllRead: (): Promise<CountResponse> =>
    request<CountResponse>("/notifications/read-all", { method: "POST" }),
};

export const appointmentsApi = {
  create: (data: AppointmentCreateRequest): Promise<AppointmentResponse> =>
    request<AppointmentResponse>("/appointments", {
      method: "POST",
      body: JSON.stringify(data),
    }),

  listMy: (params?: {
    status?: string;
    upcoming?: boolean;
    limit?: number;
    offset?: number;
  }): Promise<AppointmentListResponse> => {
    const search = new URLSearchParams();
    if (params?.status) search.set("status", params.status);
    if (params?.upcoming !== undefined) search.set("upcoming", String(params.upcoming));
    if (params?.limit) search.set("limit", String(params.limit));
    if (params?.offset !== undefined) search.set("offset", String(params.offset));
    return request<AppointmentListResponse>(`/appointments/my?${search.toString()}`, { method: "GET" });
  },

  getById: (id: string): Promise<AppointmentResponse> =>
    request<AppointmentResponse>(`/appointments/${id}`, { method: "GET" }),

  cancel: (id: string, reason?: string): Promise<AppointmentResponse> =>
    request<AppointmentResponse>(`/appointments/${id}/cancel`, {
      method: "POST",
      body: JSON.stringify({ reason }),
    }),

  confirm: (id: string): Promise<AppointmentResponse> =>
    request<AppointmentResponse>(`/appointments/${id}/confirm`, {
      method: "POST",
      body: JSON.stringify({}),
    }),

  startConsultation: (id: string): Promise<{ consultation_id: string }> =>
    request<{ consultation_id: string }>(`/appointments/${id}/start-consultation`, {
      method: "POST",
      body: JSON.stringify({}),
    }),
};

export const facilitiesApi = {
  search: (query?: string, limit = 20, offset = 0): Promise<{ items: Facility[]; total: number; limit: number; offset: number }> => {
    const search = new URLSearchParams();
    if (query) search.set("q", query);
    search.set("limit", String(limit));
    search.set("offset", String(offset));
    return request<{ items: Facility[]; total: number; limit: number; offset: number }>(`/appointments/facilities?${search.toString()}`, { method: "GET" });
  },

  getById: (id: string): Promise<Facility> =>
    request<Facility>(`/appointments/facilities/${id}`, { method: "GET" }),

  getDoctors: (id: string): Promise<
    { id: string; name: string; specialty: string }[]
  > =>
    request<{ id: string; name: string; specialty: string }[]>(`/appointments/facilities/${id}/doctors`, {
      method: "GET",
    }),
};

export const auditApi = {
  getAccessHistory: (params?: {
    limit?: number;
    offset?: number;
  }): Promise<{ items: AuditLogEntry[]; total: number }> => {
    const search = new URLSearchParams();
    if (params?.limit) search.set("limit", String(params.limit));
    if (params?.offset !== undefined) search.set("offset", String(params.offset));
    return request<{ items: AuditLogEntry[]; total: number }>(`/audit/history?${search.toString()}`, { method: "GET" });
  },
};

export const scheduleApi = {
  getMySchedule: (): Promise<DoctorScheduleView> =>
    request<DoctorScheduleView>("/doctor/schedule", { method: "GET" }),

  getMyAppointments: (): Promise<ScheduleAppointment[]> =>
    request<ScheduleAppointment[]>("/doctor/appointments", { method: "GET" }),

  getMyAppointmentsToday: (): Promise<ScheduleAppointment[]> =>
    request<ScheduleAppointment[]>("/doctor/appointments/today", { method: "GET" }),

  updateAppointmentStatus: (id: string, status: AppointmentStatus): Promise<ScheduleAppointment> =>
    request<ScheduleAppointment>(`/doctor/appointments/${id}/status`, {
      method: "PUT",
      body: JSON.stringify({ status }),
    }),

  requestLeave: (data: TimeOffRequest): Promise<TimeOffResponse> =>
    request<TimeOffResponse>("/doctor/time-off", {
      method: "POST",
      body: JSON.stringify(data),
    }),
};

// ------------------------------------------------------------------
// Admin API
// ------------------------------------------------------------------

export const adminApi = {
  getDashboard: (): Promise<AdminDashboardStats> =>
    request<AdminDashboardStats>("/appointments/admin/dashboard", { method: "GET" }),

  listDoctors: (params?: { limit?: number; offset?: number }): Promise<AdminDoctorListItem[]> => {
    const search = new URLSearchParams();
    if (params?.limit) search.set("limit", String(params.limit));
    if (params?.offset !== undefined) search.set("offset", String(params.offset));
    return request<AdminDoctorListItem[]>(`/appointments/admin/doctors?${search.toString()}`, { method: "GET" });
  },

  getDoctorSchedule: (doctorId: string): Promise<DoctorScheduleResponse> =>
    request<DoctorScheduleResponse>(`/appointments/admin/doctors/${doctorId}/schedule`, { method: "GET" }),

  updateDoctorSchedule: (doctorId: string, data: ScheduleUpdateRequest): Promise<DoctorScheduleResponse> =>
    request<DoctorScheduleResponse>(`/appointments/admin/doctors/${doctorId}/schedule`, {
      method: "PUT",
      body: JSON.stringify(data),
    }),

  addTimeOff: (doctorId: string, data: TimeOffAdminRequest): Promise<TimeOffEntry> =>
    request<TimeOffEntry>(`/appointments/admin/doctors/${doctorId}/time-off`, {
      method: "POST",
      body: JSON.stringify(data),
    }),

  listDoctorTimeOff: (doctorId: string): Promise<TimeOffEntry[]> =>
    request<TimeOffEntry[]>(`/appointments/admin/doctors/${doctorId}/time-off`, { method: "GET" }),

  approveTimeOff: (timeOffId: string): Promise<TimeOffEntry> =>
    request<TimeOffEntry>(`/appointments/admin/doctors/time-off/${timeOffId}/approve`, { method: "POST" }),

  rejectTimeOff: (timeOffId: string): Promise<TimeOffEntry> =>
    request<TimeOffEntry>(`/appointments/admin/doctors/time-off/${timeOffId}/reject`, { method: "POST" }),

  listAppointments: (filters?: AppointmentAdminFilters): Promise<PaginatedAdminAppointments> => {
    const search = new URLSearchParams();
    if (filters?.date_from) search.set("date_from", filters.date_from);
    if (filters?.date_to) search.set("date_to", filters.date_to);
    if (filters?.facility_id) search.set("facility_id", filters.facility_id);
    if (filters?.status) search.set("status", filters.status);
    if (filters?.priority) search.set("priority", filters.priority);
    if (filters?.doctor_search) search.set("doctor_search", filters.doctor_search);
    if (filters?.patient_search) search.set("patient_search", filters.patient_search);
    // Convert page/page_size to limit/offset for backend
    const page = filters?.page ?? 1;
    const page_size = filters?.page_size ?? 20;
    search.set("limit", String(page_size));
    search.set("offset", String((page - 1) * page_size));
    return request<{ items: AppointmentAdminItem[]; total: number; limit: number; offset: number }>(
      `/appointments/admin/appointments?${search.toString()}`,
      { method: "GET" }
    ).then((r) => ({
      items: r.items,
      total: r.total,
      page,
      page_size,
      total_pages: Math.max(1, Math.ceil(r.total / page_size)),
    }));
  },

  cancelAppointment: (appointmentId: string): Promise<{ message: string }> =>
    request<{ message: string }>(`/appointments/admin/appointments/${appointmentId}/cancel`, { method: "PUT" }),

  reassignDoctor: (appointmentId: string, doctorId: string): Promise<AppointmentAdminItem> =>
    request<AppointmentAdminItem>(`/appointments/admin/appointments/${appointmentId}/reassign`, {
      method: "PUT",
      body: JSON.stringify({ doctor_id: doctorId }),
    }),

  // Settings
  listSettings: (): Promise<SystemConfigItem[]> =>
    request<SystemConfigItem[]>("/admin/settings", { method: "GET" }),

  updateSetting: (key: string, data: UpdateSystemConfigPayload): Promise<SystemConfigItem> =>
    request<SystemConfigItem>(`/admin/settings/${key}`, { method: "PUT", body: JSON.stringify(data) }),

  // Facilities CRUD
  listFacilities: (): Promise<AdminFacilityItem[]> =>
    request<AdminFacilityItem[]>("/admin/facilities", { method: "GET" }),

  getFacility: (id: string): Promise<AdminFacilityItem> =>
    request<AdminFacilityItem>(`/admin/facilities/${id}`, { method: "GET" }),

  createFacility: (data: CreateFacilityPayload): Promise<AdminFacilityItem> =>
    request<AdminFacilityItem>("/admin/facilities", {
      method: "POST",
      body: JSON.stringify(data),
    }),

  updateFacility: (id: string, data: UpdateFacilityPayload): Promise<AdminFacilityItem> =>
    request<AdminFacilityItem>(`/admin/facilities/${id}`, {
      method: "PUT",
      body: JSON.stringify(data),
    }),

  deleteFacility: (id: string): Promise<void> =>
    request<void>(`/admin/facilities/${id}`, { method: "DELETE" }),
};


