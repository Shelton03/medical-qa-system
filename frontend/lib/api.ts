/**
 * Mirage Typed API Client
 *
 * Centralized fetch-based API client with:
 * - Automatic JWT injection from localStorage
 * - Automatic 401 handling with single refresh attempt
 * - Standard Envelope parsing
 * - Per-endpoint grouped API exports
 */

import type {
  ApiEnvelope,
  AddDiagnosisPayload,
  AddMedicationPayload,
  AddNotePayload,
  AiMessage,
  AiSession,
  Consultation,
  ConsentRequest,
  CreateConsentPayload,
  LoginResponse,
  Notification,
  PatientOverview,
  PatientSearchResult,
  SendMessagePayload,
  StartConsultationPayload,
  UserProfile,
} from "./types";

// ------------------------------------------------------------------
// Configuration
// ------------------------------------------------------------------

const API_BASE = "/api/v1";

const STORAGE_KEYS = {
  accessToken: "mirage_access_token",
  refreshToken: "mirage_refresh_token",
} as const;

// ------------------------------------------------------------------
// Helpers
// ------------------------------------------------------------------

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

function clearStoredTokens(): void {
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

async function request<T>(
  endpoint: string,
  options: RequestOptions = {}
): Promise<T> {
  const url = `${API_BASE}${endpoint}`;
  const headers = new Headers(options.headers);

  headers.set("Accept", "application/json");
  headers.set("Content-Type", "application/json");

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

  // Handle 204 No Content
  if (response.status === 204) {
    return undefined as unknown as T;
  }

  // Attempt to parse envelope — some error responses may not be JSON
  let body: ApiEnvelope<T> | null = null;
  const contentType = response.headers.get("content-type");
  if (contentType && contentType.includes("application/json")) {
    body = (await response.json()) as ApiEnvelope<T>;
  }

  // Automatic 401 handling
  if (response.status === 401) {
    const refreshed = await attemptTokenRefresh();
    if (!refreshed) {
      clearStoredTokens();
      redirectToLogin();
      throw new ApiError("UNAUTHORIZED", "Session expired. Please log in again.");
    }
    // Retry original request once with new token
    const retryHeaders = new Headers(options.headers);
    retryHeaders.set("Accept", "application/json");
    retryHeaders.set("Content-Type", "application/json");
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

// Prevent infinite refresh loops
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
      body: JSON.stringify({ refreshToken }),
    });

    if (!response.ok) return false;

    const envelope = (await response.json()) as ApiEnvelope<{
      accessToken: string;
      refreshToken: string;
      expiresIn: number;
    }>;

    if (!envelope.success || !envelope.data) return false;

    setStoredTokens(envelope.data.accessToken, envelope.data.refreshToken);
    return true;
  } catch {
    return false;
  } finally {
    isRefreshing = false;
  }
}

// ------------------------------------------------------------------
// ApiError class
// ------------------------------------------------------------------

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

// ------------------------------------------------------------------
// API Endpoint Groups
// ------------------------------------------------------------------

export const authApi = {
  loginDoctor: (email: string, password: string): Promise<LoginResponse> =>
    request<LoginResponse>("/auth/login", {
      method: "POST",
      body: JSON.stringify({ email, password }),
      skipAuth: true,
    }),

  loginPatient: (nationalId: string, pin: string): Promise<LoginResponse> =>
    request<LoginResponse>("/auth/login", {
      method: "POST",
      body: JSON.stringify({ nationalId, pin }),
      skipAuth: true,
    }),

  demoLogin: (role: "doctor" | "patient" | "admin"): Promise<LoginResponse> =>
    request<LoginResponse>("/auth/demo-login", {
      method: "POST",
      body: JSON.stringify({ role }),
      skipAuth: true,
    }),

  refreshToken: (refreshToken: string): Promise<{ accessToken: string; refreshToken: string; expiresIn: number }> =>
    request<{ accessToken: string; refreshToken: string; expiresIn: number }>("/auth/refresh", {
      method: "POST",
      body: JSON.stringify({ refreshToken }),
      skipAuth: true,
    }),

  logout: (): Promise<void> =>
    request<void>("/auth/logout", {
      method: "POST",
    }),

  getMe: (): Promise<UserProfile> =>
    request<UserProfile>("/auth/me", {
      method: "GET",
    }),
};

export const patientsApi = {
  searchPatients: (query: string, limit = 20, offset = 0): Promise<PatientSearchResult[]> =>
    request<PatientSearchResult[]>(
      `/doctor/search?query=${encodeURIComponent(query)}&limit=${limit}&offset=${offset}`,
      { method: "GET" }
    ),

  getPatient: (patientId: string): Promise<PatientOverview> =>
    request<PatientOverview>(`/doctor/patient/${patientId}`, { method: "GET" }),

  getPatientRecords: (patientId: string): Promise<unknown> =>
    request<unknown>(`/records/${patientId}`, { method: "GET" }),

  getPatientTimeline: (patientId: string): Promise<unknown[]> =>
    request<unknown[]>(`/doctor/patient/${patientId}/timeline`, { method: "GET" }),

  getMe: (): Promise<PatientOverview> =>
    request<PatientOverview>("/patients/me", { method: "GET" }),
};

export const consentsApi = {
  createConsent: (data: CreateConsentPayload): Promise<ConsentRequest> =>
    request<ConsentRequest>("/consent/request", {
      method: "POST",
      body: JSON.stringify(data),
    }),

  listConsents: (params?: {
    status?: string;
    patientId?: string;
    doctorId?: string;
    page?: number;
    pageSize?: number;
  }): Promise<ConsentRequest[]> => {
    const search = new URLSearchParams();
    if (params?.status) search.set("status", params.status);
    if (params?.patientId) search.set("patientId", params.patientId);
    if (params?.doctorId) search.set("doctorId", params.doctorId);
    if (params?.page) search.set("page", String(params.page));
    if (params?.pageSize) search.set("pageSize", String(params.pageSize));
    return request<ConsentRequest[]>(`/consent/history?${search.toString()}`, { method: "GET" });
  },

  getConsent: (consentId: string): Promise<ConsentRequest> =>
    request<ConsentRequest>(`/consent/${consentId}`, { method: "GET" }),

  approveConsent: (consentId: string): Promise<ConsentRequest> =>
    request<ConsentRequest>(`/consent/${consentId}/approve`, { method: "POST" }),

  declineConsent: (consentId: string): Promise<ConsentRequest> =>
    request<ConsentRequest>(`/consent/${consentId}/deny`, { method: "POST" }),

  revokeConsent: (consentId: string): Promise<ConsentRequest> =>
    request<ConsentRequest>(`/consent/${consentId}/cancel`, { method: "POST" }),
};

export const consultationsApi = {
  startConsultation: (data: StartConsultationPayload): Promise<Consultation> =>
    request<Consultation>(`/doctor/patient/${data.patientId}/consultation`, {
      method: "POST",
      body: JSON.stringify({ reason: data.reason }),
    }),

  listConsultations: (params?: {
    status?: string;
    patientId?: string;
    doctorId?: string;
    dateFrom?: string;
    dateTo?: string;
    page?: number;
    pageSize?: number;
  }): Promise<Consultation[]> => {
    const search = new URLSearchParams();
    if (params?.status) search.set("status", params.status);
    if (params?.patientId) search.set("patientId", params.patientId);
    if (params?.doctorId) search.set("doctorId", params.doctorId);
    if (params?.dateFrom) search.set("dateFrom", params.dateFrom);
    if (params?.dateTo) search.set("dateTo", params.dateTo);
    if (params?.page) search.set("page", String(params.page));
    if (params?.pageSize) search.set("pageSize", String(params.pageSize));
    return request<Consultation[]>(`/consultations?${search.toString()}`, { method: "GET" });
  },

  getConsultation: (visitId: string): Promise<Consultation> =>
    request<Consultation>(`/doctor/patient/${visitId}/consultation`, { method: "GET" }),

  addNote: (visitId: string, data: AddNotePayload): Promise<unknown> =>
    request<unknown>(`/doctor/patient/${visitId}/notes`, {
      method: "POST",
      body: JSON.stringify(data),
    }),

  addDiagnosis: (visitId: string, data: AddDiagnosisPayload): Promise<unknown> =>
    request<unknown>(`/diagnoses`, {
      method: "POST",
      body: JSON.stringify({ ...data, consultationId: visitId }),
    }),

  addMedication: (visitId: string, data: AddMedicationPayload): Promise<unknown> =>
    request<unknown>(`/prescriptions`, {
      method: "POST",
      body: JSON.stringify({ ...data, consultationId: visitId }),
    }),

  completeConsultation: (visitId: string): Promise<Consultation> =>
    request<Consultation>(`/consultations/${visitId}/complete`, { method: "POST" }),

  cancelConsultation: (visitId: string): Promise<Consultation> =>
    request<Consultation>(`/consultations/${visitId}/cancel`, { method: "POST" }),
};

export const aiApi = {
  createSession: (patientId?: string, consultationId?: string): Promise<AiSession> =>
    request<AiSession>("/ai/session", {
      method: "POST",
      body: JSON.stringify({ patientId, consultationId }),
    }),

  listSessions: (): Promise<AiSession[]> =>
    request<AiSession[]>("/ai/session", { method: "GET" }),

  getSession: (sessionId: string): Promise<AiSession> =>
    request<AiSession>(`/ai/session/${sessionId}`, { method: "GET" }),

  sendMessage: (sessionId: string, content: string): Promise<AiMessage> =>
    request<AiMessage>(`/ai/session/${sessionId}/message`, {
      method: "POST",
      body: JSON.stringify({ message: content } as SendMessagePayload),
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

    const response = await fetch(`${API_BASE}/ai/session/${sessionId}/message/stream`, {
      method: "POST",
      headers,
      body: JSON.stringify({ message: content } as SendMessagePayload),
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
              const parsed = JSON.parse(data) as { token?: string; content?: string };
              const chunk = parsed.token ?? parsed.content ?? "";
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
    unread?: boolean;
    category?: string;
    page?: number;
    pageSize?: number;
  }): Promise<Notification[]> => {
    const search = new URLSearchParams();
    if (params?.unread !== undefined) search.set("unread", String(params.unread));
    if (params?.category) search.set("category", params.category);
    if (params?.page) search.set("page", String(params.page));
    if (params?.pageSize) search.set("pageSize", String(params.pageSize));
    return request<Notification[]>(`/notifications?${search.toString()}`, { method: "GET" });
  },

  getUnreadCount: (): Promise<number> =>
    request<number>("/notifications/unread/count", { method: "GET" }),

  markRead: (notificationId: string): Promise<Notification> =>
    request<Notification>(`/notifications/${notificationId}`, {
      method: "PATCH",
      body: JSON.stringify({ read: true }),
    }),

  markAllRead: (): Promise<void> =>
    request<void>("/notifications/read-all", { method: "PUT" }),
};
