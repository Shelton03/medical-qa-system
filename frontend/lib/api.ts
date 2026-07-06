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
  ApiEnvelope,
  AIMessageCreatePayload,
  AIMessageResponse,
  AISessionCreatePayload,
  AISessionResponse,
  AISessionWithMessagesResponse,
  ConsentListResponse,
  ConsentRequestResponse,
  CountResponse,
  CreateConsentPayload,
  ClinicalNoteCreatePayload,
  ClinicalNoteResponse,
  ClinicalSummary,
  DiagnosisCreatePayload,
  DiagnosisResponse,
  DifferentialDiagnosis,
  MedicationCreatePayload,
  MedicationResponse,
  NotificationListResponse,
  NotificationResponse,
  PatientFullProfileResponse,
  PatientResponse,
  TokenPair,
  UnreadCountResponse,
  UserProfile,
  VisitCreatePayload,
  VisitResponse,
  VisitWithDetailsResponse,
  AuditLogEntry,
} from "./types";

const API_BASE = "/api/v1";

const STORAGE_KEYS = {
  accessToken: "mirage_access_token",
  refreshToken: "mirage_refresh_token",
} as const;

function getStoredAccessToken(): string | null {
  if (typeof window === "undefined") return null;
  return localStorage.getItem(STORAGE_KEYS.accessToken);
}

function getStoredRefreshToken(): string | null {
  if (typeof window === "undefined") return null;
  return localStorage.getItem(STORAGE_KEYS.refreshToken);
}

function setStoredTokens(access: string, refresh: string): void {
  if (typeof window === "undefined") return;
  localStorage.setItem(STORAGE_KEYS.accessToken, access);
  localStorage.setItem(STORAGE_KEYS.refreshToken, refresh);
}

export function clearStoredTokens(): void {
  if (typeof window === "undefined") return;
  localStorage.removeItem(STORAGE_KEYS.accessToken);
  localStorage.removeItem(STORAGE_KEYS.refreshToken);
}

function redirectToLogin(): void {
  if (typeof window === "undefined") return;
  const path = window.location.pathname;
  if (path.startsWith("/doctor")) {
    window.location.href = "/doctor/login";
  } else if (path.startsWith("/patient")) {
    window.location.href = "/patient/login";
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

  static fromEnvelope<T>(envelope: ApiEnvelope<T> | null): ApiError {
    if (!envelope || !envelope.errors || envelope.errors.length === 0) {
      return new ApiError("UNKNOWN", "An unknown error occurred.");
    }
    const first = envelope.errors[0];
    return new ApiError(first.code, first.message, first.field);
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

  if (response.status === 401) {
    const refreshed = await attemptTokenRefresh();
    if (!refreshed) {
      clearStoredTokens();
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
      throw ApiError.fromEnvelope(retryBody);
    }
    return parseEnvelope(retryBody);
  }

  if (!response.ok) {
    throw ApiError.fromEnvelope(body);
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
    setStoredTokens(envelope.data.access_token, refreshToken);
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

  getMyTimeline: (): Promise<VisitResponse[]> =>
    request<VisitResponse[]>("/me/patient/timeline", { method: "GET" }),

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
    request<VisitResponse>("/consultations", {
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
    return request<VisitResponse[]>(`/consultations?${search.toString()}`, { method: "GET" });
  },

  getConsultation: (visitId: string): Promise<VisitWithDetailsResponse> =>
    request<VisitWithDetailsResponse>(`/consultations/${visitId}`, { method: "GET" }),

  addNote: (visitId: string, data: ClinicalNoteCreatePayload): Promise<ClinicalNoteResponse> =>
    request<ClinicalNoteResponse>(`/consultations/${visitId}/notes`, {
      method: "POST",
      body: JSON.stringify(data),
    }),

  addDiagnosis: (visitId: string, data: DiagnosisCreatePayload): Promise<DiagnosisResponse> =>
    request<DiagnosisResponse>(`/consultations/${visitId}/diagnoses`, {
      method: "POST",
      body: JSON.stringify(data),
    }),

  addMedication: (visitId: string, data: MedicationCreatePayload): Promise<MedicationResponse> =>
    request<MedicationResponse>(`/consultations/${visitId}/medications`, {
      method: "POST",
      body: JSON.stringify(data),
    }),

  completeConsultation: (visitId: string): Promise<VisitResponse> =>
    request<VisitResponse>(`/consultations/${visitId}/complete`, { method: "POST", body: JSON.stringify({}) }),

  cancelConsultation: (visitId: string): Promise<VisitResponse> =>
    request<VisitResponse>(`/consultations/${visitId}/cancel`, { method: "POST", body: JSON.stringify({}) }),
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
    onChunk: (chunk: string) => void
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
              const parsed = JSON.parse(data) as { token?: string; done?: boolean };
              if (parsed.done) return;
              const chunk = parsed.token ?? "";
              if (chunk) onChunk(chunk);
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
