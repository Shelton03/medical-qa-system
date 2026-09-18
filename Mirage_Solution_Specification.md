# Mirage: Consent-Driven Patient Records with AI Clinical Assistance

**Solution Specification | 2026 POTRAZ Innovation Expo and Conference**

Theme: Harnessing Local Innovation for Inclusive Industrial Transformation and Sustainable Development. Sub-theme: Emerging Technologies and Digital Transformation for Industry Solutions (Digital Health Services). Competition category: Tertiary Level.

---

## Table of Contents

1. Solution Specification (Problem, Objectives, User Needs, Features)
2. Target Market and Value Proposition
3. Business and Revenue Model
4. Solution Design and Architecture
5. Implementation, Testing and Proof of Concept
6. Social and Technological Impact
7. Data Security and Privacy
8. Previous Projects and Evidence
9. User / Product Manual

---

## 1. Solution Specification

**Problem addressed.** Healthcare information in Zimbabwe is fragmented across hospitals, clinics and private practices. Patients carry paper records between facilities; histories are incomplete; laboratory results and medication histories are unavailable during consultations; previous diagnoses are inaccessible. Providers respond by repeating tests and imaging, prescribing without complete allergy information, and spending consultation time reconstructing history instead of treating. The problem is compounded by a severe health-workforce shortage: the WHO-assisted Health Labour Market Analysis recorded a need-based shortage of 57,543 health workers in 2022, projected to reach 64,363 by 2030, with only about 23 doctors, nurses and midwives per 10,000 population, less than half the WHO threshold for universal health coverage. Every minute a clinician spends reconstructing a paper history is a minute not spent on care.

**Solution objectives.**

1. Place ownership and control of medical records in the hands of patients, not institutions.
2. Guarantee that verified practitioners access records only with explicit, per-episode, time-scoped patient consent.
3. Let AI assist (symptom assessment, differential diagnosis, clinical summaries) while the clinician remains responsible for every final decision and record update.
4. Present each patient's history as one continuous timeline regardless of where treatment occurred.
5. Log every access and change to an immutable audit trail that patients can review.

**User and stakeholder needs.** Patients need safety (allergy warnings always visible), control (approve or deny every request on a phone they already own), and continuity (one timeline across facilities). Doctors need speed (patient found and record unlocked within seconds of approval), reduced documentation burden (AI-drafted notes they review and approve), and decision support (ranked differentials with confidence estimates). Facility administrators need practitioner verification and audit-ready compliance records.

**Key functional features.** Patient app (mobile-first): secure login, home dashboard, complete medical record, AI symptom assessment, consent approvals, real-time notifications, health timeline, medical ID with pinned allergy banner, personal access log. Doctor portal: tolerant patient search, consent request and management, consent-gated record review, AI-assisted consultation with streaming chat, editable clinical summary (SOAP) generation, ranked differential diagnoses with confidence, prescriptions, access history. Platform: one-click demo mode with seeded synthetic data, immutable audit logging, medical-record versioning (corrections create new versions, nothing is deleted).

**Non-functional features.** Real-time patient-doctor synchronisation over WebSockets with a Redis pub/sub event bus; versioned typed REST API with a uniform response envelope; role-based access control with short-lived JWTs; AI layer abstracted behind provider interfaces so the model vendor is swappable per deployment; offline-first design for rural facilities (facility-level cache, background sync with conflict resolution); containerised deployment that starts the full stack with one command.

## 2. Target Market and Value Proposition

**Primary users.** Patients (urban and rural) who move between facilities and currently carry paper records; doctors and nurses at hospitals, clinics and private practices; facility administrators responsible for practitioner verification; and the ministry's public-health reporting function.

**Market context.** Zimbabwe has approximately 17.1 million people. The 2025 ICT Access by Households and Use by Individuals Survey (ZimStat and POTRAZ) found 96.4% of households have access to a mobile phone, 75.1% own smartphones, and 92.5% of households are covered by a mobile network. A mobile-first delivery model therefore matches how Zimbabweans actually access digital services. Health-sector demand is structural: Zimbabwe needs at least 5.15 generalist doctors per 10,000 population (about 1 per 1,942 people), and the projected workforce shortfall reaches 64,363 by 2030. Technology that raises clinician productivity and record quality addresses a national bottleneck rather than a convenience. The same model extends to neighbouring health systems with comparable fragmented, paper-based records.

**Beachhead and expansion.** The immediate beachhead is pilot partnerships: one private clinic group and one university teaching-hospital department, running alongside existing paper processes. Expansion follows the referral network: facilities that share patients adopt the platform to receive complete histories. Each facility's value case is fewer repeated tests, faster consultations, complete allergy information at the point of prescribing, and audit-ready records.

**Value proposition.** For patients: your record follows you, you decide who sees it, and critical safety information is always visible. For doctors: complete history in seconds instead of minutes of reconstruction, AI-drafted documentation you approve, decision support with the clinician signing every diagnosis. For the health system: fewer duplicate investigations, better data quality for public-health reporting, and a consent model that builds patient trust.

## 3. Business and Revenue Model

**Revenue streams.**

1. **Facility subscriptions:** tiered per-clinician monthly licensing for private clinics and practices (pilot pricing USD 20-50 per clinician per month by tier).
2. **Public-sector deployment contracts:** per-facility or per-district licensing sold to government and donor-funded health programmes, aligned with existing digital-health procurement.
3. **Integration and setup services:** one-time onboarding, migration from paper archives, and staff training.
4. **Consented analytics (future):** anonymised, aggregate-level public-health reporting sold to ministries and NGOs. Individual records are never exported to the analytics layer.

**Cost structure.** Cloud hosting scales with usage (containerised, stateless services over managed PostgreSQL, Redis and object storage). AI inference is usage-based and provider-agnostic, so the most cost-effective suitable model can be selected per deployment. The dominant pilot-phase costs are engineering and clinical-partner engagement.

**Pricing strategy.** Free for patients, always. Patient-side charging would undermine the ownership model that is the point of the platform. Facilities pay because the platform saves clinician time and repeated-test costs; subscriptions are priced against the measurable value of avoided duplicate laboratory tests and shorter consultations.

**Sustainability pathway.** Phase 1 (validation): university and private-clinic pilots at partner cost. Phase 2 (commercialisation): paid pilots convert to subscriptions; donor-funded digital-health programmes provide public-sector entry. Phase 3 (scale): regional expansion plus API licensing to health-financing schemes that require portable records. The open-source core (record model, consent engine, AI safety harness) keeps vendor lock-in low and builds ecosystem trust.

## 4. Solution Design and Architecture

Mirage is a cloud-native, layered architecture designed for scalability, offline resilience and patient data sovereignty, hosted in an African cloud region for data-residency compliance.

**Layer 1 - Client surfaces.** Patient App (mobile-first: record, consent, AI chat, offline cache), Doctor Portal (web: search, records, AI assistance, clinical notes, low-bandwidth optimised), Admin Console (facility administration and analytics), and a national surveillance dashboard for population-health reporting. The patient experience renders inside a realistic phone-frame simulator with a split-screen demo mode showing both sides of a consent episode on one screen.

**Layer 2 - Gateway and access control.** API Gateway (rate limiting, routing, TLS termination, load balancing), Auth Service (JWT issuance, role verification, session management), Consent Orchestrator (request/approve flow, time-scoped access-token issuance, audit logging, WebSocket real-time push), and a Clinician Registry that verifies practitioners against professional council registers (medical and nursing councils) before any access request is dispatched.

**Layer 3 - Application services.** Patient Record Service (CRUD, history, versioning), Notification Service (WebSocket push with SMS fallback through local mobile-network operators), Analytics Service (anonymised, aggregate only), and Session Transcription Service (consultation audio capture, speech-to-text, draft summary pending doctor approval).

**Layer 4 - AI services.** An AI Diagnostic Service behind a vendor-agnostic provider interface: a structured medical question engine, ranked differential-diagnosis generation, and clinical context tuning to local epidemiology. Business logic depends only on the interface; the concrete model is selected per deployment and can be replaced without code changes. Future direction: fine-tuning on local clinical data.

**Layer 5 - Data.** Patient Records database (PostgreSQL, encrypted, multi-AZ backups), Clinician database (verified practitioners), an append-only immutable Audit Log recording every access event, and a read-optimised Analytics Store holding only anonymised, aggregated data. A Redis session cache backs real-time and WebSocket features.

**External integrations.** SMS gateway connectivity to local mobile-network operators for notification fallback, and integration with the national health management information system for facility reporting.

**Key design decisions.**

- **Consent-first.** (1) Practitioner sends an access request, verified against the Clinician Registry before dispatch; (2) the patient receives a real-time push with the practitioner's identity, facility and reason; (3) approval issues a time-scoped access token and record data flows; (4) every event is written to the immutable Audit Log, reviewable by the patient at any time. Requests carry requester, facility, registration number, reason, scope and expiry; denial closes the request and expiry revokes access automatically.
- **AI safety model.** (1) AI reads only the approved patient history before starting a diagnostic session; (2) questions follow a structured sequence, not free-form generation; (3) differentials are ranked suggestions that the doctor must confirm before any record update; (4) allergy conflicts are surfaced automatically in any recommendation involving flagged medications. Every AI output carries a clinical disclaimer and requires clinician approval.
- **Offline-first for rural facilities.** Facility-level read caches store approved records locally; new entries queue when offline and sync on reconnection with conflict resolution; critical allergy flags are always available from local cache.
- **Data sovereignty.** All data hosted in an African cloud region so nothing leaves national jurisdiction; encryption at rest and in transit; analytics uses anonymised aggregates only; alignment with the Zimbabwe Data Protection Act and national health-data governance guidelines.

**Primary data flows.**

| Flow | Trigger | Path | Security control |
|---|---|---|---|
| Record access request | Doctor requests records | Portal → Gateway → Consent Orchestrator → Notification Service → Patient App | Registry verification; patient approval required |
| Record access grant | Patient approves | Patient App → Consent Orchestrator → time-scoped token → Record Service → Doctor Portal | Time-limited token; access logged |
| AI diagnostic session | Doctor opens AI tab | Portal → Gateway → AI Service → Records DB (read) → model provider → Portal | Valid access token; output marked as suggestion |
| Record update | Doctor confirms diagnosis | Portal → Gateway → Record Service → PostgreSQL + Audit Log | Practitioner authentication; writes versioned |
| Analytics pipeline | Scheduled batch | Record Service → anonymiser → Analytics Store → surveillance dashboard | Anonymised before write; no individual records |
| Offline sync | Connectivity restored | Local cache → sync agent → Gateway → Record Service → conflict resolution | Clinical-priority conflict rules; sync events logged |

## 5. Implementation, Testing and Proof of Concept

**Development process.** The platform was built spec-first: a 13-document specification set (product requirements, technical architecture, API contract, database schema, UI screen specification, user flows and state machines) was written before implementation, and code was generated phase by phase against it, keeping the implementation consistent with documented intent.

**Implemented and tested.** The working core exists in a public repository: a FastAPI backend with versioned REST routes for authentication, patients, doctors, consents, records, timeline, AI sessions, notifications, transcription and audit; a PostgreSQL schema of 21 relational tables with migrations; Redis pub/sub driving real-time WebSocket events (consent requested, approved, declined, revoked; record updated; AI response ready); JWT authentication with role-based access and refresh-token rotation; a Next.js frontend with the patient app, doctor portal and split-screen demo; and Docker Compose orchestration with health checks for all services. Automated tests cover authentication, consent, records, AI, audit, middleware, migrations, providers, WebSocket and seeding on the backend, plus component tests on the frontend. Demo mode seeds a complete synthetic world so the full workflow can be exhibited without real patient data.

**Proof of concept - the exhibited workflow.** The Expo demonstration runs a complete clinical episode in under five minutes: (1) the doctor logs in and searches for the demo patient; (2) the doctor requests record access with reason, scope and expiry; (3) the request appears instantly on the patient's phone; (4) the patient approves and the doctor's view unlocks in real time; (5) the patient completes an AI symptom assessment; (6) the doctor consults with AI assistance: streaming chat, ranked differential with confidence, editable SOAP summary; (7) the doctor confirms the diagnosis and approves the note; (8) the record updates and the patient sees the new entry immediately, with the access logged for patient review. The AI layer runs on a deterministic mock provider during exhibition so the demo has no network dependency.

**Validation plan.** Next: a supervised pilot with one teaching-hospital department and one private clinic running alongside paper processes, measured on consultation preparation time, duplicate-test rate and consent completion rate. The immediate engineering milestone is wiring the standalone medical question-answering engine (self-consistency voting with abstention-by-default under uncertainty) into the platform as a live symptom-assessment provider behind the existing interface.

## 6. Social and Technological Impact

**Social impact.** Patient safety: complete allergy and medication information at the point of care directly reduces preventable prescribing errors. Continuity of care benefits rural and low-income patients most, since they visit multiple facilities. Inclusion: the patient app runs in any browser on the phones 96.4% of households already own, with SMS fallback for notifications; no new hardware and a two-tap consent flow readable on a small screen. Youth and skills: the project demonstrates local tertiary students building production-grade health infrastructure, and its open-source LLM safety-evaluation toolkit contributes to a local responsible-AI skills base aligned with the Expo's future-workforce goals.

**Technological impact.** Mirage is a working reference implementation of three patterns the national digital-health ecosystem needs: (1) consent-based health-data sharing, a patient-approval gate that regulators can reference when drafting health-data governance rules; (2) vendor-agnostic AI in clinical workflows, with every capability behind an interface, a clinical disclaimer and a human-approval gate, demonstrating responsible AI as the sub-theme requires; (3) real-time, mobile-first service delivery on existing infrastructure (92.5% household mobile coverage). The architecture is portable across model vendors and deployable on modest infrastructure.

**Sustainability and ethics.** The consent model is the ethics: no data leaves the patient's control without an explicit, scoped, expiring approval that the patient can review afterwards. AI never writes to the record unreviewed; the clinician signs every diagnosis. Equitable access (free, browser-only patient side), algorithmic transparency (confidence estimates and rationales shown to the clinician), and the deliberate exclusion of emergency-override paths until such policy is formally defined are documented in the product requirements.

## 7. Data Security and Privacy

**Consent-first access control.** Every record access requires a patient-approved consent request carrying requester identity, facility, registration number, reason, scope and expiry. Approval is immediate and logged; access expires automatically; denial and revocation are supported; patients can review who viewed their records and when.

**Technical measures.** Role-based access control (patient, doctor, admin) enforced server-side on every endpoint; short-lived JWT access tokens with refresh-token rotation and hash-at-rest storage; logout token blacklisting; per-IP and per-endpoint rate limiting; correlation IDs on every request for traceability. Encryption at rest and TLS in transit terminate at the deployment layer, with managed-database encryption and multi-AZ backups for the system of record. Secrets live in environment configuration, never in source.

**Auditability and privacy by design.** An immutable, append-only audit log records every access, consent transition, record change and AI session; middleware writes an entry for every request. Record corrections create new versions rather than overwriting, preserving full history. The AI layer receives only the data the approved consent scope covers, and its outputs require clinician approval before touching the record. The analytics path anonymises before writing; individual records never enter the analytics layer. Compliance is aligned to the Zimbabwe Data Protection Act and national health-data governance guidelines. All exhibition data is synthetic; no real patient information is used.

## 8. Previous Projects and Evidence

- **Mirage platform (this project):** github.com/Shelton03/medical-qa-system - full source: FastAPI backend, Next.js frontend, 13-document specification set, automated tests, Docker deployment, and the split-screen demo mode built for live exhibition.
- **aiguard-safety (team lead):** github.com/Shelton03/aiguard and on PyPI - an open-source LLM safety-evaluation toolkit (prompt-injection, jailbreak and harmful-content test harnesses) directly relevant to the responsible-AI sub-theme.
- **Medical QA System (prior iteration):** the team's earlier interactive medical question-answering engine with self-consistency voting and abstention-by-default decision logic, included in the same repository and being integrated as the platform's symptom-assessment provider.
- **Specification documents:** docs/ in the repository: product requirements, technical architecture, API contract, database schema, UI screen specification, user flows and state machines, deployment guide.

## 9. User / Product Manual (Brief Guide)

**Running the demonstration.** The stack starts with two commands (copy the environment template, then build and start with Docker Compose). The split-screen exhibition view shows the doctor portal on the left and the patient app inside a phone frame on the right; a guided ten-step walkthrough plays the full consent episode with narration, driven by keyboard controls (arrow keys to step, space to play/pause, R to restart).

**Access.** Demo mode is enabled by default: one-click demo login for the patient and doctor roles, with seeded synthetic data. The backend API and interactive documentation are served on port 8000. Server deployment follows the same Docker Compose file; the repository README documents the full procedure, and the design targets container deployment in an African cloud region with managed database backups.

---

*Statistics cited: ZimStat/POTRAZ 2025 ICT Access by Households and Use by Individuals Survey (household mobile access 96.4%, smartphone ownership 75.1%, mobile network coverage 92.5%); WHO Zimbabwe Health Labour Market Analysis 2023 (need-based health-workforce shortage 57,543 in 2022, projected 64,363 by 2030; approximately 23 doctors, nurses and midwives per 10,000 population; 5.15 generalist doctors required per 10,000). Sources available on request.*
