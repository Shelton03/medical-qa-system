1|/**
2| * Mirage Typed API Client — Aligned with actual backend routers
3| *
4| * Backend routers (see main.py):
5| *   /api/v1/auth       → Authentication
6| *   /api/v1/patients   → Patients
7| *   /api/v1/consents   → Consent
8| *   /api/v1/consultations → Consultations
9| *   /api/v1/ai         → AI
10| *   /api/v1/notifications → Notifications
11| */
12|
13|import type {
14|  AIMessageCreatePayload,
15|  AIMessageResponse,
16|  AIMessageStreamChunk,
17|  AISessionCreatePayload,
18|  AISessionResponse,
19|  AISessionWithMessagesResponse,
20|  AdminFacilityItem,
21|  ApiEnvelope,
22|  AdminDashboardStats,
23|  AdminDoctorListItem,
24|  AppointmentAdminFilters,
25|  AppointmentAdminItem,
26|  AppointmentCreateRequest,
27|  AppointmentListResponse,
28|  AppointmentResponse,
29|  AppointmentStatus,
30|  AuditLogEntry,
31|  ClinicalNoteCreatePayload,
32|  ClinicalNoteResponse,
33|  ClinicalSummary,
34|  ConsentListResponse,
35|  ConsentRequestResponse,
36|  CountResponse,
37|  CreateConsentPayload,
38|  CreateFacilityPayload,
39|  DiagnosisCreatePayload,
40|  DiagnosisResponse,
41|  DifferentialDiagnosis,
42|  DoctorSchedule,
43|  DoctorScheduleResponse,
44|  DoctorScheduleView,
45|  Facility,
46|  MedicationCreatePayload,
47|  MedicationResponse,
48|  NotificationListResponse,
49|  NotificationResponse,
50|  PaginatedAdminAppointments,
51|  PatientFullProfileResponse,
52|  PatientResponse,
53|  ScheduleAppointment,
54|  ScheduleUpdateRequest,
55|  SystemConfigItem,
56|  TimeOffAdminRequest,
57|  TimeOffEntry,
58|  TimeOffRequest,
59|  TimeOffResponse,
60|  TimelineEvent,
61|  TokenPair,
62|  UnreadCountResponse,
63|  UpdateFacilityPayload,
64|  UpdateSystemConfigPayload,
65|  UserProfile,
66|  VisitCreatePayload,
67|  VisitResponse,
68|  VisitWithDetailsResponse,
69|  DoctorPatientOverview,
70|} from "./types";
71|
72|const API_BASE = "/api/v1";
73|
74|export const STORAGE_KEYS = {
75|  accessToken: "mirage_access_token",
76|  refreshToken: "mirage_refresh_token",
77|} as const;
78|
79|/** Derive role-specific token keys from the current page path. */
80|function _detectRoleFromPath(): string {
81|  if (typeof window === "undefined") return "global";
82|  const path = window.location.pathname;
83|  if (path.startsWith("/doctor")) return "doctor";
84|  if (path.startsWith("/patient")) return "patient";
85|  if (path.startsWith("/admin")) return "admin";
86|  return "global";
87|}
88|
89|function _tokenKey(role: string, suffix: string): string {
90|  return `mirage_${role}_${suffix}`;
91|}
92|
93|function getCurrentRole(): string {
94|  if (typeof window === "undefined") return "global";
95|  // Try to infer from stored token, then fall back to path
96|  const path = window.location.pathname;
97|  if (path.startsWith("/doctor")) return "doctor";
98|  if (path.startsWith("/patient")) return "patient";
99|  if (path.startsWith("/admin")) return "admin";
100|  return "global";
101|}
102|
103|export function getStoredAccessToken(): string | null {
104|  if (typeof window === "undefined") return null;
105|  const key = _tokenKey(getCurrentRole(), "access_token");
106|  return localStorage.getItem(key);
107|}
108|
109|export function getStoredRefreshToken(): string | null {
110|  if (typeof window === "undefined") return null;
111|  const key = _tokenKey(getCurrentRole(), "refresh_token");
112|  return localStorage.getItem(key);
113|}
114|
115|export function setStoredTokens(role: string, access: string, refresh: string): void {
116|  if (typeof window === "undefined") return;
117|  const accessKey = _tokenKey(role, "access_token");
118|  const refreshKey = _tokenKey(role, "refresh_token");
119|  localStorage.setItem(accessKey, access);
120|  localStorage.setItem(refreshKey, refresh);
121|  const expires = new Date(Date.now() + 7 * 24 * 60 * 60 * 1000).toUTCString();
122|  document.cookie = `access_token=${encodeURIComponent(access)}; path=/; expires=${expires}; SameSite=Lax`;
123|}
124|
125|export function clearStoredTokensForRole(role: string): void {
126|  if (typeof window === "undefined") return;
127|  localStorage.removeItem(_tokenKey(role, "access_token"));
128|  localStorage.removeItem(_tokenKey(role, "refresh_token"));
129|}
130|
131|export function clearStoredTokens(): void {
132|  if (typeof window === "undefined") return;
133|  for (const role of ["doctor", "patient", "admin", "global"]) {
134|    localStorage.removeItem(_tokenKey(role, "access_token"));
135|    localStorage.removeItem(_tokenKey(role, "refresh_token"));
136|  }
137|  document.cookie = "access_token=; path=/; expires=Thu, 01 Jan 1970 00:00:00 GMT; SameSite=Lax";
138|}
139|
140|function redirectToLogin(): void {
141|  if (typeof window === "undefined") return;
142|  const path = window.location.pathname;
143|  if (path.startsWith("/doctor")) {
144|    window.location.href = "/doctor/login";
145|  } else if (path.startsWith("/patient")) {
146|    window.location.href = "/patient/login";
147|  } else if (path.startsWith("/admin")) {
148|    window.location.href = "/admin/login";
149|  } else {
150|    window.location.href = "/";
151|  }
152|}
153|
154|// ------------------------------------------------------------------
155|// Core request wrapper
156|// ------------------------------------------------------------------
157|
158|interface RequestOptions extends RequestInit {
159|  skipAuth?: boolean;
160|}
161|
162|export class ApiError extends Error {
163|  code: string;
164|  field?: string;
165|  status?: number;
166|
167|  constructor(code: string, message: string, field?: string, status?: number) {
168|    super(message);
169|    this.name = "ApiError";
170|    this.code = code;
171|    this.field = field;
172|    this.status = status;
173|  }
174|
175|  static fromEnvelope<T>(envelope: ApiEnvelope<T> | null, status?: number): ApiError {
176|    if (!envelope || !envelope.errors || envelope.errors.length === 0) {
177|      return new ApiError("UNKNOWN", "An unknown error occurred.", undefined, status);
178|    }
179|    const first = envelope.errors[0];
180|    return new ApiError(first.code, first.message, first.field, status);
181|  }
182|}
183|
184|async function request<T>(
185|  endpoint: string,
186|  options: RequestOptions = {}
187|): Promise<T> {
188|  const url = `${API_BASE}${endpoint}`;
189|  const headers = new Headers(options.headers);
190|
191|  headers.set("Accept", "application/json");
192|  if (!options.body || !(options.body instanceof FormData)) {
193|    headers.set("Content-Type", "application/json");
194|  }
195|
196|  if (!options.skipAuth) {
197|    const token = getStoredAccessToken();
198|    if (token) {
199|      headers.set("Authorization", `Bearer ${token}`);
200|    }
201|  }
202|
203|  const response = await fetch(url, {
204|    ...options,
205|    headers,
206|  });
207|
208|  if (response.status === 204) {
209|    return undefined as unknown as T;
210|  }
211|
212|  let body: ApiEnvelope<T> | null = null;
213|  const contentType = response.headers.get("content-type");
214|  if (contentType && contentType.includes("application/json")) {
215|    body = (await response.json()) as ApiEnvelope<T>;
216|  }
217|
218|  // Authentication endpoints intentionally return 401 for invalid credentials.
219|  // They must not invoke token refresh or navigate away from the login form.
220|  if (response.status === 401 && !options.skipAuth) {
221|    const refreshed = await attemptTokenRefresh();
222|    if (!refreshed) {
223|      clearStoredTokensForRole(getCurrentRole());
224|      redirectToLogin();
225|      throw new ApiError("UNAUTHORIZED", "Session expired. Please log in again.");
226|    }
227|    const retryHeaders = new Headers(options.headers);
228|    retryHeaders.set("Accept", "application/json");
229|    if (!options.body || !(options.body instanceof FormData)) {
230|      retryHeaders.set("Content-Type", "application/json");
231|    }
232|    const newToken = getStoredAccessToken();
233|    if (newToken) {
234|      retryHeaders.set("Authorization", `Bearer ${newToken}`);
235|    }
236|
237|    const retryResponse = await fetch(url, {
238|      ...options,
239|      headers: retryHeaders,
240|    });
241|
242|    if (retryResponse.status === 204) {
243|      return undefined as unknown as T;
244|    }
245|
246|    const retryBody = (await retryResponse.json()) as ApiEnvelope<T>;
247|    if (!retryResponse.ok) {
248|      throw ApiError.fromEnvelope(retryBody, retryResponse.status);
249|    }
250|    return parseEnvelope(retryBody);
251|  }
252|
253|  if (!response.ok) {
254|    throw ApiError.fromEnvelope(body, response.status);
255|  }
256|
257|  if (!body) {
258|    throw new ApiError("UNKNOWN", "Empty response from server.");
259|  }
260|
261|  return parseEnvelope(body);
262|}
263|
264|function parseEnvelope<T>(envelope: ApiEnvelope<T>): T {
265|  if (!envelope.success) {
266|    throw ApiError.fromEnvelope(envelope);
267|  }
268|  if (envelope.data === null || envelope.data === undefined) {
269|    throw new ApiError("NO_DATA", "Response envelope contained no data.");
270|  }
271|  return envelope.data;
272|}
273|
274|let isRefreshing = false;
275|
276|async function attemptTokenRefresh(): Promise<boolean> {
277|  if (isRefreshing) return false;
278|  const refreshToken = getStoredRefreshToken();
279|  if (!refreshToken) return false;
280|
281|  isRefreshing = true;
282|  try {
283|    const response = await fetch(`${API_BASE}/auth/refresh`, {
284|      method: "POST",
285|      headers: {
286|        "Content-Type": "application/json",
287|        Accept: "application/json",
288|      },
289|      body: JSON.stringify({ refresh_token: refreshToken }),
290|    });
291|
292|    if (!response.ok) return false;
293|
294|    const envelope = (await response.json()) as ApiEnvelope<{
295|      access_token: string;
296|      token_type: string;
297|      expires_in: number;
298|    }>;
299|
300|    if (!envelope.success || !envelope.data) return false;
301|
302|    // Keep existing refresh token unless backend returns a new one
303|    setStoredTokens(getCurrentRole(), envelope.data.access_token, refreshToken);
304|    return true;
305|  } catch {
306|    return false;
307|  } finally {
308|    isRefreshing = false;
309|  }
310|}
311|
312|// ------------------------------------------------------------------
313|// API Endpoint Groups
314|// ------------------------------------------------------------------
315|
316|export const authApi = {
317|  loginDoctor: (email: string, password: string): Promise<TokenPair> =>
318|    request<TokenPair>("/auth/doctor/login", {
319|      method: "POST",
320|      body: JSON.stringify({ email, password }),
321|      skipAuth: true,
322|    }),
323|
324|  loginAdmin: (email: string, password: string): Promise<TokenPair> =>
325|    request<TokenPair>("/auth/admin/login", {
326|      method: "POST",
327|      body: JSON.stringify({ email, password }),
328|      skipAuth: true,
329|    }),
330|
331|  loginPatient: (national_id: string, pin: string): Promise<TokenPair> =>
332|    request<TokenPair>("/auth/patient/login", {
333|      method: "POST",
334|      body: JSON.stringify({ national_id, pin }),
335|      skipAuth: true,
336|    }),
337|
338|  refreshToken: (refresh_token: string): Promise<{ access_token: string; token_type: string; expires_in: number }> =>
339|    request<{ access_token: string; token_type: string; expires_in: number }>("/auth/refresh", {
340|      method: "POST",
341|      body: JSON.stringify({ refresh_token }),
342|      skipAuth: true,
343|    }),
344|
345|  logout: (): Promise<{ message: string }> =>
346|    request<{ message: string }>("/auth/logout", {
347|      method: "POST",
348|    }),
349|
350|  getMe: (): Promise<UserProfile> =>
351|    request<UserProfile>("/auth/me", {
352|      method: "GET",
353|    }),
354|};
355|
356|export const patientsApi = {
357|  searchPatients: (query: string, limit = 20, offset = 0): Promise<PatientResponse[]> =>
358|    request<PatientResponse[]>(
359|      `/patients?q=${encodeURIComponent(query)}&limit=${limit}&offset=${offset}`,
360|      { method: "GET" }
361|    ),
362|
363|  getPatient: (patientId: string): Promise<PatientFullProfileResponse> =>
364|    request<PatientFullProfileResponse>(`/patients/${patientId}`, { method: "GET" }),
365|
366|  getMyProfile: (): Promise<PatientFullProfileResponse> =>
367|    request<PatientFullProfileResponse>("/me/patient", { method: "GET" }),
368|
369|  getMyTimeline: (): Promise<TimelineEvent[]> =>
370|    request<TimelineEvent[]>("/me/patient/timeline", { method: "GET" }),
371|
372|  getMyVisit: (visitId: string): Promise<VisitWithDetailsResponse> =>
373|    request<VisitWithDetailsResponse>(`/me/patient/visit/${visitId}`, { method: "GET" }),
374|
375|  getMyNotifications: (params?: { unread_only?: boolean; limit?: number; offset?: number }): Promise<NotificationListResponse> => {
376|    const search = new URLSearchParams();
377|    if (params?.unread_only !== undefined) search.set("unread_only", String(params.unread_only));
378|    if (params?.limit) search.set("limit", String(params.limit));
379|    if (params?.offset !== undefined) search.set("offset", String(params.offset));
380|    return request<NotificationListResponse>(`/me/patient/notifications?${search.toString()}`, { method: "GET" });
381|  },
382|
383|  getMyAccessHistory: (): Promise<unknown> =>
384|    request<unknown>("/me/patient/access-history", { method: "GET" }),
385|
386|  getPatientRecords: (patientId: string): Promise<unknown> =>
387|    request<unknown>(`/patients/${patientId}/records`, { method: "GET" }),
388|
389|  registerPatient: (data: Record<string, unknown>): Promise<PatientResponse> =>
390|    request<PatientResponse>("/patients", {
391|      method: "POST",
392|      body: JSON.stringify(data),
393|    }),
394|};
395|
396|export const doctorApi = {
397|  getDoctorPatientOverview: (patientId: string): Promise<DoctorPatientOverview> =>
398|    request<DoctorPatientOverview>(`/doctor/patient/${patientId}`, { method: "GET" }),
399|
400|  updateVisitTranscript: (visitId: string, transcript: string): Promise<VisitResponse> =>
401|    request<VisitResponse>(`/doctor/${visitId}/transcript`, {
402|      method: "PATCH",
403|      body: JSON.stringify(transcript),
404|    }),
405|};
406|
407|export const consentsApi = {
408|  createConsent: (data: CreateConsentPayload): Promise<ConsentRequestResponse> =>
409|    request<ConsentRequestResponse>("/consents", {
410|      method: "POST",
411|      body: JSON.stringify(data),
412|    }),
413|
414|  listConsents: (params?: {
415|    status?: string;
416|    limit?: number;
417|    offset?: number;
418|  }): Promise<ConsentListResponse> => {
419|    const search = new URLSearchParams();
420|    if (params?.status) search.set("status", params.status);
421|    if (params?.limit) search.set("limit", String(params.limit));
422|    if (params?.offset !== undefined) search.set("offset", String(params.offset));
423|    return request<ConsentListResponse>(`/consents?${search.toString()}`, { method: "GET" });
424|  },
425|
426|  getConsent: (consentId: string): Promise<ConsentRequestResponse> =>
427|    request<ConsentRequestResponse>(`/consents/${consentId}`, { method: "GET" }),
428|
429|  approveConsent: (consentId: string): Promise<ConsentRequestResponse> =>
430|    request<ConsentRequestResponse>(`/consents/${consentId}/approve`, { method: "POST" }),
431|
432|  declineConsent: (consentId: string): Promise<ConsentRequestResponse> =>
433|    request<ConsentRequestResponse>(`/consents/${consentId}/decline`, { method: "POST" }),
434|
435|  revokeConsent: (consentId: string): Promise<ConsentRequestResponse> =>
436|    request<ConsentRequestResponse>(`/consents/${consentId}/revoke`, { method: "POST" }),
437|};
438|
439|export const consultationsApi = {
440|  startConsultation: (data: VisitCreatePayload): Promise<VisitResponse> =>
441|444|    request<VisitResponse>("/doctor", {
445|446|      method: "POST",
447|      body: JSON.stringify(data),
448|    }),
449|
450|  listConsultations: (params?: {
451|    status?: string;
452|    limit?: number;
453|    offset?: number;
454|  }): Promise<VisitResponse[]> => {
455|    const search = new URLSearchParams();
456|    if (params?.status) search.set("status", params.status);
457|    if (params?.limit) search.set("limit", String(params.limit));
458|    if (params?.offset !== undefined) search.set("offset", String(params.offset));
459|469|    return request<VisitResponse[]>(`/doctor?${search.toString()}`, { method: "GET" });
470|  },
471|
472|  getConsultation: (visitId: string): Promise<VisitWithDetailsResponse> =>
473|    request<VisitWithDetailsResponse>(`/doctor/${visitId}`, { method: "GET" }),
474|
475|  addNote: (visitId: string, data: ClinicalNoteCreatePayload): Promise<ClinicalNoteResponse> =>
476|    request<ClinicalNoteResponse>(`/doctor/${visitId}/notes`, {
477|478|      method: "POST",
479|      body: JSON.stringify(data),
480|    }),
481|
482|  addDiagnosis: (visitId: string, data: DiagnosisCreatePayload): Promise<DiagnosisResponse> =>
483|486|    request<DiagnosisResponse>(`/doctor/${visitId}/diagnoses`, {
487|488|      method: "POST",
489|      body: JSON.stringify(data),
490|    }),
491|
492|  addMedication: (visitId: string, data: MedicationCreatePayload): Promise<MedicationResponse> =>
493|496|    request<MedicationResponse>(`/doctor/${visitId}/medications`, {
497|498|      method: "POST",
499|      body: JSON.stringify(data),
500|    }),
501|
502|  completeConsultation: (visitId: string): Promise<VisitResponse> =>
503|509|    request<VisitResponse>(`/doctor/${visitId}/complete`, { method: "POST", body: JSON.stringify({}) }),
510|
511|  cancelConsultation: (visitId: string): Promise<VisitResponse> =>
512|    request<VisitResponse>(`/doctor/${visitId}/cancel`, { method: "POST", body: JSON.stringify({}) }),
513|514|};
515|
516|export const aiApi = {
517|  createSession: (patientId?: string): Promise<AISessionResponse> =>
518|    request<AISessionResponse>("/ai/sessions", {
519|      method: "POST",
520|      body: JSON.stringify({ patient_id: patientId } as AISessionCreatePayload),
521|    }),
522|
523|  listSessions: (page = 1, pageSize = 20): Promise<AISessionResponse[]> =>
524|    request<AISessionResponse[]>(`/ai/sessions?page=${page}&page_size=${pageSize}`, { method: "GET" }),
525|
526|  getSession: (sessionId: string): Promise<AISessionWithMessagesResponse> =>
527|    request<AISessionWithMessagesResponse>(`/ai/sessions/${sessionId}`, { method: "GET" }),
528|
529|  sendMessage: (sessionId: string, content: string): Promise<AIMessageResponse> =>
530|    request<AIMessageResponse>(`/ai/sessions/${sessionId}/messages`, {
531|      method: "POST",
532|      body: JSON.stringify({ content } as AIMessageCreatePayload),
533|    }),
534|
535|  getDifferentialDiagnosis: (sessionId: string): Promise<DifferentialDiagnosis[]> =>
536|    request<DifferentialDiagnosis[]>(`/ai/sessions/${sessionId}/diagnosis`, {
537|      method: "POST",
538|      body: JSON.stringify({}),
539|    }),
540|
541|  getClinicalSummary: (sessionId: string): Promise<ClinicalSummary> =>
542|    request<ClinicalSummary>(`/ai/sessions/${sessionId}/summary`, {
543|      method: "POST",
544|      body: JSON.stringify({}),
545|    }),
546|
547|  sendMessageStream: async (
548|    sessionId: string,
549|    content: string,
550|    onChunk: (chunk: AIMessageStreamChunk) => void
551|  ): Promise<void> => {
552|    const token = getStoredAccessToken();
553|    const headers: Record<string, string> = {
554|      "Content-Type": "application/json",
555|      Accept: "text/event-stream",
556|    };
557|    if (token) {
558|      headers["Authorization"] = `Bearer ${token}`;
559|    }
560|
561|    const response = await fetch(`${API_BASE}/ai/sessions/${sessionId}/messages/stream`, {
562|      method: "POST",
563|      headers,
564|      body: JSON.stringify({ content } as AIMessageCreatePayload),
565|    });
566|
567|    if (!response.ok) {
568|      throw new ApiError("AI_STREAM_ERROR", "Failed to start AI message stream.");
569|    }
570|
571|    const reader = response.body?.getReader();
572|    if (!reader) {
573|      throw new ApiError("AI_STREAM_ERROR", "Readable stream not supported.");
574|    }
575|
576|    const decoder = new TextDecoder();
577|    let buffer = "";
578|
579|    try {
580|      while (true) {
581|        const { done, value } = await reader.read();
582|        if (done) break;
583|
584|        buffer += decoder.decode(value, { stream: true });
585|        const lines = buffer.split("\n");
586|        buffer = lines.pop() ?? "";
587|
588|        for (const line of lines) {
589|          const trimmed = line.trim();
590|          if (trimmed.startsWith("data: ")) {
591|            const data = trimmed.slice(6);
592|            if (data === "[DONE]") return;
593|            try {
594|              const parsed = JSON.parse(data) as AIMessageStreamChunk;
595|              if (parsed.done) return;
596|              onChunk(parsed);
597|            } catch {
598|              // Ignore malformed JSON lines
599|            }
600|          }
601|        }
602|      }
603|    } finally {
604|      reader.releaseLock();
605|    }
606|  },
607|};
608|
609|export const notificationsApi = {
610|  listNotifications: (params?: {
611|    unread_only?: boolean;
612|    limit?: number;
613|    offset?: number;
614|  }): Promise<NotificationListResponse> => {
615|    const search = new URLSearchParams();
616|    if (params?.unread_only !== undefined) search.set("unread_only", String(params.unread_only));
617|    if (params?.limit) search.set("limit", String(params.limit));
618|    if (params?.offset !== undefined) search.set("offset", String(params.offset));
619|    return request<NotificationListResponse>(`/notifications?${search.toString()}`, { method: "GET" });
620|  },
621|
622|  getUnreadCount: (): Promise<UnreadCountResponse> =>
623|    request<UnreadCountResponse>("/notifications/unread-count", { method: "GET" }),
624|
625|  markRead: (notificationId: string): Promise<NotificationResponse> =>
626|    request<NotificationResponse>(`/notifications/${notificationId}/read`, { method: "POST" }),
627|
628|  markAllRead: (): Promise<CountResponse> =>
629|    request<CountResponse>("/notifications/read-all", { method: "POST" }),
630|};
631|
632|export const appointmentsApi = {
633|  create: (data: AppointmentCreateRequest): Promise<AppointmentResponse> =>
634|    request<AppointmentResponse>("/appointments", {
635|      method: "POST",
636|      body: JSON.stringify(data),
637|    }),
638|
639|  listMy: (params?: {
640|    status?: string;
641|    upcoming?: boolean;
642|    limit?: number;
643|    offset?: number;
644|  }): Promise<AppointmentListResponse> => {
645|    const search = new URLSearchParams();
646|    if (params?.status) search.set("status", params.status);
647|    if (params?.upcoming !== undefined) search.set("upcoming", String(params.upcoming));
648|    if (params?.limit) search.set("limit", String(params.limit));
649|    if (params?.offset !== undefined) search.set("offset", String(params.offset));
650|    return request<AppointmentListResponse>(`/appointments/my?${search.toString()}`, { method: "GET" });
651|  },
652|
653|  getById: (id: string): Promise<AppointmentResponse> =>
654|    request<AppointmentResponse>(`/appointments/${id}`, { method: "GET" }),
655|
656|  cancel: (id: string, reason?: string): Promise<AppointmentResponse> =>
657|    request<AppointmentResponse>(`/appointments/${id}/cancel`, {
658|      method: "POST",
659|      body: JSON.stringify({ reason }),
660|    }),
661|
662|  confirm: (id: string): Promise<AppointmentResponse> =>
663|    request<AppointmentResponse>(`/appointments/${id}/confirm`, {
664|      method: "POST",
665|      body: JSON.stringify({}),
666|    }),
667|
668|  startConsultation: (id: string): Promise<{ consultation_id: string }> =>
669|    request<{ consultation_id: string }>(`/appointments/${id}/start-consultation`, {
670|      method: "POST",
671|      body: JSON.stringify({}),
672|    }),
673|};
674|
675|export const facilitiesApi = {
676|  search: (query?: string, limit = 20, offset = 0): Promise<{ items: Facility[]; total: number; limit: number; offset: number }> => {
677|    const search = new URLSearchParams();
678|    if (query) search.set("q", query);
679|    search.set("limit", String(limit));
680|    search.set("offset", String(offset));
681|    return request<{ items: Facility[]; total: number; limit: number; offset: number }>(`/appointments/facilities?${search.toString()}`, { method: "GET" });
682|  },
683|
684|  getById: (id: string): Promise<Facility> =>
685|    request<Facility>(`/appointments/facilities/${id}`, { method: "GET" }),
686|
687|  getDoctors: (id: string): Promise<
688|    { id: string; name: string; specialty: string }[]
689|  > =>
690|    request<{ id: string; name: string; specialty: string }[]>(`/appointments/facilities/${id}/doctors`, {
691|      method: "GET",
692|    }),
693|};
694|
695|export const auditApi = {
696|  getAccessHistory: (params?: {
697|    limit?: number;
698|    offset?: number;
699|  }): Promise<{ items: AuditLogEntry[]; total: number }> => {
700|    const search = new URLSearchParams();
701|    if (params?.limit) search.set("limit", String(params.limit));
702|    if (params?.offset !== undefined) search.set("offset", String(params.offset));
703|    return request<{ items: AuditLogEntry[]; total: number }>(`/audit/history?${search.toString()}`, { method: "GET" });
704|  },
705|};
706|
707|export const scheduleApi = {
708|  getMySchedule: (): Promise<DoctorScheduleView> =>
709|    request<DoctorScheduleView>("/doctor/schedule", { method: "GET" }),
710|
711|  getMyAppointments: (): Promise<ScheduleAppointment[]> =>
712|    request<ScheduleAppointment[]>("/doctor/appointments", { method: "GET" }),
713|
714|  getMyAppointmentsToday: (): Promise<ScheduleAppointment[]> =>
715|    request<ScheduleAppointment[]>("/doctor/appointments/today", { method: "GET" }),
716|
717|  updateAppointmentStatus: (id: string, status: AppointmentStatus): Promise<ScheduleAppointment> =>
718|    request<ScheduleAppointment>(`/doctor/appointments/${id}/status`, {
719|      method: "PUT",
720|      body: JSON.stringify({ status }),
721|    }),
722|
723|  requestLeave: (data: TimeOffRequest): Promise<TimeOffResponse> =>
724|    request<TimeOffResponse>("/doctor/time-off", {
725|      method: "POST",
726|      body: JSON.stringify(data),
727|    }),
728|};
729|
730|// ------------------------------------------------------------------
731|// Admin API
732|// ------------------------------------------------------------------
733|
734|export const adminApi = {
735|  getDashboard: (): Promise<AdminDashboardStats> =>
736|    request<AdminDashboardStats>("/appointments/admin/dashboard", { method: "GET" }),
737|
738|  listDoctors: (params?: { limit?: number; offset?: number }): Promise<AdminDoctorListItem[]> => {
739|    const search = new URLSearchParams();
740|    if (params?.limit) search.set("limit", String(params.limit));
741|    if (params?.offset !== undefined) search.set("offset", String(params.offset));
742|    return request<AdminDoctorListItem[]>(`/appointments/admin/doctors?${search.toString()}`, { method: "GET" });
743|  },
744|
745|  getDoctorSchedule: (doctorId: string): Promise<DoctorScheduleResponse> =>
746|    request<DoctorScheduleResponse>(`/appointments/admin/doctors/${doctorId}/schedule`, { method: "GET" }),
747|
748|  updateDoctorSchedule: (doctorId: string, data: ScheduleUpdateRequest): Promise<DoctorScheduleResponse> =>
749|    request<DoctorScheduleResponse>(`/appointments/admin/doctors/${doctorId}/schedule`, {
750|      method: "PUT",
751|      body: JSON.stringify(data),
752|    }),
753|
754|  addTimeOff: (doctorId: string, data: TimeOffAdminRequest): Promise<TimeOffEntry> =>
755|    request<TimeOffEntry>(`/appointments/admin/doctors/${doctorId}/time-off`, {
756|      method: "POST",
757|      body: JSON.stringify(data),
758|    }),
759|
760|  listDoctorTimeOff: (doctorId: string): Promise<TimeOffEntry[]> =>
761|    request<TimeOffEntry[]>(`/appointments/admin/doctors/${doctorId}/time-off`, { method: "GET" }),
762|
763|  approveTimeOff: (timeOffId: string): Promise<TimeOffEntry> =>
764|    request<TimeOffEntry>(`/appointments/admin/doctors/time-off/${timeOffId}/approve`, { method: "POST" }),
765|
766|  rejectTimeOff: (timeOffId: string): Promise<TimeOffEntry> =>
767|    request<TimeOffEntry>(`/appointments/admin/doctors/time-off/${timeOffId}/reject`, { method: "POST" }),
768|
769|  listAppointments: (filters?: AppointmentAdminFilters): Promise<PaginatedAdminAppointments> => {
770|    const search = new URLSearchParams();
771|    if (filters?.date_from) search.set("date_from", filters.date_from);
772|    if (filters?.date_to) search.set("date_to", filters.date_to);
773|    if (filters?.facility_id) search.set("facility_id", filters.facility_id);
774|    if (filters?.status) search.set("status", filters.status);
775|    if (filters?.priority) search.set("priority", filters.priority);
776|    if (filters?.doctor_search) search.set("doctor_search", filters.doctor_search);
777|    if (filters?.patient_search) search.set("patient_search", filters.patient_search);
778|    // Convert page/page_size to limit/offset for backend
779|    const page = filters?.page ?? 1;
780|    const page_size = filters?.page_size ?? 20;
781|    search.set("limit", String(page_size));
782|    search.set("offset", String((page - 1) * page_size));
783|    return request<{ items: AppointmentAdminItem[]; total: number; limit: number; offset: number }>(
784|      `/appointments/admin/appointments?${search.toString()}`,
785|      { method: "GET" }
786|    ).then((r) => ({
787|      items: r.items,
788|      total: r.total,
789|      page,
790|      page_size,
791|      total_pages: Math.max(1, Math.ceil(r.total / page_size)),
792|    }));
793|  },
794|
795|  cancelAppointment: (appointmentId: string): Promise<{ message: string }> =>
796|    request<{ message: string }>(`/appointments/admin/appointments/${appointmentId}/cancel`, { method: "PUT" }),
797|
798|  reassignDoctor: (appointmentId: string, doctorId: string): Promise<AppointmentAdminItem> =>
799|    request<AppointmentAdminItem>(`/appointments/admin/appointments/${appointmentId}/reassign`, {
800|      method: "PUT",
801|      body: JSON.stringify({ doctor_id: doctorId }),
802|    }),
803|
804|  // Settings
805|  listSettings: (): Promise<SystemConfigItem[]> =>
806|    request<SystemConfigItem[]>("/admin/settings", { method: "GET" }),
807|
808|  updateSetting: (key: string, data: UpdateSystemConfigPayload): Promise<SystemConfigItem> =>
809|    request<SystemConfigItem>(`/admin/settings/${key}`, { method: "PUT", body: JSON.stringify(data) }),
810|
811|  // Facilities CRUD
812|  listFacilities: (): Promise<AdminFacilityItem[]> =>
813|    request<AdminFacilityItem[]>("/admin/facilities", { method: "GET" }),
814|
815|  getFacility: (id: string): Promise<AdminFacilityItem> =>
816|    request<AdminFacilityItem>(`/admin/facilities/${id}`, { method: "GET" }),
817|
818|  createFacility: (data: CreateFacilityPayload): Promise<AdminFacilityItem> =>
819|    request<AdminFacilityItem>("/admin/facilities", {
820|      method: "POST",
821|      body: JSON.stringify(data),
822|    }),
823|
824|  updateFacility: (id: string, data: UpdateFacilityPayload): Promise<AdminFacilityItem> =>
825|    request<AdminFacilityItem>(`/admin/facilities/${id}`, {
826|      method: "PUT",
827|      body: JSON.stringify(data),
828|    }),
829|
830|  deleteFacility: (id: string): Promise<void> =>
831|    request<void>(`/admin/facilities/${id}`, { method: "DELETE" }),
832|};
833|