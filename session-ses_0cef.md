# Create subagents with Agents.md

**Session ID:** ses_0cef0f91cffev5YdmREHxthEji
**Created:** 7/5/2026, 8:54:56 AM
**Updated:** 7/5/2026, 5:10:25 PM

---

## User

use Agents.md and create subagents to do the tasks we need to work

---

## Assistant (Plan · Kimi · 4.0s)

_Thinking:_

 Let me understand the request. The user wants me to use AGENTS.md and create subagents to do tasks. However, I'm currently in Plan Mode, which means I can only read/inspect and plan — no file edits or modifications.

First, I should read the AGENTS.md file and the other documentation files mentioned in it to understand the project structure and requirements. Then I can create a plan and potentially delegate exploration tasks to subagents.

Let me start by reading the AGENTS.md and the key documentation files.

 I'll read the project documentation to understand the structure and requirements, then create a plan with subagents. 

**Tool: read**

**Input:**
```json
{
  "filePath": "/Users/sheltonmutambirwa/Desktop/medic/AGENTS.md"
}
```

**Output:**
```
<path>/Users/sheltonmutambirwa/Desktop/medic/AGENTS.md</path>
<type>file</type>
<content>
1: # Mirage Development Instructions
2: 
3: Before generating code, read these documents in order:
4: 
5: docs/00_Project_Index.md
6: 
7: docs/01_Product_Requirements_Document.md
8: 
9: docs/02_Technical_Architecture.md
10: 
11: docs/03_Design_System.md
12: 
13: docs/04_Implementation_Plan.md
14: 
15: docs/05_API_Contract.md
16: 
17: docs/06_Database_Schema.md
18: 
19: docs/07_Master_Generation_Prompt.md
20: 
21: docs/08_Coding_Standards.md
22: 
23: docs/09_Deployment_Guide.md
24: 
25: docs/10_UI_Screen_Specification.md
26: 
27: docs/11_User_Flows_and_State_Machines.md
28: 
29: The Product Requirements Document is the authoritative source of product behaviour.
30: 
31: The Technical Architecture is the authoritative source of implementation.
32: 
33: The Database Schema is the authoritative source of persistence.
34: 
35: The API Contract is the authoritative source of API behaviour.
36: 
37: The Coding Standards define repository conventions.
38: 
39: Do not invent functionality not described in the documentation.
40: 
41: When uncertain, stop and ask for clarification rather than making assumptions.

(End of file - total 41 lines)
</content>
```

**Tool: read**

**Input:**
```json
{
  "filePath": "/Users/sheltonmutambirwa/Desktop/medic/docs/00_Project_Index.md"
}
```

**Output:**
```
<path>/Users/sheltonmutambirwa/Desktop/medic/docs/00_Project_Index.md</path>
<type>file</type>
<content>
1: # Mirage
2: # Project Index
3: 
4: Version: 1.0
5: 
6: ---
7: 
8: # Purpose
9: 
10: Welcome to the Mirage project.
11: 
12: This document is the entry point for the entire repository and should be the **first document read** by any engineer or AI coding assistant before implementation begins.
13: 
14: It defines:
15: 
16: - The project vision
17: - Documentation hierarchy
18: - Reading order
19: - Source-of-truth precedence
20: - Implementation phases
21: - Success criteria
22: 
23: Every other document assumes this file has already been read.
24: 
25: ---
26: 
27: # Project Overview
28: 
29: Mirage is a healthcare platform designed to improve patient-doctor interactions through secure, real-time collaboration and AI-assisted clinical workflows.
30: 
31: The system consists of two primary applications:
32: 
33: ## Patient Application
34: 
35: A mobile-first web application rendered inside a realistic simulated phone frame.
36: 
37: The patient application allows users to:
38: 
39: - Log in securely
40: - Complete an AI-powered symptom assessment
41: - Receive consent requests
42: - Approve or deny access to medical records
43: - Participate in consultations
44: - View medical history
45: - Review consultation summaries
46: - Receive notifications
47: 
48: The application is intentionally designed to mimic a native mobile application while running entirely in the browser.
49: 
50: ---
51: 
52: ## Doctor Portal
53: 
54: A desktop-first clinical dashboard.
55: 
56: Doctors can:
57: 
58: - Search for patients
59: - Request consent
60: - Review patient timelines
61: - Conduct consultations
62: - Generate AI-assisted documentation
63: - Finalize consultation notes
64: - Update medical records
65: - Monitor notifications
66: 
67: ---
68: 
69: ## Demonstration Mode
70: 
71: The repository also includes a split-screen demonstration mode.
72: 
73: This mode displays:
74: 
75: Patient Application
76: 
77: ↓
78: 
79: Doctor Portal
80: 
81: side by side.
82: 
83: The purpose is to demonstrate:
84: 
85: - Consent workflow
86: - Real-time synchronization
87: - AI assistance
88: - Notification delivery
89: - Medical record updates
90: 
91: without requiring multiple physical devices.
92: 
93: ---
94: 
95: # Technology Stack
96: 
97: ## Backend
98: 
99: - Python 3.12+
100: - FastAPI
101: - SQLAlchemy 2.x
102: - PostgreSQL
103: - Redis
104: - Alembic
105: - JWT Authentication
106: 
107: ---
108: 
109: ## Frontend
110: 
111: - Next.js
112: - TypeScript
113: - TailwindCSS
114: - Framer Motion
115: - React Query
116: - React Hook Form
117: - Zod
118: 
119: ---
120: 
121: ## Infrastructure
122: 
123: - Docker
124: - Docker Compose
125: 
126: The repository should run locally using a single command:
127: 
128: ```
129: docker compose up
130: ```
131: 
132: ---
133: 
134: # AI Architecture
135: 
136: The system integrates multiple AI capabilities.
137: 
138: These include:
139: 
140: - Existing Symptom Checker
141: - Transcription
142: - Clinical Summaries
143: - Diagnostic Suggestions
144: 
145: These services are **not implemented directly**.
146: 
147: Instead they are abstracted behind provider interfaces.
148: 
149: Business logic must never depend directly on any AI vendor SDK.
150: 
151: ---
152: 
153: # Documentation Structure
154: 
155: The repository documentation consists of the following files.
156: 
157: ```
158: docs/
159: 
160: 00_Project_Index.md
161: 
162: 01_Product_Requirements_Document.md
163: 
164: 02_Technical_Architecture.md
165: 
166: 03_Design_System.md
167: 
168: 04_Implementation_Plan.md
169: 
170: 05_API_Contract.md
171: 
172: 06_Database_Schema.md
173: 
174: 07_Master_Generation_Prompt.md
175: 
176: 08_Coding_Standards.md
177: 
178: 09_Deployment_Guide.md
179: 
180: 09_Deployment_Guide.md
181: 
182: 10_UI_Screen_Specification.md
183: 
184: 11_User_Flows_and_State_Machines.md
185: ```
186: 
187: Each document has a distinct responsibility.
188: 
189: ---
190: 
191: # Reading Order
192: 
193: Documentation should be read in the following order.
194: 
195: Project Index
196: 
197: ↓
198: 
199: Product Requirements
200: 
201: ↓
202: 
203: Technical Architecture
204: 
205: ↓
206: 
207: Design System
208: 
209: ↓
210: 
211: Implementation Plan
212: 
213: ↓
214: 
215: API Contract
216: 
217: ↓
218: 
219: Database Schema
220: 
221: ↓
222: 
223: Master Generation Prompt
224: 
225: ↓
226: 
227: Coding Standards
228: 
229: ↓
230: 
231: Deployment Guide
232: 
233: ↓
234: 
235: UI Screen Specification
236: 
237: ↓
238: 
239: User Flows and State Machines
240: 
241: This order is intentional.
242: 
243: Later documents assume knowledge established by earlier documents.
244: 
245: ---
246: 
247: # Document Responsibilities
248: 
249: ## 00 — Project Index
250: 
251: Defines the project and documentation hierarchy.
252: 
253: ---
254: 
255: ## 01 — Product Requirements
256: 
257: Defines the product vision, user journeys, functional requirements, and success criteria.
258: 
259: ---
260: 
261: ## 02 — Technical Architecture
262: 
263: Defines system architecture, services, providers, repositories, and infrastructure.
264: 
265: ---
266: 
267: ## 03 — Design System
268: 
269: Defines the visual language, mobile simulation, components, animations, spacing, and interaction patterns.
270: 
271: ---
272: 
273: ## 04 — Implementation Plan
274: 
275: Defines implementation phases and build order.
276: 
277: ---
278: 
279: ## 05 — API Contract
280: 
281: Defines every REST endpoint, request, response, WebSocket event, and authentication rule.
282: 
283: ---
284: 
285: ## 06 — Database Schema
286: 
287: Defines the relational database model and persistence layer.
288: 
289: ---
290: 
291: ## 07 — Master Generation Prompt
292: 
293: Defines how an AI coding assistant should think, reason, and generate the repository.
294: 
295: ---
296: 
297: ## 08 — Coding Standards
298: 
299: Defines engineering conventions for backend, frontend, testing, and collaboration.
300: 
301: ---
302: 
303: ## 09 — Deployment Guide
304: 
305: Defines local development, Docker, production deployment, monitoring, backups, and scaling.
306: 
307: ---
308: 
309: ## 10 — UI Screen Specification
310: 
311: Defines every screen, widget, navigation flow,
312: loading state, empty state and API dependency.
313: 
314: ---
315: 
316: ## 11 — User Flows and State Machines
317: 
318: Defines the lifecycle and transitions for
319: authentication, consent, consultation,
320: notifications and AI workflows.
321: 
322: ---
323: 
324: # Source of Truth Priority
325: 
326: If documentation appears to conflict, use the following order of precedence.
327: 
328: 1.
329: 
330: Product Requirements
331: 
332: ↓
333: 
334: 2.
335: 
336: Technical Architecture
337: 
338: ↓
339: 
340: 3.
341: 
342: API Contract
343: 
344: ↓
345: 
346: 4.
347: 
348: Database Schema
349: 
350: ↓
351: 
352: 5.
353: 
354: Design System
355: 
356: ↓
357: 
358: 6.
359: 
360: Implementation Plan
361: 
362: ↓
363: 
364: 7.
365: 
366: Coding Standards
367: 
368: ↓
369: 
370: 8.
371: 
372: Deployment Guide
373: 
374: The Master Generation Prompt should always operate within the constraints of these documents.
375: 
376: It must never override the documented requirements.
377: 
378: ---
379: 
380: # Development Principles
381: 
382: The repository should prioritize:
383: 
384: - Maintainability
385: - Readability
386: - Extensibility
387: - Security
388: - Accessibility
389: - Performance
390: - Testability
391: 
392: Avoid unnecessary complexity.
393: 
394: Build for long-term maintainability rather than rapid prototyping.
395: 
396: ---
397: 
398: # AI Coding Assistant Workflow
399: 
400: When generating the repository, follow this process:
401: 
402: 1. Read every documentation file.
403: 2. Build the repository incrementally according to the Implementation Plan.
404: 3. Ensure each phase compiles before moving to the next.
405: 4. Preserve architectural consistency.
406: 5. Generate tests alongside implementation.
407: 6. Update documentation when implementation changes.
408: 7. Refactor where appropriate before proceeding.
409: 
410: Do not skip phases or generate unrelated features.
411: 
412: ---
413: 
414: # Repository Deliverables
415: 
416: The completed repository should include:
417: 
418: - Backend application
419: - Frontend application
420: - Docker Compose configuration
421: - PostgreSQL integration
422: - Redis integration
423: - JWT authentication
424: - Demo mode authentication
425: - Provider abstractions
426: - Existing symptom checker integration
427: - AI provider interfaces
428: - WebSocket communication
429: - Split-screen demonstration
430: - PhoneFrame mobile simulator
431: - Doctor dashboard
432: - Patient application
433: - Unit tests
434: - Integration tests
435: - Documentation
436: - Database migrations
437: - Seed data
438: 
439: ---
440: 
441: # Success Criteria
442: 
443: The project is considered complete when:
444: 
445: - All Product Requirements have been implemented.
446: - Docker Compose starts the complete system.
447: - Database migrations execute successfully.
448: - Seed data loads correctly.
449: - Demo mode works.
450: - JWT authentication works.
451: - Patient and doctor workflows are complete.
452: - Consent workflow synchronizes in real time.
453: - AI integrations remain provider-agnostic.
454: - All tests pass.
455: - Documentation is complete.
456: - The repository can be cloned and run without undocumented setup.
457: 
458: ---
459: 
460: # Final Objective
461: 
462: Mirage should resemble a production-quality healthcare platform built by an experienced engineering team.
463: 
464: The generated repository should be coherent, maintainable, well-documented, and ready for future expansion beyond the demonstration environment.
465: 
466: # End of Project Index

(End of file - total 466 lines)
</content>
```

**Tool: read**

**Input:**
```json
{
  "filePath": "/Users/sheltonmutambirwa/Desktop/medic/docs/01_Product_Requirements_Document.md"
}
```

**Output:**
```
<path>/Users/sheltonmutambirwa/Desktop/medic/docs/01_Product_Requirements_Document.md</path>
<type>file</type>
<content>
1: # Mirage
2: # Product Requirements Document (PRD)
3: 
4: **Version:** 1.0
5: 
6: **Project Name:** Mirage
7: 
8: **Project Type:**
9: AI-Assisted National Patient Record Platform
10: 
11: **Technology Stack**
12: - Frontend: Next.js
13: - Backend: FastAPI (Python)
14: - Database: PostgreSQL
15: - Cache: Redis
16: - Deployment: Docker Compose
17: - Authentication: JWT + Demo Authentication Mode
18: - AI Layer: Provider Abstraction Interfaces
19: - Real-time Communication: WebSockets
20: 
21: ---
22: 
23: # 1. Executive Summary
24: 
25: Mirage is an AI-assisted digital health platform designed to modernize patient record management by placing ownership and control of medical records in the hands of patients while enabling verified healthcare practitioners to securely request, access, and update those records with explicit patient consent.
26: 
27: Unlike traditional Electronic Health Record (EHR) systems that are fragmented across healthcare providers, Mirage creates a longitudinal patient record that follows the patient instead of remaining locked inside individual institutions.
28: 
29: The system combines:
30: 
31: - National patient records
32: - Practitioner verification
33: - Consent-based access
34: - AI-assisted symptom assessment
35: - AI-assisted clinical documentation
36: - Structured consultation workflows
37: - Real-time patient notifications
38: - Comprehensive audit logging
39: 
40: The Healthathon demonstration focuses on a narrow but complete clinical workflow rather than attempting to build an entire national healthcare system.
41: 
42: The MVP demonstrates how patient-controlled records, artificial intelligence, and secure access controls can improve continuity of care without replacing clinical decision making.
43: 
44: ---
45: 
46: # 2. Problem Statement
47: 
48: Healthcare information in Zimbabwe remains fragmented across hospitals, clinics, and private practices.
49: 
50: Patients frequently carry paper records between facilities.
51: 
52: Medical histories are often incomplete.
53: 
54: Laboratory results may be unavailable during consultations.
55: 
56: Medication histories can be difficult to retrieve.
57: 
58: Previous diagnoses are frequently inaccessible.
59: 
60: When providers cannot access historical information they often:
61: 
62: - repeat laboratory tests
63: - repeat imaging
64: - prescribe medications without complete allergy information
65: - spend consultation time reconstructing medical history
66: - lose continuity of care
67: 
68: These issues contribute to increased healthcare costs, longer waiting times, poorer patient experiences, and greater clinical risk.
69: 
70: Mirage addresses these problems by creating a secure, consent-driven national patient record that follows the patient regardless of where care is delivered.
71: 
72: ---
73: 
74: # 3. Vision
75: 
76: Create a future where every patient owns a lifelong medical record that is instantly accessible—with consent—to any verified healthcare professional, regardless of institution.
77: 
78: The platform should improve:
79: 
80: - patient safety
81: - continuity of care
82: - healthcare efficiency
83: - clinical documentation
84: - public health reporting
85: - patient trust
86: 
87: while ensuring clinicians remain responsible for all final medical decisions.
88: 
89: Artificial Intelligence assists clinicians.
90: 
91: It never replaces them.
92: 
93: ---
94: 
95: # 4. Product Goals
96: 
97: The MVP has six primary goals.
98: 
99: ## Goal 1
100: 
101: Demonstrate patient-controlled medical records.
102: 
103: Patients—not hospitals—control who accesses their health information.
104: 
105: ---
106: 
107: ## Goal 2
108: 
109: Demonstrate secure practitioner verification.
110: 
111: Only registered clinicians may request access to patient records.
112: 
113: ---
114: 
115: ## Goal 3
116: 
117: Demonstrate explicit patient consent.
118: 
119: Every access request requires patient approval unless future emergency access rules are introduced.
120: 
121: ---
122: 
123: ## Goal 4
124: 
125: Demonstrate AI-assisted clinical workflows.
126: 
127: Artificial Intelligence should:
128: 
129: - ask structured questions
130: - summarize conversations
131: - draft consultation notes
132: - generate ranked differential diagnoses
133: 
134: The clinician remains responsible for every diagnosis and every record update.
135: 
136: ---
137: 
138: ## Goal 5
139: 
140: Demonstrate longitudinal health records.
141: 
142: Medical history should appear as one continuous timeline regardless of where treatment occurred.
143: 
144: ---
145: 
146: ## Goal 6
147: 
148: Demonstrate a realistic production-ready architecture.
149: 
150: Although the Healthathon focuses on an MVP, the architecture should be scalable enough to evolve into a national platform without requiring fundamental redesign.
151: 
152: ---
153: 
154: # 5. Non-Goals
155: 
156: The MVP intentionally excludes:
157: 
158: - Appointment scheduling
159: - Billing
160: - Insurance claims
161: - Pharmacy inventory
162: - Laboratory management
163: - Radiology PACS
164: - Hospital administration
165: - Emergency override workflows
166: - National identity management
167: - Offline synchronization
168: - Multi-language support
169: - Wearable integrations
170: 
171: These features may be introduced in future phases.
172: 
173: ---
174: 
175: # 6. Product Philosophy
176: 
177: The system should embody five principles.
178: 
179: ## 6.1 Patient Ownership
180: 
181: Patients own their records.
182: 
183: Healthcare providers become trusted contributors rather than record owners.
184: 
185: ---
186: 
187: ## 6.2 Consent First
188: 
189: Every access request should be transparent.
190: 
191: Patients always know:
192: 
193: - who requested access
194: - why
195: - when
196: - from which facility
197: 
198: ---
199: 
200: ## 6.3 AI Assists
201: 
202: Artificial Intelligence never writes directly into permanent records.
203: 
204: Every AI-generated output requires clinician review.
205: 
206: Nothing reaches the medical record without practitioner approval.
207: 
208: ---
209: 
210: ## 6.4 Modular Architecture
211: 
212: Every major subsystem must be replaceable.
213: 
214: Examples include:
215: 
216: - authentication provider
217: - symptom checker
218: - transcription engine
219: - diagnosis engine
220: - summarization engine
221: - notification provider
222: 
223: The application should depend on interfaces rather than implementations.
224: 
225: ---
226: 
227: ## 6.5 Transparency
228: 
229: Every action should be logged.
230: 
231: Patients should always be able to review:
232: 
233: - who viewed their records
234: - who requested access
235: - when records changed
236: - which clinician approved updates
237: 
238: ---
239: 
240: # 7. Target Users
241: 
242: The MVP supports four user types.
243: 
244: ## Patient
245: 
246: Primary owner of medical information.
247: 
248: Responsibilities include:
249: 
250: - reviewing records
251: - approving access requests
252: - completing AI symptom assessments
253: - reviewing access history
254: - managing profile information
255: 
256: ---
257: 
258: ## Doctor
259: 
260: Licensed medical practitioner.
261: 
262: Responsibilities include:
263: 
264: - searching for patients
265: - requesting record access
266: - reviewing records
267: - conducting consultations
268: - interacting with AI assistance
269: - approving documentation
270: - updating patient records
271: 
272: ---
273: 
274: ## System Administrator
275: 
276: Administrative role used only for development and testing.
277: 
278: Can:
279: 
280: - manage facilities
281: - manage practitioner registry
282: - monitor system health
283: 
284: This role is not part of the demonstration flow.
285: 
286: ---
287: 
288: ## AI Providers
289: 
290: The AI layer is treated as an external service.
291: 
292: Providers are interchangeable.
293: 
294: Examples include:
295: 
296: - Existing Symptom Checker
297: - OpenAI
298: - Azure OpenAI
299: - Ollama
300: - Anthropic
301: - Future custom models
302: 
303: The backend communicates with provider interfaces only.
304: 
305: ---
306: 
307: # 8. User Stories
308: 
309: ## Patient
310: 
311: As a patient,
312: 
313: I want to approve requests for my records,
314: 
315: so that I remain in control of my health information.
316: 
317: ---
318: 
319: As a patient,
320: 
321: I want my complete history available regardless of hospital,
322: 
323: so I never have to remember every diagnosis myself.
324: 
325: ---
326: 
327: As a patient,
328: 
329: I want allergies displayed prominently,
330: 
331: so clinicians immediately see critical safety information.
332: 
333: ---
334: 
335: As a patient,
336: 
337: I want to complete an AI symptom assessment before my visit,
338: 
339: so my consultation begins with relevant clinical context.
340: 
341: ---
342: 
343: ## Doctor
344: 
345: As a doctor,
346: 
347: I want to search for patients quickly,
348: 
349: so consultations begin without unnecessary delay.
350: 
351: ---
352: 
353: As a doctor,
354: 
355: I want immediate access after consent,
356: 
357: so I don't waste consultation time.
358: 
359: ---
360: 
361: As a doctor,
362: 
363: I want AI assistance during consultations,
364: 
365: so documentation takes less time.
366: 
367: ---
368: 
369: As a doctor,
370: 
371: I want to review every AI suggestion before saving,
372: 
373: so I remain responsible for clinical decisions.
374: 
375: ---
376: 
377: # 9. Success Metrics
378: 
379: The MVP will be considered successful if judges can complete the following demonstration without assistance:
380: 
381: ✓ Doctor logs in.
382: 
383: ✓ Doctor searches patient.
384: 
385: ✓ Patient found.
386: 
387: ✓ Doctor requests access.
388: 
389: ✓ Patient immediately receives request.
390: 
391: ✓ Patient approves.
392: 
393: ✓ Doctor gains access.
394: 
395: ✓ Doctor reviews patient history.
396: 
397: ✓ AI assists consultation.
398: 
399: ✓ AI produces structured differential diagnosis.
400: 
401: ✓ Doctor confirms diagnosis.
402: 
403: ✓ Consultation note generated.
404: 
405: ✓ Doctor approves note.
406: 
407: ✓ Record updated.
408: 
409: ✓ Patient immediately sees updated record.
410: 
411: This complete workflow should require less than five minutes during demonstration.
412: 
413: ---
414: 
415: # 10. Design Principles
416: 
417: The system should feel:
418: 
419: - modern
420: - trustworthy
421: - lightweight
422: - responsive
423: - clinically safe
424: - patient-centered
425: 
426: The patient experience should resemble a premium mobile application.
427: 
428: The clinician experience should resemble a professional clinical dashboard optimized for speed and clarity.
429: 
430: Both interfaces should feel like two views into the same real-time healthcare platform rather than separate applications.
431: 
432: ---
433: 
434: # 11. High-Level Functional Scope
435: 
436: The MVP consists of two applications sharing one backend.
437: 
438: ## Patient Application
439: 
440: Built in Next.js but rendered inside a simulated mobile device frame.
441: 
442: Features:
443: 
444: - Login
445: - Home Dashboard
446: - Medical Record
447: - AI Symptom Check
448: - Consent Requests
449: - Notifications
450: - Access Log
451: - Health Timeline
452: - Medical ID
453: - Profile
454: 
455: ---
456: 
457: ## Doctor Portal
458: 
459: Desktop-oriented responsive web application.
460: 
461: Features:
462: 
463: - Login
464: - Dashboard
465: - Patient Search
466: - Consent Requests
467: - Patient Record
468: - AI Consultation
469: - Diagnosis Review
470: - Clinical Notes
471: - Record Update
472: - Access History
473: 
474: # 12. Functional Requirements
475: 
476: The following functional requirements define the complete MVP that will be implemented for the Healthathon demonstration.
477: 
478: ---
479: 
480: # FR-1 Authentication
481: 
482: ## Objectives
483: 
484: Provide both rapid demonstration access and production-ready authentication.
485: 
486: ### Functional Requirements
487: 
488: The system shall support two authentication modes.
489: 
490: ### Demo Mode
491: 
492: Designed for rapid demonstrations and development.
493: 
494: Users can enter the application with one click.
495: 
496: Available demo accounts include:
497: 
498: - Demo Patient
499: - Demo Doctor
500: - Demo Administrator
501: 
502: No passwords are required.
503: 
504: No JWT validation occurs.
505: 
506: Demo Mode is enabled through configuration.
507: 
508: ```env
509: DEMO_MODE=true
510: ```
511: 
512: ---
513: 
514: ### Production Mode
515: 
516: Production mode enables:
517: 
518: - JWT Authentication
519: - Refresh Tokens
520: - Password Hashing
521: - Secure Sessions
522: - Role-Based Authorization
523: 
524: Users authenticate using email and password.
525: 
526: JWT expiration should be configurable.
527: 
528: Refresh tokens should be securely stored.
529: 
530: Authentication providers must remain replaceable.
531: 
532: ---
533: 
534: # FR-2 Patient Management
535: 
536: The system shall maintain a longitudinal patient profile.
537: 
538: Each patient contains:
539: 
540: - Unique Medical Record Number
541: - National ID
542: - Name
543: - Date of Birth
544: - Gender
545: - Blood Group
546: - Emergency Contact
547: - Contact Details
548: - Allergies
549: - Chronic Conditions
550: - Medical Timeline
551: - Previous Consultations
552: - Current Medications
553: 
554: Patients cannot directly modify clinical records.
555: 
556: Patients may update:
557: 
558: - phone number
559: - address
560: - emergency contacts
561: 
562: ---
563: 
564: # FR-3 Practitioner Registry
565: 
566: The system shall maintain a verified practitioner registry.
567: 
568: Each practitioner contains:
569: 
570: - Name
571: - Registration Number
572: - Facility
573: - Role
574: - Speciality
575: - Verification Status
576: 
577: Only verified practitioners may request patient records.
578: 
579: Inactive practitioners cannot log in.
580: 
581: ---
582: 
583: # FR-4 Consent Management
584: 
585: Consent is the foundation of Mirage.
586: 
587: No patient records are released without patient approval.
588: 
589: Exception handling for emergency override is intentionally excluded from the MVP.
590: 
591: Each consent request includes:
592: 
593: Requester
594: 
595: Facility
596: 
597: Registration Number
598: 
599: Reason
600: 
601: Scope
602: 
603: Expiry Time
604: 
605: Timestamp
606: 
607: Status
608: 
609: Possible statuses:
610: 
611: Pending
612: 
613: Approved
614: 
615: Denied
616: 
617: Expired
618: 
619: Cancelled
620: 
621: ---
622: 
623: Patient approval immediately unlocks records.
624: 
625: Patient denial immediately closes the request.
626: 
627: Expired requests automatically revoke access.
628: 
629: ---
630: 
631: # FR-5 Access Control
632: 
633: Access permissions are temporary.
634: 
635: Doctors do not permanently gain access.
636: 
637: Permission expires after the consultation.
638: 
639: Every permission must include:
640: 
641: Patient
642: 
643: Doctor
644: 
645: Facility
646: 
647: Time Granted
648: 
649: Expiry
650: 
651: Reason
652: 
653: Approval Source
654: 
655: ---
656: 
657: # FR-6 Medical Record Management
658: 
659: Medical records form one continuous timeline.
660: 
661: Each visit contains:
662: 
663: Visit Date
664: 
665: Facility
666: 
667: Doctor
668: 
669: Diagnosis
670: 
671: Symptoms
672: 
673: Vitals
674: 
675: Prescriptions
676: 
677: Notes
678: 
679: Investigations
680: 
681: Attachments
682: 
683: AI Summary
684: 
685: Every update generates an immutable audit log.
686: 
687: No records are deleted.
688: 
689: Corrections generate new versions.
690: 
691: ---
692: 
693: # FR-7 Allergy Management
694: 
695: Allergy information is treated as critical safety information.
696: 
697: Allergy warnings appear:
698: 
699: Patient Home
700: 
701: Patient Record
702: 
703: Doctor Record
704: 
705: AI Diagnosis
706: 
707: Clinical Notes
708: 
709: Prescription Screen
710: 
711: Critical allergies must never scroll off-screen.
712: 
713: Pinned warnings remain visible.
714: 
715: ---
716: 
717: # FR-8 Patient Timeline
718: 
719: The patient timeline presents the complete health history chronologically.
720: 
721: Timeline entries include:
722: 
723: Admissions
724: 
725: Outpatient Visits
726: 
727: Diagnoses
728: 
729: Vaccinations
730: 
731: Lab Results
732: 
733: Procedures
734: 
735: Medications
736: 
737: Notes
738: 
739: AI Assessments
740: 
741: Each entry opens detailed information.
742: 
743: Timeline is read-only for patients.
744: 
745: ---
746: 
747: # FR-9 AI Symptom Assessment
748: 
749: The AI Symptom Assessment exists as an independent provider.
750: 
751: The application never depends on a specific implementation.
752: 
753: Instead it communicates through:
754: 
755: SymptomAssessmentProvider
756: 
757: Responsibilities:
758: 
759: Start Session
760: 
761: Load Patient Context
762: 
763: Submit Patient Response
764: 
765: Receive Next Question
766: 
767: End Assessment
768: 
769: Store Conversation
770: 
771: The provider implementation may change without affecting application code.
772: 
773: Examples:
774: 
775: Current QA System
776: 
777: OpenAI
778: 
779: Azure
780: 
781: Anthropic
782: 
783: Local LLM
784: 
785: ---
786: 
787: The AI receives:
788: 
789: Known allergies
790: 
791: Previous diagnoses
792: 
793: Age
794: 
795: Gender
796: 
797: Medical history
798: 
799: Current medications
800: 
801: The provider returns:
802: 
803: Question
804: 
805: Clinical reasoning metadata
806: 
807: Conversation state
808: 
809: Completion status
810: 
811: ---
812: 
813: # FR-10 AI Diagnostic Assistant
814: 
815: The doctor portal includes AI assistance.
816: 
817: Responsibilities include:
818: 
819: Generate differential diagnosis
820: 
821: Suggest additional questions
822: 
823: Recommend investigations
824: 
825: Highlight risks
826: 
827: Reference previous history
828: 
829: Display confidence estimates
830: 
831: AI outputs are suggestions only.
832: 
833: Doctors remain responsible for:
834: 
835: Diagnosis
836: 
837: Treatment
838: 
839: Documentation
840: 
841: Approval
842: 
843: ---
844: 
845: # FR-11 AI Clinical Summary
846: 
847: The consultation summary provider creates structured documentation.
848: 
849: Input:
850: 
851: Conversation
852: 
853: Patient history
854: 
855: Symptoms
856: 
857: Doctor observations
858: 
859: Output:
860: 
861: Chief Complaint
862: 
863: History of Present Illness
864: 
865: Clinical Findings
866: 
867: Assessment
868: 
869: Plan
870: 
871: Recommendations
872: 
873: Doctors may edit every field.
874: 
875: Nothing is automatically committed.
876: 
877: ---
878: 
879: # FR-12 AI Transcription
880: 
881: Consultations may optionally be transcribed.
882: 
883: The transcription provider remains abstract.
884: 
885: Possible providers include:
886: 
887: Whisper
888: 
889: Azure Speech
890: 
891: Deepgram
892: 
893: AssemblyAI
894: 
895: Future Provider
896: 
897: The backend communicates only through:
898: 
899: TranscriptionProvider
900: 
901: ---
902: 
903: # FR-13 Notifications
904: 
905: Notifications appear in real time.
906: 
907: Patient notifications include:
908: 
909: Consent Requests
910: 
911: Record Updated
912: 
913: Access Granted
914: 
915: Access Expired
916: 
917: Doctor notifications include:
918: 
919: Consent Approved
920: 
921: Consent Denied
922: 
923: Patient Updated
924: 
925: AI Complete
926: 
927: Notifications should use WebSockets.
928: 
929: Fallback polling should exist.
930: 
931: ---
932: 
933: # FR-14 Search
934: 
935: Doctors can search patients using:
936: 
937: Medical Record Number
938: 
939: National ID
940: 
941: Full Name
942: 
943: Partial Name
944: 
945: Search should tolerate spelling errors.
946: 
947: Results appear instantly.
948: 
949: ---
950: 
951: # FR-15 Audit Logging
952: 
953: Every important action generates an audit entry.
954: 
955: Examples include:
956: 
957: Login
958: 
959: Logout
960: 
961: Consent Requested
962: 
963: Consent Approved
964: 
965: Consent Denied
966: 
967: Record Viewed
968: 
969: Record Updated
970: 
971: AI Started
972: 
973: AI Completed
974: 
975: Diagnosis Confirmed
976: 
977: Audit logs are immutable.
978: 
979: ---
980: 
981: # 13. Patient Journey
982: 
983: The patient application is designed as a simulated mobile application running inside the browser.
984: 
985: The experience should feel indistinguishable from a native application.
986: 
987: ---
988: 
989: ## Step 1
990: 
991: Patient launches Mirage.
992: 
993: If Demo Mode is enabled,
994: 
995: the patient can enter immediately.
996: 
997: Otherwise authentication occurs.
998: 
999: ---
1000: 
1001: ## Step 2
1002: 
1003: Patient lands on Home Dashboard.
1004: 
1005: Dashboard contains:
1006: 
1007: Greeting
1008: 
1009: Profile Summary
1010: 
1011: Medical Record Summary
1012: 
1013: Upcoming Notifications
1014: 
1015: Quick Actions
1016: 
1017: Recent Visit
1018: 
1019: Critical Allergy Banner
1020: 
1021: Medical ID Shortcut
1022: 
1023: ---
1024: 
1025: ## Step 3
1026: 
1027: Patient views complete medical history.
1028: 
1029: History is presented chronologically.
1030: 
1031: Each visit expands.
1032: 
1033: Patient may view:
1034: 
1035: Diagnosis
1036: 
1037: Facility
1038: 
1039: Doctor
1040: 
1041: Prescriptions
1042: 
1043: Notes
1044: 
1045: Attachments
1046: 
1047: ---
1048: 
1049: ## Step 4
1050: 
1051: Patient receives doctor access request.
1052: 
1053: A notification appears instantly.
1054: 
1055: The request clearly displays:
1056: 
1057: Doctor
1058: 
1059: Facility
1060: 
1061: Registration Number
1062: 
1063: Purpose
1064: 
1065: Requested Scope
1066: 
1067: Expiration
1068: 
1069: Patient selects:
1070: 
1071: Approve
1072: 
1073: or
1074: 
1075: Deny
1076: 
1077: ---
1078: 
1079: ## Step 5
1080: 
1081: Doctor immediately receives response.
1082: 
1083: If approved,
1084: 
1085: the patient sees:
1086: 
1087: Access Active
1088: 
1089: Doctor Name
1090: 
1091: Expiration Time
1092: 
1093: ---
1094: 
1095: ## Step 6
1096: 
1097: Patient completes AI symptom assessment.
1098: 
1099: The conversation resembles a modern messaging application.
1100: 
1101: The AI should:
1102: 
1103: Reference previous history
1104: 
1105: Avoid asking redundant questions
1106: 
1107: Remember previous answers
1108: 
1109: Guide the conversation naturally
1110: 
1111: ---
1112: 
1113: ## Step 7
1114: 
1115: Assessment completes.
1116: 
1117: Patient receives confirmation.
1118: 
1119: Conversation becomes available to the doctor.
1120: 
1121: ---
1122: 
1123: ## Step 8
1124: 
1125: Following consultation,
1126: 
1127: the patient immediately sees:
1128: 
1129: Updated diagnosis
1130: 
1131: New consultation
1132: 
1133: Updated medications
1134: 
1135: New notes
1136: 
1137: Latest recommendations
1138: 
1139: Recent activity
1140: 
1141: The updated visit appears at the top of the timeline.
1142: 
1143: ---
1144: 
1145: # 14. Patient Screens
1146: 
1147: The MVP includes the following screens.
1148: 
1149: Authentication
1150: 
1151: Home Dashboard
1152: 
1153: Medical Timeline
1154: 
1155: Visit Details
1156: 
1157: Consent Request
1158: 
1159: Consent History
1160: 
1161: Notifications
1162: 
1163: AI Symptom Assessment
1164: 
1165: Medical ID
1166: 
1167: Profile
1168: 
1169: Settings
1170: 
1171: Access Log
1172: 
1173: Emergency Information
1174: 
1175: About Mirage
1176: 
1177: Each screen must support:
1178: 
1179: Loading State
1180: 
1181: Empty State
1182: 
1183: Error State
1184: 
1185: Offline Placeholder
1186: 
1187: Animated Transitions
1188: 
1189: Responsive Layout
1190: 
1191: Accessibility
1192: 
1193: # 15. Doctor Journey
1194: 
1195: The Doctor Portal is designed to provide healthcare practitioners with a fast, intuitive, and clinically safe workflow. Unlike the patient application, which prioritizes transparency and patient ownership, the doctor portal prioritizes efficiency, clarity, and rapid decision support while ensuring that every clinical action remains under physician control.
1196: 
1197: The complete demonstration should resemble a realistic consultation from beginning to end.
1198: 
1199: ---
1200: 
1201: ## Step 1 — Doctor Authentication
1202: 
1203: The doctor accesses the Mirage Doctor Portal.
1204: 
1205: If Demo Mode is enabled:
1206: 
1207: - One-click login as Demo Doctor.
1208: 
1209: If Production Mode is enabled:
1210: 
1211: - Email
1212: - Password
1213: - JWT Authentication
1214: - Role Validation
1215: 
1216: Successful authentication loads:
1217: 
1218: - Today's Dashboard
1219: - Patient Queue
1220: - Recent Activity
1221: - Notifications
1222: 
1223: ---
1224: 
1225: ## Step 2 — Dashboard
1226: 
1227: The Doctor Dashboard acts as the landing page.
1228: 
1229: Displayed information includes:
1230: 
1231: ### Today's Queue
1232: 
1233: Patients currently waiting.
1234: 
1235: Each card displays:
1236: 
1237: - Patient Name
1238: - Appointment Time
1239: - Consultation Status
1240: 
1241: ---
1242: 
1243: ### Recent Patients
1244: 
1245: Recently accessed patients.
1246: 
1247: Allows clinicians to resume interrupted consultations.
1248: 
1249: ---
1250: 
1251: ### Pending Consent Requests
1252: 
1253: Displays requests awaiting patient approval.
1254: 
1255: Status examples:
1256: 
1257: Pending
1258: 
1259: Approved
1260: 
1261: Denied
1262: 
1263: Expired
1264: 
1265: ---
1266: 
1267: ### Notifications
1268: 
1269: Examples:
1270: 
1271: Patient approved request
1272: 
1273: AI assessment completed
1274: 
1275: Record updated
1276: 
1277: System announcements
1278: 
1279: ---
1280: 
1281: ### Quick Actions
1282: 
1283: Search Patient
1284: 
1285: New Consultation
1286: 
1287: Review AI Sessions
1288: 
1289: View Recent Records
1290: 
1291: ---
1292: 
1293: ## Step 3 — Search Patient
1294: 
1295: The clinician searches using:
1296: 
1297: Medical Record Number
1298: 
1299: National ID
1300: 
1301: Full Name
1302: 
1303: Partial Name
1304: 
1305: Autocomplete should begin after two characters.
1306: 
1307: Search results display:
1308: 
1309: Patient Name
1310: 
1311: Date of Birth
1312: 
1313: Medical Record Number
1314: 
1315: Blood Group
1316: 
1317: Verification Status
1318: 
1319: Current Consent Status
1320: 
1321: The clinician can immediately determine whether:
1322: 
1323: Patient exists
1324: 
1325: Consent exists
1326: 
1327: Access is active
1328: 
1329: ---
1330: 
1331: ## Step 4 — Request Record Access
1332: 
1333: If access is unavailable:
1334: 
1335: Doctor presses
1336: 
1337: Request Record Access
1338: 
1339: Immediately:
1340: 
1341: Backend validates practitioner.
1342: 
1343: Consent request created.
1344: 
1345: Notification pushed to patient.
1346: 
1347: Doctor sees:
1348: 
1349: Waiting for patient approval...
1350: 
1351: The interface remains responsive.
1352: 
1353: No manual refresh required.
1354: 
1355: ---
1356: 
1357: ## Step 5 — Patient Approval
1358: 
1359: Once approval occurs:
1360: 
1361: Dashboard updates instantly.
1362: 
1363: Patient record unlocks.
1364: 
1365: Visual confirmation displayed.
1366: 
1367: Doctor proceeds directly into consultation.
1368: 
1369: ---
1370: 
1371: ## Step 6 — Review Patient Record
1372: 
1373: The clinician first sees a concise summary.
1374: 
1375: Pinned information:
1376: 
1377: Critical Allergies
1378: 
1379: Active Conditions
1380: 
1381: Current Medication
1382: 
1383: Recent Visits
1384: 
1385: Previous Diagnoses
1386: 
1387: Medical Timeline
1388: 
1389: Nothing important should require scrolling before consultation begins.
1390: 
1391: ---
1392: 
1393: ## Step 7 — Begin AI Consultation
1394: 
1395: The clinician launches the AI assistant.
1396: 
1397: The assistant already knows:
1398: 
1399: Patient demographics
1400: 
1401: Medical history
1402: 
1403: Known allergies
1404: 
1405: Current medications
1406: 
1407: Past diagnoses
1408: 
1409: Recent symptom assessment
1410: 
1411: The doctor does not manually load context.
1412: 
1413: ---
1414: 
1415: ## Step 8 — AI Conversation
1416: 
1417: The AI guides the consultation.
1418: 
1419: The clinician remains in control.
1420: 
1421: The AI may:
1422: 
1423: Ask targeted questions.
1424: 
1425: Highlight missing information.
1426: 
1427: Reference previous illnesses.
1428: 
1429: Suggest investigations.
1430: 
1431: Raise safety alerts.
1432: 
1433: The doctor may:
1434: 
1435: Accept
1436: 
1437: Ignore
1438: 
1439: Skip
1440: 
1441: Modify
1442: 
1443: Any recommendation.
1444: 
1445: ---
1446: 
1447: ## Step 9 — Differential Diagnosis
1448: 
1449: Following sufficient questioning,
1450: 
1451: the AI generates:
1452: 
1453: Ranked differential diagnoses.
1454: 
1455: Each includes:
1456: 
1457: Probability
1458: 
1459: Reasoning Summary
1460: 
1461: Supporting Evidence
1462: 
1463: Contradictory Evidence
1464: 
1465: Suggested Investigations
1466: 
1467: Potential Risks
1468: 
1469: Medication Warnings
1470: 
1471: Doctors may expand each diagnosis.
1472: 
1473: No diagnosis is automatically accepted.
1474: 
1475: ---
1476: 
1477: ## Step 10 — Clinical Documentation
1478: 
1479: The AI generates a structured consultation note.
1480: 
1481: Sections include:
1482: 
1483: Chief Complaint
1484: 
1485: History of Present Illness
1486: 
1487: Review of Systems
1488: 
1489: Assessment
1490: 
1491: Differential
1492: 
1493: Plan
1494: 
1495: Prescriptions
1496: 
1497: Follow-up
1498: 
1499: Doctors may edit any field.
1500: 
1501: ---
1502: 
1503: ## Step 11 — Record Confirmation
1504: 
1505: Nothing is written until confirmation.
1506: 
1507: Confirmation screen displays:
1508: 
1509: Original Patient Record
1510: 
1511: Proposed Changes
1512: 
1513: Diagnosis
1514: 
1515: Medications
1516: 
1517: Clinical Notes
1518: 
1519: AI Summary
1520: 
1521: Doctor presses:
1522: 
1523: Confirm & Update Record
1524: 
1525: Backend:
1526: 
1527: Creates new record version.
1528: 
1529: Updates patient timeline.
1530: 
1531: Creates audit log.
1532: 
1533: Notifies patient.
1534: 
1535: ---
1536: 
1537: ## Step 12 — Consultation Complete
1538: 
1539: Doctor returns to dashboard.
1540: 
1541: Patient immediately receives:
1542: 
1543: Updated timeline
1544: 
1545: New consultation
1546: 
1547: Medication
1548: 
1549: Recommendations
1550: 
1551: Notification
1552: 
1553: ---
1554: 
1555: # 16. Doctor Portal Screens
1556: 
1557: The Doctor Portal includes the following pages.
1558: 
1559: ---
1560: 
1561: ## Authentication
1562: 
1563: Purpose:
1564: 
1565: Authenticate practitioners.
1566: 
1567: Functions:
1568: 
1569: Login
1570: 
1571: Forgot Password (future)
1572: 
1573: Demo Login
1574: 
1575: Session Management
1576: 
1577: ---
1578: 
1579: ## Dashboard
1580: 
1581: Purpose:
1582: 
1583: Daily overview.
1584: 
1585: Widgets:
1586: 
1587: Today's Queue
1588: 
1589: Recent Patients
1590: 
1591: Notifications
1592: 
1593: Pending Requests
1594: 
1595: Quick Actions
1596: 
1597: System Status
1598: 
1599: ---
1600: 
1601: ## Patient Search
1602: 
1603: Purpose:
1604: 
1605: Locate patient records.
1606: 
1607: Capabilities:
1608: 
1609: Search
1610: 
1611: Filters
1612: 
1613: Sorting
1614: 
1615: Recent Searches
1616: 
1617: Suggestions
1618: 
1619: ---
1620: 
1621: ## Consent Waiting Screen
1622: 
1623: Purpose:
1624: 
1625: Display pending approval.
1626: 
1627: Shows:
1628: 
1629: Patient Name
1630: 
1631: Elapsed Time
1632: 
1633: Status
1634: 
1635: Cancel Request
1636: 
1637: Retry Notification
1638: 
1639: ---
1640: 
1641: ## Patient Overview
1642: 
1643: Purpose:
1644: 
1645: Clinical summary before consultation.
1646: 
1647: Sections:
1648: 
1649: Demographics
1650: 
1651: Allergies
1652: 
1653: Conditions
1654: 
1655: Medication
1656: 
1657: Timeline
1658: 
1659: Recent Notes
1660: 
1661: ---
1662: 
1663: ## Medical Timeline
1664: 
1665: Purpose:
1666: 
1667: Chronological history.
1668: 
1669: Each entry expands.
1670: 
1671: Supports:
1672: 
1673: Diagnosis
1674: 
1675: Medication
1676: 
1677: Attachments
1678: 
1679: Notes
1680: 
1681: Lab Results
1682: 
1683: ---
1684: 
1685: ## Visit Details
1686: 
1687: Purpose:
1688: 
1689: Review historical encounters.
1690: 
1691: Contains:
1692: 
1693: Facility
1694: 
1695: Doctor
1696: 
1697: Diagnosis
1698: 
1699: Investigations
1700: 
1701: Treatment
1702: 
1703: Prescriptions
1704: 
1705: Notes
1706: 
1707: ---
1708: 
1709: ## AI Consultation
1710: 
1711: Purpose:
1712: 
1713: Interactive consultation.
1714: 
1715: Contains:
1716: 
1717: Conversation
1718: 
1719: Suggested Questions
1720: 
1721: Clinical Context
1722: 
1723: Current Assessment
1724: 
1725: History Panel
1726: 
1727: ---
1728: 
1729: ## Differential Review
1730: 
1731: Purpose:
1732: 
1733: Present AI recommendations.
1734: 
1735: Displays:
1736: 
1737: Diagnosis Ranking
1738: 
1739: Confidence
1740: 
1741: Evidence
1742: 
1743: Risks
1744: 
1745: Next Steps
1746: 
1747: Clinician Notes
1748: 
1749: ---
1750: 
1751: ## Documentation Review
1752: 
1753: Purpose:
1754: 
1755: Approve generated documentation.
1756: 
1757: Editable fields:
1758: 
1759: SOAP Note
1760: 
1761: Assessment
1762: 
1763: Plan
1764: 
1765: Diagnosis
1766: 
1767: Medication
1768: 
1769: Instructions
1770: 
1771: ---
1772: 
1773: ## Confirmation
1774: 
1775: Purpose:
1776: 
1777: Final review.
1778: 
1779: Actions:
1780: 
1781: Confirm
1782: 
1783: Cancel
1784: 
1785: Return to Edit
1786: 
1787: ---
1788: 
1789: ## Access History
1790: 
1791: Purpose:
1792: 
1793: Review previous patient access.
1794: 
1795: Shows:
1796: 
1797: Patient
1798: 
1799: Facility
1800: 
1801: Time
1802: 
1803: Purpose
1804: 
1805: Duration
1806: 
1807: Outcome
1808: 
1809: ---
1810: 
1811: ## Notifications
1812: 
1813: Purpose:
1814: 
1815: Review alerts.
1816: 
1817: Categories:
1818: 
1819: Consent
1820: 
1821: Patient Updates
1822: 
1823: AI Events
1824: 
1825: System
1826: 
1827: ---
1828: 
1829: ## Settings
1830: 
1831: Purpose:
1832: 
1833: Personal preferences.
1834: 
1835: Contains:
1836: 
1837: Profile
1838: 
1839: Notification Preferences
1840: 
1841: Theme
1842: 
1843: Accessibility
1844: 
1845: Security
1846: 
1847: ---
1848: 
1849: # 17. Real-Time Consent Workflow
1850: 
1851: Mirage demonstrates patient-controlled healthcare through a real-time consent workflow.
1852: 
1853: This interaction is the centrepiece of the demonstration.
1854: 
1855: ---
1856: 
1857: Doctor searches patient.
1858: 
1859: ↓
1860: 
1861: Patient located.
1862: 
1863: ↓
1864: 
1865: Doctor requests access.
1866: 
1867: ↓
1868: 
1869: Backend validates practitioner.
1870: 
1871: ↓
1872: 
1873: Consent request created.
1874: 
1875: ↓
1876: 
1877: WebSocket event emitted.
1878: 
1879: ↓
1880: 
1881: Patient immediately receives notification.
1882: 
1883: ↓
1884: 
1885: Patient reviews request.
1886: 
1887: ↓
1888: 
1889: Approve or Deny.
1890: 
1891: ↓
1892: 
1893: Backend records decision.
1894: 
1895: ↓
1896: 
1897: Access token generated.
1898: 
1899: ↓
1900: 
1901: Doctor interface unlocks instantly.
1902: 
1903: ↓
1904: 
1905: Consultation begins.
1906: 
1907: ↓
1908: 
1909: Consultation ends.
1910: 
1911: ↓
1912: 
1913: Access expires automatically.
1914: 
1915: ↓
1916: 
1917: Audit log written.
1918: 
1919: ↓
1920: 
1921: Patient Access History updated.
1922: 
1923: ---
1924: 
1925: # 18. AI Workflow
1926: 
1927: Artificial Intelligence exists as a supporting clinical tool.
1928: 
1929: It never makes autonomous clinical decisions.
1930: 
1931: The workflow is:
1932: 
1933: Patient completes symptom assessment.
1934: 
1935: ↓
1936: 
1937: Assessment stored.
1938: 
1939: ↓
1940: 
1941: Doctor requests consultation.
1942: 
1943: ↓
1944: 
1945: Patient context loaded.
1946: 
1947: ↓
1948: 
1949: AI receives:
1950: 
1951: History
1952: 
1953: Medications
1954: 
1955: Allergies
1956: 
1957: Previous diagnoses
1958: 
1959: Symptoms
1960: 
1961: ↓
1962: 
1963: AI asks structured questions.
1964: 
1965: ↓
1966: 
1967: Doctor enters responses.
1968: 
1969: ↓
1970: 
1971: AI produces:
1972: 
1973: Differential diagnosis
1974: 
1975: Clinical summary
1976: 
1977: Suggested investigations
1978: 
1979: Suggested documentation
1980: 
1981: ↓
1982: 
1983: Doctor reviews.
1984: 
1985: ↓
1986: 
1987: Doctor edits.
1988: 
1989: ↓
1990: 
1991: Doctor approves.
1992: 
1993: ↓
1994: 
1995: Backend updates medical record.
1996: 
1997: ---
1998: 
1999: # AI Provider Architecture
2000: 

(Showing lines 1-2000 of 2540. Use offset=2001 to continue.)
</content>
```

**Tool: read**

**Input:**
```json
{
  "filePath": "/Users/sheltonmutambirwa/Desktop/medic/docs/02_Technical_Architecture.md"
}
```

**Output:**
```
<path>/Users/sheltonmutambirwa/Desktop/medic/docs/02_Technical_Architecture.md</path>
<type>file</type>
<content>
1: # Mirage
2: # Technical Architecture Specification
3: 
4: Version: 1.0
5: 
6: ---
7: 
8: # 1. Architecture Philosophy
9: 
10: Mirage is designed as a modular healthcare platform rather than a monolithic web application.
11: 
12: Every subsystem should be independently replaceable.
13: 
14: Business logic must never depend directly on infrastructure implementations.
15: 
16: Instead, every external dependency is accessed through interfaces.
17: 
18: Examples include:
19: 
20: - Authentication
21: - AI Providers
22: - Notifications
23: - Storage
24: - Email
25: - Speech-to-Text
26: - Clinical Summarization
27: 
28: This allows Mirage to evolve from a Healthathon MVP into a production healthcare platform without requiring large architectural rewrites.
29: 
30: ---
31: 
32: # 2. High-Level Architecture
33: 
34: Mirage consists of five major layers.
35: 
36: ┌──────────────────────────────────────┐
37: │           Next.js Frontend           │
38: │                                      │
39: │  Patient App     Doctor Portal       │
40: └──────────────────────────────────────┘
41:                  │
42:                  │ REST + WebSockets
43:                  ▼
44: ┌──────────────────────────────────────┐
45: │           FastAPI Backend            │
46: │                                      │
47: │ Authentication                       │
48: │ API                                  │
49: │ Services                             │
50: │ Domain Logic                         │
51: │ AI Interfaces                        │
52: └──────────────────────────────────────┘
53:                  │
54:         ┌────────┴────────┐
55:         ▼                 ▼
56:  PostgreSQL           Redis
57:  Database          Cache / Events
58:         │
59:         ▼
60:  AI Provider Interfaces
61: 
62: - Symptom Checker
63: - Diagnosis
64: - Summary
65: - Transcription
66: - Notifications
67: 
68: ---
69: 
70: # 3. Design Principles
71: 
72: The architecture follows several principles.
73: 
74: ## Separation of Concerns
75: 
76: Presentation
77: 
78: ↓
79: 
80: Application
81: 
82: ↓
83: 
84: Domain
85: 
86: ↓
87: 
88: Infrastructure
89: 
90: No UI code should contain business logic.
91: 
92: ---
93: 
94: ## Dependency Inversion
95: 
96: High-level services depend only on interfaces.
97: 
98: Never concrete implementations.
99: 
100: For example:
101: 
102: PatientService
103: 
104: depends on
105: 
106: PatientRepository
107: 
108: not
109: 
110: SQLAlchemyPatientRepository
111: 
112: ---
113: 
114: ## Single Responsibility
115: 
116: Each module performs one responsibility.
117: 
118: Authentication should never contain patient logic.
119: 
120: Patient services should never perform notification delivery.
121: 
122: ---
123: 
124: ## Event Driven
125: 
126: Important system events should be emitted rather than tightly coupling services.
127: 
128: Examples:
129: 
130: ConsentApproved
131: 
132: ↓
133: 
134: Notification Service
135: 
136: ↓
137: 
138: Audit Service
139: 
140: ↓
141: 
142: WebSocket Service
143: 
144: ↓
145: 
146: Analytics
147: 
148: ---
149: 
150: # 4. Repository Structure
151: 
152: mirage/
153: 
154: │
155: 
156: ├── frontend/
157: 
158: │   ├── app/
159: 
160: │   ├── components/
161: 
162: │   ├── features/
163: 
164: │   ├── hooks/
165: 
166: │   ├── providers/
167: 
168: │   ├── services/
169: 
170: │   ├── lib/
171: 
172: │   ├── styles/
173: 
174: │   ├── types/
175: 
176: │   └── utils/
177: 
178: │
179: 
180: ├── backend/
181: 
182: │
183: 
184: │   ├── api/
185: 
186: │   ├── core/
187: 
188: │   ├── domain/
189: 
190: │   ├── repositories/
191: 
192: │   ├── services/
193: 
194: │   ├── interfaces/
195: 
196: │   ├── infrastructure/
197: 
198: │   ├── websocket/
199: 
200: │   ├── auth/
201: 
202: │   ├── workers/
203: 
204: │   ├── models/
205: 
206: │   ├── migrations/
207: 
208: │   ├── tests/
209: 
210: │   └── main.py
211: 
212: │
213: 
214: ├── docker/
215: 
216: │
217: 
218: ├── docs/
219: 
220: │
221: 
222: ├── scripts/
223: 
224: │
225: 
226: ├── seed/
227: 
228: │
229: 
230: └── docker-compose.yml
231: 
232: ---
233: 
234: # 5. Backend Folder Structure
235: 
236: backend/
237: 
238: api/
239: 
240: Contains all HTTP routes.
241: 
242: No business logic.
243: 
244: Controllers only.
245: 
246: ---
247: 
248: services/
249: 
250: Business logic.
251: 
252: Examples:
253: 
254: PatientService
255: 
256: DoctorService
257: 
258: ConsentService
259: 
260: NotificationService
261: 
262: RecordService
263: 
264: ConsultationService
265: 
266: DiagnosisService
267: 
268: TimelineService
269: 
270: AuditService
271: 
272: ---
273: 
274: repositories/
275: 
276: Database access.
277: 
278: Examples:
279: 
280: PatientRepository
281: 
282: VisitRepository
283: 
284: ConsentRepository
285: 
286: DoctorRepository
287: 
288: AuditRepository
289: 
290: MedicationRepository
291: 
292: NotificationRepository
293: 
294: Repositories communicate with SQLAlchemy.
295: 
296: Services never do.
297: 
298: ---
299: 
300: interfaces/
301: 
302: Contains contracts.
303: 
304: Examples:
305: 
306: SymptomCheckerProvider
307: 
308: DiagnosisProvider
309: 
310: SummaryProvider
311: 
312: NotificationProvider
313: 
314: TranscriptionProvider
315: 
316: StorageProvider
317: 
318: EmailProvider
319: 
320: ---
321: 
322: infrastructure/
323: 
324: Concrete implementations.
325: 
326: OpenAIProvider
327: 
328: RedisNotificationProvider
329: 
330: WebSocketProvider
331: 
332: PostgresRepositories
333: 
334: Future providers belong here.
335: 
336: ---
337: 
338: models/
339: 
340: SQLAlchemy models.
341: 
342: Contains only persistence definitions.
343: 
344: ---
345: 
346: domain/
347: 
348: Pure business objects.
349: 
350: No framework dependencies.
351: 
352: ---
353: 
354: core/
355: 
356: Configuration.
357: 
358: Dependency Injection.
359: 
360: Logging.
361: 
362: Environment variables.
363: 
364: Application startup.
365: 
366: ---
367: 
368: auth/
369: 
370: JWT
371: 
372: Password Hashing
373: 
374: Roles
375: 
376: Permissions
377: 
378: Session management
379: 
380: ---
381: 
382: websocket/
383: 
384: Real-time event handling.
385: 
386: ---
387: 
388: workers/
389: 
390: Background jobs.
391: 
392: Future AI processing.
393: 
394: Notification delivery.
395: 
396: Long-running tasks.
397: 
398: ---
399: 
400: # 6. Frontend Structure
401: 
402: The frontend follows feature-first organization.
403: 
404: components/
405: 
406: Reusable UI.
407: 
408: Buttons
409: 
410: Cards
411: 
412: Inputs
413: 
414: Sheets
415: 
416: PhoneFrame
417: 
418: Timeline
419: 
420: Dialogs
421: 
422: Tables
423: 
424: Navigation
425: 
426: ---
427: 
428: features/
429: 
430: Patient
431: 
432: Doctor
433: 
434: Authentication
435: 
436: Notifications
437: 
438: Consent
439: 
440: Timeline
441: 
442: AI Consultation
443: 
444: Medical Records
445: 
446: Each feature contains:
447: 
448: components/
449: 
450: hooks/
451: 
452: services/
453: 
454: types/
455: 
456: utils/
457: 
458: ---
459: 
460: app/
461: 
462: Next.js routing.
463: 
464: Should remain thin.
465: 
466: Pages compose features.
467: 
468: ---
469: 
470: providers/
471: 
472: Global providers.
473: 
474: Theme
475: 
476: Authentication
477: 
478: WebSocket
479: 
480: React Query
481: 
482: Motion
483: 
484: ---
485: 
486: hooks/
487: 
488: Shared hooks.
489: 
490: Examples:
491: 
492: useAuth()
493: 
494: usePatient()
495: 
496: useDoctor()
497: 
498: useTimeline()
499: 
500: useConsent()
501: 
502: useNotification()
503: 
504: ---
505: 
506: services/
507: 
508: REST API.
509: 
510: WebSocket Client.
511: 
512: Caching.
513: 
514: ---
515: 
516: lib/
517: 
518: Shared utilities.
519: 
520: Date formatting.
521: 
522: Validation.
523: 
524: Constants.
525: 
526: Helpers.
527: 
528: ---
529: 
530: # 7. Docker Architecture
531: 
532: The project must launch with a single command.
533: 
534: docker compose up
535: 
536: Required containers:
537: 
538: frontend
539: 
540: backend
541: 
542: postgres
543: 
544: redis
545: 
546: worker
547: 
548: Optional:
549: 
550: adminer
551: 
552: pgadmin
553: 
554: mailhog
555: 
556: The frontend communicates only with the backend.
557: 
558: The backend owns all database communication.
559: 
560: No frontend code accesses PostgreSQL directly.
561: 
562: ---
563: 
564: # 8. Environment Configuration
565: 
566: Each service should expose configuration using environment variables.
567: 
568: Frontend
569: 
570: NEXT_PUBLIC_API_URL
571: 
572: NEXT_PUBLIC_WS_URL
573: 
574: DEMO_MODE
575: 
576: Backend
577: 
578: DATABASE_URL
579: 
580: REDIS_URL
581: 
582: JWT_SECRET
583: 
584: JWT_EXPIRATION
585: 
586: REFRESH_SECRET
587: 
588: OPENAI_KEY
589: 
590: SYMPTOM_PROVIDER
591: 
592: SUMMARY_PROVIDER
593: 
594: TRANSCRIPTION_PROVIDER
595: 
596: LOG_LEVEL
597: 
598: All configuration should be injectable.
599: 
600: No secrets should exist inside source code.
601: 
602: ---
603: 
604: # 9. Coding Standards
605: 
606: Backend
607: 
608: Python 3.12+
609: 
610: Type hints everywhere.
611: 
612: Black
613: 
614: Ruff
615: 
616: Pytest
617: 
618: SQLAlchemy 2.x
619: 
620: Alembic
621: 
622: Frontend
623: 
624: TypeScript Strict Mode
625: 
626: ESLint
627: 
628: Prettier
629: 
630: TailwindCSS
631: 
632: Framer Motion
633: 
634: React Query
635: 
636: No `any` types unless absolutely unavoidable.
637: 
638: # 10. Domain-Driven Design
639: 
640: Mirage should follow a Domain-Driven Design (DDD) inspired architecture.
641: 
642: The application should be organized around business concepts rather than infrastructure.
643: 
644: Primary Domains:
645: 
646: - Authentication
647: - Patient Management
648: - Practitioner Registry
649: - Medical Records
650: - Consultations
651: - Consent Management
652: - AI Services
653: - Notifications
654: - Audit Logging
655: 
656: Each domain owns:
657: 
658: - Models
659: - Services
660: - Repositories
661: - Events
662: - DTOs
663: - Validation
664: 
665: Cross-domain communication should occur through service interfaces or events, never by directly manipulating another domain's persistence layer.
666: 
667: ---
668: 
669: # 11. Database Architecture
670: 
671: Database Engine
672: 
673: PostgreSQL
674: 
675: ORM
676: 
677: SQLAlchemy 2.x
678: 
679: Migration Tool
680: 
681: Alembic
682: 
683: Database Naming Convention
684: 
685: snake_case
686: 
687: Primary Keys
688: 
689: UUID
690: 
691: Foreign Keys
692: 
693: UUID
694: 
695: Soft Deletes
696: 
697: Not initially.
698: 
699: Instead use immutable history and audit logs.
700: 
701: Created At
702: 
703: Every table.
704: 
705: Updated At
706: 
707: Every mutable table.
708: 
709: ---
710: 
711: # 12. Core Database Entities
712: 
713: The following entities form the foundation of Mirage.
714: 
715: Users
716: 
717: Roles
718: 
719: Patients
720: 
721: Doctors
722: 
723: Facilities
724: 
725: Practitioner Registry
726: 
727: Medical Records
728: 
729: Visits
730: 
731: Diagnoses
732: 
733: Medications
734: 
735: Allergies
736: 
737: Conditions
738: 
739: Lab Results
740: 
741: Clinical Notes
742: 
743: Consent Requests
744: 
745: Consent Sessions
746: 
747: Notifications
748: 
749: Audit Logs
750: 
751: Access Logs
752: 
753: AI Sessions
754: 
755: AI Messages
756: 
757: Attachments
758: 
759: Refresh Tokens
760: 
761: ---
762: 
763: # 13. Entity Relationships
764: 
765: User
766: 
767: ↓
768: 
769: Patient Profile
770: 
771: or
772: 
773: Doctor Profile
774: 
775: ↓
776: 
777: Consultation
778: 
779: ↓
780: 
781: Visit
782: 
783: ↓
784: 
785: Medical Record
786: 
787: ↓
788: 
789: Timeline
790: 
791: Doctors belong to Facilities.
792: 
793: Patients own Medical Records.
794: 
795: Medical Records contain Visits.
796: 
797: Visits contain:
798: 
799: Diagnoses
800: 
801: Notes
802: 
803: Medication
804: 
805: Attachments
806: 
807: AI Sessions
808: 
809: Lab Results
810: 
811: Consent links Patient and Doctor.
812: 
813: Audit logs reference every important entity.
814: 
815: ---
816: 
817: # 14. Users Table
818: 
819: Purpose
820: 
821: Authentication.
822: 
823: Columns
824: 
825: id
826: 
827: email
828: 
829: password_hash
830: 
831: role
832: 
833: status
834: 
835: is_demo
836: 
837: created_at
838: 
839: updated_at
840: 
841: Relationships
842: 
843: One Patient
844: 
845: or
846: 
847: One Doctor
848: 
849: Future Admin
850: 
851: ---
852: 
853: # 15. Patients Table
854: 
855: Columns
856: 
857: id
858: 
859: medical_record_number
860: 
861: national_id
862: 
863: first_name
864: 
865: last_name
866: 
867: date_of_birth
868: 
869: gender
870: 
871: blood_group
872: 
873: phone
874: 
875: email
876: 
877: address
878: 
879: emergency_contact
880: 
881: created_at
882: 
883: updated_at
884: 
885: Relationships
886: 
887: One Medical Record
888: 
889: Many Visits
890: 
891: Many Notifications
892: 
893: Many Consent Requests
894: 
895: Many Access Logs
896: 
897: ---
898: 
899: # 16. Doctors Table
900: 
901: Columns
902: 
903: id
904: 
905: user_id
906: 
907: registration_number
908: 
909: facility_id
910: 
911: speciality
912: 
913: verification_status
914: 
915: phone
916: 
917: email
918: 
919: created_at
920: 
921: Relationships
922: 
923: Many Consultations
924: 
925: Many Consent Requests
926: 
927: Many Clinical Notes
928: 
929: Many AI Sessions
930: 
931: ---
932: 
933: # 17. Facilities
934: 
935: Columns
936: 
937: id
938: 
939: name
940: 
941: province
942: 
943: district
944: 
945: facility_type
946: 
947: address
948: 
949: contact_number
950: 
951: status
952: 
953: Relationships
954: 
955: Many Doctors
956: 
957: Many Visits
958: 
959: Many Notifications
960: 
961: ---
962: 
963: # 18. Medical Records
964: 
965: Every patient owns exactly one longitudinal record.
966: 
967: Columns
968: 
969: id
970: 
971: patient_id
972: 
973: created_at
974: 
975: updated_at
976: 
977: Relationships
978: 
979: Many Visits
980: 
981: Many Allergies
982: 
983: Many Conditions
984: 
985: Many Medications
986: 
987: Many Attachments
988: 
989: ---
990: 
991: # 19. Visits
992: 
993: Visits represent consultations.
994: 
995: Columns
996: 
997: id
998: 
999: medical_record_id
1000: 
1001: facility_id
1002: 
1003: doctor_id
1004: 
1005: visit_date
1006: 
1007: chief_complaint
1008: 
1009: status
1010: 
1011: created_at
1012: 
1013: Relationships
1014: 
1015: Diagnoses
1016: 
1017: Clinical Notes
1018: 
1019: Medication
1020: 
1021: Investigations
1022: 
1023: Lab Results
1024: 
1025: AI Session
1026: 
1027: ---
1028: 
1029: # 20. Diagnoses
1030: 
1031: Columns
1032: 
1033: id
1034: 
1035: visit_id
1036: 
1037: diagnosis
1038: 
1039: confidence
1040: 
1041: confirmed
1042: 
1043: notes
1044: 
1045: created_at
1046: 
1047: Only confirmed diagnoses become part of permanent history.
1048: 
1049: ---
1050: 
1051: # 21. Medications
1052: 
1053: Columns
1054: 
1055: id
1056: 
1057: visit_id
1058: 
1059: drug_name
1060: 
1061: strength
1062: 
1063: frequency
1064: 
1065: duration
1066: 
1067: instructions
1068: 
1069: ---
1070: 
1071: # 22. Allergies
1072: 
1073: Critical safety information.
1074: 
1075: Columns
1076: 
1077: id
1078: 
1079: patient_id
1080: 
1081: substance
1082: 
1083: reaction
1084: 
1085: severity
1086: 
1087: status
1088: 
1089: Critical allergies should be surfaced throughout the application.
1090: 
1091: ---
1092: 
1093: # 23. Clinical Notes
1094: 
1095: AI generated.
1096: 
1097: Doctor reviewed.
1098: 
1099: Columns
1100: 
1101: id
1102: 
1103: visit_id
1104: 
1105: subjective
1106: 
1107: objective
1108: 
1109: assessment
1110: 
1111: plan
1112: 
1113: doctor_modified
1114: 
1115: approved
1116: 
1117: approved_by
1118: 
1119: approved_at
1120: 
1121: ---
1122: 
1123: # 24. Consent Requests
1124: 
1125: Columns
1126: 
1127: id
1128: 
1129: patient_id
1130: 
1131: doctor_id
1132: 
1133: facility_id
1134: 
1135: status
1136: 
1137: requested_at
1138: 
1139: approved_at
1140: 
1141: expires_at
1142: 
1143: reason
1144: 
1145: scope
1146: 
1147: Every consultation requires a consent request.
1148: 
1149: ---
1150: 
1151: # 25. Consent Sessions
1152: 
1153: Tracks active permissions.
1154: 
1155: Columns
1156: 
1157: id
1158: 
1159: consent_request_id
1160: 
1161: started_at
1162: 
1163: expires_at
1164: 
1165: active
1166: 
1167: Automatically expires.
1168: 
1169: ---
1170: 
1171: # 26. Notifications
1172: 
1173: Columns
1174: 
1175: id
1176: 
1177: recipient_id
1178: 
1179: type
1180: 
1181: title
1182: 
1183: message
1184: 
1185: read
1186: 
1187: created_at
1188: 
1189: Notification types
1190: 
1191: Consent
1192: 
1193: Consultation
1194: 
1195: Medical Record
1196: 
1197: AI
1198: 
1199: System
1200: 
1201: ---
1202: 
1203: # 27. Access Logs
1204: 
1205: Every record view generates an access log.
1206: 
1207: Columns
1208: 
1209: id
1210: 
1211: patient_id
1212: 
1213: doctor_id
1214: 
1215: facility_id
1216: 
1217: purpose
1218: 
1219: access_time
1220: 
1221: duration
1222: 
1223: ip_address
1224: 
1225: user_agent
1226: 
1227: ---
1228: 
1229: # 28. Audit Logs
1230: 
1231: Immutable.
1232: 
1233: Never edited.
1234: 
1235: Columns
1236: 
1237: id
1238: 
1239: actor
1240: 
1241: action
1242: 
1243: entity
1244: 
1245: entity_id
1246: 
1247: timestamp
1248: 
1249: metadata
1250: 
1251: Audit logs form the legal record of system activity.
1252: 
1253: ---
1254: 
1255: # 29. AI Sessions
1256: 
1257: Represents a consultation with AI assistance.
1258: 
1259: Columns
1260: 
1261: id
1262: 
1263: visit_id
1264: 
1265: provider
1266: 
1267: started_at
1268: 
1269: completed_at
1270: 
1271: status
1272: 
1273: summary
1274: 
1275: Relationships
1276: 
1277: Many Messages
1278: 
1279: Generated Diagnosis
1280: 
1281: Generated Summary
1282: 
1283: ---
1284: 
1285: # 30. AI Messages
1286: 
1287: Conversation history.
1288: 
1289: Columns
1290: 
1291: id
1292: 
1293: session_id
1294: 
1295: role
1296: 
1297: content
1298: 
1299: timestamp
1300: 
1301: Messages remain immutable.
1302: 
1303: ---
1304: 
1305: # 31. Attachments
1306: 
1307: Future compatible.
1308: 
1309: Examples
1310: 
1311: Lab Reports
1312: 
1313: Scans
1314: 
1315: Images
1316: 
1317: Documents
1318: 
1319: Columns
1320: 
1321: id
1322: 
1323: visit_id
1324: 
1325: filename
1326: 
1327: mime_type
1328: 
1329: storage_key
1330: 
1331: uploaded_at
1332: 
1333: ---
1334: 
1335: # 32. Refresh Tokens
1336: 
1337: Production mode only.
1338: 
1339: Columns
1340: 
1341: id
1342: 
1343: user_id
1344: 
1345: token_hash
1346: 
1347: expires_at
1348: 
1349: revoked
1350: 
1351: created_at
1352: 
1353: ---
1354: 
1355: # 33. Repository Pattern
1356: 
1357: Every database table should expose a repository.
1358: 
1359: PatientRepository
1360: 
1361: DoctorRepository
1362: 
1363: VisitRepository
1364: 
1365: ConsentRepository
1366: 
1367: DiagnosisRepository
1368: 
1369: MedicationRepository
1370: 
1371: TimelineRepository
1372: 
1373: NotificationRepository
1374: 
1375: AuditRepository
1376: 
1377: Repositories perform persistence only.
1378: 
1379: No business logic.
1380: 
1381: ---
1382: 
1383: # 34. Service Layer
1384: 
1385: Business rules belong here.
1386: 
1387: PatientService
1388: 
1389: DoctorService
1390: 
1391: ConsentService
1392: 
1393: TimelineService
1394: 
1395: RecordService
1396: 
1397: ConsultationService
1398: 
1399: DiagnosisService
1400: 
1401: AuthenticationService
1402: 
1403: NotificationService
1404: 
1405: AuditService
1406: 
1407: AISessionService
1408: 
1409: These services coordinate repositories and providers.
1410: 
1411: ---
1412: 
1413: # 35. Transaction Boundaries
1414: 
1415: Each business operation should execute within a transaction.
1416: 
1417: Example:
1418: 
1419: Doctor confirms consultation
1420: 
1421: ↓
1422: 
1423: Save diagnosis
1424: 
1425: ↓
1426: 
1427: Save notes
1428: 
1429: ↓
1430: 
1431: Update timeline
1432: 
1433: ↓
1434: 
1435: Create audit log
1436: 
1437: ↓
1438: 
1439: Create notification
1440: 
1441: ↓
1442: 
1443: Commit
1444: 
1445: If any step fails:
1446: 
1447: Rollback entire transaction.
1448: 
1449: Never leave partially written medical records.
1450: 
1451: ---
1452: 
1453: # 36. Dependency Injection
1454: 
1455: FastAPI dependency injection should be used throughout.
1456: 
1457: Example flow
1458: 
1459: API Route
1460: 
1461: ↓
1462: 
1463: Service
1464: 
1465: ↓
1466: 
1467: Repository
1468: 
1469: ↓
1470: 
1471: Database
1472: 
1473: External providers
1474: 
1475: ↓
1476: 
1477: Interfaces
1478: 
1479: ↓
1480: 
1481: Concrete implementations
1482: 
1483: No service should instantiate dependencies directly.
1484: 
1485: All dependencies should be injected.
1486: 
1487: This enables testing, mocking, and provider replacement.
1488: 
1489: # 37. Backend Application Architecture
1490: 
1491: The FastAPI backend follows a layered architecture.
1492: 
1493: ```
1494: HTTP Request
1495:       │
1496:       ▼
1497: API Router
1498:       │
1499:       ▼
1500: Request Validation (Pydantic)
1501:       │
1502:       ▼
1503: Application Service
1504:       │
1505:       ▼
1506: Repository + Domain Services
1507:       │
1508:       ▼
1509: Database / AI Provider / Notification Provider
1510:       │
1511:       ▼
1512: Response DTO
1513:       │
1514:       ▼
1515: HTTP Response
1516: ```
1517: 
1518: Routes should never contain business logic.
1519: 
1520: Business rules belong inside Services.
1521: 
1522: Repositories only perform persistence.
1523: 
1524: ---
1525: 
1526: # 38. REST API Design
1527: 
1528: The backend exposes a versioned REST API.
1529: 
1530: ```
1531: /api/v1/
1532: ```
1533: 
1534: Future breaking changes become:
1535: 
1536: ```
1537: /api/v2/
1538: ```
1539: 
1540: ---
1541: 
1542: # 39. Authentication Endpoints
1543: 
1544: ## Demo Login
1545: 
1546: ```
1547: POST /api/v1/auth/demo-login
1548: ```
1549: 
1550: Request
1551: 
1552: ```
1553: {
1554:     "role": "patient"
1555: }
1556: ```
1557: 
1558: or
1559: 
1560: ```
1561: {
1562:     "role": "doctor"
1563: }
1564: ```
1565: 
1566: Returns
1567: 
1568: JWT (optional)
1569: 
1570: User profile
1571: 
1572: Permissions
1573: 
1574: Demo flag
1575: 
1576: ---
1577: 
1578: ## Production Login
1579: 
1580: ```
1581: POST /api/v1/auth/login
1582: ```
1583: 
1584: Returns
1585: 
1586: Access Token
1587: 
1588: Refresh Token
1589: 
1590: Profile
1591: 
1592: Permissions
1593: 
1594: ---
1595: 
1596: ## Refresh Token
1597: 
1598: ```
1599: POST /api/v1/auth/refresh
1600: ```
1601: 
1602: ---
1603: 
1604: ## Logout
1605: 
1606: ```
1607: POST /api/v1/auth/logout
1608: ```
1609: 
1610: Revokes refresh token.
1611: 
1612: ---
1613: 
1614: # 40. Patient Endpoints
1615: 
1616: ```
1617: GET /patients/me
1618: ```
1619: 
1620: Returns patient profile.
1621: 
1622: ---
1623: 
1624: ```
1625: GET /patients/me/timeline
1626: ```
1627: 
1628: Returns longitudinal timeline.
1629: 
1630: ---
1631: 
1632: ```
1633: GET /patients/me/notifications
1634: ```
1635: 
1636: ---
1637: 
1638: ```
1639: GET /patients/me/access-history
1640: ```
1641: 
1642: ---
1643: 
1644: ```
1645: GET /patients/me/medical-record
1646: ```
1647: 
1648: ---
1649: 
1650: ```
1651: GET /patients/me/visits
1652: ```
1653: 
1654: ---
1655: 
1656: ```
1657: GET /patients/me/visit/{id}
1658: ```
1659: 
1660: ---
1661: 
1662: ```
1663: PUT /patients/me/profile
1664: ```
1665: 
1666: Patient-editable information only.
1667: 
1668: ---
1669: 
1670: # 41. Doctor Endpoints
1671: 
1672: ```
1673: GET /doctor/dashboard
1674: ```
1675: 
1676: ---
1677: 
1678: ```
1679: GET /doctor/recent-patients
1680: ```
1681: 
1682: ---
1683: 
1684: ```
1685: GET /doctor/pending-consent
1686: ```
1687: 
1688: ---
1689: 
1690: ```
1691: POST /doctor/search
1692: ```
1693: 
1694: ---
1695: 
1696: ```
1697: GET /doctor/patient/{id}
1698: ```
1699: 
1700: ---
1701: 
1702: ```
1703: GET /doctor/patient/{id}/timeline
1704: ```
1705: 
1706: ---
1707: 
1708: ```
1709: POST /doctor/patient/{id}/consultation
1710: ```
1711: 
1712: Creates a consultation session.
1713: 
1714: ---
1715: 
1716: # 42. Consent API
1717: 
1718: Request Access
1719: 
1720: ```
1721: POST /consent/request
1722: ```
1723: 
1724: Approve
1725: 
1726: ```
1727: POST /consent/approve
1728: ```
1729: 
1730: Reject
1731: 
1732: ```
1733: POST /consent/reject
1734: ```
1735: 
1736: Cancel
1737: 
1738: ```
1739: POST /consent/cancel
1740: ```
1741: 
1742: Status
1743: 
1744: ```
1745: GET /consent/{id}
1746: ```
1747: 
1748: History
1749: 
1750: ```
1751: GET /consent/history
1752: ```
1753: 
1754: ---
1755: 
1756: # 43. Medical Record API
1757: 
1758: Retrieve record
1759: 
1760: ```
1761: GET /records/{id}
1762: ```
1763: 
1764: Retrieve visit
1765: 
1766: ```
1767: GET /visits/{id}
1768: ```
1769: 
1770: Update record
1771: 
1772: ```
1773: POST /records/update
1774: ```
1775: 
1776: Only after doctor approval.
1777: 
1778: ---
1779: 
1780: # 44. AI Session API
1781: 
1782: Create AI Session
1783: 
1784: ```
1785: POST /ai/session
1786: ```
1787: 
1788: Returns
1789: 
1790: Session ID
1791: 
1792: Provider
1793: 
1794: Patient Context Loaded
1795: 
1796: ---
1797: 
1798: Continue Session
1799: 
1800: ```
1801: POST /ai/session/{id}/message
1802: ```
1803: 
1804: Returns
1805: 
1806: AI Response
1807: 
1808: Suggested Questions
1809: 
1810: Updated Context
1811: 
1812: ---
1813: 
1814: Generate Differential
1815: 
1816: ```
1817: POST /ai/session/{id}/diagnosis
1818: ```
1819: 
1820: ---
1821: 
1822: Generate Summary
1823: 
1824: ```
1825: POST /ai/session/{id}/summary
1826: ```
1827: 
1828: ---
1829: 
1830: Close Session
1831: 
1832: ```
1833: POST /ai/session/{id}/complete
1834: ```
1835: 
1836: ---
1837: 
1838: # 45. Notification API
1839: 
1840: ```
1841: GET /notifications
1842: ```
1843: 
1844: ```
1845: PUT /notifications/read
1846: ```
1847: 
1848: ```
1849: DELETE /notifications/{id}
1850: ```
1851: 
1852: ---
1853: 
1854: # 46. WebSocket Architecture
1855: 
1856: Real-time communication should use WebSockets.
1857: 
1858: Endpoint
1859: 
1860: ```
1861: /ws
1862: ```
1863: 
1864: Authenticated using JWT.
1865: 
1866: Clients subscribe after login.
1867: 
1868: ---
1869: 
1870: Supported Events
1871: 
1872: Consent Requested
1873: 
1874: Consent Approved
1875: 
1876: Consent Denied
1877: 
1878: Consultation Started
1879: 
1880: Consultation Completed
1881: 
1882: Record Updated
1883: 
1884: Notification Created
1885: 
1886: Patient Timeline Updated
1887: 
1888: Doctor Dashboard Updated
1889: 
1890: AI Response Ready
1891: 
1892: ---
1893: 
1894: WebSocket payloads should be lightweight.
1895: 
1896: Heavy data should still be retrieved using REST.
1897: 
1898: ---
1899: 
1900: # 47. Redis Event Bus
1901: 
1902: Redis should act as the application's event broker.
1903: 
1904: Example
1905: 
1906: Doctor requests consent
1907: 
1908: ↓
1909: 
1910: Consent Event
1911: 
1912: ↓
1913: 
1914: Redis
1915: 
1916: ↓
1917: 
1918: Notification Worker
1919: 
1920: ↓
1921: 
1922: WebSocket
1923: 
1924: ↓
1925: 
1926: Patient receives request
1927: 
1928: Multiple workers should be able to subscribe independently.
1929: 
1930: ---
1931: 
1932: # 48. AI Provider Architecture
1933: 
1934: The application must never call OpenAI (or any provider) directly from business logic.
1935: 
1936: Instead:
1937: 
1938: ```
1939: Application Service
1940: 
1941: ↓
1942: 
1943: DiagnosisProvider Interface
1944: 
1945: ↓
1946: 
1947: Concrete Provider
1948: 
1949: ↓
1950: 
1951: Vendor API
1952: ```
1953: 
1954: ---
1955: 
1956: Required Provider Interfaces
1957: 
1958: SymptomCheckerProvider
1959: 
1960: DiagnosisProvider
1961: 
1962: ClinicalSummaryProvider
1963: 
1964: TranscriptionProvider
1965: 
1966: NotificationProvider
1967: 
1968: FutureProvider
1969: 
1970: ---
1971: 
1972: Every provider should implement a common lifecycle:
1973: 
1974: Initialize
1975: 
1976: Validate
1977: 
1978: Execute
1979: 
1980: Handle Errors
1981: 
1982: Return Standardized Response
1983: 
1984: ---
1985: 
1986: # 49. Symptom Checker Integration
1987: 
1988: The existing symptom checker is an external dependency.
1989: 
1990: The backend must treat it as a provider.
1991: 
1992: It is NOT implemented inside Mirage.
1993: 
1994: Responsibilities:
1995: 
1996: Load patient context.
1997: 
1998: Begin session.
1999: 
2000: Receive patient answers.

(Showing lines 1-2000 of 2916. Use offset=2001 to continue.)
</content>
```

---

## Assistant (Plan · Kimi · 4.1s)

_Thinking:_

 Let me continue reading the remaining documentation files to get a complete picture before creating a plan and subagents.

 

**Tool: read**

**Input:**
```json
{
  "filePath": "/Users/sheltonmutambirwa/Desktop/medic/docs/04_Implementation_Plan.md"
}
```

**Output:**
```
<path>/Users/sheltonmutambirwa/Desktop/medic/docs/04_Implementation_Plan.md</path>
<type>file</type>
<content>
1: # Mirage
2: # Implementation Plan
3: 
4: Version 1.0
5: 
6: ---
7: 
8: # Purpose
9: 
10: This document defines the recommended implementation order for Mirage.
11: 
12: The coding assistant should complete one phase at a time.
13: 
14: Each phase should compile successfully before beginning the next.
15: 
16: No placeholder implementations should remain unless explicitly documented.
17: 
18: Every phase should leave the repository in a runnable state.
19: 
20: ---
21: 
22: ## Prerequisites
23: 
24: Before implementation begins, the AI assistant must
25: read every document in docs/.
26: 
27: No implementation should begin until the
28: UI Screen Specification and User Flow Specification
29: have also been loaded into context.
30: 
31: ---
32: 
33: # Guiding Principles
34: 
35: The coding assistant should:
36: 
37: - Prefer incremental delivery over large batches.
38: - Keep the application runnable after every phase.
39: - Avoid speculative abstractions.
40: - Follow the Technical Architecture document.
41: - Follow the Design System document.
42: - Never bypass provider interfaces.
43: - Never embed business logic inside UI components.
44: - Never hardcode provider implementations.
45: 
46: ---
47: 
48: # Phase 1 — Repository Bootstrap
49: 
50: ## Goal
51: 
52: Create the complete repository structure.
53: 
54: Nothing functional yet.
55: 
56: Only scaffolding.
57: 
58: ---
59: 
60: Deliverables
61: 
62: ```
63: mirage/
64: 
65: frontend/
66: 
67: backend/
68: 
69: docker/
70: 
71: docs/
72: 
73: seed/
74: 
75: scripts/
76: 
77: .github/
78: 
79: docker-compose.yml
80: 
81: README.md
82: 
83: .env.example
84: 
85: .gitignore
86: ```
87: 
88: ---
89: 
90: Backend folders
91: 
92: ```
93: api/
94: 
95: auth/
96: 
97: core/
98: 
99: domain/
100: 
101: interfaces/
102: 
103: models/
104: 
105: repositories/
106: 
107: services/
108: 
109: workers/
110: 
111: websocket/
112: 
113: tests/
114: 
115: migrations/
116: ```
117: 
118: ---
119: 
120: Frontend folders
121: 
122: ```
123: app/
124: 
125: components/
126: 
127: features/
128: 
129: providers/
130: 
131: hooks/
132: 
133: services/
134: 
135: types/
136: 
137: utils/
138: 
139: styles/
140: ```
141: 
142: ---
143: 
144: Acceptance Criteria
145: 
146: ✓ Repository builds.
147: 
148: ✓ Docker folders exist.
149: 
150: ✓ Folder naming follows architecture.
151: 
152: ✓ README explains project.
153: 
154: ---
155: 
156: # Phase 2 — Docker Environment
157: 
158: ## Goal
159: 
160: Launch the entire stack with one command.
161: 
162: ```
163: docker compose up
164: ```
165: 
166: ---
167: 
168: Containers
169: 
170: Frontend
171: 
172: Backend
173: 
174: PostgreSQL
175: 
176: Redis
177: 
178: Worker
179: 
180: Optional
181: 
182: Adminer
183: 
184: Mailhog
185: 
186: ---
187: 
188: Networking
189: 
190: Internal Docker network.
191: 
192: Backend communicates with:
193: 
194: Postgres
195: 
196: Redis
197: 
198: Frontend communicates only with backend.
199: 
200: ---
201: 
202: Acceptance Criteria
203: 
204: ✓ Every container starts.
205: 
206: ✓ Health checks pass.
207: 
208: ✓ Logs are readable.
209: 
210: ✓ Volumes persist.
211: 
212: ---
213: 
214: # Phase 3 — Backend Bootstrap
215: 
216: Goal
217: 
218: Create FastAPI application.
219: 
220: Implement:
221: 
222: Application startup
223: 
224: Configuration
225: 
226: Dependency Injection
227: 
228: Logging
229: 
230: Health endpoints
231: 
232: Swagger
233: 
234: ReDoc
235: 
236: ---
237: 
238: Routes
239: 
240: ```
241: /health
242: 
243: /live
244: 
245: /ready
246: ```
247: 
248: ---
249: 
250: Acceptance Criteria
251: 
252: Backend starts.
253: 
254: Swagger available.
255: 
256: Health endpoints operational.
257: 
258: ---
259: 
260: # Phase 4 — Database
261: 
262: Goal
263: 
264: Configure PostgreSQL.
265: 
266: Install:
267: 
268: SQLAlchemy
269: 
270: Alembic
271: 
272: Create:
273: 
274: Base Model
275: 
276: Session Factory
277: 
278: Migration configuration
279: 
280: Connection pooling
281: 
282: ---
283: 
284: Acceptance Criteria
285: 
286: Database connects.
287: 
288: Migration executes.
289: 
290: Tables created.
291: 
292: ---
293: 
294: # Phase 5 — Authentication Foundation
295: 
296: Goal
297: 
298: Implement authentication.
299: 
300: Features
301: 
302: JWT
303: 
304: Refresh Tokens
305: 
306: Password Hashing
307: 
308: Roles
309: 
310: Permissions
311: 
312: Demo Mode
313: 
314: ---
315: 
316: Demo Accounts
317: 
318: Patient
319: 
320: Doctor
321: 
322: Administrator
323: 
324: Demo mode should be switchable using:
325: 
326: ```
327: DEMO_MODE=true
328: ```
329: 
330: ---
331: 
332: Acceptance Criteria
333: 
334: Demo login works.
335: 
336: JWT login works.
337: 
338: Protected routes function.
339: 
340: Role authorization functions.
341: 
342: ---
343: 
344: # Phase 6 — Core Database Models
345: 
346: Implement every SQLAlchemy model.
347: 
348: Minimum
349: 
350: Users
351: 
352: Patients
353: 
354: Doctors
355: 
356: Facilities
357: 
358: Medical Records
359: 
360: Visits
361: 
362: Diagnoses
363: 
364: Allergies
365: 
366: Medications
367: 
368: Consent Requests
369: 
370: Notifications
371: 
372: Audit Logs
373: 
374: AI Sessions
375: 
376: Refresh Tokens
377: 
378: ---
379: 
380: Acceptance Criteria
381: 
382: Alembic migration succeeds.
383: 
384: Relationships valid.
385: 
386: No circular imports.
387: 
388: ---
389: 
390: # Phase 7 — Repository Layer
391: 
392: Create repositories.
393: 
394: Each repository includes:
395: 
396: Create
397: 
398: Retrieve
399: 
400: Update
401: 
402: Delete (where appropriate)
403: 
404: Pagination
405: 
406: Filtering
407: 
408: Searching
409: 
410: Repositories contain no business logic.
411: 
412: ---
413: 
414: Acceptance Criteria
415: 
416: Repositories tested.
417: 
418: No service accesses SQLAlchemy directly.
419: 
420: ---
421: 
422: # Phase 8 — Service Layer
423: 
424: Implement:
425: 
426: PatientService
427: 
428: DoctorService
429: 
430: ConsentService
431: 
432: TimelineService
433: 
434: RecordService
435: 
436: NotificationService
437: 
438: AuditService
439: 
440: AuthenticationService
441: 
442: ConsultationService
443: 
444: AISessionService
445: 
446: ---
447: 
448: Acceptance Criteria
449: 
450: Business logic isolated.
451: 
452: Dependency Injection used.
453: 
454: Repositories injected.
455: 
456: No direct database access from routes.
457: 
458: # Phase 9 — REST API
459: 
460: ## Goal
461: 
462: Implement the complete REST API described in the Technical Architecture document.
463: 
464: Modules:
465: 
466: Authentication
467: 
468: Patients
469: 
470: Doctors
471: 
472: Medical Records
473: 
474: Timeline
475: 
476: Visits
477: 
478: Consent
479: 
480: Notifications
481: 
482: AI Sessions
483: 
484: Audit Logs
485: 
486: Settings
487: 
488: ---
489: 
490: Every endpoint should include:
491: 
492: Request validation
493: 
494: Response DTOs
495: 
496: Permission validation
497: 
498: Structured errors
499: 
500: OpenAPI documentation
501: 
502: Pagination where appropriate
503: 
504: Filtering
505: 
506: Sorting
507: 
508: ---
509: 
510: Acceptance Criteria
511: 
512: ✓ Swagger fully documents every endpoint.
513: 
514: ✓ Endpoints return standardized responses.
515: 
516: ✓ Error handling is consistent.
517: 
518: ✓ Authorization enforced server-side.
519: 
520: ---
521: 
522: # Phase 10 — WebSocket Infrastructure
523: 
524: ## Goal
525: 
526: Implement real-time communication.
527: 
528: WebSocket endpoint:
529: 
530: ```
531: /ws
532: ```
533: 
534: Events:
535: 
536: Consent Requested
537: 
538: Consent Approved
539: 
540: Consent Denied
541: 
542: Timeline Updated
543: 
544: Notification Created
545: 
546: Consultation Started
547: 
548: Consultation Completed
549: 
550: AI Response Ready
551: 
552: Dashboard Updated
553: 
554: ---
555: 
556: Requirements
557: 
558: JWT Authentication
559: 
560: Automatic reconnect
561: 
562: Heartbeat
563: 
564: Graceful disconnect
565: 
566: Subscription model
567: 
568: ---
569: 
570: Acceptance Criteria
571: 
572: Real-time updates function.
573: 
574: Browser refresh reconnects correctly.
575: 
576: No duplicate subscriptions.
577: 
578: ---
579: 
580: # Phase 11 — Provider Interfaces
581: 
582: ## Goal
583: 
584: Implement abstraction layers for every external dependency.
585: 
586: Interfaces:
587: 
588: SymptomCheckerProvider
589: 
590: DiagnosisProvider
591: 
592: ClinicalSummaryProvider
593: 
594: TranscriptionProvider
595: 
596: NotificationProvider
597: 
598: StorageProvider
599: 
600: EmailProvider
601: 
602: ---
603: 
604: Initially implement mock providers for all services.
605: 
606: The existing symptom checker should be wrapped behind the SymptomCheckerProvider interface rather than called directly.
607: 
608: Acceptance Criteria
609: 
610: ✓ Business logic depends only on interfaces.
611: 
612: ✓ Swapping providers requires configuration only.
613: 
614: ---
615: 
616: # Phase 12 — Seed Data
617: 
618: Generate realistic demonstration data.
619: 
620: Minimum:
621: 
622: 10 Patients
623: 
624: 5 Doctors
625: 
626: 3 Facilities
627: 
628: 50 Historical Visits
629: 
630: 20 Consent Requests
631: 
632: 100 Notifications
633: 
634: 20 AI Sessions
635: 
636: 100 Clinical Notes
637: 
638: Medication History
639: 
640: Allergies
641: 
642: Chronic Conditions
643: 
644: Lab Results
645: 
646: ---
647: 
648: Data should appear realistic.
649: 
650: Avoid placeholder values such as:
651: 
652: John Doe
653: 
654: Test Patient
655: 
656: Lorem Ipsum
657: 
658: Use geographically and culturally appropriate mock data for the intended demonstration region where possible.
659: 
660: ---
661: 
662: Acceptance Criteria
663: 
664: Application appears populated immediately after setup.
665: 
666: ---
667: 
668: # Phase 13 — Patient Application
669: 
670: Implement every patient screen.
671: 
672: Required screens:
673: 
674: Authentication
675: 
676: Dashboard
677: 
678: Timeline
679: 
680: Visit Details
681: 
682: Medical Record
683: 
684: Notifications
685: 
686: Consent Requests
687: 
688: Consent History
689: 
690: Profile
691: 
692: Settings
693: 
694: Medical ID
695: 
696: AI Symptom Assessment
697: 
698: Access History
699: 
700: About
701: 
702: ---
703: 
704: Every screen includes:
705: 
706: Loading State
707: 
708: Error State
709: 
710: Empty State
711: 
712: Success Feedback
713: 
714: Transitions
715: 
716: ---
717: 
718: Acceptance Criteria
719: 
720: Entire patient journey functions.
721: 
722: ---
723: 
724: # Phase 14 — Doctor Portal
725: 
726: Implement:
727: 
728: Dashboard
729: 
730: Patient Search
731: 
732: Patient Overview
733: 
734: Timeline
735: 
736: Visit Details
737: 
738: AI Consultation
739: 
740: Differential Diagnosis
741: 
742: Clinical Summary
743: 
744: Notifications
745: 
746: Access History
747: 
748: Settings
749: 
750: ---
751: 
752: Acceptance Criteria
753: 
754: Complete consultation workflow operational.
755: 
756: ---
757: 
758: # Phase 15 — Mobile Simulation
759: 
760: Implement PhoneFrame.
761: 
762: Features:
763: 
764: Fixed viewport
765: 
766: Status bar
767: 
768: Safe areas
769: 
770: Notch
771: 
772: Glass bezel
773: 
774: Rounded display
775: 
776: Bottom navigation
777: 
778: Responsive scaling
779: 
780: Motion
781: 
782: No browser scrollbars inside the simulated device.
783: 
784: ---
785: 
786: Acceptance Criteria
787: 
788: Patient application visually resembles a native mobile application.
789: 
790: ---
791: 
792: # Phase 16 — Split-Screen Demonstration
793: 
794: Create dedicated demonstration mode.
795: 
796: Layout:
797: 
798: ```
799: ---------------------------------------------------------
800: 
801: Patient Phone
802: 
803: Doctor Portal
804: 
805: ---------------------------------------------------------
806: ```
807: 
808: Synchronization:
809: 
810: Doctor requests consent.
811: 
812: ↓
813: 
814: Patient notification appears.
815: 
816: ↓
817: 
818: Patient approves.
819: 
820: ↓
821: 
822: Doctor portal unlocks.
823: 
824: ↓
825: 
826: Consultation proceeds.
827: 
828: ↓
829: 
830: Patient timeline updates.
831: 
832: ---
833: 
834: Acceptance Criteria
835: 
836: Entire demonstration completes without refreshing either side.
837: 
838: ---
839: 
840: # Phase 17 — AI Consultation
841: 
842: Integrate provider interfaces.
843: 
844: Workflow:
845: 
846: Patient assessment.
847: 
848: ↓
849: 
850: Doctor consultation.
851: 
852: ↓
853: 
854: Differential diagnosis.
855: 
856: ↓
857: 
858: Clinical summary.
859: 
860: ↓
861: 
862: Doctor edits.
863: 
864: ↓
865: 
866: Confirmation.
867: 
868: ---
869: 
870: Streaming responses preferred.
871: 
872: Fallback to standard responses if unsupported.
873: 
874: ---
875: 
876: Acceptance Criteria
877: 
878: Entire AI workflow functions through provider abstractions.
879: 
880: ---
881: 
882: # Phase 18 — Audit Logging
883: 
884: Every important action should create an immutable audit record.
885: 
886: Events include:
887: 
888: Authentication
889: 
890: Consent
891: 
892: Medical Record Access
893: 
894: Medical Record Updates
895: 
896: AI Sessions
897: 
898: Notifications
899: 
900: Settings Changes
901: 
902: ---
903: 
904: Acceptance Criteria
905: 
906: Audit trail visible and complete.
907: 
908: ---
909: 
910: # Phase 19 — Notification System
911: 
912: Implement:
913: 
914: In-app notifications
915: 
916: Unread count
917: 
918: Toast notifications
919: 
920: Real-time delivery
921: 
922: Notification history
923: 
924: Mark read
925: 
926: Delete
927: 
928: ---
929: 
930: Acceptance Criteria
931: 
932: Notifications synchronize across browser tabs and active sessions.
933: 
934: ---
935: 
936: # Phase 20 — Authentication Completion
937: 
938: Finalize authentication.
939: 
940: Verify:
941: 
942: Demo Mode
943: 
944: JWT Mode
945: 
946: Refresh Tokens
947: 
948: Logout
949: 
950: Permission Guards
951: 
952: Route Protection
953: 
954: Session Recovery
955: 
956: ---
957: 
958: Acceptance Criteria
959: 
960: Application can switch between Demo Mode and Production Mode via configuration only.
961: 
962: ---
963: 
964: # Phase 21 — Testing
965: 
966: Backend:
967: 
968: Pytest
969: 
970: Repository tests
971: 
972: Service tests
973: 
974: API tests
975: 
976: Authentication tests
977: 
978: ---
979: 
980: Frontend:
981: 
982: Vitest
983: 
984: React Testing Library
985: 
986: Critical user flow tests
987: 
988: ---
989: 
990: Integration:
991: 
992: Consent workflow
993: 
994: Timeline updates
995: 
996: Notifications
997: 
998: Authentication
999: 
1000: AI provider mocks
1001: 
1002: ---
1003: 
1004: Acceptance Criteria
1005: 
1006: Critical workflows covered by automated tests.
1007: 
1008: ---
1009: 
1010: # Phase 22 — Documentation
1011: 
1012: Complete project documentation.
1013: 
1014: Required documents:
1015: 
1016: README
1017: 
1018: Architecture
1019: 
1020: Design System
1021: 
1022: API Guide
1023: 
1024: Environment Variables
1025: 
1026: Docker Setup
1027: 
1028: Development Guide
1029: 
1030: Testing Guide
1031: 
1032: Deployment Guide
1033: 
1034: Provider Integration Guide
1035: 
1036: ---
1037: 
1038: README should allow a new developer to start the project within minutes.
1039: 
1040: ---
1041: 
1042: # Phase 23 — Performance & Polish
1043: 
1044: Review the application for:
1045: 
1046: Animation consistency
1047: 
1048: Loading states
1049: 
1050: Accessibility
1051: 
1052: Responsive layouts
1053: 
1054: Keyboard navigation
1055: 
1056: Error handling
1057: 
1058: Empty states
1059: 
1060: Performance bottlenecks
1061: 
1062: Remove dead code.
1063: 
1064: Standardize naming.
1065: 
1066: Review component reuse.
1067: 
1068: ---
1069: 
1070: Acceptance Criteria
1071: 
1072: Application feels production quality.
1073: 
1074: ---
1075: 
1076: # Phase 24 — Final Demonstration
1077: 
1078: Execute the complete demonstration.
1079: 
1080: Scenario:
1081: 
1082: 1. Launch Docker Compose.
1083: 2. Open split-screen mode.
1084: 3. Login as Demo Patient.
1085: 4. Login as Demo Doctor.
1086: 5. Doctor searches patient.
1087: 6. Doctor requests consent.
1088: 7. Patient receives notification.
1089: 8. Patient approves.
1090: 9. Doctor reviews medical history.
1091: 10. AI consultation begins.
1092: 11. Differential diagnosis generated.
1093: 12. Clinical summary generated.
1094: 13. Doctor edits notes.
1095: 14. Doctor confirms consultation.
1096: 15. Patient immediately receives updated timeline and notification.
1097: 16. Audit logs confirm every critical action.
1098: 
1099: The entire demonstration should complete without manual database edits, page refreshes, or developer intervention.
1100: 
1101: ---
1102: 
1103: # Definition of Project Completion
1104: 
1105: Mirage is considered complete when:
1106: 
1107: - All Product Requirements are implemented.
1108: - Technical Architecture is faithfully followed.
1109: - Design System is consistently applied.
1110: - Every implementation phase passes its acceptance criteria.
1111: - The project starts with a single `docker compose up`.
1112: - Demo Mode and JWT Mode are both fully operational.
1113: - AI integrations are abstracted behind provider interfaces.
1114: - Split-screen mode demonstrates the complete patient–doctor workflow.
1115: - The repository is well documented, tested, and ready for future extension.
1116: 
1117: ---
1118: 
1119: # End of Implementation Plan

(End of file - total 1119 lines)
</content>
```

**Tool: read**

**Input:**
```json
{
  "filePath": "/Users/sheltonmutambirwa/Desktop/medic/docs/05_API_Contract.md"
}
```

**Output:**
```
<path>/Users/sheltonmutambirwa/Desktop/medic/docs/05_API_Contract.md</path>
<type>file</type>
<content>
1: # Mirage
2: # API Contract
3: 
4: Version: 1.0
5: 
6: ---
7: 
8: # Purpose
9: 
10: This document defines every public API exposed by the Mirage backend.
11: 
12: The API contract is the single source of truth for communication between:
13: 
14: - Frontend
15: - Backend
16: - AI Providers
17: - Future Mobile Applications
18: - Third-party integrations
19: 
20: Implementation must conform to this specification.
21: 
22: ---
23: 
24: # API Design Principles
25: 
26: The API should be:
27: 
28: - RESTful
29: - Predictable
30: - Versioned
31: - Typed
32: - Consistent
33: - Secure
34: - Documented
35: 
36: Every endpoint returns the same response envelope.
37: 
38: ---
39: 
40: # Base URL
41: 
42: Development
43: 
44: ```
45: http://localhost:8000/api/v1
46: ```
47: 
48: Production
49: 
50: ```
51: https://api.mirage.health/api/v1
52: ```
53: 
54: ---
55: 
56: # Versioning
57: 
58: All endpoints must be versioned.
59: 
60: ```
61: /api/v1/
62: ```
63: 
64: Breaking changes require a new version.
65: 
66: ```
67: /api/v2/
68: ```
69: 
70: Never silently change response structures.
71: 
72: ---
73: 
74: # Authentication
75: 
76: Production authentication uses JWT.
77: 
78: Headers
79: 
80: ```
81: Authorization: Bearer <access_token>
82: ```
83: 
84: Access tokens should be short-lived.
85: 
86: Refresh tokens are stored securely and rotated on refresh.
87: 
88: ---
89: 
90: # Demo Mode Authentication
91: 
92: When `DEMO_MODE=true`, the API exposes:
93: 
94: ```
95: POST /auth/demo-login
96: ```
97: 
98: Body
99: 
100: ```json
101: {
102:   "role": "patient"
103: }
104: ```
105: 
106: or
107: 
108: ```json
109: {
110:   "role": "doctor"
111: }
112: ```
113: 
114: Returns a valid JWT along with a demo user profile.
115: 
116: This endpoint must be disabled in production.
117: 
118: ---
119: 
120: # Standard Response Envelope
121: 
122: Success
123: 
124: ```json
125: {
126:   "success": true,
127:   "data": {},
128:   "errors": [],
129:   "meta": {
130:     "requestId": "uuid",
131:     "timestamp": "ISO-8601"
132:   }
133: }
134: ```
135: 
136: Failure
137: 
138: ```json
139: {
140:   "success": false,
141:   "data": null,
142:   "errors": [
143:     {
144:       "code": "VALIDATION_ERROR",
145:       "message": "Validation failed.",
146:       "field": "email"
147:     }
148:   ],
149:   "meta": {
150:     "requestId": "uuid",
151:     "timestamp": "ISO-8601"
152:   }
153: }
154: ```
155: 
156: All endpoints must follow this structure.
157: 
158: ---
159: 
160: # Pagination Standard
161: 
162: Collection endpoints should support:
163: 
164: ```
165: ?page=1
166: &pageSize=20
167: &sort=createdAt
168: &order=desc
169: ```
170: 
171: Response
172: 
173: ```json
174: {
175:   "success": true,
176:   "data": [...],
177:   "meta": {
178:     "page": 1,
179:     "pageSize": 20,
180:     "total": 247,
181:     "totalPages": 13
182:   }
183: }
184: ```
185: 
186: ---
187: 
188: # Filtering
189: 
190: Supported query parameters:
191: 
192: ```
193: status
194: 
195: dateFrom
196: 
197: dateTo
198: 
199: doctorId
200: 
201: patientId
202: 
203: facilityId
204: 
205: search
206: ```
207: 
208: Unknown filters should return HTTP 400.
209: 
210: ---
211: 
212: # Sorting
213: 
214: Supported:
215: 
216: ```
217: createdAt
218: 
219: updatedAt
220: 
221: date
222: 
223: lastName
224: 
225: firstName
226: 
227: status
228: ```
229: 
230: ---
231: 
232: # Standard Error Codes
233: 
234: Authentication
235: 
236: ```
237: UNAUTHORIZED
238: 
239: TOKEN_EXPIRED
240: 
241: INVALID_TOKEN
242: 
243: FORBIDDEN
244: ```
245: 
246: Validation
247: 
248: ```
249: VALIDATION_ERROR
250: 
251: INVALID_REQUEST
252: 
253: MISSING_FIELD
254: ```
255: 
256: Consent
257: 
258: ```
259: CONSENT_REQUIRED
260: 
261: CONSENT_DENIED
262: 
263: CONSENT_EXPIRED
264: ```
265: 
266: Medical Records
267: 
268: ```
269: RECORD_NOT_FOUND
270: 
271: VISIT_NOT_FOUND
272: 
273: PATIENT_NOT_FOUND
274: ```
275: 
276: AI
277: 
278: ```
279: AI_PROVIDER_UNAVAILABLE
280: 
281: AI_TIMEOUT
282: 
283: AI_RESPONSE_INVALID
284: ```
285: 
286: General
287: 
288: ```
289: NOT_FOUND
290: 
291: INTERNAL_SERVER_ERROR
292: 
293: CONFLICT
294: 
295: RATE_LIMITED
296: ```
297: 
298: Codes should remain stable across releases.
299: 
300: ---
301: 
302: # Date Format
303: 
304: Always ISO-8601.
305: 
306: Example
307: 
308: ```
309: 2026-07-05T14:42:18Z
310: ```
311: 
312: Never return locale-specific formats.
313: 
314: ---
315: 
316: # UUID Format
317: 
318: Primary identifiers use UUID v4.
319: 
320: Example
321: 
322: ```
323: 8b9f13b4-f90b-41d9-b5e4-3a63cde2c87f
324: ```
325: 
326: Integer IDs should not be exposed publicly.
327: 
328: ---
329: 
330: # Common Objects
331: 
332: ## User
333: 
334: ```json
335: {
336:   "id": "uuid",
337:   "role": "doctor",
338:   "firstName": "Jane",
339:   "lastName": "Smith",
340:   "email": "jane@example.com",
341:   "avatarUrl": null
342: }
343: ```
344: 
345: ---
346: 
347: ## Doctor
348: 
349: ```json
350: {
351:   "id": "uuid",
352:   "registrationNumber": "MED12345",
353:   "specialty": "General Practice",
354:   "facilityId": "uuid"
355: }
356: ```
357: 
358: ---
359: 
360: ## Patient
361: 
362: ```json
363: {
364:   "id": "uuid",
365:   "medicalRecordNumber": "MRN-100234",
366:   "dateOfBirth": "1995-03-20",
367:   "gender": "Female"
368: }
369: ```
370: 
371: ---
372: 
373: ## Facility
374: 
375: ```json
376: {
377:   "id": "uuid",
378:   "name": "Harare Central Hospital",
379:   "address": "...",
380:   "phone": "..."
381: }
382: ```
383: 
384: ---
385: 
386: ## Notification
387: 
388: ```json
389: {
390:   "id": "uuid",
391:   "type": "CONSENT_REQUEST",
392:   "title": "Access Request",
393:   "body": "Dr. Smith has requested access.",
394:   "read": false,
395:   "createdAt": "..."
396: }
397: ```
398: 
399: ---
400: 
401: ## Audit Entry
402: 
403: ```json
404: {
405:   "id": "uuid",
406:   "userId": "uuid",
407:   "action": "CONSENT_APPROVED",
408:   "resource": "ConsentRequest",
409:   "resourceId": "uuid",
410:   "timestamp": "..."
411: }
412: ```
413: 
414: ---
415: 
416: # Idempotency
417: 
418: The following endpoints should accept an optional:
419: 
420: ```
421: Idempotency-Key
422: ```
423: 
424: Header.
425: 
426: Examples:
427: 
428: Create consultation
429: 
430: Submit AI request
431: 
432: Approve consent
433: 
434: Record update
435: 
436: Repeated requests with the same key should return the original response where appropriate.
437: 
438: ---
439: 
440: # Rate Limiting
441: 
442: Authentication endpoints:
443: 
444: 10 requests/minute
445: 
446: AI endpoints:
447: 
448: 30 requests/minute
449: 
450: Search endpoints:
451: 
452: 60 requests/minute
453: 
454: General API:
455: 
456: Configurable via environment variables.
457: 
458: Rate limit responses return HTTP 429.
459: 
460: ---
461: 
462: # Correlation IDs
463: 
464: Every request receives a server-generated correlation ID.
465: 
466: Response header:
467: 
468: ```
469: X-Request-ID
470: ```
471: 
472: This value should also appear in structured logs to support tracing across services.
473: 
474: # Authentication API
475: 
476: ---
477: 
478: ## POST /auth/demo-login
479: 
480: Purpose
481: 
482: Authenticate instantly using predefined demonstration accounts.
483: 
484: Authentication
485: 
486: None
487: 
488: Request
489: 
490: ```json
491: {
492:   "role": "patient"
493: }
494: ```
495: 
496: Allowed values
497: 
498: ```
499: patient
500: 
501: doctor
502: 
503: admin
504: ```
505: 
506: Success
507: 
508: ```json
509: {
510:   "success": true,
511:   "data": {
512:     "accessToken": "...",
513:     "refreshToken": "...",
514:     "expiresIn": 3600,
515:     "user": {
516:       "id": "uuid",
517:       "role": "patient",
518:       "firstName": "Alice",
519:       "lastName": "Ncube"
520:     }
521:   }
522: }
523: ```
524: 
525: ---
526: 
527: ## POST /auth/login
528: 
529: Purpose
530: 
531: Authenticate using username/password.
532: 
533: Authentication
534: 
535: None
536: 
537: Request
538: 
539: ```json
540: {
541:   "email": "doctor@example.com",
542:   "password": "password"
543: }
544: ```
545: 
546: Response
547: 
548: Same structure as Demo Login.
549: 
550: Errors
551: 
552: ```
553: INVALID_CREDENTIALS
554: 
555: ACCOUNT_DISABLED
556: 
557: ACCOUNT_LOCKED
558: ```
559: 
560: ---
561: 
562: ## POST /auth/refresh
563: 
564: Request
565: 
566: ```json
567: {
568:   "refreshToken": "..."
569: }
570: ```
571: 
572: Returns
573: 
574: New access token.
575: 
576: Rotated refresh token.
577: 
578: ---
579: 
580: ## POST /auth/logout
581: 
582: Authentication
583: 
584: Required
585: 
586: Request
587: 
588: Empty
589: 
590: Response
591: 
592: 204 No Content
593: 
594: Refresh token revoked.
595: 
596: ---
597: 
598: ## GET /auth/me
599: 
600: Returns
601: 
602: Current authenticated user.
603: 
604: ---
605: 
606: # Patient API
607: 
608: ---
609: 
610: ## GET /patients/me
611: 
612: Returns
613: 
614: Patient profile.
615: 
616: Example
617: 
618: ```json
619: {
620:   "success": true,
621:   "data": {
622:     "id": "uuid",
623:     "medicalRecordNumber": "MRN-0001",
624:     "firstName": "Alice",
625:     "lastName": "Ncube",
626:     "gender": "Female",
627:     "dateOfBirth": "1998-01-15",
628:     "bloodType": "O+",
629:     "allergies": [],
630:     "conditions": [],
631:     "medications": []
632:   }
633: }
634: ```
635: 
636: ---
637: 
638: ## PUT /patients/me
639: 
640: Editable fields
641: 
642: Phone
643: 
644: Email
645: 
646: Emergency Contact
647: 
648: Address
649: 
650: Preferred Language
651: 
652: Notification Preferences
653: 
654: Immutable fields
655: 
656: MRN
657: 
658: Date of Birth
659: 
660: Legal Name
661: 
662: National Identifier
663: 
664: ---
665: 
666: ## GET /patients/me/timeline
667: 
668: Returns
669: 
670: Chronological medical history.
671: 
672: Response
673: 
674: ```json
675: {
676:   "success": true,
677:   "data": [
678:     {
679:       "visitId": "uuid",
680:       "date": "...",
681:       "facility": "...",
682:       "doctor": "...",
683:       "summary": "...",
684:       "diagnosis": "...",
685:       "status": "completed"
686:     }
687:   ]
688: }
689: ```
690: 
691: ---
692: 
693: ## GET /patients/me/visits
694: 
695: Paginated visit history.
696: 
697: Supports
698: 
699: Date filtering
700: 
701: Facility filtering
702: 
703: Search
704: 
705: ---
706: 
707: ## GET /patients/me/visit/{visitId}
708: 
709: Returns complete visit details.
710: 
711: Includes
712: 
713: Diagnoses
714: 
715: Medication
716: 
717: Clinical Notes
718: 
719: Attachments
720: 
721: Lab Results
722: 
723: AI Summary
724: 
725: Audit Metadata
726: 
727: ---
728: 
729: ## GET /patients/me/notifications
730: 
731: Returns notifications ordered by newest first.
732: 
733: Supports
734: 
735: Pagination
736: 
737: Unread filter
738: 
739: Category filter
740: 
741: ---
742: 
743: ## PUT /patients/me/notifications/{id}/read
744: 
745: Marks notification as read.
746: 
747: ---
748: 
749: ## GET /patients/me/access-history
750: 
751: Returns every healthcare professional that has viewed the patient's record.
752: 
753: Each record includes
754: 
755: Doctor
756: 
757: Facility
758: 
759: Purpose
760: 
761: Timestamp
762: 
763: Consent Reference
764: 
765: ---
766: 
767: # Doctor API
768: 
769: ---
770: 
771: ## GET /doctor/dashboard
772: 
773: Returns
774: 
775: Today's appointments
776: 
777: Pending consent
778: 
779: Recent activity
780: 
781: Statistics
782: 
783: Notifications
784: 
785: AI tasks
786: 
787: ---
788: 
789: ## POST /doctor/search
790: 
791: Purpose
792: 
793: Search patients.
794: 
795: Request
796: 
797: ```json
798: {
799:   "query": "Alice"
800: }
801: ```
802: 
803: Response
804: 
805: ```json
806: [
807:   {
808:     "patientId": "...",
809:     "medicalRecordNumber": "...",
810:     "fullName": "...",
811:     "dateOfBirth": "...",
812:     "gender": "..."
813:   }
814: ]
815: ```
816: 
817: ---
818: 
819: Supports
820: 
821: Partial search
822: 
823: MRN
824: 
825: National ID
826: 
827: Phone
828: 
829: Email
830: 
831: Name
832: 
833: ---
834: 
835: ## GET /doctor/patient/{patientId}
836: 
837: Returns
838: 
839: Patient overview.
840: 
841: Requires
842: 
843: Approved consent.
844: 
845: Errors
846: 
847: ```
848: CONSENT_REQUIRED
849: 
850: CONSENT_EXPIRED
851: 
852: PATIENT_NOT_FOUND
853: ```
854: 
855: ---
856: 
857: ## GET /doctor/patient/{patientId}/timeline
858: 
859: Returns
860: 
861: Full timeline.
862: 
863: Requires
864: 
865: Valid consent.
866: 
867: ---
868: 
869: ## POST /doctor/patient/{patientId}/consultation
870: 
871: Creates consultation session.
872: 
873: Request
874: 
875: ```json
876: {
877:   "reason": "Routine consultation"
878: }
879: ```
880: 
881: Returns
882: 
883: ```json
884: {
885:   "consultationId": "uuid",
886:   "status": "ACTIVE"
887: }
888: ```
889: 
890: ---
891: 
892: ## POST /doctor/patient/{patientId}/notes
893: 
894: Creates clinician notes.
895: 
896: Notes remain editable until finalized.
897: 
898: ---
899: 
900: ## POST /doctor/patient/{patientId}/summary
901: 
902: Requests AI clinical summary.
903: 
904: Returns
905: 
906: Job ID.
907: 
908: ---
909: 
910: # Consent API
911: 
912: ---
913: 
914: ## POST /consent/request
915: 
916: Purpose
917: 
918: Doctor requests patient access.
919: 
920: Request
921: 
922: ```json
923: {
924:   "patientId": "...",
925:   "purpose": "Emergency consultation",
926:   "scope": [
927:     "medical_record",
928:     "timeline",
929:     "lab_results"
930:   ],
931:   "expiresInMinutes": 60
932: }
933: ```
934: 
935: Returns
936: 
937: Consent request object.
938: 
939: Triggers
940: 
941: Notification
942: 
943: WebSocket event
944: 
945: Audit log
946: 
947: ---
948: 
949: ## GET /consent/{consentId}
950: 
951: Returns
952: 
953: Consent details.
954: 
955: Status
956: 
957: Pending
958: 
959: Approved
960: 
961: Denied
962: 
963: Expired
964: 
965: Cancelled
966: 
967: ---
968: 
969: ## POST /consent/{consentId}/approve
970: 
971: Authentication
972: 
973: Patient
974: 
975: Returns
976: 
977: Updated consent.
978: 
979: Triggers
980: 
981: Doctor notification
982: 
983: Dashboard refresh
984: 
985: Audit event
986: 
987: ---
988: 
989: ## POST /consent/{consentId}/deny
990: 
991: Authentication
992: 
993: Patient
994: 
995: Request
996: 
997: Optional reason.
998: 
999: Returns
1000: 
1001: Updated consent.
1002: 
1003: ---
1004: 
1005: ## POST /consent/{consentId}/cancel
1006: 
1007: Authentication
1008: 
1009: Doctor
1010: 
1011: Purpose
1012: 
1013: Withdraw request before approval.
1014: 
1015: ---
1016: 
1017: ## GET /consent/history
1018: 
1019: Returns
1020: 
1021: Historical consent requests.
1022: 
1023: Supports
1024: 
1025: Status filter
1026: 
1027: Date filter
1028: 
1029: Patient filter
1030: 
1031: Doctor filter
1032: 
1033: Pagination
1034: 
1035: ---
1036: 
1037: # Permissions Matrix
1038: 
1039: | Endpoint | Patient | Doctor | Admin |
1040: |-----------|:------:|:------:|:-----:|
1041: | Demo Login | ✓ | ✓ | ✓ |
1042: | Login | ✓ | ✓ | ✓ |
1043: | Patient Profile | ✓ | ✗ | ✓ |
1044: | Doctor Dashboard | ✗ | ✓ | ✓ |
1045: | Patient Timeline | ✓ | ✓ (with consent) | ✓ |
1046: | Request Consent | ✗ | ✓ | ✓ |
1047: | Approve Consent | ✓ | ✗ | ✓ |
1048: | Deny Consent | ✓ | ✗ | ✓ |
1049: | Notifications | ✓ | ✓ | ✓ |
1050: | AI Consultation | ✗ | ✓ | ✓ |
1051: 
1052: Permission enforcement must occur server-side regardless of any frontend restrictions.
1053: 
1054: ---
1055: 
1056: # Authorization Rules
1057: 
1058: The backend is the ultimate authority for access control.
1059: 
1060: The frontend may hide unavailable actions for usability, but it must never be relied upon for security.
1061: 
1062: Every protected endpoint must verify:
1063: 
1064: - Authentication
1065: - User role
1066: - Consent status (where applicable)
1067: - Resource ownership or authorization
1068: - Token validity
1069: 
1070: Requests failing any of these checks should return the appropriate HTTP status code and standardized error response.
1071: 
1072: # Medical Record API
1073: 
1074: ---
1075: 
1076: ## GET /records/{recordId}
1077: 
1078: Purpose
1079: 
1080: Retrieve a patient's complete medical record.
1081: 
1082: Authentication
1083: 
1084: Doctor (with valid consent)
1085: 
1086: Patient (own record)
1087: 
1088: Admin
1089: 
1090: Response
1091: 
1092: ```json
1093: {
1094:   "success": true,
1095:   "data": {
1096:     "patient": {},
1097:     "conditions": [],
1098:     "allergies": [],
1099:     "medications": [],
1100:     "vaccinations": [],
1101:     "labResults": [],
1102:     "imaging": [],
1103:     "documents": []
1104:   }
1105: }
1106: ```
1107: 
1108: ---
1109: 
1110: ## PATCH /records/{recordId}
1111: 
1112: Purpose
1113: 
1114: Update patient record.
1115: 
1116: Authentication
1117: 
1118: Doctor
1119: 
1120: Restrictions
1121: 
1122: Changes remain in a draft state until the consultation is finalized.
1123: 
1124: Every update generates:
1125: 
1126: - Audit log
1127: - Version history
1128: - Updated timestamp
1129: 
1130: ---
1131: 
1132: ## GET /records/{recordId}/versions
1133: 
1134: Returns
1135: 
1136: Historical versions of the medical record.
1137: 
1138: Supports comparison between versions.
1139: 
1140: ---
1141: 
1142: # Timeline API
1143: 
1144: ---
1145: 
1146: ## GET /timeline/{patientId}
1147: 
1148: Returns
1149: 
1150: Complete chronological timeline.
1151: 
1152: Each event includes:
1153: 
1154: ```json
1155: {
1156:   "eventId": "uuid",
1157:   "eventType": "VISIT",
1158:   "date": "...",
1159:   "facility": {},
1160:   "doctor": {},
1161:   "summary": "...",
1162:   "attachments": [],
1163:   "status": "COMPLETED"
1164: }
1165: ```
1166: 
1167: Supported event types
1168: 
1169: - Visit
1170: - Prescription
1171: - Diagnosis
1172: - Laboratory
1173: - Imaging
1174: - Surgery
1175: - Vaccination
1176: - Allergy Update
1177: - Consent Event
1178: - AI Consultation
1179: 
1180: ---
1181: 
1182: ## GET /timeline/event/{eventId}
1183: 
1184: Returns
1185: 
1186: Expanded timeline event.
1187: 
1188: ---
1189: 
1190: # AI Session API
1191: 
1192: ---
1193: 
1194: ## POST /ai/session
1195: 
1196: Purpose
1197: 
1198: Create an AI consultation session.
1199: 
1200: Request
1201: 
1202: ```json
1203: {
1204:   "patientId": "uuid",
1205:   "consultationId": "uuid"
1206: }
1207: ```
1208: 
1209: Response
1210: 
1211: ```json
1212: {
1213:   "sessionId": "uuid",
1214:   "provider": "mock",
1215:   "status": "ACTIVE"
1216: }
1217: ```
1218: 
1219: ---
1220: 
1221: ## POST /ai/session/{sessionId}/message
1222: 
1223: Purpose
1224: 
1225: Continue an AI conversation.
1226: 
1227: Request
1228: 
1229: ```json
1230: {
1231:   "message": "The patient reports chest pain for three days."
1232: }
1233: ```
1234: 
1235: Response
1236: 
1237: ```json
1238: {
1239:   "messageId": "uuid",
1240:   "role": "assistant",
1241:   "content": "...",
1242:   "suggestedQuestions": [],
1243:   "citations": [],
1244:   "complete": false
1245: }
1246: ```
1247: 
1248: Streaming responses should be supported when the provider allows it.
1249: 
1250: ---
1251: 
1252: ## POST /ai/session/{sessionId}/diagnosis
1253: 
1254: Purpose
1255: 
1256: Generate differential diagnosis.
1257: 
1258: Returns
1259: 
1260: ```json
1261: {
1262:   "diagnoses": [
1263:     {
1264:       "name": "Community-acquired pneumonia",
1265:       "confidence": 0.83,
1266:       "reasoning": "...",
1267:       "recommendedInvestigations": [],
1268:       "medicationWarnings": []
1269:     }
1270:   ]
1271: }
1272: ```
1273: 
1274: AI responses remain advisory.
1275: 
1276: Nothing is persisted automatically.
1277: 
1278: ---
1279: 
1280: ## POST /ai/session/{sessionId}/summary
1281: 
1282: Purpose
1283: 
1284: Generate structured consultation notes.
1285: 
1286: Returns
1287: 
1288: ```json
1289: {
1290:   "soap": {
1291:     "subjective": "...",
1292:     "objective": "...",
1293:     "assessment": "...",
1294:     "plan": "..."
1295:   }
1296: }
1297: ```
1298: 
1299: Doctors may edit every section before saving.
1300: 
1301: ---
1302: 
1303: ## POST /ai/session/{sessionId}/complete
1304: 
1305: Purpose
1306: 
1307: Close AI consultation.
1308: 
1309: Response
1310: 
1311: ```json
1312: {
1313:   "status": "COMPLETED"
1314: }
1315: ```
1316: 
1317: ---
1318: 
1319: # Transcription API
1320: 
1321: ---
1322: 
1323: ## POST /transcription/start
1324: 
1325: Purpose
1326: 
1327: Begin live transcription.
1328: 
1329: Returns
1330: 
1331: Session identifier.
1332: 
1333: ---
1334: 
1335: ## POST /transcription/{sessionId}/audio
1336: 
1337: Purpose
1338: 
1339: Upload audio chunk.
1340: 
1341: Request
1342: 
1343: Binary stream or multipart upload.
1344: 
1345: ---
1346: 
1347: ## GET /transcription/{sessionId}
1348: 
1349: Returns
1350: 
1351: Current transcript.
1352: 
1353: ```json
1354: {
1355:   "segments": [
1356:     {
1357:       "speaker": "Doctor",
1358:       "text": "...",
1359:       "timestamp": "..."
1360:     }
1361:   ]
1362: }
1363: ```
1364: 
1365: ---
1366: 
1367: ## POST /transcription/{sessionId}/stop
1368: 
1369: Stops transcription.
1370: 
1371: Returns finalized transcript.
1372: 
1373: ---
1374: 
1375: # Notification API
1376: 
1377: ---
1378: 
1379: ## GET /notifications
1380: 
1381: Supports
1382: 
1383: Pagination
1384: 
1385: Unread filter
1386: 
1387: Category filter
1388: 
1389: Priority filter
1390: 
1391: ---
1392: 
1393: ## GET /notifications/{notificationId}
1394: 
1395: Returns
1396: 
1397: Complete notification.
1398: 
1399: ---
1400: 
1401: ## PATCH /notifications/{notificationId}
1402: 
1403: Purpose
1404: 
1405: Update notification.
1406: 
1407: Examples
1408: 
1409: Mark read
1410: 
1411: Archive
1412: 
1413: Pin
1414: 
1415: ---
1416: 
1417: ## DELETE /notifications/{notificationId}
1418: 
1419: Soft delete only.
1420: 
1421: ---
1422: 
1423: # Audit API
1424: 
1425: ---
1426: 
1427: ## GET /audit
1428: 
1429: Admin only.
1430: 
1431: Supports
1432: 
1433: User filter
1434: 
1435: Patient filter
1436: 
1437: Action filter
1438: 
1439: Date filter
1440: 
1441: ---
1442: 
1443: ## GET /audit/{auditId}
1444: 
1445: Returns complete audit event.
1446: 
1447: Includes
1448: 
1449: User
1450: 
1451: Timestamp
1452: 
1453: IP Address
1454: 
1455: User Agent
1456: 
1457: Affected Resource
1458: 
1459: Action
1460: 
1461: Metadata
1462: 
1463: Audit entries are immutable.
1464: 
1465: ---
1466: 
1467: # WebSocket Contract
1468: 
1469: Endpoint
1470: 
1471: ```
1472: /ws
1473: ```
1474: 
1475: Authentication
1476: 
1477: JWT during connection establishment.
1478: 
1479: After authentication, the client subscribes to one or more channels.
1480: 
1481: Examples
1482: 
1483: ```
1484: patient:{patientId}
1485: 
1486: doctor:{doctorId}
1487: 
1488: notifications
1489: 
1490: consultations
1491: 
1492: dashboard
1493: ```
1494: 
1495: ---
1496: 
1497: # WebSocket Event Envelope
1498: 
1499: Every event follows the same structure.
1500: 
1501: ```json
1502: {
1503:   "type": "CONSENT_APPROVED",
1504:   "timestamp": "...",
1505:   "payload": {}
1506: }
1507: ```
1508: 
1509: ---
1510: 
1511: # Supported Events
1512: 
1513: ## Consent Requested
1514: 
1515: ```json
1516: {
1517:   "type": "CONSENT_REQUESTED",
1518:   "payload": {
1519:     "consentId": "uuid",
1520:     "doctorId": "uuid",
1521:     "patientId": "uuid"
1522:   }
1523: }
1524: ```
1525: 
1526: ---
1527: 
1528: ## Consent Approved
1529: 
1530: ```json
1531: {
1532:   "type": "CONSENT_APPROVED",
1533:   "payload": {
1534:     "consentId": "uuid"
1535:   }
1536: }
1537: ```
1538: 
1539: ---
1540: 
1541: ## Consent Denied
1542: 
1543: ---
1544: 
1545: ## Consultation Started
1546: 
1547: ---
1548: 
1549: ## Consultation Completed
1550: 
1551: ---
1552: 
1553: ## Timeline Updated
1554: 
1555: ---
1556: 
1557: ## Medical Record Updated
1558: 
1559: ---
1560: 
1561: ## Notification Created
1562: 
1563: ---
1564: 
1565: ## AI Response Ready
1566: 
1567: ---
1568: 
1569: ## AI Streaming Token (optional)
1570: 
1571: ```json
1572: {
1573:   "type": "AI_STREAM",
1574:   "payload": {
1575:     "sessionId": "uuid",
1576:     "token": "partial text"
1577:   }
1578: }
1579: ```
1580: 
1581: The frontend should assemble streamed tokens into a complete message.
1582: 
1583: ---
1584: 
1585: # Enumerations
1586: 
1587: ## UserRole
1588: 
1589: ```
1590: PATIENT
1591: 
1592: DOCTOR
1593: 
1594: ADMIN
1595: ```
1596: 
1597: ---
1598: 
1599: ## ConsentStatus
1600: 
1601: ```
1602: PENDING
1603: 
1604: APPROVED
1605: 
1606: DENIED
1607: 
1608: EXPIRED
1609: 
1610: CANCELLED
1611: ```
1612: 
1613: ---
1614: 
1615: ## ConsultationStatus
1616: 
1617: ```
1618: CREATED
1619: 
1620: ACTIVE
1621: 
1622: PAUSED
1623: 
1624: COMPLETED
1625: 
1626: CANCELLED
1627: ```
1628: 
1629: ---
1630: 
1631: ## NotificationType
1632: 
1633: ```
1634: CONSENT
1635: 
1636: MEDICAL_RECORD
1637: 
1638: CONSULTATION
1639: 
1640: REMINDER
1641: 
1642: SYSTEM
1643: 
1644: AI
1645: ```
1646: 
1647: ---
1648: 
1649: ## AI Session Status
1650: 
1651: ```
1652: CREATED
1653: 
1654: ACTIVE
1655: 
1656: PROCESSING
1657: 
1658: COMPLETED
1659: 
1660: FAILED
1661: ```
1662: 
1663: ---
1664: 
1665: ## Visit Status
1666: 
1667: ```
1668: SCHEDULED
1669: 
1670: IN_PROGRESS
1671: 
1672: COMPLETED
1673: 
1674: CANCELLED
1675: ```
1676: 
1677: ---
1678: 
1679: # HTTP Status Code Usage
1680: 
1681: 200 — Successful retrieval
1682: 
1683: 201 — Resource created
1684: 
1685: 202 — Accepted for asynchronous processing
1686: 
1687: 204 — Successful operation with no content
1688: 
1689: 400 — Invalid request
1690: 
1691: 401 — Authentication required
1692: 
1693: 403 — Authenticated but not authorized
1694: 
1695: 404 — Resource not found
1696: 
1697: 409 — Conflict
1698: 
1699: 422 — Validation error
1700: 
1701: 429 — Rate limit exceeded
1702: 
1703: 500 — Internal server error
1704: 
1705: 503 — External provider unavailable
1706: 
1707: Status codes should be used consistently across the API.
1708: 
1709: ---
1710: 
1711: # API Definition of Done
1712: 
1713: The API contract is complete when:
1714: 
1715: - Every endpoint required by the Product Requirements Document is defined.
1716: - Every request and response is explicitly specified.
1717: - Standard response envelopes are used throughout.
1718: - Authentication and authorization rules are documented.
1719: - Error codes are stable and documented.
1720: - WebSocket payloads are standardized.
1721: - AI interactions remain provider-agnostic.
1722: - The contract is sufficient for frontend and backend teams to work independently without additional clarification.
1723: 
1724: # End of API Contract

(End of file - total 1724 lines)
</content>
```

**Tool: read**

**Input:**
```json
{
  "filePath": "/Users/sheltonmutambirwa/Desktop/medic/docs/06_Database_Schema.md"
}
```

**Output:**
```
<path>/Users/sheltonmutambirwa/Desktop/medic/docs/06_Database_Schema.md</path>
<type>file</type>
<content>
1: # Mirage
2: # Database Schema Specification
3: 
4: Version: 1.0
5: 
6: ---
7: 
8: # Purpose
9: 
10: This document defines the relational database schema for Mirage.
11: 
12: It is the single source of truth for:
13: 
14: - PostgreSQL schema
15: - SQLAlchemy models
16: - Alembic migrations
17: - Repository implementations
18: - Seed data
19: - Foreign key relationships
20: 
21: The database should follow normalization principles while remaining practical for healthcare workloads.
22: 
23: ---
24: 
25: # Database Technology
26: 
27: Database
28: 
29: PostgreSQL 16+
30: 
31: ORM
32: 
33: SQLAlchemy 2.x
34: 
35: Migration Tool
36: 
37: Alembic
38: 
39: Driver
40: 
41: psycopg
42: 
43: ---
44: 
45: # General Rules
46: 
47: Primary keys
48: 
49: UUID v4
50: 
51: Public identifiers
52: 
53: UUID only
54: 
55: Timestamps
56: 
57: UTC
58: 
59: Soft deletion
60: 
61: Supported where appropriate
62: 
63: Audit logging
64: 
65: Immutable
66: 
67: Foreign keys
68: 
69: Explicitly declared
70: 
71: Indexes
72: 
73: Added to commonly queried fields
74: 
75: ---
76: 
77: # Common Columns
78: 
79: Nearly every table should include:
80: 
81: ```
82: id UUID PRIMARY KEY
83: 
84: created_at TIMESTAMP WITH TIME ZONE
85: 
86: updated_at TIMESTAMP WITH TIME ZONE
87: 
88: created_by UUID NULL
89: 
90: updated_by UUID NULL
91: ```
92: 
93: Optional
94: 
95: ```
96: deleted_at TIMESTAMP NULL
97: ```
98: 
99: Soft deletion should be avoided for clinical events that require permanent history.
100: 
101: ---
102: 
103: # Enumerations
104: 
105: ## UserRole
106: 
107: ```
108: PATIENT
109: 
110: DOCTOR
111: 
112: ADMIN
113: ```
114: 
115: ---
116: 
117: ## ConsentStatus
118: 
119: ```
120: PENDING
121: 
122: APPROVED
123: 
124: DENIED
125: 
126: EXPIRED
127: 
128: CANCELLED
129: ```
130: 
131: ---
132: 
133: ## VisitStatus
134: 
135: ```
136: SCHEDULED
137: 
138: IN_PROGRESS
139: 
140: COMPLETED
141: 
142: CANCELLED
143: ```
144: 
145: ---
146: 
147: ## NotificationType
148: 
149: ```
150: CONSENT
151: 
152: VISIT
153: 
154: REMINDER
155: 
156: SYSTEM
157: 
158: AI
159: 
160: MEDICAL_RECORD
161: ```
162: 
163: ---
164: 
165: ## AISessionStatus
166: 
167: ```
168: CREATED
169: 
170: ACTIVE
171: 
172: PROCESSING
173: 
174: COMPLETED
175: 
176: FAILED
177: ```
178: 
179: ---
180: 
181: # Entity Relationship Overview
182: 
183: ```
184: User
185: │
186: ├── Patient
187: │     │
188: │     ├── MedicalRecord
189: │     │       │
190: │     │       ├── Visit
191: │     │       ├── Allergy
192: │     │       ├── Medication
193: │     │       ├── Diagnosis
194: │     │       ├── LabResult
195: │     │       └── Document
196: │     │
197: │     ├── Notification
198: │     ├── ConsentRequest
199: │     └── AISession
200: │
201: └── Doctor
202:       │
203:       ├── Consultation
204:       ├── ClinicalNote
205:       └── Facility
206: ```
207: 
208: ---
209: 
210: # users
211: 
212: Purpose
213: 
214: Authentication and identity.
215: 
216: Columns
217: 
218: ```
219: id
220: 
221: email
222: 
223: password_hash
224: 
225: role
226: 
227: first_name
228: 
229: last_name
230: 
231: avatar_url
232: 
233: phone_number
234: 
235: is_active
236: 
237: last_login_at
238: 
239: created_at
240: 
241: updated_at
242: ```
243: 
244: Indexes
245: 
246: ```
247: email UNIQUE
248: 
249: role
250: 
251: is_active
252: ```
253: 
254: ---
255: 
256: # patients
257: 
258: Purpose
259: 
260: Patient demographic profile.
261: 
262: Relationship
263: 
264: One-to-one with User.
265: 
266: Columns
267: 
268: ```
269: id
270: 
271: user_id
272: 
273: medical_record_number
274: 
275: national_identifier
276: 
277: date_of_birth
278: 
279: gender
280: 
281: blood_type
282: 
283: address
284: 
285: emergency_contact_name
286: 
287: emergency_contact_phone
288: 
289: preferred_language
290: ```
291: 
292: Indexes
293: 
294: ```
295: medical_record_number UNIQUE
296: 
297: national_identifier
298: 
299: date_of_birth
300: ```
301: 
302: ---
303: 
304: # doctors
305: 
306: Purpose
307: 
308: Doctor profile.
309: 
310: Columns
311: 
312: ```
313: id
314: 
315: user_id
316: 
317: registration_number
318: 
319: specialty
320: 
321: facility_id
322: 
323: department
324: 
325: license_expiry
326: 
327: years_experience
328: ```
329: 
330: Indexes
331: 
332: ```
333: registration_number UNIQUE
334: 
335: facility_id
336: 
337: specialty
338: ```
339: 
340: ---
341: 
342: # facilities
343: 
344: Columns
345: 
346: ```
347: id
348: 
349: name
350: 
351: address
352: 
353: phone
354: 
355: email
356: 
357: city
358: 
359: country
360: 
361: timezone
362: ```
363: 
364: Indexes
365: 
366: ```
367: name
368: 
369: city
370: ```
371: 
372: ---
373: 
374: # medical_records
375: 
376: Purpose
377: 
378: Root clinical record.
379: 
380: One record per patient.
381: 
382: Columns
383: 
384: ```
385: id
386: 
387: patient_id
388: 
389: primary_physician_id
390: 
391: record_status
392: 
393: created_at
394: 
395: updated_at
396: ```
397: 
398: Indexes
399: 
400: ```
401: patient_id UNIQUE
402: ```
403: 
404: ---
405: 
406: # visits
407: 
408: Purpose
409: 
410: Every clinical encounter.
411: 
412: Columns
413: 
414: ```
415: id
416: 
417: medical_record_id
418: 
419: doctor_id
420: 
421: facility_id
422: 
423: visit_date
424: 
425: status
426: 
427: reason
428: 
429: chief_complaint
430: 
431: summary
432: 
433: ai_summary
434: 
435: follow_up_required
436: ```
437: 
438: Indexes
439: 
440: ```
441: visit_date
442: 
443: doctor_id
444: 
445: facility_id
446: 
447: status
448: ```
449: 
450: Visits are immutable after finalization except through versioned amendments.
451: 
452: ---
453: 
454: # diagnoses
455: 
456: Columns
457: 
458: ```
459: id
460: 
461: visit_id
462: 
463: diagnosis_name
464: 
465: icd10_code
466: 
467: confidence
468: 
469: primary_diagnosis
470: 
471: notes
472: ```
473: 
474: Indexes
475: 
476: ```
477: visit_id
478: 
479: icd10_code
480: ```
481: 
482: Multiple diagnoses per visit supported.
483: 
484: ---
485: 
486: # medications
487: 
488: Columns
489: 
490: ```
491: id
492: 
493: visit_id
494: 
495: name
496: 
497: dosage
498: 
499: frequency
500: 
501: duration
502: 
503: instructions
504: 
505: start_date
506: 
507: end_date
508: ```
509: 
510: Indexes
511: 
512: ```
513: visit_id
514: 
515: name
516: ```
517: 
518: ---
519: 
520: # allergies
521: 
522: Columns
523: 
524: ```
525: id
526: 
527: medical_record_id
528: 
529: allergen
530: 
531: reaction
532: 
533: severity
534: 
535: notes
536: ```
537: 
538: Indexes
539: 
540: ```
541: medical_record_id
542: 
543: severity
544: ```
545: 
546: ---
547: 
548: # chronic_conditions
549: 
550: Purpose
551: 
552: Long-term medical history.
553: 
554: Columns
555: 
556: ```
557: id
558: 
559: medical_record_id
560: 
561: condition_name
562: 
563: diagnosed_date
564: 
565: status
566: 
567: notes
568: ```
569: 
570: ---
571: 
572: # laboratory_results
573: 
574: Columns
575: 
576: ```
577: id
578: 
579: visit_id
580: 
581: test_name
582: 
583: result
584: 
585: reference_range
586: 
587: status
588: 
589: performed_at
590: ```
591: 
592: Indexes
593: 
594: ```
595: performed_at
596: 
597: visit_id
598: ```
599: 
600: ---
601: 
602: # imaging_results
603: 
604: Columns
605: 
606: ```
607: id
608: 
609: visit_id
610: 
611: modality
612: 
613: study_name
614: 
615: report
616: 
617: performed_at
618: ```
619: 
620: Examples
621: 
622: X-Ray
623: 
624: CT
625: 
626: MRI
627: 
628: Ultrasound
629: 
630: ---
631: 
632: # clinical_documents
633: 
634: Purpose
635: 
636: Uploaded PDFs, referrals, discharge summaries, reports, and attachments.
637: 
638: Columns
639: 
640: ```
641: id
642: 
643: medical_record_id
644: 
645: storage_key
646: 
647: filename
648: 
649: mime_type
650: 
651: uploaded_by
652: 
653: uploaded_at
654: ```
655: 
656: The storage provider determines where the file is physically stored (local, S3, Azure Blob, etc.), keeping the database independent of storage implementation.
657: 
658: ---
659: 
660: # Relationship Rules
661: 
662: User → Patient
663: 
664: One-to-one
665: 
666: User → Doctor
667: 
668: One-to-one
669: 
670: Patient → MedicalRecord
671: 
672: One-to-one
673: 
674: MedicalRecord → Visits
675: 
676: One-to-many
677: 
678: Visit → Diagnoses
679: 
680: One-to-many
681: 
682: Visit → Medications
683: 
684: One-to-many
685: 
686: MedicalRecord → Allergies
687: 
688: One-to-many
689: 
690: MedicalRecord → ChronicConditions
691: 
692: One-to-many
693: 
694: Visit → LaboratoryResults
695: 
696: One-to-many
697: 
698: Visit → ImagingResults
699: 
700: One-to-many
701: 
702: MedicalRecord → ClinicalDocuments
703: 
704: One-to-many
705: 
706: Foreign key constraints should enforce referential integrity. Cascading deletes should generally be avoided for clinical data; instead, records should be retained or archived in accordance with audit and retention requirements.
707: 
708: # consent_requests
709: 
710: Purpose
711: 
712: Represents a doctor's request to access a patient's medical information.
713: 
714: Consent is explicit, time-bound, and fully auditable.
715: 
716: Columns
717: 
718: ```
719: id
720: 
721: patient_id
722: 
723: doctor_id
724: 
725: facility_id
726: 
727: purpose
728: 
729: scope
730: 
731: status
732: 
733: requested_at
734: 
735: approved_at
736: 
737: expires_at
738: 
739: denied_reason
740: 
741: cancelled_at
742: ```
743: 
744: Scope should be stored as a JSON array for flexibility.
745: 
746: Example
747: 
748: ```json
749: [
750:   "medical_record",
751:   "timeline",
752:   "lab_results"
753: ]
754: ```
755: 
756: Indexes
757: 
758: ```
759: patient_id
760: 
761: doctor_id
762: 
763: status
764: 
765: expires_at
766: ```
767: 
768: Rules
769: 
770: - Only one ACTIVE/PENDING consent request per doctor-patient pair.
771: - Expired consent must not grant access.
772: - Historical consent records are immutable.
773: 
774: ---
775: 
776: # ai_sessions
777: 
778: Purpose
779: 
780: Tracks AI-assisted consultations.
781: 
782: Columns
783: 
784: ```
785: id
786: 
787: patient_id
788: 
789: doctor_id
790: 
791: consultation_id
792: 
793: provider_name
794: 
795: status
796: 
797: started_at
798: 
799: completed_at
800: 
801: provider_metadata
802: 
803: conversation_summary
804: ```
805: 
806: Indexes
807: 
808: ```
809: patient_id
810: 
811: doctor_id
812: 
813: status
814: 
815: started_at
816: ```
817: 
818: provider_metadata should be stored as JSONB.
819: 
820: ---
821: 
822: # ai_messages
823: 
824: Purpose
825: 
826: Stores conversation history for AI consultations.
827: 
828: Columns
829: 
830: ```
831: id
832: 
833: session_id
834: 
835: role
836: 
837: content
838: 
839: token_count
840: 
841: created_at
842: ```
843: 
844: Role values
845: 
846: ```
847: SYSTEM
848: 
849: USER
850: 
851: ASSISTANT
852: ```
853: 
854: Indexes
855: 
856: ```
857: session_id
858: 
859: created_at
860: ```
861: 
862: Messages should never be edited after creation.
863: 
864: ---
865: 
866: # clinical_notes
867: 
868: Purpose
869: 
870: Doctor-authored consultation notes.
871: 
872: Columns
873: 
874: ```
875: id
876: 
877: visit_id
878: 
879: doctor_id
880: 
881: subjective
882: 
883: objective
884: 
885: assessment
886: 
887: plan
888: 
889: is_finalized
890: 
891: created_at
892: 
893: updated_at
894: ```
895: 
896: Rules
897: 
898: Notes remain editable until finalized.
899: 
900: Finalized notes create a new version instead of overwriting.
901: 
902: ---
903: 
904: # notifications
905: 
906: Purpose
907: 
908: Stores all in-app notifications.
909: 
910: Columns
911: 
912: ```
913: id
914: 
915: recipient_user_id
916: 
917: type
918: 
919: title
920: 
921: body
922: 
923: payload
924: 
925: priority
926: 
927: is_read
928: 
929: read_at
930: 
931: created_at
932: ```
933: 
934: Payload stored as JSONB.
935: 
936: Example
937: 
938: ```json
939: {
940:   "consentId": "uuid",
941:   "patientId": "uuid"
942: }
943: ```
944: 
945: Indexes
946: 
947: ```
948: recipient_user_id
949: 
950: is_read
951: 
952: type
953: 
954: created_at
955: ```
956: 
957: ---
958: 
959: # refresh_tokens
960: 
961: Purpose
962: 
963: Supports secure JWT refresh token rotation.
964: 
965: Columns
966: 
967: ```
968: id
969: 
970: user_id
971: 
972: token_hash
973: 
974: expires_at
975: 
976: revoked_at
977: 
978: created_at
979: 
980: last_used_at
981: ```
982: 
983: Rules
984: 
985: Store only hashed refresh tokens.
986: 
987: Never store raw refresh tokens.
988: 
989: ---
990: 
991: # audit_logs
992: 
993: Purpose
994: 
995: Immutable record of every sensitive action.
996: 
997: Columns
998: 
999: ```
1000: id
1001: 
1002: user_id
1003: 
1004: action
1005: 
1006: resource_type
1007: 
1008: resource_id
1009: 
1010: ip_address
1011: 
1012: user_agent
1013: 
1014: metadata
1015: 
1016: created_at
1017: ```
1018: 
1019: Metadata stored as JSONB.
1020: 
1021: Examples of actions
1022: 
1023: ```
1024: LOGIN
1025: 
1026: LOGOUT
1027: 
1028: CONSENT_REQUESTED
1029: 
1030: CONSENT_APPROVED
1031: 
1032: CONSENT_DENIED
1033: 
1034: PATIENT_RECORD_VIEWED
1035: 
1036: PATIENT_RECORD_UPDATED
1037: 
1038: AI_SESSION_STARTED
1039: 
1040: AI_SUMMARY_GENERATED
1041: 
1042: PROFILE_UPDATED
1043: ```
1044: 
1045: Indexes
1046: 
1047: ```
1048: user_id
1049: 
1050: resource_type
1051: 
1052: resource_id
1053: 
1054: created_at
1055: 
1056: action
1057: ```
1058: 
1059: Audit logs must never be updated or deleted.
1060: 
1061: ---
1062: 
1063: # websocket_connections (Optional)
1064: 
1065: Purpose
1066: 
1067: Track active WebSocket connections.
1068: 
1069: Useful for scaling to multiple backend instances.
1070: 
1071: Columns
1072: 
1073: ```
1074: id
1075: 
1076: user_id
1077: 
1078: connection_id
1079: 
1080: connected_at
1081: 
1082: last_seen_at
1083: 
1084: server_instance
1085: ```
1086: 
1087: This table may be omitted in MVP if connection state is maintained in memory.
1088: 
1089: ---
1090: 
1091: # background_jobs (Optional)
1092: 
1093: Purpose
1094: 
1095: Track long-running asynchronous work.
1096: 
1097: Columns
1098: 
1099: ```
1100: id
1101: 
1102: job_type
1103: 
1104: status
1105: 
1106: payload
1107: 
1108: result
1109: 
1110: created_at
1111: 
1112: started_at
1113: 
1114: completed_at
1115: 
1116: error_message
1117: ```
1118: 
1119: Status
1120: 
1121: ```
1122: QUEUED
1123: 
1124: RUNNING
1125: 
1126: COMPLETED
1127: 
1128: FAILED
1129: ```
1130: 
1131: This is optional if Redis-based queues already provide sufficient tracking.
1132: 
1133: ---
1134: 
1135: # medical_record_versions
1136: 
1137: Purpose
1138: 
1139: Maintain version history for patient records.
1140: 
1141: Columns
1142: 
1143: ```
1144: id
1145: 
1146: medical_record_id
1147: 
1148: version_number
1149: 
1150: changed_by
1151: 
1152: change_summary
1153: 
1154: snapshot
1155: 
1156: created_at
1157: ```
1158: 
1159: Snapshot stored as JSONB.
1160: 
1161: Supports:
1162: 
1163: - Rollback
1164: - Audit
1165: - Historical comparison
1166: 
1167: Medical records should never lose historical state.
1168: 
1169: ---
1170: 
1171: # Database Constraints
1172: 
1173: Required unique constraints
1174: 
1175: Users
1176: 
1177: ```
1178: email
1179: ```
1180: 
1181: Patients
1182: 
1183: ```
1184: medical_record_number
1185: ```
1186: 
1187: Doctors
1188: 
1189: ```
1190: registration_number
1191: ```
1192: 
1193: Medical Records
1194: 
1195: ```
1196: patient_id
1197: ```
1198: 
1199: Refresh Tokens
1200: 
1201: ```
1202: token_hash
1203: ```
1204: 
1205: ---
1206: 
1207: # Foreign Key Rules
1208: 
1209: Every foreign key should specify explicit actions.
1210: 
1211: Preferred defaults
1212: 
1213: ```
1214: ON UPDATE CASCADE
1215: 
1216: ON DELETE RESTRICT
1217: ```
1218: 
1219: Clinical information should not be deleted automatically.
1220: 
1221: ---
1222: 
1223: # JSONB Usage
1224: 
1225: Use JSONB only for semi-structured data.
1226: 
1227: Examples
1228: 
1229: AI metadata
1230: 
1231: Notification payloads
1232: 
1233: Consent scope
1234: 
1235: Audit metadata
1236: 
1237: Medical record snapshots
1238: 
1239: Avoid storing structured relational data in JSONB.
1240: 
1241: ---
1242: 
1243: # Indexing Strategy
1244: 
1245: Indexes should exist for:
1246: 
1247: Primary keys
1248: 
1249: Foreign keys
1250: 
1251: Search fields
1252: 
1253: Frequently filtered timestamps
1254: 
1255: Status columns
1256: 
1257: Medical Record Number
1258: 
1259: Registration Number
1260: 
1261: Notification recipient
1262: 
1263: Consent status
1264: 
1265: Visit date
1266: 
1267: Avoid unnecessary indexes that slow writes.
1268: 
1269: ---
1270: 
1271: # Soft Deletion Strategy
1272: 
1273: Soft deletion (`deleted_at`) may be used for:
1274: 
1275: User accounts
1276: 
1277: Notifications
1278: 
1279: Draft consultations
1280: 
1281: Do NOT soft-delete:
1282: 
1283: Medical records
1284: 
1285: Visits
1286: 
1287: Diagnoses
1288: 
1289: Clinical notes
1290: 
1291: Audit logs
1292: 
1293: Consent history
1294: 
1295: Clinical history should remain permanently traceable.
1296: 
1297: ---
1298: 
1299: # Alembic Migration Strategy
1300: 
1301: Migration rules
1302: 
1303: - One migration per logical change.
1304: - Never edit an existing migration after it has been committed.
1305: - Use descriptive migration names.
1306: - Test upgrades and downgrades locally.
1307: - Seed data should not be embedded inside schema migrations.
1308: 
1309: Example
1310: 
1311: ```
1312: 001_create_users.py
1313: 
1314: 002_create_patients.py
1315: 
1316: 003_create_medical_records.py
1317: 
1318: 004_create_visits.py
1319: 
1320: 005_create_consent_requests.py
1321: ```
1322: 
1323: ---
1324: 
1325: # Seed Data Relationships
1326: 
1327: Initial seed data should create a realistic ecosystem.
1328: 
1329: Minimum dataset
1330: 
1331: ```
1332: 10 Users (Patients)
1333: 
1334: 5 Users (Doctors)
1335: 
1336: 3 Facilities
1337: 
1338: 10 Medical Records
1339: 
1340: 50 Visits
1341: 
1342: 120 Diagnoses
1343: 
1344: 150 Medications
1345: 
1346: 40 Allergies
1347: 
1348: 30 Chronic Conditions
1349: 
1350: 75 Laboratory Results
1351: 
1352: 25 Imaging Reports
1353: 
1354: 100 Notifications
1355: 
1356: 20 Consent Requests
1357: 
1358: 15 AI Sessions
1359: 
1360: 500 Audit Log Entries
1361: ```
1362: 
1363: Seeded data should maintain referential integrity and realistic timelines.
1364: 
1365: ---
1366: 
1367: # Database Definition of Done
1368: 
1369: The database layer is complete when:
1370: 
1371: - Every entity required by the Product Requirements Document exists.
1372: - Relationships are normalized and enforce referential integrity.
1373: - UUIDs are used consistently as public identifiers.
1374: - Audit logs are immutable.
1375: - Medical history is preserved through versioning.
1376: - Provider-specific data remains abstracted via JSONB where appropriate.
1377: - Alembic migrations can create the schema from an empty database.
1378: - Seed data produces a realistic demonstration environment without manual intervention.
1379: 
1380: # End of Database Schema Specification

(End of file - total 1380 lines)
</content>
```

**Tool: read**

**Input:**
```json
{
  "filePath": "/Users/sheltonmutambirwa/Desktop/medic/docs/07_Master_Generation_Prompt.md"
}
```

**Output:**
```
<path>/Users/sheltonmutambirwa/Desktop/medic/docs/07_Master_Generation_Prompt.md</path>
<type>file</type>
<content>
1: # Mirage
2: # Master Generation Prompt
3: 
4: You are a senior software architect and staff-level engineer responsible for implementing the Mirage healthcare platform.
5: 
6: You are not merely generating code.
7: 
8: You are designing and implementing a maintainable production-quality software system.
9: 
10: Your objective is to create a repository that another experienced engineer would enjoy maintaining.
11: 
12: You should optimize for:
13: 
14: - Maintainability
15: - Readability
16: - Correctness
17: - Extensibility
18: - Developer Experience
19: - Healthcare safety
20: - Clean Architecture
21: 
22: Never optimize for generating the fewest lines of code.
23: 
24: Always optimize for producing the highest-quality repository.
25: 
26: ---
27: 
28: # Project Context
29: 
30: Mirage is a healthcare platform consisting of two applications.
31: 
32: 1.
33: 
34: Patient Application
35: 
36: Runs inside a simulated mobile device rendered in the browser.
37: 
38: 2.
39: 
40: Doctor Portal
41: 
42: Desktop-first clinical interface.
43: 
44: The backend is implemented using:
45: 
46: FastAPI
47: 
48: Python
49: 
50: PostgreSQL
51: 
52: Redis
53: 
54: SQLAlchemy
55: 
56: Alembic
57: 
58: Docker Compose
59: 
60: The frontend uses:
61: 
62: Next.js
63: 
64: TypeScript
65: 
66: TailwindCSS
67: 
68: Framer Motion
69: 
70: React Query
71: 
72: The application demonstrates a patient-controlled healthcare workflow centered around real-time consent management and AI-assisted consultations.
73: 
74: ---
75: 
76: # Existing AI Systems
77: 
78: The repository should NOT implement AI directly.
79: 
80: Instead,
81: 
82: it communicates through provider interfaces.
83: 
84: The existing symptom checker already exists.
85: 
86: Treat it as an external dependency.
87: 
88: Wrap it behind:
89: 
90: SymptomCheckerProvider
91: 
92: Likewise:
93: 
94: DiagnosisProvider
95: 
96: ClinicalSummaryProvider
97: 
98: TranscriptionProvider
99: 
100: NotificationProvider
101: 
102: StorageProvider
103: 
104: EmailProvider
105: 
106: These implementations must remain replaceable.
107: 
108: Never couple business logic to a specific vendor.
109: 
110: ---
111: 
112: # Development Philosophy
113: 
114: Prefer:
115: 
116: Simple
117: 
118: Explicit
119: 
120: Predictable
121: 
122: Typed
123: 
124: Documented
125: 
126: Composable
127: 
128: Avoid:
129: 
130: Magic
131: 
132: Hidden behaviour
133: 
134: Global state
135: 
136: Overengineering
137: 
138: Premature optimization
139: 
140: ---
141: 
142: # Architectural Rules
143: 
144: Follow the supplied documentation.
145: 
146: The order of authority is:
147: 
148: 1.
149: 
150: Product Requirements
151: 
152: 2.
153: 
154: Technical Architecture
155: 
156: 3.
157: 
158: Design System
159: 
160: 4.
161: 
162: Implementation Plan
163: 
164: If ambiguity exists,
165: 
166: choose the interpretation most consistent with healthcare software best practices.
167: 
168: ---
169: 
170: # Repository Expectations
171: 
172: The repository should feel as though it was created by an experienced engineering team.
173: 
174: Every folder should have a purpose.
175: 
176: Every file should belong somewhere obvious.
177: 
178: Avoid dumping unrelated utilities into shared folders.
179: 
180: ---
181: 
182: # Code Quality
183: 
184: Backend
185: 
186: Python 3.12+
187: 
188: Strict typing
189: 
190: Docstrings
191: 
192: Dependency Injection
193: 
194: Repository Pattern
195: 
196: Service Layer
197: 
198: Pydantic v2
199: 
200: SQLAlchemy 2.x
201: 
202: Alembic
203: 
204: Frontend
205: 
206: Strict TypeScript
207: 
208: Functional Components
209: 
210: Composition over inheritance
211: 
212: Reusable hooks
213: 
214: Feature-first organization
215: 
216: Accessibility
217: 
218: No duplicated business logic.
219: 
220: ---
221: 
222: # UI Expectations
223: 
224: Patient application:
225: 
226: Native mobile experience.
227: 
228: Doctor portal:
229: 
230: Professional clinical dashboard.
231: 
232: Animations:
233: 
234: Purposeful.
235: 
236: Subtle.
237: 
238: Fast.
239: 
240: Never distracting.
241: 
242: ---
243: 
244: # Demo Requirements
245: 
246: Support both:
247: 
248: Demo Mode
249: 
250: Production Mode
251: 
252: Demo Mode should allow instant login.
253: 
254: Production Mode should use JWT authentication.
255: 
256: Both should coexist.
257: 
258: Configuration determines which is active.
259: 
260: ---
261: 
262: # Docker
263: 
264: The repository should start using:
265: 
266: docker compose up
267: 
268: No manual setup.
269: 
270: No undocumented steps.
271: 
272: ---
273: 
274: # Testing
275: 
276: Every major feature should include tests.
277: 
278: Prioritize:
279: 
280: Authentication
281: 
282: Consent
283: 
284: Medical records
285: 
286: Timeline
287: 
288: Notifications
289: 
290: AI provider interfaces
291: 
292: Split-screen workflow
293: 
294: Focus on behaviour rather than implementation details.
295: 
296: ---
297: 
298: # Documentation
299: 
300: Every major subsystem should be documented.
301: 
302: README
303: 
304: Architecture
305: 
306: Environment variables
307: 
308: Provider integrations
309: 
310: Development setup
311: 
312: Deployment
313: 
314: Testing
315: 
316: Avoid undocumented behaviour.
317: 
318: ---
319: 
320: # Coding Behaviour
321: 
322: Never invent functionality that contradicts the supplied specifications.
323: 
324: If requirements are missing,
325: 
326: create the smallest reasonable implementation that preserves extensibility.
327: 
328: Avoid speculative features.
329: 
330: Do not implement Phase 2 functionality unless explicitly required.
331: 
332: ---
333: 
334: # Provider Behaviour
335: 
336: Every provider should expose interfaces.
337: 
338: Business logic should never import vendor SDKs.
339: 
340: Instead:
341: 
342: Application Service
343: 
344: ↓
345: 
346: Provider Interface
347: 
348: ↓
349: 
350: Concrete Provider
351: 
352: ↓
353: 
354: Vendor SDK
355: 
356: Dependency Injection should resolve providers.
357: 
358: ---
359: 
360: # Medical Safety
361: 
362: AI never replaces clinicians.
363: 
364: AI suggestions require doctor review.
365: 
366: Nothing should automatically modify patient records.
367: 
368: Clinical approval always occurs before persistence.
369: 
370: ---
371: 
372: # Definition of Success
373: 
374: The repository should appear production quality.
375: 
376: Another engineer should be able to:
377: 
378: Clone
379: 
380: Configure
381: 
382: Run
383: 
384: Understand
385: 
386: Extend
387: 
388: Deploy
389: 
390: without needing undocumented knowledge.
391: 
392: The finished repository should resemble software built by an experienced startup engineering team rather than an automatically generated prototype.
393: 
394: # Repository Generation Protocol
395: 
396: You are responsible for generating an entire software repository.
397: 
398: Do not think of this as generating code.
399: 
400: Think of it as leading an engineering project.
401: 
402: Your responsibility is to preserve architectural consistency across every file.
403: 
404: Every implementation decision should be evaluated against the overall system architecture rather than the individual feature being developed.
405: 
406: ---
407: 
408: # Incremental Development
409: 
410: Never attempt to build the entire repository in a single step.
411: 
412: Instead:
413: 
414: Complete one implementation phase.
415: 
416: Verify the phase.
417: 
418: Refactor if necessary.
419: 
420: Only then continue.
421: 
422: The repository should compile after every completed phase.
423: 
424: Never intentionally leave the repository in a broken state.
425: 
426: ---
427: 
428: # Implementation Order
429: 
430: Always follow the Implementation Plan.
431: 
432: Do not reorder phases unless absolutely necessary.
433: 
434: Preferred sequence:
435: 
436: Repository
437: 
438: ↓
439: 
440: Docker
441: 
442: ↓
443: 
444: Backend Foundation
445: 
446: ↓
447: 
448: Database
449: 
450: ↓
451: 
452: Authentication
453: 
454: ↓
455: 
456: Repositories
457: 
458: ↓
459: 
460: Services
461: 
462: ↓
463: 
464: REST API
465: 
466: ↓
467: 
468: WebSockets
469: 
470: ↓
471: 
472: Provider Interfaces
473: 
474: ↓
475: 
476: Frontend Foundation
477: 
478: ↓
479: 
480: Patient Application
481: 
482: ↓
483: 
484: Doctor Portal
485: 
486: ↓
487: 
488: Split Screen
489: 
490: ↓
491: 
492: AI Integration
493: 
494: ↓
495: 
496: Testing
497: 
498: ↓
499: 
500: Documentation
501: 
502: ↓
503: 
504: Polish
505: 
506: Each completed phase becomes the foundation for the next.
507: 
508: ---
509: 
510: # Self-Review Before Completing Any Phase
511: 
512: Before marking a phase complete, review the generated code.
513: 
514: Ask:
515: 
516: Does this compile?
517: 
518: Does it follow the architecture?
519: 
520: Does it duplicate logic?
521: 
522: Does it violate dependency inversion?
523: 
524: Does it expose secrets?
525: 
526: Does it introduce technical debt?
527: 
528: Would another engineer understand this immediately?
529: 
530: If the answer is "no" to any question, improve the implementation before proceeding.
531: 
532: ---
533: 
534: # Refactoring Policy
535: 
536: You are encouraged to refactor previously generated code.
537: 
538: Do not preserve poor code merely because it already exists.
539: 
540: Improve:
541: 
542: Naming
543: 
544: Structure
545: 
546: Abstractions
547: 
548: Documentation
549: 
550: Typing
551: 
552: Reuse
553: 
554: while preserving behaviour.
555: 
556: Avoid unnecessary rewrites.
557: 
558: ---
559: 
560: # Architectural Consistency
561: 
562: Every new feature should resemble existing features.
563: 
564: Examples:
565: 
566: PatientService
567: 
568: DoctorService
569: 
570: ConsentService
571: 
572: should share similar structure.
573: 
574: Repository implementations should feel consistent.
575: 
576: API routes should follow identical conventions.
577: 
578: UI components should expose similar props.
579: 
580: Animations should use the same motion presets.
581: 
582: Consistency is more valuable than cleverness.
583: 
584: ---
585: 
586: # Dependency Rules
587: 
588: Business logic may depend on:
589: 
590: Interfaces
591: 
592: Domain Models
593: 
594: Repositories
595: 
596: Services
597: 
598: Business logic may NOT depend directly on:
599: 
600: OpenAI SDK
601: 
602: Redis Client
603: 
604: SQLAlchemy Sessions
605: 
606: Email SDKs
607: 
608: Storage SDKs
609: 
610: Framework-specific infrastructure
611: 
612: Every infrastructure dependency must be abstracted.
613: 
614: ---
615: 
616: # Code Organization
617: 
618: When creating a new file,
619: 
620: first determine whether an appropriate location already exists.
621: 
622: Avoid creating:
623: 
624: misc/
625: 
626: helpers/
627: 
628: random/
629: 
630: common/
631: 
632: general/
633: 
634: unless explicitly justified.
635: 
636: Folders should communicate purpose.
637: 
638: ---
639: 
640: # Naming Standards
641: 
642: Names should describe intent.
643: 
644: Prefer:
645: 
646: ConsentService
647: 
648: instead of
649: 
650: ConsentManager
651: 
652: Prefer:
653: 
654: PatientRepository
655: 
656: instead of
657: 
658: PatientDatabase
659: 
660: Avoid abbreviations.
661: 
662: Avoid single-letter variables except loop indices.
663: 
664: Medical terminology should remain explicit.
665: 
666: ---
667: 
668: # Documentation Standards
669: 
670: Every public module should include documentation.
671: 
672: Public classes should explain:
673: 
674: Purpose
675: 
676: Responsibilities
677: 
678: Dependencies
679: 
680: Extension points
681: 
682: Complex business rules should include comments explaining why, not merely what.
683: 
684: ---
685: 
686: # Error Handling
687: 
688: Recoverable errors should return structured responses.
689: 
690: Unexpected errors should:
691: 
692: Log details internally.
693: 
694: Return safe messages externally.
695: 
696: Never expose stack traces.
697: 
698: Never leak secrets.
699: 
700: ---
701: 
702: # Logging
703: 
704: Every important operation should generate structured logs.
705: 
706: Include:
707: 
708: Request ID
709: 
710: User ID
711: 
712: Operation
713: 
714: Duration
715: 
716: Result
717: 
718: Logs should support future observability tooling.
719: 
720: ---
721: 
722: # Testing Expectations
723: 
724: Every significant feature should include tests.
725: 
726: Prioritize testing behaviour.
727: 
728: Avoid brittle implementation-specific tests.
729: 
730: Critical workflows should include integration tests.
731: 
732: ---
733: 
734: # UI Expectations
735: 
736: The patient application should never feel like a desktop application squeezed into a small screen.
737: 
738: It should feel native.
739: 
740: The doctor portal should emphasize information density while remaining readable.
741: 
742: Animations should reinforce navigation.
743: 
744: Accessibility should never be sacrificed for aesthetics.
745: 
746: ---
747: 
748: # Mobile Simulation
749: 
750: The PhoneFrame is part of the architecture.
751: 
752: It is not a demo gimmick.
753: 
754: All patient screens should assume a fixed mobile viewport.
755: 
756: Never implement responsive behaviour inside patient screens.
757: 
758: The PhoneFrame is responsible for responsiveness.
759: 
760: ---
761: 
762: # Split-Screen Demonstration
763: 
764: The split-screen mode is a first-class feature.
765: 
766: It should not be implemented as an afterthought.
767: 
768: The demonstration should clearly show:
769: 
770: Doctor requests consent.
771: 
772: ↓
773: 
774: Patient notification appears.
775: 
776: ↓
777: 
778: Patient approves.
779: 
780: ↓
781: 
782: Doctor gains access.
783: 
784: ↓
785: 
786: Consultation proceeds.
787: 
788: ↓
789: 
790: Patient receives updated medical record.
791: 
792: Real-time synchronization is one of the project's defining capabilities.
793: 
794: ---
795: 
796: # AI Integration
797: 
798: AI providers are interchangeable.
799: 
800: Never assume a particular vendor.
801: 
802: The system should continue functioning if an AI provider becomes unavailable.
803: 
804: AI failures should never prevent clinicians from completing documentation.
805: 
806: ---
807: 
808: # Security Expectations
809: 
810: Treat every API as though it will eventually process real medical data.
811: 
812: Validate all inputs.
813: 
814: Authorize every protected request.
815: 
816: Log sensitive operations.
817: 
818: Hash passwords.
819: 
820: Never trust the client.
821: 
822: ---
823: 
824: # Performance Expectations
825: 
826: Optimize for perceived responsiveness.
827: 
828: Prefer:
829: 
830: Skeleton loading.
831: 
832: Optimistic updates.
833: 
834: Incremental rendering.
835: 
836: Caching.
837: 
838: Do not prematurely optimize algorithms unless profiling demonstrates a bottleneck.
839: 
840: ---
841: 
842: # When Requirements Are Ambiguous
843: 
844: If documentation provides sufficient context,
845: 
846: make the smallest reasonable assumption.
847: 
848: Do not invent major features.
849: 
850: If a decision affects architecture,
851: 
852: document the assumption.
853: 
854: If a decision changes user workflows,
855: 
856: stop and request clarification.
857: 
858: ---
859: 
860: # Anti-Patterns To Avoid
861: 
862: Do not:
863: 
864: Embed SQL inside routes.
865: 
866: Place business logic inside React components.
867: 
868: Call AI SDKs directly from services.
869: 
870: Duplicate validation logic.
871: 
872: Duplicate API clients.
873: 
874: Create circular dependencies.
875: 
876: Store secrets in source code.
877: 
878: Use global mutable state unnecessarily.
879: 
880: Create tightly coupled modules.
881: 
882: Bypass provider interfaces.
883: 
884: Hardcode configuration values.
885: 
886: Ignore accessibility.
887: 
888: Ignore loading states.
889: 
890: Ignore error states.
891: 
892: ---
893: 
894: # Repository Completion Checklist
895: 
896: Before declaring the repository complete, verify:
897: 
898: ✓ Docker Compose launches successfully.
899: 
900: ✓ Backend passes health checks.
901: 
902: ✓ Database migrations execute.
903: 
904: ✓ Demo Mode functions.
905: 
906: ✓ JWT authentication functions.
907: 
908: ✓ Patient application operates inside PhoneFrame.
909: 
910: ✓ Doctor portal implements consultation workflow.
911: 
912: ✓ Split-screen demonstration functions.
913: 
914: ✓ Consent workflow updates in real time.
915: 
916: ✓ Existing symptom checker integrates through its provider interface.
917: 
918: ✓ AI providers remain replaceable.
919: 
920: ✓ Notifications synchronize.
921: 
922: ✓ Audit logs are generated.
923: 
924: ✓ Documentation is complete.
925: 
926: ✓ Tests pass.
927: 
928: ✓ No placeholder implementations remain.
929: 
930: ---
931: 
932: # Final Objective
933: 
934: The finished repository should not resemble an AI-generated proof of concept.
935: 
936: It should resemble software produced by a disciplined engineering team following a clear architecture, consistent design system, and modern development practices.
937: 
938: Every file should have a clear purpose.
939: 
940: Every abstraction should justify its existence.
941: 
942: Every feature should contribute to a coherent, maintainable healthcare platform.
943: 
944: # End of Master Generation Prompt

(End of file - total 944 lines)
</content>
```

---

## Assistant (Plan · Kimi · 5.6s)

_Thinking:_

 Now I have a comprehensive understanding of the Mirage project. Let me also check the remaining documentation files and the current state of the repository to understand what already exists.

 

**Tool: read**

**Input:**
```json
{
  "filePath": "/Users/sheltonmutambirwa/Desktop/medic/docs/03_Design_System.md"
}
```

**Output:**
```
<path>/Users/sheltonmutambirwa/Desktop/medic/docs/03_Design_System.md</path>
<type>file</type>
<content>
1: # Mirage
2: # Design System Specification
3: 
4: Version: 1.0
5: 
6: ---
7: 
8: # 1. Design Philosophy
9: 
10: Mirage is a healthcare application.
11: 
12: Healthcare software must inspire confidence before it communicates information.
13: 
14: The interface should therefore feel:
15: 
16: - Calm
17: - Clean
18: - Trustworthy
19: - Modern
20: - Fast
21: - Predictable
22: - Accessible
23: 
24: The visual language should avoid unnecessary decoration while remaining polished enough for public demonstrations.
25: 
26: Animations should support understanding rather than entertain.
27: 
28: Every interaction should reinforce clarity.
29: 
30: ---
31: 
32: # 2. Core Design Principles
33: 
34: The UI follows six principles.
35: 
36: ## Clinical First
37: 
38: Important information should always be visible.
39: 
40: Critical allergies.
41: 
42: Warnings.
43: 
44: Consent status.
45: 
46: Current consultation.
47: 
48: These must never become hidden beneath secondary content.
49: 
50: ---
51: 
52: ## Mobile Native Feel
53: 
54: Although implemented in Next.js, the patient application should feel indistinguishable from a native mobile application.
55: 
56: Users should forget they are using a browser.
57: 
58: Scrolling.
59: 
60: Spacing.
61: 
62: Touch targets.
63: 
64: Animations.
65: 
66: Typography.
67: 
68: Everything should resemble iOS and modern Android applications.
69: 
70: ---
71: 
72: ## Progressive Disclosure
73: 
74: Do not overwhelm users.
75: 
76: Show summaries first.
77: 
78: Expand into detail only when requested.
79: 
80: Example:
81: 
82: Timeline
83: 
84: ↓
85: 
86: Visit Card
87: 
88: ↓
89: 
90: Expanded Visit
91: 
92: ↓
93: 
94: Diagnosis
95: 
96: ↓
97: 
98: Medication
99: 
100: ↓
101: 
102: Clinical Notes
103: 
104: ---
105: 
106: ## Consistency
107: 
108: Every card.
109: 
110: Every button.
111: 
112: Every sheet.
113: 
114: Every dialog.
115: 
116: Every navigation pattern.
117: 
118: Should follow identical rules.
119: 
120: Consistency reduces cognitive load.
121: 
122: ---
123: 
124: ## Immediate Feedback
125: 
126: Every user interaction should provide feedback.
127: 
128: Button
129: 
130: ↓
131: 
132: Pressed
133: 
134: ↓
135: 
136: Loading
137: 
138: ↓
139: 
140: Completed
141: 
142: ↓
143: 
144: Success
145: 
146: Never leave users wondering whether something happened.
147: 
148: ---
149: 
150: ## Motion With Purpose
151: 
152: Animations communicate:
153: 
154: Hierarchy
155: 
156: State
157: 
158: Navigation
159: 
160: Context
161: 
162: Never animate simply because animation is possible.
163: 
164: ---
165: 
166: # 3. Visual Identity
167: 
168: The visual identity should communicate modern digital healthcare.
169: 
170: Suggested keywords:
171: 
172: Minimal
173: 
174: Premium
175: 
176: Professional
177: 
178: Human
179: 
180: Trustworthy
181: 
182: Accessible
183: 
184: Soft
185: 
186: Lightweight
187: 
188: ---
189: 
190: # 4. Color System
191: 
192: The application should define semantic colors rather than feature-specific colors.
193: 
194: ## Primary
195: 
196: Primary brand color.
197: 
198: Used for:
199: 
200: Primary buttons
201: 
202: Links
203: 
204: Highlights
205: 
206: Selected navigation
207: 
208: Progress
209: 
210: ---
211: 
212: ## Secondary
213: 
214: Surface accents.
215: 
216: Cards.
217: 
218: Inputs.
219: 
220: Backgrounds.
221: 
222: ---
223: 
224: ## Accent
225: 
226: Used sparingly.
227: 
228: AI highlights.
229: 
230: Interactive elements.
231: 
232: Illustrations.
233: 
234: ---
235: 
236: ## Success
237: 
238: Clinical confirmation.
239: 
240: Approved consent.
241: 
242: Completed consultation.
243: 
244: Successful updates.
245: 
246: ---
247: 
248: ## Warning
249: 
250: Expiring consent.
251: 
252: Medication warnings.
253: 
254: Potential risks.
255: 
256: ---
257: 
258: ## Destructive
259: 
260: Denied consent.
261: 
262: Errors.
263: 
264: Delete actions.
265: 
266: Critical failures.
267: 
268: ---
269: 
270: ## Information
271: 
272: General informational banners.
273: 
274: Help.
275: 
276: Guidance.
277: 
278: ---
279: 
280: ## Neutral
281: 
282: Text.
283: 
284: Borders.
285: 
286: Backgrounds.
287: 
288: Dividers.
289: 
290: Cards.
291: 
292: ---
293: 
294: Never hardcode colors.
295: 
296: Everything should reference design tokens.
297: 
298: ---
299: 
300: # 5. Typography
301: 
302: Typography should prioritize readability.
303: 
304: Suggested hierarchy:
305: 
306: Display
307: 
308: 32–36px
309: 
310: Page Title
311: 
312: 28px
313: 
314: Section Title
315: 
316: 22px
317: 
318: Card Title
319: 
320: 18px
321: 
322: Body
323: 
324: 14–16px
325: 
326: Caption
327: 
328: 12px
329: 
330: Micro Labels
331: 
332: 10–11px
333: 
334: Line heights should prioritize readability.
335: 
336: Avoid dense paragraphs.
337: 
338: ---
339: 
340: # 6. Iconography
341: 
342: Use Lucide icons consistently.
343: 
344: Icons should communicate meaning rather than decoration.
345: 
346: Examples:
347: 
348: Patient
349: 
350: Doctor
351: 
352: Hospital
353: 
354: Medication
355: 
356: Timeline
357: 
358: AI
359: 
360: Notification
361: 
362: Settings
363: 
364: Security
365: 
366: Search
367: 
368: Consent
369: 
370: Laboratory
371: 
372: Diagnosis
373: 
374: Documentation
375: 
376: Avoid mixing icon libraries.
377: 
378: ---
379: 
380: # 7. Spacing Scale
381: 
382: Spacing should use a fixed scale.
383: 
384: 4
385: 
386: 8
387: 
388: 12
389: 
390: 16
391: 
392: 20
393: 
394: 24
395: 
396: 32
397: 
398: 40
399: 
400: 48
401: 
402: 64
403: 
404: Avoid arbitrary spacing values.
405: 
406: ---
407: 
408: # 8. Radius Scale
409: 
410: Consistent rounded corners improve familiarity.
411: 
412: Buttons
413: 
414: Full
415: 
416: Cards
417: 
418: 16px
419: 
420: Sheets
421: 
422: 32px
423: 
424: Inputs
425: 
426: 16px
427: 
428: Dialogs
429: 
430: 24px
431: 
432: Phone Frame
433: 
434: 44px+
435: 
436: ---
437: 
438: # 9. Elevation
439: 
440: Use elevation sparingly.
441: 
442: Level 0
443: 
444: Background
445: 
446: Level 1
447: 
448: Cards
449: 
450: Level 2
451: 
452: Floating buttons
453: 
454: Level 3
455: 
456: Bottom sheets
457: 
458: Level 4
459: 
460: Dialogs
461: 
462: Level 5
463: 
464: Notifications
465: 
466: Shadow intensity should remain subtle.
467: 
468: ---
469: 
470: # 10. Glass Morphism
471: 
472: Glass surfaces are a defining characteristic of Mirage.
473: 
474: Used for:
475: 
476: Bottom Navigation
477: 
478: Floating Panels
479: 
480: Bottom Sheets
481: 
482: Dialogs
483: 
484: Status Cards
485: 
486: Floating Actions
487: 
488: Properties:
489: 
490: Translucent background
491: 
492: Backdrop blur
493: 
494: Soft border
495: 
496: Subtle shadow
497: 
498: Never reduce readability.
499: 
500: Glass should support content rather than obscure it.
501: 
502: ---
503: 
504: # 11. Motion System
505: 
506: All animations should use Framer Motion.
507: 
508: Default spring:
509: 
510: ```
511: 
512: stiffness: 380
513: 
514: damping: 32
515: 
516: ```
517: 
518: These values should be reused throughout the application.
519: 
520: Consistency is more important than novelty.
521: 
522: ---
523: 
524: # 12. Animation Categories
525: 
526: Navigation
527: 
528: Fade + slight slide.
529: 
530: Bottom Sheets
531: 
532: Slide upward.
533: 
534: Dialogs
535: 
536: Fade + scale.
537: 
538: Cards
539: 
540: Fade.
541: 
542: Buttons
543: 
544: Scale on press.
545: 
546: Notifications
547: 
548: Slide from top.
549: 
550: Timeline
551: 
552: Progressive reveal.
553: 
554: Never animate large layout shifts.
555: 
556: ---
557: 
558: # 13. Timing
559: 
560: Instant
561: 
562: 100ms
563: 
564: Fast
565: 
566: 200ms
567: 
568: Standard
569: 
570: 300ms
571: 
572: Slow
573: 
574: 450ms
575: 
576: Background
577: 
578: 800ms+
579: 
580: Users should never wait on animations.
581: 
582: ---
583: 
584: # 14. Accessibility
585: 
586: Minimum touch target:
587: 
588: 44 × 44
589: 
590: Minimum contrast:
591: 
592: WCAG AA
593: 
594: Focus indicators:
595: 
596: Always visible.
597: 
598: Reduced motion:
599: 
600: Supported.
601: 
602: Animations should disable gracefully.
603: 
604: ---
605: 
606: # 15. Component Design Rules
607: 
608: Every component should expose:
609: 
610: Variant
611: 
612: Size
613: 
614: Disabled
615: 
616: Loading
617: 
618: Icon
619: 
620: Accessibility label
621: 
622: Class overrides
623: 
624: Avoid creating one-off components.
625: 
626: Everything should be reusable.
627: 
628: # 16. PhoneFrame Component
629: 
630: The PhoneFrame is the foundation of the patient application.
631: 
632: It is not decorative.
633: 
634: It defines the rendering environment for every patient screen.
635: 
636: Every patient page must render inside PhoneFrame.
637: 
638: ---
639: 
640: ## Responsibilities
641: 
642: The PhoneFrame should:
643: 
644: - Simulate a modern smartphone.
645: - Maintain a fixed viewport.
646: - Prevent browser resizing from affecting layouts.
647: - Provide realistic safe areas.
648: - Render the decorative device frame.
649: - Provide an authentic mobile experience inside the browser.
650: 
651: ---
652: 
653: ## Dimensions
654: 
655: Large screens
656: 
657: ```
658: 370px × 800px
659: ```
660: 
661: Smaller laptops
662: 
663: ```
664: 350px × 760px
665: ```
666: 
667: These dimensions remain fixed.
668: 
669: The application scales around the frame rather than resizing its internal layout.
670: 
671: ---
672: 
673: ## Physical Device Elements
674: 
675: The frame should include:
676: 
677: Rounded bezel
678: 
679: Side buttons
680: 
681: Speaker notch
682: 
683: Camera cut-out
684: 
685: Glass reflection
686: 
687: Soft shadow
688: 
689: Optional home indicator
690: 
691: These elements are decorative and should not interfere with interaction.
692: 
693: ---
694: 
695: ## Screen Container
696: 
697: The screen container is the only scrollable region.
698: 
699: ```
700: PhoneFrame
701: 
702: ├── Device Frame
703: 
704: ├── Status Bar
705: 
706: ├── Safe Area
707: 
708: ├── Application
709: 
710: └── Bottom Navigation
711: ```
712: 
713: Content must never overflow beyond the rounded screen boundaries.
714: 
715: ---
716: 
717: # 17. Status Bar
718: 
719: The patient application always displays a simulated status bar.
720: 
721: Contents:
722: 
723: Time
724: 
725: Signal
726: 
727: 5G
728: 
729: Battery
730: 
731: Camera notch
732: 
733: Values remain static during the demo.
734: 
735: The goal is realism rather than device integration.
736: 
737: ---
738: 
739: # 18. Bottom Navigation
740: 
741: The bottom navigation remains persistent.
742: 
743: Recommended tabs:
744: 
745: Home
746: 
747: Timeline
748: 
749: Symptoms
750: 
751: Notifications
752: 
753: Profile
754: 
755: ---
756: 
757: Requirements
758: 
759: Glassmorphism background.
760: 
761: Blur.
762: 
763: Rounded edges.
764: 
765: Animated active indicator.
766: 
767: Touch-friendly spacing.
768: 
769: Safe area padding.
770: 
771: Navigation transitions should feel native.
772: 
773: ---
774: 
775: # 19. Header Pattern
776: 
777: Each screen begins with a consistent header.
778: 
779: Header includes:
780: 
781: Title
782: 
783: Optional subtitle
784: 
785: Back button
786: 
787: Optional action
788: 
789: Search (where applicable)
790: 
791: Headers should never exceed two lines.
792: 
793: ---
794: 
795: # 20. Card Component
796: 
797: Cards are the primary information container.
798: 
799: Every card should support:
800: 
801: Variant
802: 
803: Size
804: 
805: Leading icon
806: 
807: Trailing action
808: 
809: Loading state
810: 
811: Selected state
812: 
813: Disabled state
814: 
815: Hover state (desktop)
816: 
817: Cards should animate subtly when entering the screen.
818: 
819: ---
820: 
821: Card variants:
822: 
823: Information
824: 
825: Medical Record
826: 
827: Timeline
828: 
829: Notification
830: 
831: Consent
832: 
833: AI Suggestion
834: 
835: Alert
836: 
837: Statistic
838: 
839: ---
840: 
841: # 21. Button Component
842: 
843: Supported variants:
844: 
845: Primary
846: 
847: Secondary
848: 
849: Ghost
850: 
851: Outline
852: 
853: Danger
854: 
855: Success
856: 
857: Text
858: 
859: Sizes:
860: 
861: Small
862: 
863: Medium
864: 
865: Large
866: 
867: Buttons should support:
868: 
869: Loading
870: 
871: Disabled
872: 
873: Icons
874: 
875: Full width
876: 
877: Rounded
878: 
879: Accessibility labels
880: 
881: Loading buttons replace the label with a spinner.
882: 
883: ---
884: 
885: # 22. Input Components
886: 
887: Supported inputs:
888: 
889: Text
890: 
891: Password
892: 
893: Search
894: 
895: Email
896: 
897: Phone
898: 
899: Date
900: 
901: Select
902: 
903: Multi-select
904: 
905: Textarea
906: 
907: Medical Notes
908: 
909: Every input includes:
910: 
911: Label
912: 
913: Placeholder
914: 
915: Validation
916: 
917: Helper text
918: 
919: Error state
920: 
921: Success state
922: 
923: Disabled state
924: 
925: ---
926: 
927: Search inputs should debounce requests.
928: 
929: ---
930: 
931: # 23. Search Experience
932: 
933: Patient search should feel instantaneous.
934: 
935: Features:
936: 
937: Debounced typing
938: 
939: Keyboard navigation
940: 
941: Highlight matches
942: 
943: Empty state
944: 
945: Loading indicator
946: 
947: Recent searches
948: 
949: Duplicate patient differentiation
950: 
951: ---
952: 
953: # 24. Timeline Component
954: 
955: The medical timeline is central to Mirage.
956: 
957: Each entry displays:
958: 
959: Date
960: 
961: Facility
962: 
963: Doctor
964: 
965: Diagnosis
966: 
967: Medication
968: 
969: Summary
970: 
971: Expandable indicator
972: 
973: ---
974: 
975: Expanding a visit reveals:
976: 
977: Clinical notes
978: 
979: Medications
980: 
981: Investigations
982: 
983: Attachments
984: 
985: AI summary
986: 
987: Timeline animations should preserve orientation.
988: 
989: The user should never lose their place.
990: 
991: ---
992: 
993: # 25. Consent Card
994: 
995: Displays:
996: 
997: Doctor
998: 
999: Facility
1000: 
1001: Registration Number
1002: 
1003: Purpose
1004: 
1005: Requested Scope
1006: 
1007: Expiration
1008: 
1009: Buttons:
1010: 
1011: Approve
1012: 
1013: Deny
1014: 
1015: Animation:
1016: 
1017: Card slides into view.
1018: 
1019: Approval immediately updates UI.
1020: 
1021: ---
1022: 
1023: # 26. Notification Card
1024: 
1025: Supports:
1026: 
1027: Unread indicator
1028: 
1029: Category icon
1030: 
1031: Timestamp
1032: 
1033: Title
1034: 
1035: Body
1036: 
1037: Quick actions
1038: 
1039: Notification categories:
1040: 
1041: Consent
1042: 
1043: Medical Record
1044: 
1045: Reminder
1046: 
1047: System
1048: 
1049: AI
1050: 
1051: ---
1052: 
1053: # 27. AI Conversation
1054: 
1055: The AI consultation resembles modern messaging applications.
1056: 
1057: Messages include:
1058: 
1059: Speaker
1060: 
1061: Timestamp
1062: 
1063: Avatar
1064: 
1065: Markdown support
1066: 
1067: Code blocks disabled
1068: 
1069: Medical references highlighted
1070: 
1071: Doctor messages align right.
1072: 
1073: AI aligns left.
1074: 
1075: Typing indicators supported.
1076: 
1077: Streaming responses supported.
1078: 
1079: ---
1080: 
1081: Suggested actions appear beneath AI responses.
1082: 
1083: Examples:
1084: 
1085: Ask Follow-up
1086: 
1087: Explain
1088: 
1089: Accept
1090: 
1091: Ignore
1092: 
1093: Generate Summary
1094: 
1095: ---
1096: 
1097: # 28. Differential Diagnosis Card
1098: 
1099: Displays:
1100: 
1101: Diagnosis
1102: 
1103: Confidence
1104: 
1105: Evidence
1106: 
1107: Contradictory Findings
1108: 
1109: Suggested Tests
1110: 
1111: Medication Risks
1112: 
1113: Expandable reasoning
1114: 
1115: Doctors can:
1116: 
1117: Accept
1118: 
1119: Ignore
1120: 
1121: Edit
1122: 
1123: Compare
1124: 
1125: Nothing is committed automatically.
1126: 
1127: ---
1128: 
1129: # 29. Clinical Summary Editor
1130: 
1131: The generated summary appears inside editable sections.
1132: 
1133: Recommended layout:
1134: 
1135: SOAP
1136: 
1137: Subjective
1138: 
1139: Objective
1140: 
1141: Assessment
1142: 
1143: Plan
1144: 
1145: Rich text editing is unnecessary for MVP.
1146: 
1147: Plain structured inputs are preferred.
1148: 
1149: ---
1150: 
1151: # 30. Bottom Sheets
1152: 
1153: Bottom sheets should be used instead of full-screen dialogs where practical.
1154: 
1155: Characteristics:
1156: 
1157: Rounded top corners
1158: 
1159: Blurred background
1160: 
1161: Drag handle
1162: 
1163: Spring animation
1164: 
1165: Dismiss gesture
1166: 
1167: Tap outside to close (where safe)
1168: 
1169: Examples:
1170: 
1171: Patient Details
1172: 
1173: Notifications
1174: 
1175: Consent
1176: 
1177: Visit Preview
1178: 
1179: Medication
1180: 
1181: ---
1182: 
1183: # 31. Dialogs
1184: 
1185: Dialogs should interrupt only high-risk actions.
1186: 
1187: Examples:
1188: 
1189: Delete
1190: 
1191: Logout
1192: 
1193: Cancel Consultation
1194: 
1195: Discard Changes
1196: 
1197: Permission Errors
1198: 
1199: Dialogs should never exceed the width of the phone frame.
1200: 
1201: ---
1202: 
1203: # 32. Floating Action Button
1204: 
1205: Used sparingly.
1206: 
1207: Examples:
1208: 
1209: Start Assessment
1210: 
1211: New Consultation
1212: 
1213: Quick Search
1214: 
1215: Scroll to Top
1216: 
1217: Should remain above scrolling content.
1218: 
1219: ---
1220: 
1221: # 33. Loading Components
1222: 
1223: Avoid blank screens.
1224: 
1225: Use:
1226: 
1227: Skeleton cards
1228: 
1229: Skeleton timeline
1230: 
1231: Skeleton profile
1232: 
1233: Animated shimmer
1234: 
1235: Progress indicators
1236: 
1237: Loading indicators should resemble the final layout.
1238: 
1239: ---
1240: 
1241: # 34. Empty States
1242: 
1243: Every feature defines an empty state.
1244: 
1245: Examples:
1246: 
1247: No notifications.
1248: 
1249: No visits.
1250: 
1251: No consent requests.
1252: 
1253: No AI sessions.
1254: 
1255: Each empty state should include:
1256: 
1257: Illustration or icon
1258: 
1259: Explanation
1260: 
1261: Primary action
1262: 
1263: ---
1264: 
1265: # 35. Error States
1266: 
1267: Every feature defines a recoverable error state.
1268: 
1269: Display:
1270: 
1271: Friendly message
1272: 
1273: Retry button
1274: 
1275: Support text (optional)
1276: 
1277: Avoid technical language.
1278: 
1279: Never expose stack traces.
1280: 
1281: ---
1282: 
1283: # 36. Success States
1284: 
1285: Success feedback should be immediate.
1286: 
1287: Examples:
1288: 
1289: Consent approved
1290: 
1291: Record updated
1292: 
1293: Assessment submitted
1294: 
1295: Consultation completed
1296: 
1297: Success indicators should combine:
1298: 
1299: Icon
1300: 
1301: Color
1302: 
1303: Short confirmation message
1304: 
1305: Optional animation
1306: 
1307: ---
1308: 
1309: # 37. Toast Notifications
1310: 
1311: Transient events should appear as toast notifications.
1312: 
1313: Examples:
1314: 
1315: Saved
1316: 
1317: Updated
1318: 
1319: Connected
1320: 
1321: Disconnected
1322: 
1323: New notification
1324: 
1325: Consent approved
1326: 
1327: Position:
1328: 
1329: Top of patient frame
1330: 
1331: Top-right of doctor portal
1332: 
1333: Duration:
1334: 
1335: 3–5 seconds
1336: 
1337: User-dismissible.
1338: 
1339: ---
1340: 
1341: # 38. Doctor Dashboard Components
1342: 
1343: The dashboard is composed of reusable widgets.
1344: 
1345: Examples:
1346: 
1347: Today's Queue
1348: 
1349: Recent Patients
1350: 
1351: Pending Consent
1352: 
1353: AI Activity
1354: 
1355: System Status
1356: 
1357: Quick Actions
1358: 
1359: Statistics
1360: 
1361: Each widget should be independently reusable and independently loadable.
1362: 
1363: ---
1364: 
1365: # 39. Split-Screen Demonstration Layout
1366: 
1367: The preferred demonstration mode is split-screen.
1368: 
1369: ```
1370: --------------------------------------------------------------
1371: 
1372: Patient Phone         Doctor Dashboard
1373: 
1374: ┌──────────────┐      ┌────────────────────────────────────┐
1375: │              │      │                                    │
1376: │              │      │                                    │
1377: │              │      │                                    │
1378: │              │      │                                    │
1379: │              │      │                                    │
1380: └──────────────┘      └────────────────────────────────────┘
1381: 
1382: --------------------------------------------------------------
1383: ```
1384: 
1385: Real-time updates should be visible on both sides simultaneously.
1386: 
1387: This mode should be optimized for presentations, recordings, judging sessions, and stakeholder demonstrations.
1388: 
1389: ---
1390: 
1391: # 40. Component Definition of Done
1392: 
1393: Every reusable component should satisfy the following criteria:
1394: 
1395: - Fully typed with TypeScript.
1396: - Accessible (ARIA, keyboard navigation, focus management).
1397: - Responsive where appropriate.
1398: - Supports loading, error, and disabled states.
1399: - Exposes composable props instead of feature-specific logic.
1400: - Includes documentation/examples for future contributors.
1401: - Avoids embedding business logic.
1402: - Is visually consistent with the design tokens and motion guidelines.
1403: 
1404: Reusable components should favor composition over inheritance and remain framework-agnostic wherever practical.

(End of file - total 1404 lines)
</content>
```

**Tool: read**

**Input:**
```json
{
  "filePath": "/Users/sheltonmutambirwa/Desktop/medic/docs/10_UI_Screen_Specification.md"
}
```

**Output:**
```
<path>/Users/sheltonmutambirwa/Desktop/medic/docs/10_UI_Screen_Specification.md</path>
<type>file</type>
<content>
1: # Mirage
2: # UI Screen Specification
3: 
4: Version: 2.0
5: 
6: ---
7: 
8: # Purpose
9: 
10: This document defines every user interface within Mirage.
11: 
12: Unlike the Design System, which specifies visual language and reusable components, this document specifies the application's concrete screens exactly as they appear in the approved wireframes.
13: 
14: It is the implementation guide for the frontend.
15: 
16: ---
17: 
18: # Primary Source of Truth
19: 
20: The canonical reference for every screen is:
21: 
22: docs/wireframes.html
23: 
24: The HTML wireframes represent the approved MVP design.
25: 
26: They define:
27: 
28: - Screen order
29: - Navigation
30: - Layout
31: - Information hierarchy
32: - Component placement
33: - User interaction flow
34: - Demo presentation
35: 
36: This document extends those wireframes by defining:
37: 
38: - React component hierarchy
39: - API dependencies
40: - Backend integration
41: - State management
42: - Real-time synchronization
43: - Loading states
44: - Empty states
45: - Error handling
46: - Accessibility requirements
47: - Acceptance criteria
48: 
49: If this document conflicts with the wireframes regarding visual layout, the wireframes take precedence.
50: 
51: ---
52: 
53: # Relationship to Other Documentation
54: 
55: This document should be read after:
56: 
57: 01_Product_Requirements_Document.md
58: 
59: 02_Technical_Architecture.md
60: 
61: 03_Design_System.md
62: 
63: 05_API_Contract.md
64: 
65: 06_Database_Schema.md
66: 
67: The responsibilities are divided as follows:
68: 
69: Product Requirements
70: 
71: Defines WHAT the product should accomplish.
72: 
73: Technical Architecture
74: 
75: Defines HOW the system is implemented.
76: 
77: Design System
78: 
79: Defines HOW components should look and behave.
80: 
81: Wireframes
82: 
83: Define WHERE everything appears.
84: 
85: This document
86: 
87: Defines HOW every screen should be implemented.
88: 
89: ---
90: 
91: # Screen Fidelity Requirements
92: 
93: The generated application should closely match the supplied wireframes.
94: 
95: The coding assistant may improve:
96: 
97: ✓ Typography
98: 
99: ✓ Iconography
100: 
101: ✓ Animation quality
102: 
103: ✓ Spacing consistency
104: 
105: ✓ Accessibility
106: 
107: ✓ Responsiveness
108: 
109: ✓ Component reuse
110: 
111: The coding assistant must NOT change:
112: 
113: ✗ Screen order
114: 
115: ✗ Navigation
116: 
117: ✗ Information hierarchy
118: 
119: ✗ User workflow
120: 
121: ✗ Screen purpose
122: 
123: ✗ Core interaction patterns
124: 
125: ---
126: 
127: # Demo Layout
128: 
129: The primary demonstration environment consists of two synchronized applications.
130: 
131: Left Panel
132: 
133: Patient Application
134: 
135: Rendered inside the PhoneFrame component.
136: 
137: Right Panel
138: 
139: Doctor Portal
140: 
141: Desktop dashboard.
142: 
143: The applications should communicate exclusively through the backend using WebSockets.
144: 
145: The frontend should never directly synchronize state between the two panels.
146: 
147: ---
148: 
149: # Patient Application
150: 
151: The patient application is a mobile-first web experience.
152: 
153: Every patient screen must render inside the PhoneFrame described in:
154: 
155: 03_Design_System.md
156: 
157: The application should never detect browser width.
158: 
159: Instead, the PhoneFrame provides a fixed viewport that scales appropriately.
160: 
161: ---
162: 
163: # Doctor Portal
164: 
165: The doctor portal is desktop-first.
166: 
167: Unlike the patient application, it should maximize information density.
168: 
169: The doctor portal should support:
170: 
171: • Multi-column layouts
172: 
173: • Keyboard navigation
174: 
175: • Large datasets
176: 
177: • Simultaneous patient context
178: 
179: ---
180: 
181: # Navigation Model
182: 
183: Patient Navigation
184: 
185: The wireframes define the canonical navigation sequence.
186: 
187: Screens should appear in the exact order shown in:
188: 
189: docs/wireframes.html
190: 
191: Additional navigation should only exist where required for implementation.
192: 
193: ---
194: 
195: Doctor Navigation
196: 
197: Primary navigation should remain persistent.
198: 
199: Recommended sections:
200: 
201: • Dashboard
202: 
203: • Patients
204: 
205: • Consultation
206: 
207: • Notifications
208: 
209: • Settings
210: 
211: Navigation should never interrupt an active consultation.
212: 
213: ---
214: 
215: # Shared Component Library
216: 
217: Every screen should reuse components whenever possible.
218: 
219: Examples include:
220: 
221: PatientCard
222: 
223: MedicalRecordCard
224: 
225: ConsentCard
226: 
227: NotificationCard
228: 
229: TimelineEvent
230: 
231: DiagnosisCard
232: 
233: VitalSignsCard
234: 
235: PrescriptionCard
236: 
237: BottomNavigation
238: 
239: TopAppBar
240: 
241: SearchInput
242: 
243: PrimaryButton
244: 
245: SecondaryButton
246: 
247: StatusBadge
248: 
249: LoadingSkeleton
250: 
251: EmptyState
252: 
253: ErrorState
254: 
255: ConfirmationDialog
256: 
257: BottomSheet
258: 
259: These components should be implemented once and reused throughout the application.
260: 
261: ---
262: 
263: # API Integration Principles
264: 
265: No React component should call the backend directly.
266: 
267: Communication should follow this pattern:
268: 
269: Screen
270: 
271: ↓
272: 
273: Feature Hook
274: 
275: ↓
276: 
277: Service Layer
278: 
279: ↓
280: 
281: Typed API Client
282: 
283: ↓
284: 
285: FastAPI Backend
286: 
287: ↓
288: 
289: Repository
290: 
291: ↓
292: 
293: Database
294: 
295: All API requests should use React Query.
296: 
297: ---
298: 
299: # Real-Time Updates
300: 
301: Real-time communication should occur exclusively through WebSockets.
302: 
303: The UI should subscribe to events rather than poll for updates.
304: 
305: Expected events include:
306: 
307: Consent Requested
308: 
309: Consent Approved
310: 
311: Consent Denied
312: 
313: Consultation Started
314: 
315: Consultation Completed
316: 
317: Timeline Updated
318: 
319: Medical Record Updated
320: 
321: Notification Created
322: 
323: Notification Read
324: 
325: ---
326: 
327: # Standard Screen Template
328: 
329: Every screen described in this document follows the same specification.
330: 
331: Each screen includes:
332: 
333: 1. Purpose
334: 
335: 2. Wireframe Reference
336: 
337: 3. Layout
338: 
339: 4. Component Hierarchy
340: 
341: 5. API Dependencies
342: 
343: 6. WebSocket Events
344: 
345: 7. User Actions
346: 
347: 8. Loading Behaviour
348: 
349: 9. Empty State
350: 
351: 10. Error State
352: 
353: 11. Accessibility
354: 
355: 12. Acceptance Criteria
356: 
357: Every implementation should satisfy every acceptance criterion before the screen is considered complete.
358: 
359: ---
360: 
361: # Screen Numbering
362: 
363: Screens are documented in the exact order presented by the wireframes.
364: 
365: Patient Application
366: 
367: P1
368: 
369: P2
370: 
371: P3
372: 
373: ...
374: 
375: Doctor Portal
376: 
377: D1
378: 
379: D2
380: 
381: D3
382: 
383: ...
384: 
385: This numbering should be preserved throughout implementation, testing, and future documentation.
386: 
387: ---
388: 
389: # Implementation Philosophy
390: 
391: The frontend should be viewed as an implementation of the approved wireframes rather than a reinterpretation of them.
392: 
393: Where implementation decisions are required, choose the option that best preserves the intent of the supplied prototype while maintaining consistency with the project's architecture and design system.
394: 
395: # End of Part 1
396: # Patient Application
397: 
398: The patient application is the mobile-facing experience of Mirage.
399: 
400: All patient screens must:
401: 
402: - Render inside the PhoneFrame component.
403: - Follow the layouts defined in `docs/wireframes.html`.
404: - Reuse components from the Design System.
405: - Consume backend data exclusively through the typed API layer.
406: - Synchronize with the backend through WebSockets where applicable.
407: 
408: ---
409: 
410: # P1 — Home Dashboard
411: 
412: ## Wireframe Reference
413: 
414: Source:
415: 
416: docs/wireframes.html
417: 
418: Screen:
419: 
420: Patient Application → Home Dashboard
421: 
422: This is the default landing page after authentication.
423: 
424: ---
425: 
426: ## Purpose
427: 
428: The Home Dashboard gives patients immediate visibility into:
429: 
430: - Current health status
431: - Recent consultations
432: - Outstanding actions
433: - Quick access to core features
434: 
435: This screen should minimize cognitive load while surfacing the most important information first.
436: 
437: ---
438: 
439: ## Layout
440: 
441: The implementation should preserve the visual hierarchy defined in the wireframe.
442: 
443: Top to bottom:
444: 
445: 1. Greeting & Profile Summary
446: 2. Health Summary Card
447: 3. Quick Actions
448: 4. Recent Consultation Card
449: 5. Active Consent Requests (if any)
450: 6. Recent Notifications Preview
451: 7. Bottom Navigation
452: 
453: The order should not change.
454: 
455: ---
456: 
457: ## Component Hierarchy
458: 
459: ```
460: PatientHomeScreen
461: 
462: ├── AppHeader
463: │   ├── Greeting
464: │   ├── ProfileAvatar
465: │   └── NotificationButton
466: │
467: ├── HealthSummaryCard
468: │
469: ├── QuickActionsGrid
470: │   ├── AI Symptom Check
471: │   ├── My Health Record
472: │   ├── Notifications
473: │   └── Profile
474: │
475: ├── RecentVisitCard
476: │
477: ├── ActiveConsentCard
478: │
479: ├── NotificationPreviewList
480: │
481: └── BottomNavigation
482: ```
483: 
484: Every section should be independently reusable.
485: 
486: ---
487: 
488: ## API Dependencies
489: 
490: GET /patients/me
491: 
492: GET /patients/me/summary
493: 
494: GET /consultations/recent
495: 
496: GET /consent/active
497: 
498: GET /notifications
499: 
500: ---
501: 
502: ## WebSocket Events
503: 
504: Subscribe:
505: 
506: NotificationCreated
507: 
508: ConsentRequested
509: 
510: ConsultationCompleted
511: 
512: MedicalRecordUpdated
513: 
514: TimelineUpdated
515: 
516: These events should update only the affected widgets.
517: 
518: The entire page should not reload.
519: 
520: ---
521: 
522: ## User Actions
523: 
524: Available interactions include:
525: 
526: - Open AI Symptom Checker
527: - View Health Record
528: - Open Consultation History
529: - Review Consent Request
530: - Open Notifications
531: - Navigate to Profile
532: 
533: Every card should be tappable.
534: 
535: ---
536: 
537: ## Loading Behaviour
538: 
539: Display:
540: 
541: - Skeleton header
542: - Skeleton summary card
543: - Skeleton quick actions
544: - Skeleton cards for consultations and notifications
545: 
546: Navigation should remain available while content loads.
547: 
548: ---
549: 
550: ## Empty State
551: 
552: Recent consultations:
553: 
554: "No consultations yet."
555: 
556: Notifications:
557: 
558: "You're all caught up."
559: 
560: Consent:
561: 
562: "No active consent requests."
563: 
564: ---
565: 
566: ## Error State
567: 
568: If a widget fails to load:
569: 
570: Display an inline error with:
571: 
572: - Retry button
573: 
574: Do not fail the entire dashboard because one widget fails.
575: 
576: ---
577: 
578: ## Accessibility
579: 
580: Support:
581: 
582: - Screen readers
583: - Minimum 44px touch targets
584: - VoiceOver labels
585: - Keyboard navigation (desktop demo)
586: - Dynamic text scaling where practical
587: 
588: ---
589: 
590: ## Acceptance Criteria
591: 
592: ✓ Dashboard matches the wireframe layout.
593: 
594: ✓ Widgets update independently.
595: 
596: ✓ Notification badge updates in real time.
597: 
598: ✓ Active consent appears immediately after doctor request.
599: 
600: ✓ No full-page refresh required.
601: 
602: ---
603: 
604: # P2 — Consent Request
605: 
606: ## Wireframe Reference
607: 
608: Source:
609: 
610: docs/wireframes.html
611: 
612: Screen:
613: 
614: Patient Application → Consent Request
615: 
616: ---
617: 
618: ## Purpose
619: 
620: Allow the patient to review and respond to a doctor's request for access to their medical information.
621: 
622: This is the most security-sensitive interaction in the patient application.
623: 
624: The patient must clearly understand:
625: 
626: - Who is requesting access
627: - Why access is requested
628: - What information will be shared
629: - How long access remains valid
630: 
631: ---
632: 
633: ## Layout
634: 
635: Follow the supplied wireframe.
636: 
637: Expected sections:
638: 
639: 1. Doctor Information
640: 2. Facility Information
641: 3. Consultation Reason
642: 4. Requested Data Categories
643: 5. Expiration Time
644: 6. Approve Button
645: 7. Decline Button
646: 
647: Buttons should remain fixed near the bottom of the viewport.
648: 
649: ---
650: 
651: ## Component Hierarchy
652: 
653: ```
654: ConsentScreen
655: 
656: ├── Header
657: │
658: ├── DoctorCard
659: │
660: ├── FacilityCard
661: │
662: ├── ConsentSummary
663: │
664: ├── SharedDataList
665: │
666: ├── ExpirationBanner
667: │
668: ├── ConsentActions
669: │   ├── ApproveButton
670: │   └── DeclineButton
671: │
672: └── BottomNavigation
673: ```
674: 
675: ---
676: 
677: ## API Dependencies
678: 
679: GET /consent/{id}
680: 
681: POST /consent/{id}/approve
682: 
683: POST /consent/{id}/deny
684: 
685: ---
686: 
687: ## WebSocket Events
688: 
689: Receive:
690: 
691: ConsentRequested
692: 
693: Send:
694: 
695: ConsentApproved
696: 
697: ConsentDenied
698: 
699: The doctor's dashboard should update immediately after approval or denial.
700: 
701: ---
702: 
703: ## User Actions
704: 
705: Patient may:
706: 
707: - Read consent details
708: - Expand shared data categories
709: - Approve request
710: - Decline request
711: 
712: Approval should require explicit confirmation before submission.
713: 
714: ---
715: 
716: ## Loading Behaviour
717: 
718: Display skeletons for:
719: 
720: - Doctor information
721: - Facility information
722: - Requested data
723: - Action buttons (disabled)
724: 
725: ---
726: 
727: ## Empty State
728: 
729: If the consent has expired before opening:
730: 
731: "This request has expired."
732: 
733: Provide a button to return to the dashboard.
734: 
735: ---
736: 
737: ## Error State
738: 
739: If approval fails:
740: 
741: Display:
742: 
743: "We couldn't submit your decision."
744: 
745: Allow retry without losing context.
746: 
747: ---
748: 
749: ## Accessibility
750: 
751: Consent text should support:
752: 
753: - Screen readers
754: - Logical heading hierarchy
755: - Focus management
756: - Large touch targets
757: 
758: Approval and denial buttons must be visually distinct and not rely on colour alone.
759: 
760: ---
761: 
762: ## Acceptance Criteria
763: 
764: ✓ Matches the approved wireframe.
765: 
766: ✓ Approval updates doctor dashboard in real time.
767: 
768: ✓ Denial updates doctor dashboard in real time.
769: 
770: ✓ Expired requests cannot be approved.
771: 
772: ✓ Audit event recorded.
773: 
774: ✓ User receives confirmation after submission.
775: 
776: # P3 — My Health Record
777: 
778: ## Wireframe Reference
779: 
780: Source:
781: 
782: docs/wireframes.html
783: 
784: Screen:
785: 
786: Patient Application → My Health Record
787: 
788: ---
789: 
790: ## Purpose
791: 
792: This screen provides patients with a chronological view of their personal medical information.
793: 
794: It should become the patient's primary location for reviewing healthcare history while maintaining a clean, understandable presentation for non-clinical users.
795: 
796: Unlike the doctor's record view, this interface is designed for readability rather than clinical density.
797: 
798: ---
799: 
800: ## Layout
801: 
802: Follow the approved wireframe.
803: 
804: Expected hierarchy:
805: 
806: 1. Screen Header
807: 2. Patient Summary
808: 3. Timeline Filters
809: 4. Medical Timeline
810: 5. Recent Diagnoses
811: 6. Prescriptions
812: 7. Visit History
813: 
814: Scrolling should affect only the content area.
815: 
816: The header remains fixed.
817: 
818: ---
819: 
820: ## Component Hierarchy
821: 
822: ```
823: HealthRecordScreen
824: 
825: ├── AppHeader
826: │
827: ├── PatientSummaryCard
828: │
829: ├── TimelineFilters
830: │
831: ├── MedicalTimeline
832: │   ├── TimelineEvent
833: │   ├── TimelineEvent
834: │   └── TimelineEvent
835: │
836: ├── DiagnosisSection
837: │
838: ├── PrescriptionSection
839: │
840: ├── VisitHistorySection
841: │
842: └── BottomNavigation
843: ```
844: 
845: ---
846: 
847: ## API Dependencies
848: 
849: GET /patients/me
850: 
851: GET /timeline
852: 
853: GET /medical-records
854: 
855: GET /diagnoses
856: 
857: GET /prescriptions
858: 
859: GET /consultations/history
860: 
861: ---
862: 
863: ## WebSocket Events
864: 
865: Subscribe:
866: 
867: TimelineUpdated
868: 
869: MedicalRecordUpdated
870: 
871: DiagnosisCreated
872: 
873: ConsultationCompleted
874: 
875: Updates should insert or modify only affected timeline entries.
876: 
877: ---
878: 
879: ## User Actions
880: 
881: Patient may:
882: 
883: - Scroll medical history
884: - Expand timeline events
885: - View diagnoses
886: - View prescriptions
887: - Open consultation summaries
888: - Filter timeline
889: 
890: No editing is permitted.
891: 
892: ---
893: 
894: ## Loading Behaviour
895: 
896: Skeletons:
897: 
898: - Timeline cards
899: - Diagnosis cards
900: - Prescription cards
901: 
902: Progressive loading is preferred.
903: 
904: ---
905: 
906: ## Empty State
907: 
908: Display:
909: 
910: "No medical history is available yet."
911: 
912: Offer:
913: 
914: "Complete your first consultation to begin building your medical record."
915: 
916: ---
917: 
918: ## Error State
919: 
920: Inline retry component.
921: 
922: Existing cached data should remain visible whenever possible.
923: 
924: ---
925: 
926: ## Accessibility
927: 
928: Timeline should remain fully screen-reader compatible.
929: 
930: Dates should be announced clearly.
931: 
932: Icons require accessible labels.
933: 
934: ---
935: 
936: ## Acceptance Criteria
937: 
938: ✓ Timeline ordered newest first.
939: 
940: ✓ New consultations appear automatically.
941: 
942: ✓ Record matches backend chronology.
943: 
944: ✓ No editing actions available.
945: 
946: ✓ Matches approved wireframe.
947: 
948: ---
949: 
950: # P4 — AI Symptom Check
951: 
952: ## Wireframe Reference
953: 
954: Source:
955: 
956: docs/wireframes.html
957: 
958: Screen:
959: 
960: Patient Application → AI Symptom Check
961: 
962: ---
963: 
964: ## Purpose
965: 
966: This screen integrates the existing symptom checker into Mirage.
967: 
968: Mirage does not implement symptom analysis itself.
969: 
970: Instead, this interface consumes the existing symptom checker through the SymptomCheckerProvider abstraction defined in the Technical Architecture.
971: 
972: The UI should make this interaction feel native to Mirage.
973: 
974: ---
975: 
976: ## Layout
977: 
978: The visual structure must follow the approved wireframe.
979: 
980: Expected regions:
981: 
982: 1. Introduction
983: 2. Current Question
984: 3. Conversation History
985: 4. Suggested Answers
986: 5. Free Text Input
987: 6. Continue Button
988: 
989: Conversation should expand vertically.
990: 
991: Input remains anchored to the bottom.
992: 
993: ---
994: 
995: ## Component Hierarchy
996: 
997: ```
998: SymptomCheckScreen
999: 
1000: ├── Header
1001: │
1002: ├── SessionProgress
1003: │
1004: ├── ConversationList
1005: │   ├── AIMessage
1006: │   ├── UserMessage
1007: │   └── SuggestedResponses
1008: │
1009: ├── TextInput
1010: │
1011: ├── ContinueButton
1012: │
1013: └── BottomNavigation
1014: ```
1015: 
1016: ---
1017: 
1018: ## API Dependencies
1019: 
1020: POST /symptom-check/start
1021: 
1022: POST /symptom-check/message
1023: 
1024: GET /symptom-check/{session}
1025: 
1026: POST /symptom-check/complete
1027: 
1028: ---
1029: 
1030: ## WebSocket Events
1031: 
1032: None required.
1033: 
1034: Conversation remains request/response based.
1035: 
1036: ---
1037: 
1038: ## User Actions
1039: 
1040: Patient may:
1041: 
1042: - Answer AI questions
1043: - Enter free text
1044: - Select suggested responses
1045: - Review previous answers
1046: - Complete session
1047: 
1048: Patients may not modify completed sessions.
1049: 
1050: ---
1051: 
1052: ## Provider Integration
1053: 
1054: This screen communicates only with:
1055: 
1056: SymptomCheckerProvider
1057: 
1058: The frontend must never know which provider implementation is active.
1059: 
1060: Supported implementations:
1061: 
1062: - Existing Symptom Checker
1063: - Mock Provider
1064: - Future providers
1065: 
1066: ---
1067: 
1068: ## Loading Behaviour
1069: 
1070: Typing indicator.
1071: 
1072: Animated AI placeholder.
1073: 
1074: Disable input while awaiting provider response.
1075: 
1076: ---
1077: 
1078: ## Empty State
1079: 
1080: Initial screen should display onboarding guidance explaining how symptom assessment works.
1081: 
1082: ---
1083: 
1084: ## Error State
1085: 
1086: If provider unavailable:
1087: 
1088: "We're having trouble connecting to the symptom assessment service."
1089: 
1090: Retry available.
1091: 
1092: ---
1093: 
1094: ## Accessibility
1095: 
1096: Conversation should announce newly received messages.
1097: 
1098: Suggested answers must be keyboard accessible.
1099: 
1100: ---
1101: 
1102: ## Acceptance Criteria
1103: 
1104: ✓ Existing symptom checker integrated through provider abstraction.
1105: 
1106: ✓ Conversation persists.
1107: 
1108: ✓ Responses saved.
1109: 
1110: ✓ Completion returns structured summary.
1111: 
1112: ✓ Matches supplied wireframe.
1113: 
1114: ---
1115: 
1116: # Shared Patient Navigation
1117: 
1118: The patient application's bottom navigation should exactly match the navigation model shown in the approved wireframes.
1119: 
1120: Primary destinations include:
1121: 
1122: - Home
1123: - Health Record
1124: - AI Symptom Check
1125: - Notifications
1126: - Profile
1127: 
1128: Navigation transitions should use Framer Motion according to the Design System.
1129: 
1130: Navigation state should survive page refreshes where appropriate.
1131: 
1132: ---
1133: 
1134: # Patient Notification Behaviour
1135: 
1136: Notifications may originate from:
1137: 
1138: - Consent requests
1139: - Consultation updates
1140: - Medical record changes
1141: - AI session completion
1142: - System announcements
1143: 
1144: Unread counts should update in real time through WebSockets.
1145: 
1146: ---
1147: 
1148: # Patient Offline Behaviour
1149: 
1150: If connectivity is lost:
1151: 
1152: - Existing cached records remain readable.
1153: - Navigation remains functional.
1154: - Mutating actions are disabled.
1155: - User receives connectivity warning.
1156: - Automatic reconnection occurs when available.
1157: 
1158: No clinical data should be lost because of temporary network interruption.
1159: 
1160: ---
1161: 
1162: # Patient Acceptance Criteria
1163: 
1164: The Patient Application is considered complete when:
1165: 
1166: ✓ Every screen matches the approved wireframes.
1167: 
1168: ✓ PhoneFrame behaviour matches Design System.
1169: 
1170: ✓ Existing symptom checker integrates correctly.
1171: 
1172: ✓ Consent workflow functions.
1173: 
1174: ✓ Medical timeline updates live.
1175: 
1176: ✓ Notifications synchronize.
1177: 
1178: ✓ All loading, empty and error states implemented.
1179: 
1180: ✓ Accessibility requirements satisfied.
1181: 
1182: ✓ All API interactions occur through typed service layers.
1183: 
1184: ✓ No duplicated UI components exist.
1185: 
1186: # Part 4 — Doctor Portal
1187: 
1188: The Doctor Portal is the primary clinical workspace for healthcare providers.
1189: 
1190: Unlike the Patient Application, the Doctor Portal prioritizes information density, rapid navigation, and efficient decision-making while maintaining a clean and approachable interface.
1191: 
1192: The Doctor Portal shown in `docs/wireframes.html` is the canonical layout.
1193: 
1194: ---
1195: 
1196: # D1 — Doctor Dashboard
1197: 
1198: ## Wireframe Reference
1199: 
1200: Source:
1201: 
1202: docs/wireframes.html
1203: 
1204: Screen:
1205: 
1206: Doctor Portal → Dashboard
1207: 
1208: ---
1209: 
1210: ## Purpose
1211: 
1212: The Dashboard serves as the doctor's landing page and provides an overview of current clinical activity.
1213: 
1214: It should immediately surface:
1215: 
1216: - Today's consultations
1217: - Recently viewed patients
1218: - Pending consent requests
1219: - Active AI-assisted consultations
1220: - Notifications
1221: - Quick patient search
1222: 
1223: The dashboard should minimize unnecessary clicks while avoiding information overload.
1224: 
1225: ---
1226: 
1227: ## Layout
1228: 
1229: The layout must match the approved wireframe.
1230: 
1231: Expected regions:
1232: 
1233: • Top Navigation Bar
1234: 
1235: • Search
1236: 
1237: • Today's Schedule
1238: 
1239: • Recent Patients
1240: 
1241: • Pending Consents
1242: 
1243: • Active Consultation Widget
1244: 
1245: • Notification Panel
1246: 
1247: ---
1248: 
1249: ## Component Hierarchy
1250: 
1251: ```
1252: DoctorDashboard
1253: 
1254: ├── TopNavigation
1255: │
1256: ├── SearchBar
1257: │
1258: ├── DashboardGrid
1259: │   ├── ScheduleWidget
1260: │   ├── RecentPatientsWidget
1261: │   ├── PendingConsentWidget
1262: │   ├── ActiveConsultationWidget
1263: │   └── NotificationWidget
1264: │
1265: └── UserMenu
1266: ```
1267: 
1268: ---
1269: 
1270: ## API Dependencies
1271: 
1272: GET /doctor/dashboard
1273: 
1274: GET /consultations/today
1275: 
1276: GET /consent/pending
1277: 
1278: GET /patients/recent
1279: 
1280: GET /notifications
1281: 
1282: ---
1283: 
1284: ## WebSocket Events
1285: 
1286: Subscribe:
1287: 
1288: ConsentApproved
1289: 
1290: ConsentDenied
1291: 
1292: ConsultationStarted
1293: 
1294: ConsultationCompleted
1295: 
1296: NotificationCreated
1297: 
1298: Widgets should refresh individually.
1299: 
1300: ---
1301: 
1302: ## User Actions
1303: 
1304: Doctor may:
1305: 
1306: - Search patient
1307: - Open consultation
1308: - Review consent
1309: - Open notifications
1310: - Continue active consultation
1311: 
1312: ---
1313: 
1314: ## Loading Behaviour
1315: 
1316: Dashboard widgets load independently.
1317: 
1318: Skeleton placeholders should appear for each widget.
1319: 
1320: ---
1321: 
1322: ## Empty State
1323: 
1324: If no consultations:
1325: 
1326: "No consultations scheduled."
1327: 
1328: If no pending consent:
1329: 
1330: "No pending consent requests."
1331: 
1332: ---
1333: 
1334: ## Error State
1335: 
1336: Widget-level retry.
1337: 
1338: Dashboard should never completely fail because one service is unavailable.
1339: 
1340: ---
1341: 
1342: ## Accessibility
1343: 
1344: Dashboard must support:
1345: 
1346: - Keyboard navigation
1347: 
1348: - Landmark regions
1349: 
1350: - ARIA labels
1351: 
1352: - Screen readers
1353: 
1354: ---
1355: 
1356: ## Acceptance Criteria
1357: 
1358: ✓ Matches wireframe
1359: 
1360: ✓ Widgets update independently
1361: 
1362: ✓ Dashboard responds to WebSocket events
1363: 
1364: ✓ Search available immediately
1365: 
1366: ---
1367: 
1368: # D2 — Patient Search
1369: 
1370: ## Wireframe Reference
1371: 
1372: Doctor Portal → Patient Search
1373: 
1374: ---
1375: 
1376: ## Purpose
1377: 
1378: Locate patients quickly using multiple search criteria.
1379: 
1380: The search experience should remain responsive even with large datasets.
1381: 
1382: ---
1383: 
1384: ## Layout
1385: 
1386: Expected sections:
1387: 
1388: Search Input
1389: 
1390: Search Filters
1391: 
1392: Search Results
1393: 
1394: Recent Searches
1395: 
1396: ---
1397: 
1398: ## Component Hierarchy
1399: 
1400: ```
1401: PatientSearchPage
1402: 
1403: ├── SearchInput
1404: 
1405: ├── SearchFilters
1406: 
1407: ├── ResultsTable
1408: 
1409: │   └── PatientRow
1410: 
1411: ├── Pagination
1412: 
1413: └── EmptyState
1414: ```
1415: 
1416: ---
1417: 
1418: ## API Dependencies
1419: 
1420: GET /patients/search
1421: 
1422: ---
1423: 
1424: ## Search Behaviour
1425: 
1426: Support:
1427: 
1428: - Name
1429: 
1430: - National ID
1431: 
1432: - Phone Number
1433: 
1434: - Medical Record Number
1435: 
1436: - Date of Birth
1437: 
1438: Debounce:
1439: 
1440: 300ms
1441: 
1442: ---
1443: 
1444: ## User Actions
1445: 
1446: Doctor may:
1447: 
1448: - Open patient profile
1449: 
1450: - Begin consultation
1451: 
1452: - Request consent
1453: 
1454: - View previous visits
1455: 
1456: ---
1457: 
1458: ## Loading Behaviour
1459: 
1460: Results table displays skeleton rows.
1461: 
1462: ---
1463: 
1464: ## Empty State
1465: 
1466: "No patients found."
1467: 
1468: ---
1469: 
1470: ## Error State
1471: 
1472: Retry search.
1473: 
1474: ---
1475: 
1476: ## Acceptance Criteria
1477: 
1478: ✓ Fast search
1479: 
1480: ✓ Keyboard accessible
1481: 
1482: ✓ Pagination supported
1483: 
1484: ✓ Matches wireframe
1485: 
1486: ---
1487: 
1488: # D3 — Patient Record
1489: 
1490: ## Wireframe Reference
1491: 
1492: Doctor Portal → Patient Record
1493: 
1494: ---
1495: 
1496: ## Purpose
1497: 
1498: Provide clinicians with a complete view of the patient's medical history after consent has been granted.
1499: 
1500: This screen is information-rich and optimized for clinical review.
1501: 
1502: ---
1503: 
1504: ## Layout
1505: 
1506: Expected regions:
1507: 
1508: Patient Header
1509: 
1510: Medical Timeline
1511: 
1512: Diagnoses
1513: 
1514: Prescriptions
1515: 
1516: Vitals
1517: 
1518: Previous Visits
1519: 
1520: AI Summary Panel
1521: 
1522: ---
1523: 
1524: ## Component Hierarchy
1525: 
1526: ```
1527: PatientRecordPage
1528: 
1529: ├── PatientHeader
1530: 
1531: ├── TimelinePanel
1532: 
1533: ├── DiagnosisPanel
1534: 
1535: ├── MedicationPanel
1536: 
1537: ├── VitalsPanel
1538: 
1539: ├── ConsultationHistory
1540: 
1541: └── AISummaryCard
1542: ```
1543: 
1544: ---
1545: 
1546: ## API Dependencies
1547: 
1548: GET /patients/{id}
1549: 
1550: GET /timeline/{id}
1551: 
1552: GET /diagnoses/{id}
1553: 
1554: GET /prescriptions/{id}
1555: 
1556: GET /consultations/{id}
1557: 
1558: ---
1559: 
1560: ## WebSocket Events
1561: 
1562: MedicalRecordUpdated
1563: 
1564: TimelineUpdated
1565: 
1566: ConsultationCompleted
1567: 
1568: ---
1569: 
1570: ## User Actions
1571: 
1572: Doctor may:
1573: 
1574: - Review history
1575: 
1576: - Expand records
1577: 
1578: - Filter timeline
1579: 
1580: - Open consultation
1581: 
1582: - Launch AI assistant
1583: 
1584: ---
1585: 
1586: ## Loading Behaviour
1587: 
1588: Progressive loading by section.
1589: 
1590: ---
1591: 
1592: ## Empty State
1593: 
1594: "No historical records available."
1595: 
1596: ---
1597: 
1598: ## Acceptance Criteria
1599: 
1600: ✓ Record updates after consent approval
1601: 
1602: ✓ Timeline synchronized
1603: 
1604: ✓ Matches wireframe
1605: 
1606: ---
1607: 
1608: # D4 — Consent Request Workflow
1609: 
1610: ## Wireframe Reference
1611: 
1612: Doctor Portal → Request Consent
1613: 
1614: ---
1615: 
1616: ## Purpose
1617: 
1618: Initiate secure patient authorization before viewing protected records.
1619: 
1620: Consent should be simple, transparent, and legally auditable.
1621: 
1622: ---
1623: 
1624: ## Layout
1625: 
1626: Patient Summary
1627: 
1628: Consent Explanation
1629: 
1630: Requested Information
1631: 
1632: Expiry
1633: 
1634: Send Request Button
1635: 
1636: ---
1637: 
1638: ## API Dependencies
1639: 
1640: POST /consent/request
1641: 
1642: GET /consent/{id}
1643: 
1644: ---
1645: 
1646: ## WebSocket Events
1647: 
1648: ConsentApproved
1649: 
1650: ConsentDenied
1651: 
1652: ConsentExpired
1653: 
1654: ---
1655: 
1656: ## User Actions
1657: 
1658: Doctor may:
1659: 
1660: - Send request
1661: 
1662: - Cancel request
1663: 
1664: - Monitor status
1665: 
1666: ---
1667: 
1668: ## Loading Behaviour
1669: 
1670: Disable submit while sending.
1671: 
1672: ---
1673: 
1674: ## Acceptance Criteria
1675: 
1676: ✓ Request immediately appears on patient device
1677: 
1678: ✓ Live status updates
1679: 
1680: ✓ Audit event created
1681: 
1682: ---
1683: 
1684: # D5 — AI Consultation Workspace
1685: 
1686: ## Wireframe Reference
1687: 
1688: Doctor Portal → Consultation
1689: 
1690: ---
1691: 
1692: ## Purpose
1693: 
1694: Provide the doctor's primary workspace during a consultation.
1695: 
1696: This screen combines:
1697: 
1698: - Patient information
1699: 
1700: - Live transcription
1701: 
1702: - AI diagnostic suggestions
1703: 
1704: - Clinical notes
1705: 
1706: The consultation experience should feel cohesive rather than fragmented.
1707: 
1708: ---
1709: 
1710: ## Layout
1711: 
1712: The layout should follow the approved wireframe.
1713: 
1714: Expected regions:
1715: 
1716: Patient Context
1717: 
1718: Consultation Transcript
1719: 
1720: AI Diagnostic Suggestions
1721: 
1722: Clinical Notes Editor
1723: 
1724: Recommended Questions
1725: 
1726: Consultation Controls
1727: 
1728: ---
1729: 
1730: ## Component Hierarchy
1731: 
1732: ```
1733: ConsultationWorkspace
1734: 
1735: ├── PatientContext
1736: 
1737: ├── TranscriptPanel
1738: 
1739: ├── AIAssistantPanel
1740: 
1741: ├── NotesEditor
1742: 
1743: ├── SuggestedQuestions
1744: 
1745: ├── ConsultationControls
1746: 
1747: └── StatusBar
1748: ```
1749: 
1750: ---
1751: 
1752: ## Provider Dependencies
1753: 
1754: The workspace must interact exclusively through provider abstractions.
1755: 
1756: TranscriptProvider
1757: 
1758: DiagnosisProvider
1759: 
1760: ClinicalNoteProvider
1761: 
1762: Each provider should be replaceable without modifying the UI.
1763: 
1764: ---
1765: 
1766: ## API Dependencies
1767: 
1768: POST /consultation/start
1769: 
1770: POST /consultation/end
1771: 
1772: GET /consultation/{id}
1773: 
1774: POST /notes/generate
1775: 
1776: POST /diagnosis/suggest
1777: 
1778: POST /transcription/start
1779: 
1780: ---
1781: 
1782: ## WebSocket Events
1783: 
1784: TranscriptUpdated
1785: 
1786: AISuggestionReady
1787: 
1788: ConsultationCompleted
1789: 
1790: MedicalRecordUpdated
1791: 
1792: ---
1793: 
1794: ## User Actions
1795: 
1796: Doctor may:
1797: 
1798: - Start consultation
1799: 
1800: - Pause transcription
1801: 
1802: - Accept AI suggestion
1803: 
1804: - Reject AI suggestion
1805: 
1806: - Edit notes
1807: 
1808: - Finalize consultation
1809: 
1810: ---
1811: 
1812: ## Loading Behaviour
1813: 
1814: Each AI widget loads independently.
1815: 
1816: The consultation interface must remain usable while AI processing occurs.
1817: 
1818: ---
1819: 
1820: ## Error State
1821: 
1822: Provider failures should only disable the affected panel.
1823: 
1824: Doctors should always be able to continue manually.
1825: 
1826: ---
1827: 
1828: ## Acceptance Criteria
1829: 
1830: ✓ Provider abstraction maintained
1831: 
1832: ✓ Consultation never blocked by AI
1833: 
1834: ✓ Clinical notes editable
1835: 
1836: ✓ Matches approved wireframe
1837: 
1838: ---
1839: 
1840: # Doctor Portal Acceptance Criteria
1841: 
1842: The Doctor Portal is complete when:
1843: 
1844: ✓ Every screen matches the approved wireframes.
1845: 
1846: ✓ Patient search performs efficiently.
1847: 
1848: ✓ Consent requests synchronize in real time.
1849: 
1850: ✓ Patient records remain read-only until consent is granted.
1851: 
1852: ✓ AI providers integrate exclusively through abstraction interfaces.
1853: 
1854: ✓ Clinical notes support manual editing.
1855: 
1856: ✓ All widgets implement loading, empty, and error states.
1857: 
1858: ✓ Accessibility requirements are satisfied.
1859: 
1860: ✓ WebSocket synchronization functions across all supported workflows.
1861: 
1862: # End of Part 4
1863: 
1864: # Part 5 — Cross-Screen Behaviour & Global Interface Standards
1865: 
1866: This section defines application-wide behaviour that applies to every screen in both the Patient Application and Doctor Portal.
1867: 
1868: These requirements supplement the wireframes and ensure a consistent implementation.
1869: 
1870: ---
1871: 
1872: # Navigation Behaviour
1873: 
1874: ## Patient Application
1875: 
1876: Navigation follows the order defined in `docs/wireframes.html`.
1877: 
1878: Navigation should feel identical to a native mobile application.
1879: 
1880: Requirements:
1881: 
1882: - Animated page transitions
1883: - Preserved scroll position where appropriate
1884: - Persistent bottom navigation
1885: - Current page indicator
1886: - Swipe-back support where appropriate (future)
1887: 
1888: The browser should never expose traditional desktop navigation patterns while inside the PhoneFrame.
1889: 
1890: ---
1891: 
1892: ## Doctor Portal
1893: 
1894: Navigation should remain persistent throughout the session.
1895: 
1896: The sidebar should not reload when switching pages.
1897: 
1898: Breadcrumbs should be shown whenever the doctor is deeper than one navigation level.
1899: 
1900: Example
1901: 
1902: Dashboard
1903: 
1904: ↓
1905: 
1906: Patients
1907: 
1908: ↓
1909: 
1910: John Smith
1911: 
1912: ↓
1913: 
1914: Consultation
1915: 
1916: ---
1917: 
1918: # Screen Transition Behaviour
1919: 
1920: Patient transitions should use the spring animations defined in:
1921: 
1922: 03_Design_System.md
1923: 
1924: Recommended transitions
1925: 
1926: Push Navigation
1927: 
1928: Slide Left
1929: 
1930: Back Navigation
1931: 
1932: Slide Right
1933: 
1934: Bottom Sheet
1935: 
1936: Slide Up
1937: 
1938: Dialog
1939: 
1940: Fade + Scale
1941: 
1942: Notifications
1943: 
1944: Slide Down + Fade
1945: 
1946: Loading
1947: 
1948: Skeleton fade
1949: 
1950: Animations should communicate state changes rather than act as decoration.
1951: 
1952: ---
1953: 
1954: # Global Notification System
1955: 
1956: Notifications should appear consistently throughout the application.
1957: 
1958: Types
1959: 
1960: Information
1961: 
1962: Success
1963: 
1964: Warning
1965: 
1966: Error
1967: 
1968: Clinical
1969: 
1970: Each notification should include
1971: 
1972: - Icon
1973: - Title
1974: - Description
1975: - Timestamp
1976: - Read status
1977: - Action (optional)
1978: 
1979: ---
1980: 
1981: # Notification Sources
1982: 
1983: Notifications may originate from
1984: 
1985: Patient
1986: 
1987: - Consent request
1988: - Consultation complete
1989: - Record updated
1990: - New diagnosis
1991: - Prescription issued
1992: 
1993: Doctor
1994: 
1995: - Consent approved
1996: - Consent denied
1997: - Patient joined
1998: - AI suggestion available
1999: - Consultation reminder
2000: 

(Showing lines 1-2000 of 2329. Use offset=2001 to continue.)
</content>
```

**Tool: read**

**Input:**
```json
{
  "filePath": "/Users/sheltonmutambirwa/Desktop/medic/docs/11_User_Flows_and_State_Machines.md"
}
```

**Output:**
```
<path>/Users/sheltonmutambirwa/Desktop/medic/docs/11_User_Flows_and_State_Machines.md</path>
<type>file</type>
<content>
1: # Mirage
2: # User Flows and State Machines
3: 
4: Version: 1.0
5: 
6: ---
7: 
8: # Purpose
9: 
10: This document defines every workflow implemented by Mirage.
11: 
12: Where `10_UI_Screen_Specification.md` describes what users see, this document describes how the application behaves.
13: 
14: Every workflow should be deterministic.
15: 
16: Given the same state and the same event, the application should always transition to the same next state.
17: 
18: No business logic should exist outside these workflows.
19: 
20: ---
21: 
22: # Relationship to Other Documentation
23: 
24: This document complements:
25: 
26: 01_Product_Requirements_Document.md
27: 
28: Defines product behaviour.
29: 
30: 02_Technical_Architecture.md
31: 
32: Defines implementation.
33: 
34: 05_API_Contract.md
35: 
36: Defines communication.
37: 
38: 06_Database_Schema.md
39: 
40: Defines persistence.
41: 
42: 10_UI_Screen_Specification.md
43: 
44: Defines presentation.
45: 
46: This document defines behaviour.
47: 
48: ---
49: 
50: # Workflow Design Principles
51: 
52: Every workflow should satisfy:
53: 
54: • Predictable
55: 
56: • Recoverable
57: 
58: • Observable
59: 
60: • Auditable
61: 
62: • Idempotent
63: 
64: • Testable
65: 
66: Clinical workflows should never rely on implicit state.
67: 
68: Every state transition must be explicit.
69: 
70: ---
71: 
72: # State Machine Standard
73: 
74: Each workflow follows the same specification.
75: 
76: Purpose
77: 
78: Actors
79: 
80: Entry Conditions
81: 
82: State Diagram
83: 
84: States
85: 
86: Transitions
87: 
88: API Calls
89: 
90: WebSocket Events
91: 
92: Audit Events
93: 
94: Failure Recovery
95: 
96: Acceptance Criteria
97: 
98: ---
99: 
100: # Event Naming Convention
101: 
102: Events should use the format:
103: 
104: Entity.Action
105: 
106: Examples
107: 
108: Consent.Requested
109: 
110: Consent.Approved
111: 
112: Consultation.Started
113: 
114: Consultation.Completed
115: 
116: Timeline.Updated
117: 
118: Notification.Created
119: 
120: Diagnosis.Generated
121: 
122: Transcript.Updated
123: 
124: Authentication.LoggedIn
125: 
126: Authentication.LoggedOut
127: 
128: ---
129: 
130: # Workflow Categories
131: 
132: Patient
133: 
134: Authentication
135: 
136: Home Dashboard
137: 
138: Medical Record
139: 
140: Symptom Assessment
141: 
142: Consent
143: 
144: Notifications
145: 
146: Doctor
147: 
148: Authentication
149: 
150: Dashboard
151: 
152: Patient Search
153: 
154: Patient Review
155: 
156: Consultation
157: 
158: Diagnosis
159: 
160: Clinical Notes
161: 
162: System
163: 
164: Notifications
165: 
166: WebSockets
167: 
168: Provider Integrations
169: 
170: Background Jobs
171: 
172: Synchronization
173: 
174: ---
175: 
176: # Global State Rules
177: 
178: State belongs to one owner.
179: 
180: Examples
181: 
182: Authentication State
183: 
184: Owned by Auth Service.
185: 
186: Consultation State
187: 
188: Owned by Consultation Service.
189: 
190: Consent State
191: 
192: Owned by Consent Service.
193: 
194: Medical Record
195: 
196: Owned by Medical Record Service.
197: 
198: The frontend should never invent state.
199: 
200: ---
201: 
202: # API Rule
203: 
204: Every state transition requiring persistence must pass through the backend.
205: 
206: Frontend
207: 
208: ↓
209: 
210: FastAPI
211: 
212: ↓
213: 
214: Database
215: 
216: ↓
217: 
218: WebSocket
219: 
220: ↓
221: 
222: Clients
223: 
224: Direct client-to-client communication is prohibited.
225: 
226: ---
227: 
228: # WebSocket Rule
229: 
230: WebSockets should communicate state changes only.
231: 
232: Business logic must remain on the backend.
233: 
234: Clients should react to events rather than determine state independently.
235: 
236: ---
237: 
238: # Provider Rule
239: 
240: AI providers never change workflow behaviour.
241: 
242: Regardless of implementation:
243: 
244: Mock
245: 
246: Existing Symptom Checker
247: 
248: Azure OpenAI
249: 
250: OpenAI
251: 
252: Anthropic
253: 
254: Future Provider
255: 
256: The workflow remains identical.
257: 
258: Only provider outputs differ.
259: 
260: ---
261: 
262: # Recovery Rule
263: 
264: Every workflow must define recovery paths.
265: 
266: Recoverable failures should never require restarting the application.
267: 
268: Whenever possible:
269: 
270: Retry
271: 
272: Reconnect
273: 
274: Resume
275: 
276: Continue
277: 
278: Rather than restart.
279: 
280: ---
281: 
282: # Audit Rule
283: 
284: Every clinically significant action should generate an immutable audit event.
285: 
286: Examples
287: 
288: Consent approved
289: 
290: Diagnosis confirmed
291: 
292: Record viewed
293: 
294: Record updated
295: 
296: Consultation completed
297: 
298: Prescription issued
299: 
300: Authentication success
301: 
302: Authentication failure
303: 
304: Audit logs should never be editable.
305: 
306: ---
307: 
308: # State Diagram Notation
309: 
310: Notation used throughout this document
311: 
312: ```
313: 
314: State
315: 
316: ↓
317: 
318: Event
319: 
320: ↓
321: 
322: Next State
323: 
324: ```
325: 
326: Conditional transitions use:
327: 
328: ```
329: 
330: State
331: 
332: ↓
333: 
334: Condition?
335: 
336: ↓
337: 
338: Yes → Next State
339: 
340: ↓
341: 
342: No → Alternate State
343: 
344: ```
345: 
346: All subsequent workflows follow this notation.
347: 
348: # End of Part 1
349: 
350: # Part 2 — Authentication State Machines
351: 
352: Authentication supports two distinct operating modes.
353: 
354: Development Mode
355: 
356: - Mock Login
357: - Instant role switching
358: - No credential validation
359: - No JWT enforcement
360: - Intended only for local development
361: 
362: Production Mode
363: 
364: - JWT Authentication
365: - Refresh Tokens
366: - Password validation
367: - Role-based authorization
368: 
369: The UI should behave identically in both modes.
370: 
371: Only the authentication backend changes.
372: 
373: ---
374: 
375: # Workflow A1 — Development Login
376: 
377: ## Purpose
378: 
379: Allow developers to rapidly enter either application without repeatedly authenticating.
380: 
381: This workflow exists exclusively to improve development speed.
382: 
383: It must be disabled in production.
384: 
385: ---
386: 
387: ## Actors
388: 
389: - Developer
390: 
391: ---
392: 
393: ## Entry Conditions
394: 
395: Application running with
396: 
397: ```
398: DEMO_MODE=true
399: ```
400: 
401: ---
402: 
403: ## State Diagram
404: 
405: ```
406: Application Started
407: 
408: ↓
409: 
410: Demo Login Screen
411: 
412: ↓
413: 
414: Select Role
415: 
416: ↓
417: 
418: Patient
419:         \
420:          \
421:           → Authenticated
422:          /
423: Doctor
424: ```
425: 
426: ---
427: 
428: ## States
429: 
430: Idle
431: 
432: ↓
433: 
434: Role Selection
435: 
436: ↓
437: 
438: Authenticated
439: 
440: ---
441: 
442: ## API Calls
443: 
444: None required.
445: 
446: A mock identity is generated locally.
447: 
448: ---
449: 
450: ## Stored Session
451: 
452: ```
453: user_id
454: 
455: role
456: 
457: demo_mode
458: 
459: expires_at
460: ```
461: 
462: ---
463: 
464: ## Exit Conditions
465: 
466: Logout
467: 
468: ↓
469: 
470: Return to Demo Login
471: 
472: ---
473: 
474: ## Audit Event
475: 
476: ```
477: Authentication.DemoLogin
478: ```
479: 
480: ---
481: 
482: ## Acceptance Criteria
483: 
484: ✓ One click login
485: 
486: ✓ Switch between Doctor and Patient instantly
487: 
488: ✓ No backend dependency
489: 
490: ✓ Disabled automatically in production
491: 
492: ---
493: 
494: # Workflow A2 — JWT Authentication
495: 
496: ## Purpose
497: 
498: Authenticate real users securely.
499: 
500: ---
501: 
502: ## Actors
503: 
504: Patient
505: 
506: Doctor
507: 
508: ---
509: 
510: ## Entry Conditions
511: 
512: Application started
513: 
514: Production mode
515: 
516: ---
517: 
518: ## State Diagram
519: 
520: ```
521: Unauthenticated
522: 
523: ↓
524: 
525: Submit Credentials
526: 
527: ↓
528: 
529: Valid?
530: 
531: ↓
532: 
533: Yes
534: 
535: ↓
536: 
537: Generate JWT
538: 
539: ↓
540: 
541: Authenticated
542: 
543: ↓
544: 
545: Refresh Loop
546: 
547: ↓
548: 
549: Logout
550: 
551: ↓
552: 
553: Unauthenticated
554: 
555: ------------------------
556: 
557: Invalid Credentials
558: 
559: ↓
560: 
561: Authentication Failed
562: 
563: ↓
564: 
565: Retry
566: ```
567: 
568: ---
569: 
570: ## States
571: 
572: Unauthenticated
573: 
574: Authenticating
575: 
576: Authenticated
577: 
578: Refresh Pending
579: 
580: Expired
581: 
582: Logged Out
583: 
584: ---
585: 
586: ## API Calls
587: 
588: POST /auth/login
589: 
590: POST /auth/refresh
591: 
592: POST /auth/logout
593: 
594: GET /auth/me
595: 
596: ---
597: 
598: ## WebSocket Events
599: 
600: Authenticate socket after JWT validation.
601: 
602: Disconnect immediately after logout.
603: 
604: ---
605: 
606: ## Failure Recovery
607: 
608: Invalid credentials
609: 
610: ↓
611: 
612: Display validation message
613: 
614: ↓
615: 
616: Remain on login screen
617: 
618: ---
619: 
620: Expired token
621: 
622: ↓
623: 
624: Attempt refresh
625: 
626: ↓
627: 
628: Refresh successful
629: 
630: ↓
631: 
632: Continue session
633: 
634: ---
635: 
636: Refresh failed
637: 
638: ↓
639: 
640: Return to login
641: 
642: ---
643: 
644: ## Audit Events
645: 
646: Authentication.Login
647: 
648: Authentication.Logout
649: 
650: Authentication.Refresh
651: 
652: Authentication.Failed
653: 
654: ---
655: 
656: ## Acceptance Criteria
657: 
658: ✓ JWT stored securely
659: 
660: ✓ Refresh automatic
661: 
662: ✓ Logout invalidates refresh token
663: 
664: ✓ Socket reconnects automatically
665: 
666: ---
667: 
668: # Workflow A3 — Session Restoration
669: 
670: ## Purpose
671: 
672: Restore authenticated users after browser refresh.
673: 
674: ---
675: 
676: ## State Diagram
677: 
678: ```
679: Application Starts
680: 
681: ↓
682: 
683: Existing Token?
684: 
685: ↓
686: 
687: No
688: 
689: ↓
690: 
691: Login Screen
692: 
693: ----------------------
694: 
695: Yes
696: 
697: ↓
698: 
699: Validate Token
700: 
701: ↓
702: 
703: Valid?
704: 
705: ↓
706: 
707: Yes
708: 
709: ↓
710: 
711: Restore Session
712: 
713: ↓
714: 
715: Dashboard
716: 
717: ----------------------
718: 
719: No
720: 
721: ↓
722: 
723: Attempt Refresh
724: 
725: ↓
726: 
727: Success?
728: 
729: ↓
730: 
731: Yes
732: 
733: ↓
734: 
735: Dashboard
736: 
737: ↓
738: 
739: No
740: 
741: ↓
742: 
743: Login
744: ```
745: 
746: ---
747: 
748: ## API Calls
749: 
750: GET /auth/me
751: 
752: POST /auth/refresh
753: 
754: ---
755: 
756: ## Acceptance Criteria
757: 
758: ✓ Refresh survives browser reload
759: 
760: ✓ Expired sessions handled gracefully
761: 
762: ✓ No unnecessary login prompts
763: 
764: ---
765: 
766: # Workflow A4 — Role Switching (Development)
767: 
768: ## Purpose
769: 
770: Rapidly switch between Patient and Doctor applications during demonstrations.
771: 
772: ---
773: 
774: ## Entry Conditions
775: 
776: Demo Mode enabled.
777: 
778: ---
779: 
780: ## State Diagram
781: 
782: ```
783: Patient
784: 
785: ↓
786: 
787: Switch Role
788: 
789: ↓
790: 
791: Doctor
792: 
793: ↓
794: 
795: Switch Role
796: 
797: ↓
798: 
799: Patient
800: ```
801: 
802: ---
803: 
804: ## Requirements
805: 
806: Switching roles should
807: 
808: - Preserve application state where appropriate
809: - Disconnect old WebSocket
810: - Establish new authenticated socket
811: - Reload role-specific navigation
812: - Reload permissions
813: 
814: ---
815: 
816: ## Audit Event
817: 
818: ```
819: Authentication.RoleSwitched
820: ```
821: 
822: ---
823: 
824: ## Acceptance Criteria
825: 
826: ✓ Role switch <1 second
827: 
828: ✓ No page reload required
829: 
830: ✓ New permissions applied immediately
831: 
832: ---
833: 
834: # Workflow A5 — Logout
835: 
836: ## Purpose
837: 
838: Terminate authenticated session safely.
839: 
840: ---
841: 
842: ## State Diagram
843: 
844: ```
845: Authenticated
846: 
847: ↓
848: 
849: Logout Requested
850: 
851: ↓
852: 
853: Invalidate Refresh Token
854: 
855: ↓
856: 
857: Disconnect Socket
858: 
859: ↓
860: 
861: Clear Local Storage
862: 
863: ↓
864: 
865: Login Screen
866: ```
867: 
868: ---
869: 
870: ## API Calls
871: 
872: POST /auth/logout
873: 
874: ---
875: 
876: ## Cleanup
877: 
878: Remove
879: 
880: - JWT
881: 
882: - Refresh Token
883: 
884: - Cached User
885: 
886: - Active Consultation Cache
887: 
888: - Temporary AI Sessions
889: 
890: ---
891: 
892: ## Acceptance Criteria
893: 
894: ✓ Session destroyed
895: 
896: ✓ Socket disconnected
897: 
898: ✓ Tokens removed
899: 
900: ✓ Cannot navigate using browser history into protected pages
901: 
902: ---
903: 
904: # Global Authentication Rules
905: 
906: Authentication state is owned exclusively by the Authentication Service.
907: 
908: React components should consume authentication through:
909: 
910: ```
911: Auth Context
912: 
913: ↓
914: 
915: Auth Hook
916: 
917: ↓
918: 
919: API Client
920: 
921: ↓
922: 
923: FastAPI
924: ```
925: 
926: Components should never inspect JWT contents directly.
927: 
928: Authorization decisions always belong to the backend.
929: 
930: ---
931: 
932: # Authentication Failure Matrix
933: 
934: | Failure | Recovery |
935: |----------|----------|
936: | Wrong Password | Retry |
937: | Expired JWT | Refresh |
938: | Expired Refresh | Login |
939: | Network Failure | Retry |
940: | Backend Offline | Offline Screen |
941: | Demo Login | Always succeeds |
942: 
943: # End of Part 2
944: 
945: # Part 3 — Consent Lifecycle State Machine
946: 
947: The Consent Workflow is the foundation of Mirage.
948: 
949: No protected medical information may be accessed until an active consent grant exists.
950: 
951: Consent must always be:
952: 
953: - Explicit
954: - Time-limited
955: - Auditable
956: - Revocable
957: - Observable in real time
958: 
959: The backend is the source of truth.
960: 
961: ---
962: 
963: # Workflow C1 — Doctor Requests Consent
964: 
965: ## Purpose
966: 
967: Allow a clinician to request temporary access to a patient's protected medical information before consultation.
968: 
969: ---
970: 
971: ## Actors
972: 
973: Doctor
974: 
975: Patient
976: 
977: Consent Service
978: 
979: Notification Service
980: 
981: WebSocket Gateway
982: 
983: ---
984: 
985: ## Entry Conditions
986: 
987: Doctor is authenticated.
988: 
989: Patient exists.
990: 
991: No active consent currently grants the requested permissions.
992: 
993: ---
994: 
995: ## State Diagram
996: 
997: ```
998: Patient Selected
999: 
1000: ↓
1001: 
1002: Create Consent Request
1003: 
1004: ↓
1005: 
1006: Consent Created
1007: 
1008: ↓
1009: 
1010: Patient Notified
1011: 
1012: ↓
1013: 
1014: Waiting For Response
1015: ```
1016: 
1017: ---
1018: 
1019: ## States
1020: 
1021: Idle
1022: 
1023: ↓
1024: 
1025: Creating Request
1026: 
1027: ↓
1028: 
1029: Pending
1030: 
1031: ↓
1032: 
1033: Delivered
1034: 
1035: ↓
1036: 
1037: Awaiting Response
1038: 
1039: ---
1040: 
1041: ## API Calls
1042: 
1043: POST /consent/request
1044: 
1045: GET /consent/{id}
1046: 
1047: ---
1048: 
1049: ## Backend Actions
1050: 
1051: Generate Consent Record
1052: 
1053: ↓
1054: 
1055: Store Expiry Timestamp
1056: 
1057: ↓
1058: 
1059: Create Notification
1060: 
1061: ↓
1062: 
1063: Publish WebSocket Event
1064: 
1065: ↓
1066: 
1067: Return Pending Status
1068: 
1069: ---
1070: 
1071: ## WebSocket Events
1072: 
1073: Publish
1074: 
1075: Consent.Requested
1076: 
1077: Notification.Created
1078: 
1079: Patient receives the request immediately.
1080: 
1081: ---
1082: 
1083: ## Audit Events
1084: 
1085: Consent.Requested
1086: 
1087: Notification.Created
1088: 
1089: ---
1090: 
1091: ## Acceptance Criteria
1092: 
1093: ✓ Consent stored.
1094: 
1095: ✓ Patient notified.
1096: 
1097: ✓ Dashboard immediately shows Pending.
1098: 
1099: ✓ Request visible in audit history.
1100: 
1101: ---
1102: 
1103: # Workflow C2 — Patient Reviews Consent
1104: 
1105: ## Purpose
1106: 
1107: Present the patient with sufficient information to make an informed decision.
1108: 
1109: ---
1110: 
1111: ## State Diagram
1112: 
1113: ```
1114: Notification Opened
1115: 
1116: ↓
1117: 
1118: Load Consent
1119: 
1120: ↓
1121: 
1122: Consent Displayed
1123: 
1124: ↓
1125: 
1126: Review Information
1127: ```
1128: 
1129: ---
1130: 
1131: ## Information Presented
1132: 
1133: Doctor Name
1134: 
1135: Facility
1136: 
1137: Reason
1138: 
1139: Requested Information
1140: 
1141: Expiry
1142: 
1143: Privacy Notice
1144: 
1145: ---
1146: 
1147: ## API Calls
1148: 
1149: GET /consent/{id}
1150: 
1151: ---
1152: 
1153: ## Acceptance Criteria
1154: 
1155: ✓ Patient understands exactly what will be shared.
1156: 
1157: ✓ Consent cannot be approved without loading complete details.
1158: 
1159: ---
1160: 
1161: # Workflow C3 — Patient Approves Consent
1162: 
1163: ## Purpose
1164: 
1165: Grant temporary access to requested medical records.
1166: 
1167: ---
1168: 
1169: ## State Diagram
1170: 
1171: ```
1172: Pending
1173: 
1174: ↓
1175: 
1176: Approve
1177: 
1178: ↓
1179: 
1180: Consent Active
1181: 
1182: ↓
1183: 
1184: Doctor Notified
1185: 
1186: ↓
1187: 
1188: Medical Records Unlocked
1189: ```
1190: 
1191: ---
1192: 
1193: ## States
1194: 
1195: Pending
1196: 
1197: Approved
1198: 
1199: Active
1200: 
1201: Expired
1202: 
1203: ---
1204: 
1205: ## API Calls
1206: 
1207: POST /consent/{id}/approve
1208: 
1209: ---
1210: 
1211: ## Backend Actions
1212: 
1213: Update Consent
1214: 
1215: ↓
1216: 
1217: Create Audit Event
1218: 
1219: ↓
1220: 
1221: Publish WebSocket
1222: 
1223: ↓
1224: 
1225: Enable Record Access
1226: 
1227: ---
1228: 
1229: ## WebSocket Events
1230: 
1231: Consent.Approved
1232: 
1233: MedicalRecord.AccessGranted
1234: 
1235: Notification.Created
1236: 
1237: ---
1238: 
1239: ## Acceptance Criteria
1240: 
1241: ✓ Doctor immediately gains access.
1242: 
1243: ✓ Patient receives confirmation.
1244: 
1245: ✓ Audit recorded.
1246: 
1247: ✓ Timeline updated.
1248: 
1249: ---
1250: 
1251: # Workflow C4 — Patient Denies Consent
1252: 
1253: ## Purpose
1254: 
1255: Reject access request.
1256: 
1257: ---
1258: 
1259: ## State Diagram
1260: 
1261: ```
1262: Pending
1263: 
1264: ↓
1265: 
1266: Decline
1267: 
1268: ↓
1269: 
1270: Denied
1271: 
1272: ↓
1273: 
1274: Doctor Notified
1275: 
1276: ↓
1277: 
1278: Request Closed
1279: ```
1280: 
1281: ---
1282: 
1283: ## API Calls
1284: 
1285: POST /consent/{id}/deny
1286: 
1287: ---
1288: 
1289: ## Backend Actions
1290: 
1291: Update Status
1292: 
1293: ↓
1294: 
1295: Publish Notification
1296: 
1297: ↓
1298: 
1299: Audit Log
1300: 
1301: ---
1302: 
1303: ## WebSocket Events
1304: 
1305: Consent.Denied
1306: 
1307: Notification.Created
1308: 
1309: ---
1310: 
1311: ## Acceptance Criteria
1312: 
1313: ✓ Doctor loses ability to access records.
1314: 
1315: ✓ Patient confirmation displayed.
1316: 
1317: ✓ Request closed.
1318: 
1319: ---
1320: 
1321: # Workflow C5 — Consent Expiration
1322: 
1323: ## Purpose
1324: 
1325: Automatically revoke access after the approved duration.
1326: 
1327: No manual action should be required.
1328: 
1329: ---
1330: 
1331: ## State Diagram
1332: 
1333: ```
1334: Active
1335: 
1336: ↓
1337: 
1338: Expiry Time Reached
1339: 
1340: ↓
1341: 
1342: Expired
1343: 
1344: ↓
1345: 
1346: Access Revoked
1347: 
1348: ↓
1349: 
1350: Notification Sent
1351: ```
1352: 
1353: ---
1354: 
1355: ## Trigger
1356: 
1357: Background Scheduler
1358: 
1359: ---
1360: 
1361: ## Backend Actions
1362: 
1363: Update Consent
1364: 
1365: ↓
1366: 
1367: Revoke Access
1368: 
1369: ↓
1370: 
1371: Publish Events
1372: 
1373: ↓
1374: 
1375: Audit
1376: 
1377: ---
1378: 
1379: ## WebSocket Events
1380: 
1381: Consent.Expired
1382: 
1383: MedicalRecord.AccessRevoked
1384: 
1385: ---
1386: 
1387: ## Acceptance Criteria
1388: 
1389: ✓ Automatic.
1390: 
1391: ✓ Immediate.
1392: 
1393: ✓ Logged.
1394: 
1395: ---
1396: 
1397: # Workflow C6 — Consent Revocation
1398: 
1399: ## Purpose
1400: 
1401: Allow patients to revoke previously granted consent before expiry.
1402: 
1403: ---
1404: 
1405: ## State Diagram
1406: 
1407: ```
1408: Active
1409: 
1410: ↓
1411: 
1412: Patient Revokes
1413: 
1414: ↓
1415: 
1416: Revoked
1417: 
1418: ↓
1419: 
1420: Access Removed
1421: 
1422: ↓
1423: 
1424: Doctor Updated
1425: ```
1426: 
1427: ---
1428: 
1429: ## API Calls
1430: 
1431: POST /consent/{id}/revoke
1432: 
1433: ---
1434: 
1435: ## WebSocket Events
1436: 
1437: Consent.Revoked
1438: 
1439: MedicalRecord.AccessRevoked
1440: 
1441: ---
1442: 
1443: ## Audit Events
1444: 
1445: Consent.Revoked
1446: 
1447: ---
1448: 
1449: ## Acceptance Criteria
1450: 
1451: ✓ Access removed immediately.
1452: 
1453: ✓ Doctor informed.
1454: 
1455: ✓ Timeline updated.
1456: 
1457: ---
1458: 
1459: # Permission Matrix
1460: 
1461: | Consent Status | Doctor Access |
1462: |----------------|--------------|
1463: | Pending | None |
1464: | Approved | Granted |
1465: | Active | Granted |
1466: | Expired | None |
1467: | Denied | None |
1468: | Revoked | None |
1469: 
1470: ---
1471: 
1472: # Failure Recovery
1473: 
1474: ## Patient Offline
1475: 
1476: Notification queued.
1477: 
1478: Delivered when reconnecting.
1479: 
1480: ---
1481: 
1482: ## Doctor Offline
1483: 
1484: Dashboard updated after reconnect.
1485: 
1486: ---
1487: 
1488: ## Duplicate Approval
1489: 
1490: Ignored.
1491: 
1492: Return existing Active consent.
1493: 
1494: ---
1495: 
1496: ## Expired Before Approval
1497: 
1498: Return
1499: 
1500: ```
1501: 409 Conflict
1502: ```
1503: 
1504: Display
1505: 
1506: "This consent request has expired."
1507: 
1508: ---
1509: 
1510: ## Network Failure
1511: 
1512: Remain on current screen.
1513: 
1514: Retry available.
1515: 
1516: No duplicate requests should be created.
1517: 
1518: ---
1519: 
1520: # Security Rules
1521: 
1522: Consent tokens must be:
1523: 
1524: - Unpredictable
1525: - Time limited
1526: - Single authoritative record
1527: - Audit logged
1528: 
1529: Medical data access must always validate consent at request time.
1530: 
1531: Never trust cached permissions.
1532: 
1533: ---
1534: 
1535: # Audit Trail
1536: 
1537: Every transition records
1538: 
1539: Timestamp
1540: 
1541: Actor
1542: 
1543: Consent ID
1544: 
1545: Patient ID
1546: 
1547: Doctor ID
1548: 
1549: Old State
1550: 
1551: New State
1552: 
1553: IP Address (future)
1554: 
1555: Device Information (future)
1556: 
1557: Audit entries are immutable.
1558: 
1559: ---
1560: 
1561: # Acceptance Criteria
1562: 
1563: ✓ Entire workflow matches PRD.
1564: 
1565: ✓ Doctor and Patient remain synchronized.
1566: 
1567: ✓ Expiry automatic.
1568: 
1569: ✓ Revocation immediate.
1570: 
1571: ✓ Every transition audited.
1572: 
1573: ✓ WebSocket events emitted correctly.
1574: 
1575: ✓ Permission checks enforced on every protected endpoint.
1576: 
1577: # End of Part 3
1578: 
1579: # Part 4 — Consultation Lifecycle State Machine
1580: 
1581: The Consultation Workflow is the primary clinical workflow within Mirage.
1582: 
1583: It orchestrates multiple independent services into a single seamless experience while maintaining provider abstraction.
1584: 
1585: The consultation workflow coordinates:
1586: 
1587: - Authentication
1588: - Patient Context
1589: - Active Consent Validation
1590: - Existing Symptom Checker
1591: - Live Transcription
1592: - AI Clinical Suggestions
1593: - Clinical Notes
1594: - Diagnosis
1595: - Medical Record Updates
1596: - Timeline Events
1597: - Notifications
1598: 
1599: The consultation workflow is owned by the Consultation Service.
1600: 
1601: ---
1602: 
1603: # Workflow CL1 — Consultation Initialization
1604: 
1605: ## Purpose
1606: 
1607: Initialize a consultation after patient selection and successful consent verification.
1608: 
1609: No consultation may begin unless consent validation succeeds.
1610: 
1611: ---
1612: 
1613: ## Actors
1614: 
1615: Doctor
1616: 
1617: Patient
1618: 
1619: Consultation Service
1620: 
1621: Consent Service
1622: 
1623: Medical Record Service
1624: 
1625: Notification Service
1626: 
1627: ---
1628: 
1629: ## Entry Conditions
1630: 
1631: ✓ Doctor authenticated
1632: 
1633: ✓ Patient selected
1634: 
1635: ✓ Active consent exists
1636: 
1637: ✓ Patient record accessible
1638: 
1639: ---
1640: 
1641: ## State Diagram
1642: 
1643: ```
1644: Patient Selected
1645: 
1646: ↓
1647: 
1648: Validate Consent
1649: 
1650: ↓
1651: 
1652: Consent Valid?
1653: 
1654: ↓
1655: 
1656: Yes
1657: 
1658: ↓
1659: 
1660: Create Consultation
1661: 
1662: ↓
1663: 
1664: Load Patient Context
1665: 
1666: ↓
1667: 
1668: Consultation Ready
1669: 
1670: ----------------------------
1671: 
1672: No
1673: 
1674: ↓
1675: 
1676: Access Denied
1677: 
1678: ↓
1679: 
1680: Request Consent
1681: ```
1682: 
1683: ---
1684: 
1685: ## API Calls
1686: 
1687: POST /consultations/start
1688: 
1689: GET /consultations/{id}
1690: 
1691: GET /patients/{id}
1692: 
1693: GET /timeline/{id}
1694: 
1695: GET /medical-records/{id}
1696: 
1697: ---
1698: 
1699: ## Backend Actions
1700: 
1701: Create consultation
1702: 
1703: ↓
1704: 
1705: Load patient context
1706: 
1707: ↓
1708: 
1709: Initialize AI session
1710: 
1711: ↓
1712: 
1713: Initialize transcription session
1714: 
1715: ↓
1716: 
1717: Publish Consultation.Started
1718: 
1719: ---
1720: 
1721: ## WebSocket Events
1722: 
1723: Consultation.Started
1724: 
1725: Notification.Created
1726: 
1727: ---
1728: 
1729: ## Acceptance Criteria
1730: 
1731: ✓ Consultation cannot begin without consent
1732: 
1733: ✓ Patient context loads automatically
1734: 
1735: ✓ AI services initialize in background
1736: 
1737: ✓ Dashboard updates immediately
1738: 
1739: ---
1740: 
1741: # Workflow CL2 — Existing Symptom Checker Integration
1742: 
1743: ## Purpose
1744: 
1745: Display structured symptom assessment generated by the existing symptom checker.
1746: 
1747: Mirage does not implement diagnostic questioning itself.
1748: 
1749: Instead it consumes an external provider through the SymptomCheckerProvider interface.
1750: 
1751: ---
1752: 
1753: ## Provider Architecture
1754: 
1755: ```
1756: Consultation
1757: 
1758: ↓
1759: 
1760: SymptomCheckerProvider
1761: 
1762: ↓
1763: 
1764: Current Provider
1765: 
1766: ↓
1767: 
1768: Structured Assessment
1769: ```
1770: 
1771: Future providers should be interchangeable without modifying consultation logic.
1772: 
1773: ---
1774: 
1775: ## State Diagram
1776: 
1777: ```
1778: Consultation Ready
1779: 
1780: ↓
1781: 
1782: Request Assessment
1783: 
1784: ↓
1785: 
1786: Assessment Running
1787: 
1788: ↓
1789: 
1790: Assessment Complete
1791: 
1792: ↓
1793: 
1794: Structured Summary Available
1795: ```
1796: 
1797: ---
1798: 
1799: ## API Calls
1800: 
1801: POST /symptom-check/start
1802: 
1803: POST /symptom-check/message
1804: 
1805: POST /symptom-check/complete
1806: 
1807: GET /symptom-check/{session}
1808: 
1809: ---
1810: 
1811: ## Backend Actions
1812: 
1813: Retrieve assessment
1814: 
1815: ↓
1816: 
1817: Normalize provider response
1818: 
1819: ↓
1820: 
1821: Store structured output
1822: 
1823: ↓
1824: 
1825: Attach to consultation
1826: 
1827: ---
1828: 
1829: ## Acceptance Criteria
1830: 
1831: ✓ Existing symptom checker integrated
1832: 
1833: ✓ Provider abstraction maintained
1834: 
1835: ✓ Structured assessment attached to consultation
1836: 
1837: ---
1838: 
1839: # Workflow CL3 — Live Transcription
1840: 
1841: ## Purpose
1842: 
1843: Capture clinician-patient conversation during consultation.
1844: 
1845: Transcription should be optional.
1846: 
1847: Consultation must continue if transcription becomes unavailable.
1848: 
1849: ---
1850: 
1851: ## Provider Architecture
1852: 
1853: ```
1854: TranscriptProvider
1855: 
1856: ↓
1857: 
1858: Azure
1859: 
1860: ↓
1861: 
1862: Deepgram
1863: 
1864: ↓
1865: 
1866: Whisper
1867: 
1868: ↓
1869: 
1870: Future Provider
1871: ```
1872: 
1873: ---
1874: 
1875: ## State Diagram
1876: 
1877: ```
1878: Consultation Active
1879: 
1880: ↓
1881: 
1882: Start Transcription
1883: 
1884: ↓
1885: 
1886: Streaming
1887: 
1888: ↓
1889: 
1890: Transcript Updated
1891: 
1892: ↓
1893: 
1894: Stop
1895: 
1896: ↓
1897: 
1898: Transcript Finalized
1899: ```
1900: 
1901: ---
1902: 
1903: ## API Calls
1904: 
1905: POST /transcription/start
1906: 
1907: POST /transcription/stop
1908: 
1909: GET /transcription/{id}
1910: 
1911: ---
1912: 
1913: ## WebSocket Events
1914: 
1915: Transcript.Updated
1916: 
1917: Transcript.Completed
1918: 
1919: ---
1920: 
1921: ## Failure Recovery
1922: 
1923: Provider unavailable
1924: 
1925: ↓
1926: 
1927: Pause transcription
1928: 
1929: ↓
1930: 
1931: Continue consultation
1932: 
1933: ↓
1934: 
1935: Doctor continues manually
1936: 
1937: ---
1938: 
1939: ## Acceptance Criteria
1940: 
1941: ✓ Consultation independent from transcription
1942: 
1943: ✓ Partial transcript retained
1944: 
1945: ✓ Provider abstraction preserved
1946: 
1947: ---
1948: 
1949: # Workflow CL4 — AI Diagnostic Suggestions
1950: 
1951: ## Purpose
1952: 
1953: Generate non-authoritative clinical suggestions.
1954: 
1955: AI recommendations assist the clinician but never replace clinical judgement.
1956: 
1957: ---
1958: 
1959: ## Provider Architecture
1960: 
1961: ```
1962: DiagnosisProvider
1963: 
1964: ↓
1965: 
1966: OpenAI
1967: 
1968: ↓
1969: 
1970: Azure OpenAI
1971: 
1972: ↓
1973: 
1974: Anthropic
1975: 
1976: ↓
1977: 
1978: Mock Provider
1979: ```
1980: 
1981: ---
1982: 
1983: ## State Diagram
1984: 
1985: ```
1986: Consultation Active
1987: 
1988: ↓
1989: 
1990: Generate Suggestions
1991: 
1992: ↓
1993: 
1994: Processing
1995: 
1996: ↓
1997: 
1998: Suggestions Ready
1999: 
2000: ↓

(Showing lines 1-2000 of 4011. Use offset=2001 to continue.)
</content>
```

**Tool: read**

**Input:**
```json
{
  "filePath": "/Users/sheltonmutambirwa/Desktop/medic/docs/08_Coding_Standards.md"
}
```

**Output:**
```
<path>/Users/sheltonmutambirwa/Desktop/medic/docs/08_Coding_Standards.md</path>
<type>file</type>
<content>
1: # Mirage
2: # Coding Standards
3: 
4: Version: 1.0
5: 
6: ---
7: 
8: # Purpose
9: 
10: This document defines the engineering standards for the Mirage codebase.
11: 
12: Its purpose is to ensure that every generated file follows the same conventions, regardless of which AI coding assistant or engineer creates it.
13: 
14: These standards take precedence over individual coding preferences.
15: 
16: ---
17: 
18: # Engineering Philosophy
19: 
20: The codebase should prioritize:
21: 
22: - Readability
23: - Maintainability
24: - Explicitness
25: - Consistency
26: - Simplicity
27: - Extensibility
28: - Testability
29: 
30: Never sacrifice long-term maintainability for short-term convenience.
31: 
32: ---
33: 
34: # General Principles
35: 
36: Prefer:
37: 
38: - Composition over inheritance
39: - Dependency Injection over service location
40: - Interfaces over concrete implementations
41: - Small focused modules
42: - Explicit dependencies
43: - Immutable data where practical
44: 
45: Avoid:
46: 
47: - Global mutable state
48: - Hidden side effects
49: - Circular dependencies
50: - Magic strings
51: - Hardcoded configuration
52: - Overly clever abstractions
53: 
54: ---
55: 
56: # Repository Structure
57: 
58: Backend
59: 
60: ```
61: backend/
62: 
63: app/
64:     api/
65:     core/
66:     db/
67:     models/
68:     repositories/
69:     services/
70:     providers/
71:     schemas/
72:     middleware/
73:     websocket/
74:     workers/
75:     tests/
76: ```
77: 
78: Frontend
79: 
80: ```
81: frontend/
82: 
83: app/
84: components/
85: features/
86: hooks/
87: lib/
88: providers/
89: services/
90: types/
91: styles/
92: ```
93: 
94: Each directory should have a single responsibility.
95: 
96: ---
97: 
98: # Python Version
99: 
100: Python 3.12+
101: 
102: All code should support strict type checking.
103: 
104: ---
105: 
106: # Formatting
107: 
108: Use
109: 
110: Black
111: 
112: isort
113: 
114: Ruff
115: 
116: No custom formatting rules.
117: 
118: ---
119: 
120: # Typing
121: 
122: Every function must include type hints.
123: 
124: Good
125: 
126: ```python
127: def create_patient(patient: PatientCreate) -> Patient:
128: ```
129: 
130: Avoid
131: 
132: ```python
133: def create_patient(patient):
134: ```
135: 
136: Return types are always required.
137: 
138: ---
139: 
140: # Docstrings
141: 
142: Public modules, classes, and functions require docstrings.
143: 
144: Example
145: 
146: ```python
147: class ConsentService:
148:     """
149:     Handles creation, approval, expiration,
150:     and auditing of patient consent requests.
151:     """
152: ```
153: 
154: Avoid redundant docstrings that merely repeat the function name.
155: 
156: ---
157: 
158: # Dependency Injection
159: 
160: Always inject dependencies.
161: 
162: Good
163: 
164: ```python
165: class PatientService:
166: 
167:     def __init__(
168:         self,
169:         repository: PatientRepository,
170:         notifier: NotificationProvider
171:     ):
172:         ...
173: ```
174: 
175: Avoid
176: 
177: ```python
178: repo = PatientRepository()
179: ```
180: 
181: inside services.
182: 
183: ---
184: 
185: # Layered Architecture
186: 
187: Controllers (FastAPI Routes)
188: 
189: ↓
190: 
191: Services
192: 
193: ↓
194: 
195: Repositories
196: 
197: ↓
198: 
199: Database
200: 
201: Controllers should contain almost no business logic.
202: 
203: Repositories should never contain business rules.
204: 
205: Business rules belong inside services.
206: 
207: ---
208: 
209: # Repository Pattern
210: 
211: Repositories are responsible only for persistence.
212: 
213: Example
214: 
215: ```python
216: PatientRepository
217: 
218: VisitRepository
219: 
220: ConsentRepository
221: ```
222: 
223: Repositories should never:
224: 
225: - Send notifications
226: - Call AI providers
227: - Perform authorization
228: - Contain business workflows
229: 
230: ---
231: 
232: # Service Layer
233: 
234: Services coordinate application behaviour.
235: 
236: Examples
237: 
238: ```
239: ConsentService
240: 
241: ConsultationService
242: 
243: NotificationService
244: 
245: TimelineService
246: 
247: MedicalRecordService
248: ```
249: 
250: Services may call multiple repositories and providers.
251: 
252: ---
253: 
254: # Provider Pattern
255: 
256: External integrations must always be abstracted.
257: 
258: Example
259: 
260: ```
261: DiagnosisProvider
262: 
263: EmailProvider
264: 
265: StorageProvider
266: 
267: NotificationProvider
268: 
269: SymptomCheckerProvider
270: 
271: TranscriptionProvider
272: ```
273: 
274: Concrete implementations belong inside
275: 
276: ```
277: providers/implementations/
278: ```
279: 
280: Business logic imports interfaces only.
281: 
282: ---
283: 
284: # Error Handling
285: 
286: Raise domain-specific exceptions.
287: 
288: Example
289: 
290: ```
291: ConsentRequiredError
292: 
293: PatientNotFoundError
294: 
295: ProviderUnavailableError
296: ```
297: 
298: Avoid generic Exception.
299: 
300: Errors should be translated into HTTP responses by middleware.
301: 
302: ---
303: 
304: # Logging
305: 
306: Use structured logging.
307: 
308: Every log entry should include
309: 
310: ```
311: request_id
312: 
313: user_id
314: 
315: action
316: 
317: duration
318: 
319: status
320: ```
321: 
322: Avoid print statements.
323: 
324: ---
325: 
326: # Configuration
327: 
328: Environment variables should be accessed only through a configuration module.
329: 
330: Good
331: 
332: ```python
333: settings.jwt_secret
334: ```
335: 
336: Avoid
337: 
338: ```python
339: os.getenv(...)
340: ```
341: 
342: throughout the application.
343: 
344: ---
345: 
346: # Database Access
347: 
348: Use SQLAlchemy ORM.
349: 
350: Avoid raw SQL unless performance requires it.
351: 
352: Database sessions should be request-scoped.
353: 
354: Never expose ORM models directly through the API.
355: 
356: Always map models to Pydantic schemas.
357: 
358: ---
359: 
360: # Transactions
361: 
362: Business operations involving multiple writes should execute inside a transaction.
363: 
364: Examples
365: 
366: - Consent approval
367: - Consultation completion
368: - Medical record updates
369: 
370: Partial failures should roll back automatically.
371: 
372: ---
373: 
374: # Background Tasks
375: 
376: Long-running work should execute asynchronously.
377: 
378: Examples
379: 
380: - AI summaries
381: - Email delivery
382: - Notification fan-out
383: - File processing
384: 
385: Prefer Celery or RQ with Redis.
386: 
387: The application should remain responsive while background work executes.
388: 
389: ---
390: 
391: # Security
392: 
393: Never log:
394: 
395: - Passwords
396: - JWTs
397: - Refresh tokens
398: - Medical information
399: - API keys
400: 
401: Sensitive configuration belongs in environment variables.
402: 
403: Passwords should always be hashed using Argon2 or bcrypt.
404: 
405: JWT signing keys must never be committed to source control.
406: 
407: ---
408: 
409: # API Design
410: 
411: Every endpoint should:
412: 
413: - Validate input
414: - Authorize access
415: - Return standardized responses
416: - Use appropriate HTTP status codes
417: - Include OpenAPI documentation
418: 
419: Avoid inconsistent response formats.
420: 
421: ---
422: 
423: # Database Migrations
424: 
425: Use Alembic exclusively.
426: 
427: Never modify an existing migration after it has been applied.
428: 
429: Each migration should represent one logical schema change.
430: 
431: ---
432: 
433: # Testing Philosophy
434: 
435: Prefer behavioural testing over implementation testing.
436: 
437: Test:
438: 
439: - Public APIs
440: - Service behaviour
441: - Repository queries
442: - Permission checks
443: - Consent workflow
444: - AI provider abstraction
445: 
446: Avoid testing private helper methods directly.
447: 
448: # Frontend Standards
449: 
450: ---
451: 
452: # Framework
453: 
454: The frontend should use:
455: 
456: - Next.js (App Router)
457: - TypeScript (strict mode)
458: - TailwindCSS
459: - Framer Motion
460: - React Query (TanStack Query)
461: - React Hook Form
462: - Zod
463: 
464: No page should depend directly on backend implementation details.
465: 
466: API communication should occur through dedicated service modules.
467: 
468: ---
469: 
470: # Folder Organization
471: 
472: Feature-first architecture is preferred.
473: 
474: Example
475: 
476: ```
477: features/
478: 
479:     authentication/
480: 
481:     consultation/
482: 
483:     consent/
484: 
485:     notifications/
486: 
487:     patient/
488: 
489:     doctor/
490: 
491:     timeline/
492: ```
493: 
494: Each feature should contain:
495: 
496: ```
497: components/
498: 
499: hooks/
500: 
501: services/
502: 
503: types/
504: 
505: utils/
506: ```
507: 
508: Avoid placing unrelated components in a shared directory.
509: 
510: ---
511: 
512: # Component Design
513: 
514: Components should have a single responsibility.
515: 
516: Prefer small composable components over large monolithic ones.
517: 
518: Good
519: 
520: ```
521: PatientHeader
522: 
523: PatientSummaryCard
524: 
525: TimelineItem
526: 
527: ConsentBanner
528: 
529: VisitCard
530: 
531: NotificationList
532: ```
533: 
534: Avoid
535: 
536: ```
537: PatientDashboardEverything.tsx
538: ```
539: 
540: ---
541: 
542: # Props
543: 
544: Always define explicit interfaces.
545: 
546: Example
547: 
548: ```typescript
549: interface VisitCardProps {
550:     visit: Visit
551:     onSelect: (visitId: string) => void
552: }
553: ```
554: 
555: Avoid `any`.
556: 
557: ---
558: 
559: # State Management
560: 
561: Use local state whenever possible.
562: 
563: Recommended order:
564: 
565: 1. Local component state
566: 2. React Context
567: 3. React Query cache
568: 4. URL state
569: 
570: Avoid introducing global state libraries unless there is a clear architectural benefit.
571: 
572: ---
573: 
574: # Server State
575: 
576: All backend data should be managed through React Query.
577: 
578: Benefits:
579: 
580: - Caching
581: - Automatic refetching
582: - Background updates
583: - Retry policies
584: - Optimistic updates
585: 
586: Avoid manually managing server state with `useState`.
587: 
588: ---
589: 
590: # Forms
591: 
592: All forms should use:
593: 
594: React Hook Form
595: 
596: Validation:
597: 
598: Zod
599: 
600: Validation logic should never be duplicated between frontend and backend.
601: 
602: ---
603: 
604: # API Layer
605: 
606: Never call `fetch()` directly inside components.
607: 
608: Instead:
609: 
610: ```
611: Component
612: 
613: ↓
614: 
615: Hook
616: 
617: ↓
618: 
619: API Client
620: 
621: ↓
622: 
623: Backend
624: ```
625: 
626: Example
627: 
628: ```
629: usePatientTimeline()
630: 
631: ↓
632: 
633: timelineService.getTimeline()
634: 
635: ↓
636: 
637: ApiClient
638: ```
639: 
640: This centralizes authentication, retries, error handling, and request logging.
641: 
642: ---
643: 
644: # Styling
645: 
646: TailwindCSS only.
647: 
648: Avoid inline styles except for dynamically calculated values.
649: 
650: Use design tokens for:
651: 
652: - Colors
653: - Spacing
654: - Typography
655: - Border radius
656: - Shadows
657: 
658: Do not hardcode colors throughout the application.
659: 
660: ---
661: 
662: # Mobile Patient Application
663: 
664: The patient application must always render inside the `PhoneFrame` component.
665: 
666: Patient screens should assume a fixed viewport.
667: 
668: Never implement responsive breakpoints inside patient-specific components.
669: 
670: The `PhoneFrame` is responsible for scaling.
671: 
672: ---
673: 
674: # Doctor Portal
675: 
676: The doctor portal is desktop-first.
677: 
678: Focus on:
679: 
680: - Information density
681: - Readability
682: - Fast navigation
683: - Keyboard accessibility
684: - Multi-panel layouts
685: 
686: Avoid unnecessarily large spacing that reduces usable screen area.
687: 
688: ---
689: 
690: # Animation Standards
691: 
692: Animations should communicate state changes, not decorate the interface.
693: 
694: Use Framer Motion for:
695: 
696: - Page transitions
697: - Bottom sheets
698: - Dialogs
699: - Loading states
700: - Shared element transitions
701: 
702: Preferred spring:
703: 
704: ```typescript
705: const spring = {
706:     type: "spring",
707:     stiffness: 380,
708:     damping: 32
709: }
710: ```
711: 
712: Avoid long or distracting animations.
713: 
714: ---
715: 
716: # Loading States
717: 
718: Every asynchronous operation should expose a loading state.
719: 
720: Preferred patterns:
721: 
722: - Skeleton placeholders
723: - Spinner for short operations
724: - Progressive rendering
725: - Optimistic updates where appropriate
726: 
727: Avoid blank screens.
728: 
729: ---
730: 
731: # Error States
732: 
733: Every API request should gracefully handle:
734: 
735: - Network failures
736: - Validation errors
737: - Authentication failures
738: - Provider outages
739: 
740: Users should always receive actionable feedback.
741: 
742: ---
743: 
744: # Empty States
745: 
746: Every list should define an empty state.
747: 
748: Example
749: 
750: ```
751: No consultations yet.
752: 
753: No notifications.
754: 
755: No medical history available.
756: ```
757: 
758: Avoid rendering empty containers.
759: 
760: ---
761: 
762: # Accessibility
763: 
764: Minimum requirements:
765: 
766: - Keyboard navigation
767: - Visible focus indicators
768: - Semantic HTML
769: - Accessible form labels
770: - ARIA attributes where appropriate
771: - Sufficient color contrast
772: 
773: Accessibility is required, not optional.
774: 
775: ---
776: 
777: # Icons
778: 
779: Use Lucide React consistently.
780: 
781: Avoid mixing icon libraries.
782: 
783: ---
784: 
785: # Testing Standards
786: 
787: Backend
788: 
789: pytest
790: 
791: Frontend
792: 
793: Vitest
794: 
795: React Testing Library
796: 
797: End-to-end
798: 
799: Playwright
800: 
801: Priority workflows:
802: 
803: - Login
804: - Demo mode
805: - Consent approval
806: - Consultation flow
807: - Timeline updates
808: - AI session
809: - Notifications
810: - Split-screen synchronization
811: 
812: ---
813: 
814: # Git Conventions
815: 
816: Branch naming
817: 
818: ```
819: feature/consent-workflow
820: 
821: feature/doctor-dashboard
822: 
823: fix/notification-refresh
824: 
825: refactor/provider-abstractions
826: ```
827: 
828: Commit format
829: 
830: ```
831: feat:
832: 
833: fix:
834: 
835: refactor:
836: 
837: docs:
838: 
839: test:
840: 
841: chore:
842: ```
843: 
844: Examples
845: 
846: ```
847: feat: implement consent approval workflow
848: 
849: fix: resolve timeline sorting issue
850: 
851: refactor: abstract transcription provider
852: ```
853: 
854: ---
855: 
856: # Code Review Checklist
857: 
858: Every pull request should answer:
859: 
860: - Does it follow the architecture?
861: - Does it introduce duplicate logic?
862: - Are interfaces respected?
863: - Are provider abstractions maintained?
864: - Are tests included?
865: - Is documentation updated?
866: - Are loading and error states handled?
867: - Is the feature accessible?
868: - Does it introduce unnecessary complexity?
869: 
870: Code should be easy to understand without external explanation.
871: 
872: ---
873: 
874: # Performance Guidelines
875: 
876: Prefer:
877: 
878: - Lazy loading
879: - Code splitting
880: - Memoization when justified
881: - Pagination
882: - Incremental rendering
883: - Efficient database queries
884: 
885: Avoid premature optimization.
886: 
887: Profile before optimizing complex code paths.
888: 
889: ---
890: 
891: # Security Guidelines
892: 
893: Validate all user input.
894: 
895: Escape rendered content where appropriate.
896: 
897: Protect all authenticated routes.
898: 
899: Never expose secrets in the frontend bundle.
900: 
901: Use HTTPS in production.
902: 
903: Sanitize uploaded file metadata.
904: 
905: Treat all client input as untrusted.
906: 
907: ---
908: 
909: # Documentation Standards
910: 
911: Every major module should include:
912: 
913: - Purpose
914: - Responsibilities
915: - Extension points
916: - Dependencies
917: 
918: Complex business rules should explain *why* they exist.
919: 
920: Public APIs should include OpenAPI documentation and examples.
921: 
922: ---
923: 
924: # Definition of Done
925: 
926: A feature is complete only when:
927: 
928: - Requirements from the Product Requirements Document are satisfied.
929: - Code follows the architecture.
930: - Unit tests pass.
931: - Integration tests pass (where applicable).
932: - Documentation is updated.
933: - Loading, empty, and error states are implemented.
934: - Accessibility requirements are met.
935: - Logging is in place for important operations.
936: - No TODOs or placeholder implementations remain.
937: - Code has been reviewed for consistency.
938: 
939: ---
940: 
941: # Repository Quality Checklist
942: 
943: Before considering the repository production-ready, verify:
944: 
945: ✓ Docker Compose starts the full stack.
946: 
947: ✓ Backend passes health checks.
948: 
949: ✓ Database migrations apply successfully.
950: 
951: ✓ Seed data loads without errors.
952: 
953: ✓ Demo Mode works.
954: 
955: ✓ JWT authentication works.
956: 
957: ✓ Patient application renders correctly inside the PhoneFrame.
958: 
959: ✓ Doctor dashboard supports the complete consultation workflow.
960: 
961: ✓ Real-time consent synchronization functions correctly.
962: 
963: ✓ AI providers are fully abstracted.
964: 
965: ✓ Existing Symptom Checker integrates through the provider interface.
966: 
967: ✓ Notifications update in real time.
968: 
969: ✓ Audit logs capture all sensitive operations.
970: 
971: ✓ Test suite passes.
972: 
973: ✓ Documentation is complete.
974: 
975: ✓ Environment variables are documented.
976: 
977: ✓ No placeholder code remains.
978: 
979: ---
980: 
981: # Engineering Principle
982: 
983: Every line of code should make the repository easier to understand, easier to maintain, and easier to extend.
984: 
985: Optimize for the engineer who will read this code six months from now, not the engineer writing it today.
986: 
987: # End of Coding Standards

(End of file - total 987 lines)
</content>
```

---

## Assistant (Plan · Kimi · 6.4s)

_Thinking:_

 Now I have a comprehensive understanding of the project. Let me assess the current state of the repository to understand what's already implemented vs what needs to be built.

 Now I have a thorough understanding of the project. Let me check the current state of the repository to see what exists. 

**Tool: glob**

**Input:**
```json
{
  "pattern": "**/*",
  "path": "/Users/sheltonmutambirwa/Desktop/medic"
}
```

**Output:**
```
/Users/sheltonmutambirwa/Desktop/medic/docs/11_User_Flows_and_State_Machines.md
/Users/sheltonmutambirwa/Desktop/medic/docs/10_UI_Screen_Specification.md
/Users/sheltonmutambirwa/Desktop/medic/docs/wireframes.html
/Users/sheltonmutambirwa/Desktop/medic/docs/04_Implementation_Plan.md
/Users/sheltonmutambirwa/Desktop/medic/docs/00_Project_Index.md
/Users/sheltonmutambirwa/Desktop/medic/AGENTS.md
/Users/sheltonmutambirwa/Desktop/medic/docs/09_Deployment_Guide.md
/Users/sheltonmutambirwa/Desktop/medic/docs/08_Coding_Standards.md
/Users/sheltonmutambirwa/Desktop/medic/docs/06_Database_Schema.md
/Users/sheltonmutambirwa/Desktop/medic/docs/05_API_Contract.md
/Users/sheltonmutambirwa/Desktop/medic/docs/07_Master_Generation_Prompt.md
/Users/sheltonmutambirwa/Desktop/medic/docs/03_Design_System.md
/Users/sheltonmutambirwa/Desktop/medic/docs/02_Technical_Architecture.md
/Users/sheltonmutambirwa/Desktop/medic/docs/01_Product_Requirements_Document.md
/Users/sheltonmutambirwa/Desktop/medic/.git/index
/Users/sheltonmutambirwa/Desktop/medic/app/services/gap_analysis.py
/Users/sheltonmutambirwa/Desktop/medic/app/services/orchestrator.py
/Users/sheltonmutambirwa/Desktop/medic/app/services/summarizer.py
/Users/sheltonmutambirwa/Desktop/medic/app/services/question_gen.py
/Users/sheltonmutambirwa/Desktop/medic/frontend/app/lib/types.ts
/Users/sheltonmutambirwa/Desktop/medic/app/api/routes.py
/Users/sheltonmutambirwa/Desktop/medic/app/api/responses.py
/Users/sheltonmutambirwa/Desktop/medic/requirements.txt
/Users/sheltonmutambirwa/Desktop/medic/frontend/tsconfig.json
/Users/sheltonmutambirwa/Desktop/medic/frontend/tailwind.config.js
/Users/sheltonmutambirwa/Desktop/medic/frontend/postcss.config.js
/Users/sheltonmutambirwa/Desktop/medic/frontend/package.json
/Users/sheltonmutambirwa/Desktop/medic/frontend/package-lock.json
/Users/sheltonmutambirwa/Desktop/medic/frontend/app/page.tsx
/Users/sheltonmutambirwa/Desktop/medic/frontend/app/privacy/page.tsx
/Users/sheltonmutambirwa/Desktop/medic/frontend/next.config.js
/Users/sheltonmutambirwa/Desktop/medic/frontend/app/settings/page.tsx
/Users/sheltonmutambirwa/Desktop/medic/frontend/app/not-found.tsx
/Users/sheltonmutambirwa/Desktop/medic/frontend/app/login/page.tsx
/Users/sheltonmutambirwa/Desktop/medic/frontend/app/lib/auth.ts
/Users/sheltonmutambirwa/Desktop/medic/frontend/app/lib/api.ts
/Users/sheltonmutambirwa/Desktop/medic/frontend/app/layout.tsx
/Users/sheltonmutambirwa/Desktop/medic/frontend/app/globals.css
/Users/sheltonmutambirwa/Desktop/medic/frontend/app/components/Header.tsx
/Users/sheltonmutambirwa/Desktop/medic/frontend/app/contact/page.tsx
/Users/sheltonmutambirwa/Desktop/medic/frontend/app/about/page.tsx
/Users/sheltonmutambirwa/Desktop/medic/frontend/app/chat/page.tsx
/Users/sheltonmutambirwa/Desktop/medic/frontend/app/components/Footer.tsx
/Users/sheltonmutambirwa/Desktop/medic/frontend/Dockerfile
/Users/sheltonmutambirwa/Desktop/medic/frontend/.gitignore
/Users/sheltonmutambirwa/Desktop/medic/frontend/.dockerignore
/Users/sheltonmutambirwa/Desktop/medic/frontend/.env.local
/Users/sheltonmutambirwa/Desktop/medic/docker-compose.yml
/Users/sheltonmutambirwa/Desktop/medic/app/services/input_processor.py
/Users/sheltonmutambirwa/Desktop/medic/app/services/decision_engine.py
/Users/sheltonmutambirwa/Desktop/medic/app/services/__init__.py
/Users/sheltonmutambirwa/Desktop/medic/app/services/answer_gen.py
/Users/sheltonmutambirwa/Desktop/medic/app/services/assessment.py
/Users/sheltonmutambirwa/Desktop/medic/app/main.py
/Users/sheltonmutambirwa/Desktop/medic/app/db/repositories.py
/Users/sheltonmutambirwa/Desktop/medic/app/db/postgres.py
/Users/sheltonmutambirwa/Desktop/medic/app/api/contact.py
/Users/sheltonmutambirwa/Desktop/medic/app/api/deps.py
/Users/sheltonmutambirwa/Desktop/medic/app/api/chat_sessions.py
/Users/sheltonmutambirwa/Desktop/medic/app/api/auth.py
/Users/sheltonmutambirwa/Desktop/medic/README.md
/Users/sheltonmutambirwa/Desktop/medic/app/api/__init__.py
/Users/sheltonmutambirwa/Desktop/medic/.gitignore
/Users/sheltonmutambirwa/Desktop/medic/Dockerfile
/Users/sheltonmutambirwa/Desktop/medic/.dockerignore
/Users/sheltonmutambirwa/Desktop/medic/.env.example
/Users/sheltonmutambirwa/Desktop/medic/.env
/Users/sheltonmutambirwa/Desktop/medic/app/api/__pycache__/routes.cpython-312.pyc
/Users/sheltonmutambirwa/Desktop/medic/app/api/__pycache__/deps.cpython-312.pyc
/Users/sheltonmutambirwa/Desktop/medic/app/api/__pycache__/contact.cpython-312.pyc
/Users/sheltonmutambirwa/Desktop/medic/app/api/__pycache__/sessions.cpython-312.pyc
/Users/sheltonmutambirwa/Desktop/medic/app/api/__pycache__/auth.cpython-312.pyc
/Users/sheltonmutambirwa/Desktop/medic/.git/opencode
/Users/sheltonmutambirwa/Desktop/medic/.git/config
/Users/sheltonmutambirwa/Desktop/medic/.git/refs/heads/main
/Users/sheltonmutambirwa/Desktop/medic/.git/logs/refs/heads/main
/Users/sheltonmutambirwa/Desktop/medic/.git/logs/HEAD
/Users/sheltonmutambirwa/Desktop/medic/.git/logs/refs/remotes/origin/HEAD
/Users/sheltonmutambirwa/Desktop/medic/.git/HEAD
/Users/sheltonmutambirwa/Desktop/medic/.git/packed-refs
/Users/sheltonmutambirwa/Desktop/medic/.git/refs/remotes/origin/HEAD
/Users/sheltonmutambirwa/Desktop/medic/.git/objects/pack/pack-ba9b15a7b95e81e63b77accba1475dd84127eec9.rev
/Users/sheltonmutambirwa/Desktop/medic/.git/objects/pack/pack-ba9b15a7b95e81e63b77accba1475dd84127eec9.idx
/Users/sheltonmutambirwa/Desktop/medic/.git/objects/pack/pack-ba9b15a7b95e81e63b77accba1475dd84127eec9.pack
/Users/sheltonmutambirwa/Desktop/medic/.git/hooks/push-to-checkout.sample
/Users/sheltonmutambirwa/Desktop/medic/.git/hooks/update.sample
/Users/sheltonmutambirwa/Desktop/medic/.git/hooks/pre-push.sample
/Users/sheltonmutambirwa/Desktop/medic/.git/hooks/pre-applypatch.sample
/Users/sheltonmutambirwa/Desktop/medic/.git/hooks/pre-merge-commit.sample
/Users/sheltonmutambirwa/Desktop/medic/.git/hooks/post-update.sample
/Users/sheltonmutambirwa/Desktop/medic/.git/hooks/prepare-commit-msg.sample
/Users/sheltonmutambirwa/Desktop/medic/.git/hooks/pre-receive.sample
/Users/sheltonmutambirwa/Desktop/medic/.git/hooks/fsmonitor-watchman.sample
/Users/sheltonmutambirwa/Desktop/medic/.git/hooks/applypatch-msg.sample
/Users/sheltonmutambirwa/Desktop/medic/.git/hooks/pre-commit.sample
/Users/sheltonmutambirwa/Desktop/medic/.git/hooks/sendemail-validate.sample
/Users/sheltonmutambirwa/Desktop/medic/.git/hooks/pre-rebase.sample
/Users/sheltonmutambirwa/Desktop/medic/.git/hooks/commit-msg.sample
/Users/sheltonmutambirwa/Desktop/medic/.git/description
/Users/sheltonmutambirwa/Desktop/medic/.git/info/exclude

(Results are truncated: showing first 100 results. Consider using a more specific path or pattern.)
```

---

## Assistant (Plan · Kimi · 6.5s)

_Thinking:_

 Now I have a clear picture of the project. Let me understand what exists and what needs to be built:

**Current state:**
- Some backend files exist: `app/api/`, `app/services/`, `app/db/`, `app/main.py`, `Dockerfile`, `docker-compose.yml`
- Frontend exists: `frontend/app/` with some pages but it's a basic Next.js setup, NOT the Mirage implementation
- Documentation is complete in `docs/`
- The existing code appears to be from a previous project (basic chat/symptom checker app) and does NOT match the Mirage documentation

**What needs to happen:**
According to the Implementation Plan (docs/04_Implementation_Plan.md), there are 24 phases. The existing code barely covers phase 1-2 partially (some docker, some backend).

Let me check the existing key files to see what's there more carefully.

 

**Tool: read**

**Input:**
```json
{
  "filePath": "/Users/sheltonmutambirwa/Desktop/medic/app/main.py"
}
```

**Output:**
```
<path>/Users/sheltonmutambirwa/Desktop/medic/app/main.py</path>
<type>file</type>
<content>
1: from fastapi import FastAPI
2: from fastapi.middleware.cors import CORSMiddleware
3: from contextlib import asynccontextmanager
4: from app.api import routes
5: from app.core.config import settings
6: from app.db.mongodb import db_client
7: from app.db.postgres import init_db, close_db
8: from app.core.logger import logger
9: 
10: @asynccontextmanager
11: async def lifespan(app: FastAPI):
12:     logger.info("Starting up Medical QA System...")
13:     db_client.connect()
14:     await init_db()
15:     yield
16:     logger.info("Shutting down Medical QA System...")
17:     db_client.close()
18:     await close_db()
19: 
20: app = FastAPI(
21:     title="Medical QA System",
22:     description="Interactive Medical Question Answering System with Self-Consistency and Abstention",
23:     version="1.0.0",
24:     lifespan=lifespan
25: )
26: 
27: app.add_middleware(
28:     CORSMiddleware,
29:     allow_origins=["http://localhost:3000"],
30:     allow_credentials=True,
31:     allow_methods=["*"],
32:     allow_headers=["*"],
33: )
34: 
35: app.include_router(routes.router, prefix="/api")
36: 
37: if __name__ == "__main__":
38:     import uvicorn
39:     uvicorn.run("app.main:app", host=settings.API_HOST, port=settings.API_PORT, reload=True)

(End of file - total 39 lines)
</content>
```

**Tool: read**

**Input:**
```json
{
  "filePath": "/Users/sheltonmutambirwa/Desktop/medic/docker-compose.yml"
}
```

**Output:**
```
<path>/Users/sheltonmutambirwa/Desktop/medic/docker-compose.yml</path>
<type>file</type>
<content>
1: services:
2:   frontend:
3:     build:
4:       context: ./frontend
5:       dockerfile: Dockerfile
6:     ports:
7:       - "3000:3000"
8:     environment:
9:       - NEXT_PUBLIC_API_URL=http://localhost:8000
10:     depends_on:
11:       - app
12:     restart: unless-stopped
13:     networks:
14:       - medic-network
15: 
16:   app:
17:     build: .
18:     ports:
19:       - "8000:8000"
20:     env_file:
21:       - .env
22:     environment:
23:       - MONGODB_URI=mongodb://mongodb:27017
24:       - POSTGRES_URL=postgresql+asyncpg://medic_user:${POSTGRES_PASSWORD}@postgres:5432/medic_auth
25:       - JWT_SECRET=${JWT_SECRET}
26:       - JWT_EXPIRY_HOURS=${JWT_EXPIRY_HOURS:-24}
27:       - CORS_ORIGINS=http://localhost:3000
28:     depends_on:
29:       mongodb:
30:         condition: service_healthy
31:       postgres:
32:         condition: service_healthy
33:     restart: unless-stopped
34:     networks:
35:       - medic-network
36:     healthcheck:
37:       test: ["CMD", "curl", "-f", "http://localhost:8000/docs"]
38:       interval: 30s
39:       timeout: 10s
40:       retries: 3
41:       start_period: 10s
42: 
43:   mongodb:
44:     image: mongo:7.0
45:     ports:
46:       - "27017:27017"
47:     volumes:
48:       - mongodb_data:/data/db
49:     healthcheck:
50:       test: ["CMD", "mongosh", "--eval", "db.adminCommand('ping')"]
51:       interval: 10s
52:       timeout: 5s
53:       retries: 5
54:       start_period: 10s
55:     restart: unless-stopped
56:     networks:
57:       - medic-network
58: 
59:   postgres:
60:     image: postgres:16-alpine
61:     environment:
62:       POSTGRES_USER: medic_user
63:       POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
64:       POSTGRES_DB: medic_auth
65:     volumes:
66:       - postgres_data:/var/lib/postgresql/data
67:     healthcheck:
68:       test: ["CMD-SHELL", "pg_isready -U medic_user"]
69:       interval: 10s
70:       timeout: 5s
71:       retries: 5
72:       start_period: 10s
73:     restart: unless-stopped
74:     networks:
75:       - medic-network
76: 
77: volumes:
78:   mongodb_data:
79:     driver: local
80:   postgres_data:
81:     driver: local
82: 
83: networks:
84:   medic-network:
85:     driver: bridge

(End of file - total 85 lines)
</content>
```

**Tool: read**

**Input:**
```json
{
  "filePath": "/Users/sheltonmutambirwa/Desktop/medic/frontend/app/page.tsx"
}
```

**Output:**
```
<path>/Users/sheltonmutambirwa/Desktop/medic/frontend/app/page.tsx</path>
<type>file</type>
<content>
1: import Link from 'next/link'
2: 
3: export default function LandingPage() {
4:   return (
5:     <div className="min-h-[calc(100vh-4rem)]">
6:       {/* Hero Section */}
7:       <section className="bg-primary text-white py-20 px-4">
8:         <div className="max-w-7xl mx-auto text-center">
9:           <h1 className="text-4xl md:text-5xl font-heading font-bold mb-6">
10:             Your Personal AI Medical Assistant
11:           </h1>
12:           <p className="text-xl md:text-2xl mb-8 max-w-3xl mx-auto text-white text-opacity-90">
13:             Get instant medical assessments and guidance from our AI-powered health assistant. 
14:             Professional, private, and available 24/7.
15:           </p>
16:           <div className="flex flex-col sm:flex-row gap-4 justify-center">
17:             <Link
18:               href="/login"
19:               className="bg-accent hover:bg-accent-dark text-white px-8 py-4 rounded-md text-lg font-medium transition-colors"
20:             >
21:               Start Consultation
22:             </Link>
23:             <Link
24:               href="/about"
25:               className="bg-white hover:bg-secondary text-primary px-8 py-4 rounded-md text-lg font-medium transition-colors"
26:             >
27:               Learn More
28:             </Link>
29:           </div>
30:         </div>
31:       </section>
32: 
33:       {/* Features Section */}
34:       <section className="py-20 px-4 bg-secondary">
35:         <div className="max-w-7xl mx-auto">
36:           <h2 className="text-3xl font-heading font-bold text-center text-text mb-12">
37:             Why Choose mediQAL?
38:           </h2>
39:           <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
40:             <div className="bg-white p-8 rounded-lg shadow-sm">
41:               <div className="w-12 h-12 bg-primary rounded-lg flex items-center justify-center mb-4">
42:                 <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
43:                   <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
44:                 </svg>
45:               </div>
46:               <h3 className="text-xl font-semibold text-text mb-3">Available 24/7</h3>
47:               <p className="text-text-muted">
48:                 Get medical guidance anytime, day or night. No appointments needed, no waiting rooms.
49:               </p>
50:             </div>
51: 
52:             <div className="bg-white p-8 rounded-lg shadow-sm">
53:               <div className="w-12 h-12 bg-primary rounded-lg flex items-center justify-center mb-4">
54:                 <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
55:                   <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
56:                 </svg>
57:               </div>
58:               <h3 className="text-xl font-semibold text-text mb-3">Private & Secure</h3>
59:               <p className="text-text-muted">
60:                 Your health information is protected with enterprise-grade security. We value your privacy.
61:               </p>
62:             </div>
63: 
64:             <div className="bg-white p-8 rounded-lg shadow-sm">
65:               <div className="w-12 h-12 bg-primary rounded-lg flex items-center justify-center mb-4">
66:                 <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
67:                   <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
68:                 </svg>
69:               </div>
70:               <h3 className="text-xl font-semibold text-text mb-3">AI-Powered Accuracy</h3>
71:               <p className="text-text-muted">
72:                 Advanced AI technology provides thoughtful, evidence-based medical questions and guidance.
73:               </p>
74:             </div>
75:           </div>
76:         </div>
77:       </section>
78: 
79:       {/* How It Works Section */}
80:       <section className="py-20 px-4 bg-white">
81:         <div className="max-w-7xl mx-auto">
82:           <h2 className="text-3xl font-heading font-bold text-center text-text mb-12">
83:             How mediQAL Works
84:           </h2>
85:           <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
86:             <div className="text-center">
87:               <div className="w-16 h-16 bg-primary text-white rounded-full flex items-center justify-center text-2xl font-bold mx-auto mb-4">
88:                 1
89:               </div>
90:               <h3 className="text-xl font-semibold text-text mb-3">Sign In</h3>
91:               <p className="text-text-muted">
92:                 Enter your email to create your secure account. No password needed.
93:               </p>
94:             </div>
95: 
96:             <div className="text-center">
97:               <div className="w-16 h-16 bg-primary text-white rounded-full flex items-center justify-center text-2xl font-bold mx-auto mb-4">
98:                 2
99:               </div>
100:               <h3 className="text-xl font-semibold text-text mb-3">Describe Symptoms</h3>
101:               <p className="text-text-muted">
102:                 Tell us about your symptoms or health concerns in your own words.
103:               </p>
104:             </div>
105: 
106:             <div className="text-center">
107:               <div className="w-16 h-16 bg-primary text-white rounded-full flex items-center justify-center text-2xl font-bold mx-auto mb-4">
108:                 3
109:               </div>
110:               <h3 className="text-xl font-semibold text-text mb-3">Get Guidance</h3>
111:               <p className="text-text-muted">
112:                 Receive thoughtful questions and medical insights to help you understand your condition.
113:               </p>
114:             </div>
115:           </div>
116:         </div>
117:       </section>
118: 
119:       {/* CTA Section */}
120:       <section className="py-20 px-4 bg-secondary">
121:         <div className="max-w-4xl mx-auto text-center">
122:           <h2 className="text-3xl font-heading font-bold text-text mb-6">
123:             Ready to Get Started?
124:           </h2>
125:           <p className="text-xl text-text-muted mb-8">
126:             Join thousands of users who trust mediQAL for their medical consultations.
127:           </p>
128:           <Link
129:             href="/login"
130:             className="inline-block bg-primary hover:bg-primary-dark text-white px-8 py-4 rounded-md text-lg font-medium transition-colors"
131:           >
132:             Start Your Consultation Now
133:           </Link>
134:         </div>
135:       </section>
136:     </div>
137:   )
138: }

(End of file - total 138 lines)
</content>
```

**Tool: read**

**Input:**
```json
{
  "filePath": "/Users/sheltonmutambirwa/Desktop/medic/frontend/package.json"
}
```

**Output:**
```
<path>/Users/sheltonmutambirwa/Desktop/medic/frontend/package.json</path>
<type>file</type>
<content>
1: {
2:   "name": "mediqal-frontend",
3:   "version": "1.0.0",
4:   "private": true,
5:   "scripts": {
6:     "dev": "next dev -p 3001",
7:     "build": "next build",
8:     "start": "next start",
9:     "lint": "next lint"
10:   },
11:   "dependencies": {
12:     "next": "14.2.5",
13:     "react": "18.3.1",
14:     "react-dom": "18.3.1",
15:     "axios": "1.7.2",
16:     "@tanstack/react-query": "5.51.21",
17:     "zod": "3.23.8",
18:     "react-hook-form": "7.52.1",
19:     "date-fns": "3.6.0"
20:   },
21:   "devDependencies": {
22:     "@types/node": "20.14.10",
23:     "@types/react": "18.3.3",
24:     "@types/react-dom": "18.3.0",
25:     "typescript": "5.5.4",
26:     "tailwindcss": "3.4.7",
27:     "postcss": "8.4.39",
28:     "autoprefixer": "10.4.19",
29:     "eslint": "8.57.0",
30:     "eslint-config-next": "14.2.5"
31:   }
32: }

(End of file - total 32 lines)
</content>
```

---

## Assistant (Plan · Kimi · 13.2s)

_Thinking:_

 Now I understand the current state. The repository has:

1. **Backend** (`/app/`): An existing FastAPI app for a "Medical QA System" (mediQAL) with:
   - MongoDB + PostgreSQL
   - Authentication, chat sessions, contact
   - Services: gap_analysis, orchestrator, summarizer, question_gen, input_processor, decision_engine, answer_gen, assessment
   - Not following the Mirage architecture yet

2. **Frontend** (`/frontend/`): A basic Next.js landing page for mediQAL with:
   - Simple pages: landing, login, chat, about, contact, privacy, settings
   - No PhoneFrame, no patient app, no doctor portal
   - Missing: Framer Motion, React Query setup, proper features

3. **Docs**: Full Mirage documentation

**The task is to transform this existing mediQAL app INTO the Mirage platform as defined in the docs.**

Now let me create a comprehensive plan with subagents. According to the Implementation Plan, there are 24 phases. I need to group these into logical subagent tasks.

The Implementation Plan phases are:
1. Repository Bootstrap
2. Docker Environment
3. Backend Bootstrap
4. Database
5. Authentication Foundation
6. Core Database Models
7. Repository Layer
8. Service Layer
9. REST API
10. WebSocket Infrastructure
11. Provider Interfaces
12. Seed Data
13. Patient Application
14. Doctor Portal
15. Mobile Simulation
16. Split-Screen Demonstration
17. AI Consultation
18. Audit Logging
19. Notification System
20. Authentication Completion
21. Testing
22. Documentation
23. Performance & Polish
24. Final Demonstration

I should create subagents for logical groupings of work. The existing code needs to be transformed/replaced to match Mirage spec. Let me create subagents for:

1. **Phase 1-4: Infrastructure & Backend Foundation** - Docker, FastAPI bootstrap, PostgreSQL, Redis setup
2. **Phase 5-8: Backend Core** - Auth, Models, Repositories, Services
3. **Phase 9-12: Backend API & Data** - REST API, WebSockets, Provider Interfaces, Seed Data
4. **Phase 13-16: Frontend Architecture** - PhoneFrame, Patient App, Doctor Portal, Split-Screen
5. **Phase 17-20: Frontend Features** - AI Consultation, Notifications, Audit, Auth Completion
6. **Phase 21-24: Testing & Polish** - Tests, Docs, Performance, Final Demo

Actually, since I'm in Plan Mode, I should not execute, but present a plan to the user with clarifying questions. Let me create the plan and present it.

Wait, the user said "use Agents.md and create subagents to do the tasks we need to work". They want me to create a plan using subagents. Since I'm in plan mode, I should create the plan and ask for approval before execution.

Let me structure this better. The repository currently has a "mediQAL" app that needs to be transformed into "Mirage". The docs specify a completely different architecture. There are some overlapping concepts (medical QA, chat, auth) but the architecture, screens, and features are very different.

I need to ask the user some clarifying questions before proceeding:

1. Should we keep any of the existing mediQAL code, or completely rebuild according to Mirage specs?
2. What's the timeline/priority?
3. Should all phases be implemented, or can some be simplified for the MVP?

Let me present a well-researched plan with subagent breakdowns and ask clarifying questions.

 Now I have a comprehensive understanding of the project. Let me create a detailed plan with subagents. 

**Tool: todowrite**

**Input:**
```json
{
  "todos": [
    {
      "content": "Analyze current codebase vs Mirage requirements",
      "status": "completed",
      "priority": "high"
    },
    {
      "content": "Create subagent plan for Mirage implementation",
      "status": "in_progress",
      "priority": "high"
    },
    {
      "content": "Get user approval on plan and clarifications",
      "status": "pending",
      "priority": "high"
    }
  ]
}
```

**Output:**
```
[
  {
    "content": "Analyze current codebase vs Mirage requirements",
    "status": "completed",
    "priority": "high"
  },
  {
    "content": "Create subagent plan for Mirage implementation",
    "status": "in_progress",
    "priority": "high"
  },
  {
    "content": "Get user approval on plan and clarifications",
    "status": "pending",
    "priority": "high"
  }
]
```

---

## Assistant (Plan · Kimi · 216.1s)

_Thinking:_

 Now I need to ask the user for clarifications and present them with choices about how to proceed. Let me look at the wireframes to understand the current UI, and identify key questions for the user.

Key questions/choices for the user:

1. Should we start fresh with the new architecture or try to reuse the existing code (which doesn't match)?
2. What is the priority - do we need to get the full 24-phase Mirage implementation done, or focus on the Healthathon demo flow?
3. The existing code uses MongoDB - should I drop MongoDB and use PostgreSQL + Redis as specified?

Let me formulate these as clear questions.

 Based on my thorough review of the Mirage documentation and the current codebase, I've identified a significant gap between what's documented and what currently exists. Let me present my analysis and get your input before creating subagents.

## Current State Analysis

The existing repository is a **mediQAL medical Q&A system**, but Mirage requires a **patient-controlled healthcare platform** with:

| Existing (mediQAL) | Required (Mirage) |
|---|---|
| MongoDB + Postgres | PostgreSQL + Redis |
| Single-user chatbot | Patient + Doctor dual apps |
| No authentication system | JWT + Demo Mode auth |
| No consent workflow | Real-time consent with WebSockets |
| Generic landing page | Mobile PhoneFrame + Doctor Portal |
| No medical records | Longitudinal patient records |
| Basic AI Q&A | Provider-abstracted AI (symptom, diagnosis, summary) |

## Plan Options

There are two approaches to reach the Mirage specification:

### Option A: Full Rewrite (Recommended)
Create the complete Mirage architecture from scratch, following the 24-phase Implementation Plan. This ensures architectural consistency and meets all success criteria.

### Option B: Incremental Refactor
Attempt to reuse existing components (FastAPI app, Postgres connection, some frontend) while adapting them to Mirage. This is riskier as the architectures diverge significantly.

## Questions Before Proceeding

To create the right subagents with accurate scope, I need a few clarifications: 

**Tool: question**

**Input:**
```json
{
  "questions": [
    {
      "question": "Which approach should we take?",
      "header": "Architecture Approach",
      "options": [
        {
          "label": "Full Rewrite",
          "description": "Build Mirage from scratch following the 24-phase plan. Cleanest architecture, highest quality. This is the recommended approach."
        },
        {
          "label": "Incremental Refactor",
          "description": "Try to reuse existing FastAPI/postgres code and adapt to Mirage requirements. Faster initially but may accumulate technical debt."
        }
      ]
    },
    {
      "question": "Mirage requires many UI screens for both Patient and Doctor apps. Should we focus on the core Healthathon demo flow first, or build all screens from the start?",
      "header": "Scope Priority",
      "options": [
        {
          "label": "Core Demo Flow First",
          "description": "Focus on: Login → Search → Consent → AI Consultation → Record Update. Get the end-to-end demonstration working first, then expand."
        },
        {
          "label": "All Screens at Once",
          "description": "Build every screen specified (Patient: Home, Timeline, Symptom Check, Consent, Profile, etc. + Doctor: Dashboard, Search, Record, Consultation, etc.)"
        }
      ]
    },
    {
      "question": "Should we keep the existing 'mediQAL' branding or switch to 'Mirage' throughout?",
      "header": "Branding",
      "options": [
        {
          "label": "Switch to Mirage",
          "description": "Full rebrand to match the project documentation."
        },
        {
          "label": "Keep mediQAL",
          "description": "Keep the existing branding but implement Mirage functionality."
        }
      ]
    }
  ]
}
```

**Output:**
```
User has answered your questions: "Which approach should we take?"="Full Rewrite", "Mirage requires many UI screens for both Patient and Doctor apps. Should we focus on the core Healthathon demo flow first, or build all screens from the start?"="Core Demo Flow First", "Should we keep the existing 'mediQAL' branding or switch to 'Mirage' throughout?"="Switch to Mirage". You can now continue with the user's answers in mind.
```

---

## Assistant (Plan · Kimi · 11.0s)

_Thinking:_

 The user wants:
1. Full Rewrite approach - build Mirage from scratch
2. Core Demo Flow First - focus on the essential demonstration workflow
3. Switch to Mirage branding

Now I need to create a comprehensive plan using subagents. Let me think about how to structure this.

The Mirage implementation plan has 24 phases. With the "Core Demo Flow First" approach, we should prioritize:

**Phase 1-4: Foundation**
- Repository Bootstrap
- Docker Environment
- Backend Bootstrap
- Database

**Phase 5-8: Core Backend**
- Authentication Foundation
- Core Database Models
- Repository Layer
- Service Layer

**Phase 9-10: API & Real-time**
- REST API
- WebSocket Infrastructure

**Phase 11-12: Abstractions & Data**
- Provider Interfaces
- Seed Data

**Phase 13-16: Frontend Core**
- Patient Application (core screens)
- Doctor Portal (core screens)
- Mobile Simulation
- Split-Screen Demonstration

**Phase 17: AI Integration**
- AI Consultation (mock providers)

**Phase 18-20: Polish**
- Audit Logging
- Notification System
- Authentication Completion

**Phase 21-24: Quality**
- Testing
- Documentation
- Performance & Polish
- Final Demonstration

Given we're in Plan Mode and can't execute, I should present the plan with proposed subagents for the user to approve. Let me organize the subagents:

1. **Infrastructure Subagent** - Phases 1-4: Repo structure, Docker, FastAPI bootstrap, PostgreSQL/Redis setup
2. **Backend Core Subagent** - Phases 5-8: Auth, models, repositories, services
3. **API & WebSocket Subagent** - Phases 9-10: REST API, WebSocket events
4. **Provider & Data Subagent** - Phases 11-12: Provider interfaces, seed data
5. **Patient App Subagent** - Phase 13 core: Patient app with essential screens (Login, Dashboard, Consent, Timeline)
6. **Doctor Portal Subagent** - Phase 14 core: Doctor app (Login, Dashboard, Search, Record, Consultation)
7. **Demo Mode Subagent** - Phases 15-16: PhoneFrame, split-screen, real-time sync
8. **AI Integration Subagent** - Phase 17: AI consultation workflow with mock providers
9. **Polish & Test Subagent** - Phases 18-24: Audit, notifications, tests, docs, final demo

Actually, since we're in Plan Mode, I should present this plan to the user and ask for confirmation before any subagents are dispatched. The user wants to see the plan first.

Let me create a well-structured plan document.

 

**Tool: todowrite**

**Input:**
```json
{
  "todos": [
    {
      "content": "Analyze current codebase vs Mirage requirements",
      "status": "completed",
      "priority": "high"
    },
    {
      "content": "Create subagent plan for Mirage implementation",
      "status": "completed",
      "priority": "high"
    },
    {
      "content": "Get user approval on plan and clarifications",
      "status": "completed",
      "priority": "high"
    },
    {
      "content": "Present final subagent execution plan",
      "status": "in_progress",
      "priority": "high"
    }
  ]
}
```

**Output:**
```
[
  {
    "content": "Analyze current codebase vs Mirage requirements",
    "status": "completed",
    "priority": "high"
  },
  {
    "content": "Create subagent plan for Mirage implementation",
    "status": "completed",
    "priority": "high"
  },
  {
    "content": "Get user approval on plan and clarifications",
    "status": "completed",
    "priority": "high"
  },
  {
    "content": "Present final subagent execution plan",
    "status": "in_progress",
    "priority": "high"
  }
]
```

---

## Assistant (Plan · Kimi · 34.0s)

_Thinking:_

 The user has confirmed:
1. Full Rewrite approach
2. Core Demo Flow First
3. Switch to Mirage branding

Now I need to present a well-structured plan with subagents. Since we're in plan mode (read-only), I should NOT execute anything yet. I need to present the plan to the user and ask for approval.

Let me design the subagent structure based on the 24 phases from the Implementation Plan, but focused on the core demo flow first, then expanding. The phases map to logical work units that subagents can handle.

Given the scale of the project, I'll organize subagents into groups:

**Phase 1-3: Infrastructure & Foundation**
- Subagent 1: Repository Bootstrap + Docker Environment
- Subagent 2: Backend Bootstrap (FastAPI, config, DI, health checks)

**Phase 4-6: Data Layer**
- Subagent 3: Database Setup (SQLAlchemy, Alembic, migrations)
- Subagent 4: Core Models + Seed Data

**Phase 7-9: Backend Core**
- Subagent 5: Repository Layer
- Subagent 6: Service Layer (auth, patient, doctor, consent, notification, audit)
- Subagent 7: REST API (all endpoints)

**Phase 10-12: Real-time & Providers**
- Subagent 8: WebSocket Infrastructure + Provider Interfaces

**Phase 13-16: Frontend**
- Subagent 9: Frontend Foundation (Next.js setup, auth providers, API client, design tokens)
- Subagent 10: Patient App Core Screens (Home, Consent, Health Record, Profile)
- Subagent 11: Doctor Portal Core Screens (Dashboard, Search, Patient Record, Consultation)
- Subagent 12: PhoneFrame + Split-Screen Demo

**Phase 17-20: Integration & Polish**
- Subagent 13: AI Integration + Notification System
- Subagent 14: Audit Logging + Auth Completion
- Subagent 15: Testing + Documentation
- Subagent 16: Performance Polish + Final Demo

This is 16 subagents. But we need to be practical - not all need to run at once, and some can run in parallel. Let me present this clearly.

Actually, let me reconsider. The Task tool says "When using the Task tool, you can use it to delegate a focused subtask to a subagent instance." Each subagent invocation executes code. However, we're in plan mode - read only. So I should present the plan to the user, get their go-ahead, then start invoking subagents.

Let me present a concise but detailed plan.

 ## Subagent Execution Plan for Mirage

I've designed **16 specialized subagents** to build Mirage from scratch, following the 24-phase Implementation Plan but sequenced for efficient parallel execution where possible.

---

### Group 1: Foundation (Sequential)

**Subagent 1 — Project Bootstrap & Docker**
- Task: Create the complete `mirage/` repository structure per Architecture doc (Phase 1)
- Task: Implement `docker-compose.yml` with PostgreSQL, Redis, Backend, Frontend, Worker containers (Phase 2)
- *Depends on: None*

**Subagent 2 — FastAPI Backend Skeleton**
- Task: FastAPI app, config module, dependency injection container, structured logging, health endpoints (`/health`, `/live`, `/ready`), Swagger/OpenAPI (Phase 3)
- *Depends on: Subagent 1*

---

### Group 2: Data Layer (Sequential)

**Subagent 3 — Database & Migrations**
- Task: SQLAlchemy 2.x setup, Alembic config, connection pooling, base model, session factory (Phase 4)
- *Depends on: Subagent 2*

**Subagent 4 — Core Models & Seed Data**
- Task: All SQLAlchemy models (Users, Patients, Doctors, Facilities, MedicalRecords, Visits, Diagnoses, Medications, Allergies, ConsentRequests, Notifications, AuditLogs, AISessions, AIMessages, RefreshTokens, etc.) (Phase 6)
- Task: Alembic migration scripts for all tables
- Task: Realistic Zimbabwe-centric seed data (10 patients, 5 doctors, 3 facilities, 50 visits, etc.) (Phase 12)
- *Depends on: Subagent 3*

---

### Group 3: Backend Core (Sequential after Group 2)

**Subagent 5 — Repository Layer**
- Task: CRUD repositories for all entities with pagination, filtering, searching (Phase 7)
- *Depends on: Subagent 4*

**Subagent 6 — Service Layer (Core)**
- Task: AuthenticationService (JWT + Demo Mode + Password Hashing + Refresh Tokens) (Phase 5, 20)
- Task: PatientService, DoctorService, ConsentService, TimelineService, RecordService, NotificationService, AuditService, ConsultationService, AISessionService (Phase 8)
- *Depends on: Subagent 5*

**Subagent 7 — REST API**
- Task: All API routes per API Contract (`/auth`, `/patients`, `/doctor`, `/consent`, `/records`, `/timeline`, `/visits`, `/ai`, `/notifications`, `/audit`) with Pydantic validation, standardized responses, pagination, error handling (Phase 9)
- *Depends on: Subagent 6*

---

### Group 4: Real-Time & Abstractions (Sequential after Group 3)

**Subagent 8 — WebSockets & Provider Interfaces**
- Task: WebSocket endpoint (`/ws`) with JWT auth, subscription model, event types (ConsentRequested, ConsentApproved, TimelineUpdated, etc.), auto-reconnect, heartbeat (Phase 10)
- Task: All provider interfaces (SymptomCheckerProvider, DiagnosisProvider, ClinicalSummaryProvider, TranscriptionProvider, NotificationProvider) with mock implementations (Phase 11)
- *Depends on: Subagent 7*

---

### Group 5: Frontend Foundation (Parallel with Group 4)

**Subagent 9 — Next.js Frontend Skeleton**
- Task: Next.js 14+ App Router setup, TailwindCSS, design tokens, global providers (Auth, WebSocket, React Query, Theme), typed API client, Zod schemas
- Task: Reusable component library (Button, Card, Input, Skeleton, EmptyState, ErrorState, StatusBadge, etc.)
- *Depends on: None (can start in parallel once API contract is known)*

---

### Group 6: Patient Application (Parallel with Doctor Portal)

**Subagent 10 — Patient App Core**
- Task: PhoneFrame component with status bar, safe areas, bottom navigation
- Task: Screens: Login (Demo Mode), Home Dashboard, Health Record/Timeline, Consent Request, Notifications, Profile
- Task: All loading/empty/error states, animations per Design System
- *Depends on: Subagent 9*

---

### Group 7: Doctor Portal (Parallel with Patient App)

**Subagent 11 — Doctor Portal Core**
- Task: Desktop layout with sidebar/top navigation, search bar
- Task: Screens: Login, Dashboard, Patient Search, Patient Record (timeline, allergies, medications), Consent Request/Waiting, AI Consultation Workspace
- Task: All loading/empty/error states
- *Depends on: Subagent 9*

---

### Group 8: Integration & Polish (Sequential after Groups 6-7)

**Subagent 12 — Split-Screen Demo Mode**
- Task: Route `/demo` showing Patient PhoneFrame + Doctor Portal side-by-side
- Task: WebSocket synchronization for consent flow demonstration
- *Depends on: Subagents 10, 11*

**Subagent 13 — AI Integration**
- Task: Connect AI provider interfaces to frontend flows (patient symptom check, doctor diagnosis suggestions, clinical summary generation)
- Task: Mock AI responses with realistic clinical content
- *Depends on: Subagent 8, 12*

**Subagent 14 — Notifications & Audit**
- Task: Real-time notification delivery (toast + in-app)
- Task: Audit logging integration across all critical actions
- *Depends on: Subagent 8, 12*

**Subagent 15 — Testing**
- Task: Backend tests (pytest) for repositories, services, API endpoints
- Task: Frontend tests (Vitest + React Testing Library) for critical flows
- Task: Integration tests for consent workflow
- *Depends on: Subagent 13, 14*

**Subagent 16 — Final Polish & Documentation**
- Task: Performance review, animation consistency, accessibility audit
- Task: Complete documentation (README, API guide, environment variables, deployment)
- Task: Final demonstration verification
- *Depends on: Subagent 15*

---

## Execution Flow

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│  Subagent 1     │────▶│  Subagent 2     │────▶│  Subagent 3     │
│  Bootstrap      │     │  FastAPI        │     │  Database       │
└─────────────────┘     └─────────────────┘     └─────────────────┘
                                                        │
┌─────────────────┐     ┌─────────────────┐           ▼
│  Subagent 9     │     │  Subagent 4     │────▶┌─────────────────┐
│  Frontend       │     │  Models + Seed  │     │  Subagent 5     │
│  Skeleton       │     │                 │     │  Repositories   │
└─────────────────┘     └─────────────────┘     └─────────────────┘
                                                        │
                                                        ▼
                                               ┌─────────────────┐
                                               │  Subagent 6     │
                                               │  Services       │
                                               └─────────────────┘
                                                        │
                                                        ▼
                                               ┌─────────────────┐
                                               │  Subagent 7     │
                                               │  REST API       │
                                               └─────────────────┘
                                                        │
                              ┌────────────────────────┘
                              ▼
                    ┌─────────────────┐     ┌─────────────────┐
                    │  Subagent 8     │     │  Subagent 10    │
                    │  WebSockets +   │────▶│  Patient App    │
                    │  Providers      │────▶│  Subagent 11    │
                    └─────────────────┘     │  Doctor Portal  │
                              │             └─────────────────┘
                              ▼                      │
                    ┌─────────────────┐              │
                    │  Subagent 12    │◄─────────────┘
                    │  Split-Screen   │
                    └─────────────────┘
                              │
              ┌───────────────┼───────────────┐
              ▼               ▼               ▼
    ┌─────────────────┐ ┌─────────────────┐ ┌─────────────────┐
    │  Subagent 13    │ │  Subagent 14    │ │  Subagent 15    │
    │  AI Integration │ │  Notif + Audit  │ │  Testing        │
    └─────────────────┘ └─────────────────┘ └─────────────────┘
                              │
                              ▼
                    ┌─────────────────┐
                    │  Subagent 16    │
                    │  Polish + Docs  │
                    └─────────────────┘
```

## Success Criteria
The final deliverable will:
- Start with `docker compose up`
- Run complete 5-minute Healthathon demo (doctor login → search → request consent → patient receives → approves → consultation → AI diagnosis → record update → patient sees update)
- Use JWT + Demo Mode auth
- Have provider-abstracted AI
- Include split-screen mode
- Pass all tests

---

**Ready to proceed?** I can start launching subagents. They will execute sequentially and in parallel where safe, with each one writing its output back for review before the next phase begins.

---

## User

---

## Assistant (Compaction · Kimi · 11.6s)

_Thinking:_

 The user wants me to create a new anchored summary from the conversation history. Let me review what happened:

1. I was asked to use AGENTS.md and create subagents to do the tasks needed to work on the Mirage project
2. I read all the documentation files (AGENTS.md, 00-11 docs, wireframes, etc.)
3. I analyzed the current codebase which is a mediQAL medical Q&A system
4. I identified a significant gap between mediQAL (existing) and Mirage (required)
5. I asked clarifying questions about approach, scope priority, and branding
6. User answered: Full Rewrite, Core Demo Flow First, Switch to Mirage
7. I presented a detailed subagent execution plan with 16 subagents organized into groups, showing dependencies and execution flow
8. The user hasn't yet said "proceed" - we're waiting for approval

Let me create the summary following the template exactly.

 ## Goal
- Create subagents and execution plan to build the Mirage healthcare platform (full rewrite from existing mediQAL codebase)

## Constraints & Preferences
- Full rewrite approach (not incremental refactor)
- Core Healthathon demo flow first, expand later
- Switch branding from mediQAL to Mirage
- Must follow all 11 docs in docs/ as authoritative sources
- Docker Compose deployment required
- JWT + Demo Mode authentication
- Provider-abstracted AI layer (no direct AI implementation)
- PostgreSQL + Redis stack
- Next.js 14+ App Router frontend

## Progress
### Done
- Read and analyzed all 11 project documentation files
- Analyzed existing mediQAL codebase structure and identified gaps
- Asked clarifying questions (approach, scope, branding)
- Created 16-subagent execution plan grouped by dependency graph
- Defined success criteria for final deliverable

### In Progress
- Awaiting user approval to launch subagent execution

### Blocked
- Need user confirmation to proceed with subagent dispatch

## Key Decisions
- Full rewrite chosen over incremental refactor due to architectural divergence (mediQAL: MongoDB+Postgres, generic chatbot; Mirage: Postgres+Redis, dual-app with consent workflows)
- Core demo flow prioritized to get end-to-end demonstration working before expanding to all screens
- Mirage branding to replace mediQAL throughout codebase

## Next Steps
- Await user approval to proceed
- Launch Subagent 1 (Bootstrap & Docker) and Subagent 9 (Frontend Skeleton) in parallel
- Execute remaining subagents per dependency graph
- Verify final 5-minute Healthathon demo: doctor login → search → request consent → patient receives → approves → consultation → AI diagnosis → record update → patient sees update

## Critical Context
- Existing repo path: `/Users/sheltonmutambirwa/Desktop/medic/`
- Current app is `Medical QA System` with MongoDB dependency (must be removed)
- Docker Compose currently uses `medic_auth` DB, asyncpg driver
- Frontend runs on port 3001 in existing setup; Mirage spec says 3000
- FastAPI backend currently titled "Medical QA System" with CORS to localhost:3000
- WebSocket integration required for real-time consent notifications
- AI providers must be interface-based with mock implementations initially
- Patient app runs inside PhoneFrame component simulating mobile device
- Doctor portal is desktop-first with sidebar navigation
- Split-screen `/demo` route required for presentation

## Relevant Files
- `/Users/sheltonmutambirwa/Desktop/medic/AGENTS.md`: Reading order and source-of-truth priorities
- `/Users/sheltonmutambirwa/Desktop/medic/docs/00_Project_Index.md`: Entry point, project vision, documentation hierarchy
- `/Users/sheltonmutambirwa/Desktop/medic/docs/01_Product_Requirements_Document.md`: Product behaviour authority
- `/Users/sheltonmutambirwa/Desktop/medic/docs/02_Technical_Architecture.md`: Implementation authority (5-layer architecture)
- `/Users/sheltonmutambirwa/Desktop/medic/docs/03_Design_System.md`: Visual language, tokens, animations
- `/Users/sheltonmutambirwa/Desktop/medic/docs/04_Implementation_Plan.md`: 24-phase build order
- `/Users/sheltonmutambirwa/Desktop/medic/docs/05_API_Contract.md`: REST + WebSocket API authority
- `/Users/sheltonmutambirwa/Desktop/medic/docs/06_Database_Schema.md`: PostgreSQL schema authority (UUID PKs, UTC timestamps)
- `/Users/sheltonmutambirwa/Desktop/medic/docs/07_Master_Generation_Prompt.md`: Engineering standards and philosophy
- `/Users/sheltonmutambirwa/Desktop/medic/docs/08_Coding_Standards.md`: Code conventions (Python 3.12+, strict typing)
- `/Users/sheltonmutambirwa/Desktop/medic/docs/10_UI_Screen_Specification.md`: Screen-by-screen implementation guide
- `/Users/sheltonmutambirwa/Desktop/medic/docs/11_User_Flows_and_State_Machines.md`: Workflow behaviour authority
- `/Users/sheltonmutambirwa/Desktop/medic/docs/wireframes.html`: Canonical visual reference (takes precedence over text specs)
- `/Users/sheltonmutambirwa/Desktop/medic/app/main.py`: Existing FastAPI entry point (to be replaced)
- `/Users/sheltonmutambirwa/Desktop/medic/frontend/package.json`: Existing Next.js dependencies (missing Framer Motion per spec)
- `/Users/sheltonmutambirwa/Desktop/medic/docker-compose.yml`: Existing compose config (to be rewritten for Mirage stack)

---

## User

go (ensure each subagent reads the neccesary files for guidance)

---

## Assistant (Build · Kimi · 1156.7s)

_Thinking:_

 The user wants me to proceed with building the Mirage healthcare platform. I need to:

1. Execute the subagent plan I created
2. Ensure each subagent reads the necessary documentation files
3. Follow the AGENTS.md instructions (read docs in order, PRD is authoritative for product behavior, etc.)

Let me start dispatching subagents. According to my plan:
- Phase 1: Subagent 1 (Bootstrap & Docker) + Subagent 9 (Frontend Skeleton) in parallel first
- Then continue with others

I should dispatch Subagent 1 first since it sets up the foundation directory structure and Docker stack that others depend on. Then Dispatch Subagent 9 in parallel.

Let me create the dispatch calls with very specific prompts that include:
1. Absolute paths to relevant docs they MUST read first
2. Clear task descriptions
3. Expected outputs
4. Context about current codebase

For Subagent 1 (Bootstrap & Docker):
- Must read: AGENTS.md, 00, 02, 06, 09
- Tasks:
  * Create directory structure for both apps
  * Rewrite docker-compose.yml for PostgreSQL + Redis + backend + frontend
  * Add Makefile with common commands
  * Create .env.example files
  * Update root README.md

For Subagent 9 (Frontend Skeleton):
- Must read: AGENTS.md, 00, 02, 03, 04, 08
- Tasks:
  * Set up Next.js app with App Router
  * Install tailwind, shadcn, framer-motion, etc.
  * Create base layout, theme config, animation utilities based on Design System
  * Create PhoneFrame component
  * Set up project structure for shared components, doctor app, patient app

Let me dispatch these two in parallel since they are independent.

 I'll dispatch the subagents now, starting with Phase 1 (Bootstrap and Frontend Skeleton) in parallel. 

**Tool: task**

**Input:**
```json
{
  "description": "Phase 1: Bootstrap & Docker",
  "prompt": "You are building the foundation for the Mirage healthcare platform. BEFORE writing any code, you MUST read the following documentation files IN ORDER to understand the architecture and constraints:\n\n1. /Users/sheltonmutambirwa/Desktop/medic/AGENTS.md — Development instructions and source-of-truth priority\n2. /Users/sheltonmutambirwa/Desktop/medic/docs/00_Project_Index.md — Project overview\n3. /Users/sheltonmutambirwa/Desktop/medic/docs/02_Technical_Architecture.md — Technology stack (5-layer architecture)\n4. /Users/sheltonmutambirwa/Desktop/medic/docs/06_Database_Schema.md — PostgreSQL schema (UUID PKs, UTC timestamps)\n5. /Users/sheltonmutambirwa/Desktop/medic/docs/09_Deployment_Guide.md — Docker Compose, environment variables\n\nAfter reading these files, inspect the existing codebase at /Users/sheltonmutambirwa/Desktop/medic/ to understand what currently exists and must be replaced.\n\nYOUR TASKS:\n1. **Directory Structure**: Create the full directory layout for the Mirage project under /Users/sheltonmutambirwa/Desktop/medic/:\n   - `backend/` — FastAPI application root\n   - `backend/app/` — Application modules\n   - `backend/app/doctor/` — Doctor portal API\n   - `backend/app/patient/` — Patient app API  \n   - `backend/app/shared/` — Shared models, schemas, utilities\n   - `backend/app/ai/` — AI provider abstractions and chat engine\n   - `backend/app/auth/` — JWT + Demo Mode authentication\n   - `backend/app/db/` — Database layer (SQLAlchemy, Alembic, asyncpg)\n   - `backend/app/consent/` — Consent request/approval handlers\n   - `frontend/` — Next.js 14+ App Router root\n   - `frontend/components/` — Shared React components\n   - `frontend/components/phone-frame/` — PhoneFrame component for patient app demo\n   - `frontend/app/doctor/` — Doctor portal app\n   - `frontend/app/patient/` — Patient mobile app pages (displayed inside PhoneFrame)\n   - `frontend/lib/` — Shared utilities, API clients, auth context\n   - `frontend/hooks/` — Custom React hooks\n   - `frontend/public/` — Static assets\n\n2. **Docker Compose Stack**: Rewrite `/Users/sheltonmutambirwa/Desktop/medic/docker-compose.yml` to define the Mirage services:\n   - `postgres`: PostgreSQL 15+, persistent volume, healthcheck, port 5432, database `mirage_dev`, user `mirage_user`\n   - `redis`: Redis 7, persistent volume, healthcheck, port 6379\n   - `backend`: FastAPI dev server (like uvicorn), depends on postgres + redis, port 8000, volumes mount for hot reload, environment from .env\n   - `frontend`: Next.js dev server, depends on backend, port 3000 (not 3001), volumes mount for hot reload, environment from .env\n\n3. **Environment Configuration**: Create `/Users/sheltonmutambirwa/Desktop/medic/.env.example` with all required environment variables per the Deployment Guide (database URL, Redis URL, JWT secrets, AI provider placeholders, demo mode flags).\n\n4. **Makefile**: Create `/Users/sheltonmutambirwa/Desktop/medic/Makefile` with common commands: `build`, `up`, `down`, `logs`, `migrate`, `shell-backend`, `shell-frontend`, `test`.\n\n5. **Backend Requirements**: Create `/Users/sheltonmutambirwa/Desktop/medic/backend/requirements.txt` with exact versions for: FastAPI, Uvicorn, SQLAlchemy[asyncio], asyncpg, Alembic, Pydantic, Pydantic-Settings, python-jose[cryptography], passlib[bcrypt], redis, websockets, pytest, httpx, pytest-asyncio.\n\n6. **Root README Update**: Update `/Users/sheltonmutambirwa/Desktop/medic/README.md` to reflect the new Mirage project (not mediQAL). Include: project description, quick start (`make build && make up`), architecture overview, services and ports, and a note that this is a Healthathon demonstration platform.\n\nIMPORTANT CONSTRAINTS:\n- Do NOT use MongoDB anywhere. Remove any Mongo references.\n- PostgreSQL must use UUID primary keys and UTC timestamps everywhere.\n- All Python code must be Python 3.12+ with strict typing.\n- FastAPI app title must be \"Mirage\" (not Medical QA System).\n- Frontend port must be 3000.\n- All files must use absolute paths starting from workspace root.\n- You only need to CREATE files and DIRECTORIES. You do NOT need to write full application logic here — just the skeleton, config, and infrastructure.\n\nReturn a summary of every file and directory you created/modified.",
  "subagent_type": "general"
}
```

**Output:**
```
task_id: ses_0cd3ccb62ffeE7xzH1C7c324jN (for resuming to continue this task if needed)

<task_result>
 ---

## Summary: Mirage Foundation Created

All requested files, directories and configurations have been created. The old `app/` codebase remains in place (untouched) so nothing was lost.

---

### **Directories Created (or Confirmed)**

| Path | Status |
|------|--------|
| `/Users/sheltonmutambirwa/Desktop/medic/backend/app/doctor/` | **New** — Doctor portal API module |
| `/Users/sheltonmutambirwa/Desktop/medic/backend/app/patient/` | **New** — Patient app API module |
| `/Users/sheltonmutambirwa/Desktop/medic/backend/app/shared/` | **New** — Shared models, schemas, utilities |
| `/Users/sheltonmutambirwa/Desktop/medic/backend/app/ai/` | **New** — AI provider abstractions |
| `/Users/sheltonmutambirwa/Desktop/medic/backend/app/auth/` | **New** — JWT + Demo Mode authentication |
| `/Users/sheltonmutambirwa/Desktop/medic/backend/app/db/` | **New** — Database layer (SQLAlchemy / Alembic) |
| `/Users/sheltonmutambirwa/Desktop/medic/backend/app/consent/` | **New** — Consent request/approval handlers |
| `/Users/sheltonmutambirwa/Desktop/medic/frontend/components/` | **New** — Shared React components root |
| `/Users/sheltonmutambirwa/Desktop/medic/frontend/components/phone-frame/` | **New** — PhoneFrame component directory |
| `/Users/sheltonmutambirwa/Desktop/medic/frontend/app/doctor/` | Confirmed — Doctor portal pages |
| `/Users/sheltonmutambirwa/Desktop/medic/frontend/app/patient/` | Confirmed — Patient mobile pages |
| `/Users/sheltonmutambirwa/Desktop/medic/frontend/lib/` | **New** — Shared utilities, API clients, auth context |
| `/Users/sheltonmutambirwa/Desktop/medic/frontend/hooks/` | **New** — Custom React hooks |
| `/Users/sheltonmutambirwa/Desktop/medic/frontend/public/` | Confirmed — Static assets |

---

### **Files Created**

#### Backend Skeleton
| File | Purpose |
|------|---------|
| `backend/__init__.py` | Package marker |
| `backend/app/__init__.py` | App package marker |
| `backend/app/doctor/__init__.py` | Doctor module marker |
| `backend/app/patient/__init__.py` | Patient module marker |
| `backend/app/shared/__init__.py` | Shared module marker |
| `backend/app/ai/__init__.py` | AI module marker |
| `backend/app/auth/__init__.py` | Auth module marker |
| `backend/app/db/__init__.py` | DB module marker |
| `backend/app/consent/__init__.py` | Consent module marker |
| `backend/main.py` | FastAPI entrypoint — **title set to `"Mirage"`** |
| `backend/Dockerfile` | Python 3.12 dev image with hot-reload |
| `backend/requirements.txt` | Exact pinned deps (FastAPI, SQLAlchemy[asyncio], asyncpg, Alembic, Pydantic, python-jose, passlib, redis, websockets, pytest, httpx, pytest-asyncio, etc.) |
| `backend/alembic.ini` | Alembic configuration pointing to `mirage_dev` |
| `backend/alembic/__init__.py` | Alembic scripts package |
| `backend/alembic/env.py` | Alembic migration environment |

#### Config & Infrastructure
| File | Purpose |
|------|---------|
| `docker-compose.yml` | **Rewritten** — `postgres` (16-alpine, port 5432, `mirage_dev` / `mirage_user`), `redis` (7-alpine, port 6379), `backend` (8000, depends on postgres+redis, hot-reload volume), `frontend` (3000, depends on backend, hot-reload volume). **MongoDB removed entirely.** |
| `.env.example` | **Rewritten** — All Mirage env vars per Deployment Guide (DB URL, Redis URL, JWT secrets, AI provider placeholders, demo mode flags). No Mongo references. |
| `Makefile` | **New** — `build`, `up`, `down`, `logs`, `migrate`, `shell-backend`, `shell-frontend`, `test` |
| `README.md` | **Rewritten** — Mirage project description, quick start (`make build && make up`), architecture overview, services & ports, Healthathon note. |

---

### **Key Constraints Verified**

- ❌ **No MongoDB** — Removed from `docker-compose.yml` and `.env.example`.
- ✅ **PostgreSQL** — `postgres:16-alpine`, database `mirage_dev`, user `mirage_user`, UUID PKs enforced by schema docs, UTC timestamps.
- ✅ **Frontend port** — `3000` (not 3001).
- ✅ **FastAPI title** — `"Mirage"` in `backend/main.py`.
- ✅ **Python 3.12+** — Backend Dockerfile uses `python:3.12-slim`.
- ✅ **Absolute paths** — Every operation used absolute paths.

---

### **What Was NOT Touched**

The legacy `app/` root directory (old mediQAL code), `frontend/app/components/`, `frontend/app/lib/`, `frontend/app/login/`, etc., and the `.git` history were all left intact so nothing was lost.
</task_result>
```

**Tool: task**

**Input:**
```json
{
  "description": "Phase 1: Frontend Skeleton",
  "prompt": "You are building the frontend skeleton for the Mirage healthcare platform. BEFORE writing any code, you MUST read the following documentation files IN ORDER to understand the design system and conventions:\n\n1. /Users/sheltonmutambirwa/Desktop/medic/AGENTS.md — Development instructions\n2. /Users/sheltonmutambirwa/Desktop/medic/docs/00_Project_Index.md — Project overview (dual-app: Doctor Portal + Patient App)\n3. /Users/sheltonmutambirwa/Desktop/medic/docs/02_Technical_Architecture.md — Frontend stack (Next.js 14+ App Router, Tailwind CSS, shadcn/ui)\n4. /Users/sheltonmutambirwa/Desktop/medic/docs/03_Design_System.md — Visual language, tokens, animation utilities, color palette (Celestial Blue, Stellar White, Mirage Black, etc.)\n5. /Users/sheltonmutambirwa/Desktop/medic/docs/08_Coding_Standards.md — Code conventions (TypeScript strict, file naming, component structure)\n6. /Users/sheltonmutambirwa/Desktop/medic/docs/10_UI_Screen_Specification.md — Screen specs for PhoneFrame, Doctor login, Patient consent\n\nAfter reading these files, inspect the existing frontend at /Users/sheltonmutambirwa/Desktop/medic/frontend/ to understand what currently exists and what must be replaced.\n\nYOUR TASKS:\n\n1. **Next.js App Setup**: \n   - Ensure `/Users/sheltonmutambirwa/Desktop/medic/frontend/package.json` has the correct dependencies for Next.js 14+, React 18, TypeScript, Tailwind CSS, shadcn/ui (via `npx shadcn-ui@latest init` or manual config), framer-motion, lucide-react, clsx, tailwind-merge, class-variance-authority.\n   - Update `/Users/sheltonmutambirwa/Desktop/medic/frontend/next.config.js` to set the dev port to 3000 and configure rewrites/API proxy to backend at localhost:8000.\n   - Update `/Users/sheltonmutambirwa/Desktop/medic/frontend/tailwind.config.ts` to include the Mirage Design System tokens (colors: celestialBlue, stellarWhite, mirageBlack, healthGreen, alertOrange, clinicalGrey, deepSpace; font families; animation curves; glassmorphism utilities).\n   - Create `/Users/sheltonmutambirwa/Desktop/medic/frontend/app/globals.css` with Tailwind directives and CSS variables for the Mirage theme.\n\n2. **Shared UI Utilities**:\n   - Create `/Users/sheltonmutambirwa/Desktop/medic/frontend/lib/utils.ts` containing the standard `cn()` utility (clsx + tailwind-merge).\n   - Create `/Users/sheltonmutambirwa/Desktop/medic/frontend/lib/animations.ts` exporting reusable Framer Motion variants per the Design System (fadeIn, slideIn, scaleIn, staggerContainer, pageTransition).\n\n3. **PhoneFrame Component**:\n   - Create `/Users/sheltonmutambirwa/Desktop/medic/frontend/components/phone-frame/PhoneFrame.tsx` — a React component that visually simulates a mobile phone frame (rounded corners, notch, home indicator) to wrap the Patient App pages during the demo. It must accept `children` and have a fixed vertical height matching a typical phone (~812px), centered on desktop.\n   - Create associated CSS module if needed.\n\n4. **Layout & Navigation Skeleton**:\n   - Create `/Users/sheltonmutambirwa/Desktop/medic/frontend/app/layout.tsx` as the root layout with global providers (React Query / SWR context, Auth context placeholder, Toast provider placeholder).\n   - Create `/Users/sheltonmutambirwa/Desktop/medic/frontend/app/doctor/layout.tsx` — Doctor portal layout with a sidebar navigation placeholder (desktop-first). Include navigation links: Dashboard, Patients, Consents, Consultations.\n   - Create `/Users/sheltonmutambirwa/Desktop/medic/frontend/app/patient/layout.tsx` — Minimal mobile layout (no sidebar), header with Mirage branding and notification bell placeholder.\n   - Create `/Users/sheltonmutambirwa/Desktop/medic/frontend/app/demo/page.tsx` — The SPLIT-SCREEN demo page required for presentation. Left side: Doctor Portal (live app). Right side: PhoneFrame wrapping Patient App (live app). This is the critical screen for Healthathons.\n\n5. **Placeholder Pages** (index routes so Next.js doesn't 404):\n   - `/Users/sheltonmutambirwa/Desktop/medic/frontend/app/page.tsx` — Landing/marketing page with \"Enter Demo Mode\" CTA linking to `/demo`.\n   - `/Users/sheltonmutambirwa/Desktop/medic/frontend/app/doctor/login/page.tsx` — Doctor login placeholder.\n   - `/Users/sheltonmutambirwa/Desktop/medic/frontend/app/doctor/dashboard/page.tsx` — Doctor dashboard placeholder.\n   - `/Users/sheltonmutambirwa/Desktop/medic/frontend/app/doctor/consents/page.tsx` — Consent management placeholder.\n   - `/Users/sheltonmutambirwa/Desktop/medic/frontend/app/patient/login/page.tsx` — Patient login placeholder.\n   - `/Users/sheltonmutambirwa/Desktop/medic/frontend/app/patient/consent/page.tsx` — Patient consent approval placeholder.\n\nIMPORTANT CONSTRAINTS:\n- Do NOT use MongoDB references anywhere.\n- Use TypeScript strict mode everywhere.\n- Follow the exact Mirage color palette and animation specs from the Design System.\n- Do NOT write full business logic yet — focus on structural skeleton, configuration, and the PhoneFrame + Demo split-screen layout.\n- Components must use Tailwind CSS classes, not inline styles.\n- All paths must be absolute starting from `/Users/sheltonmutambirwa/Desktop/medic/frontend/`.\n\nReturn a summary of every file and directory you created/modified.",
  "subagent_type": "general"
}
```

**Output:**
```
task_id: ses_0cd3c928bffeiKjk9TTlVD5KuH (for resuming to continue this task if needed)

<task_result>
 Here's the comprehensive summary of everything I created and modified for the Mirage frontend skeleton:

## Summary of Files Created / Modified

### Configuration Files (Updated)

1. **`/Users/sheltonmutambirwa/Desktop/medic/frontend/package.json`**  
   - Updated project name to `mirage-frontend`
   - Changed dev port from `3001` → `3000`
   - Added new dependencies: `framer-motion`, `lucide-react`, `clsx`, `tailwind-merge`, `class-variance-authority`

2. **`/Users/sheltonmutambirwa/Desktop/medic/frontend/next.config.js`**  
   - Added API rewrite rules proxying `/api/v1/*` and `/ws/*` to `localhost:8000`

3. **`/Users/sheltonmutambirwa/Desktop/medic/frontend/tailwind.config.ts`** *(NEW)*  
   - Full Mirage Design System token configuration
   - Colors: `celestialBlue`, `stellarWhite`, `mirageBlack`, `healthGreen`, `alertOrange`, `clinicalGrey`, `deepSpace`
   - Custom font sizes, spacing, border-radius, shadows, animation timing, glassmorphism utilities

4. **`/Users/sheltonmutambirwa/Desktop/medic/frontend/app/globals.css`** *(REWRITTEN)*  
   - Tailwind directives with `@layer base/components/utilities`
   - CSS variables for all Mirage tokens
   - Glassmorphism utilities (`.glass`, `.glass-dark`, `.glass-card`)
   - Skeleton shimmer animation, scrollbar utilities, touch target utilities, reduced-motion support

---

### Shared UI Utilities (NEW)

5. **`/Users/sheltonmutambirwa/Desktop/medic/frontend/lib/utils.ts`**  
   - Standard `cn()` utility combining `clsx` + `tailwind-merge`

6. **`/Users/sheltonmutambirwa/Desktop/medic/frontend/lib/animations.ts`**  
   - Framer Motion variants: `fadeIn`, `slideIn`, `slideUp`, `scaleIn`, `staggerContainer`, `staggerItem`, `pageTransition`, `bottomSheet`, `notificationSlide`
   - Default spring transition (`stiffness: 380`, `damping: 32`)

---

### PhoneFrame Component (NEW)

7. **`/Users/sheltonmutambirwa/Desktop/medic/frontend/components/phone-frame/PhoneFrame.tsx`**  
   - Simulated smartphone frame with rounded bezel, notch, camera cut-out, side buttons
   - Fixed dimensions: `350×760px` (smaller screens) / `370×800px` (`lg+`)
   - Includes simulated status bar (time, signal bars, 5G, battery), scrollable content area, home indicator
   - Wraps children inside a realistic device chrome for demo presentations

---

### Layout & Navigation Skeleton (NEW)

8. **`/Users/sheltonmutambirwa/Desktop/medic/frontend/app/layout.tsx`** *(REWRITTEN)*  
   - Server-side root layout with `Inter` font from `next/font/google`
   - Imports `Metadata` and wraps children in global `Providers`

9. **`/Users/sheltonmutambirwa/Desktop/medic/frontend/providers/index.tsx`**  
   - Composes `QueryProvider` → `AuthProvider` → `ToastProvider` → `WebSocketProvider`

10. **`/Users/sheltonmutambirwa/Desktop/medic/frontend/providers/QueryProvider.tsx`**  
    - React Query `QueryClientProvider`

11. **`/Users/sheltonmutambirwa/Desktop/medic/frontend/providers/AuthProvider.tsx`**  
    - Auth context placeholder with `login`/`logout`

12. **`/Users/sheltonmutambirwa/Desktop/medic/frontend/providers/ToastProvider.tsx`**  
    - Toast context placeholder with `show` method

13. **`/Users/sheltonmutambirwa/Desktop/medic/frontend/providers/WebSocketProvider.tsx`**  
    - WebSocket context placeholder with connection state

14. **`/Users/sheltonmutambirwa/Desktop/medic/frontend/hooks/useAuth.ts`**  
15. **`/Users/sheltonmutambirwa/Desktop/medic/frontend/hooks/useToast.ts`**  
16. **`/Users/sheltonmutambirwa/Desktop/medic/frontend/hooks/useWebSocket.ts`**  
    - Typed hooks for each provider context

17. **`/Users/sheltonmutambirwa/Desktop/medic/frontend/app/doctor/layout.tsx`**  
    - Desktop-first sidebar layout for Doctor Portal
    - Navigation links: Dashboard, Patients, Consents, Consultations
    - Notifications bell + settings at bottom, top header with user avatar

18. **`/Users/sheltonmutambirwa/Desktop/medic/frontend/app/patient/layout.tsx`**  
    - Minimal mobile layout (no sidebar)
    - Header with Mirage branding (`M` logo) and notification bell placeholder

19. **`/Users/sheltonmutambirwa/Desktop/medic/frontend/app/demo/page.tsx`**  
    - **Critical split-screen demo page for Healthathons**
    - Left panel: Doctor Portal rendered via `<iframe src="/doctor/dashboard">`
    - Right panel: `PhoneFrame` wrapping Patient App via `<iframe src="/patient/login">`
    - Dark background, labeled panels, both apps communicate through backend only

---

### Placeholder Pages (NEW)

20. **`/Users/sheltonmutambirwa/Desktop/medic/frontend/app/page.tsx`** *(REWRITTEN)*  
    - Landing/marketing page with Mirage branding
    - "Enter Demo Mode" CTA linking to `/demo`
    - "Doctor Login" secondary CTA

21. **`/Users/sheltonmutambirwa/Desktop/medic/frontend/app/doctor/login/page.tsx`**  
    - Doctor login placeholder (`'use client'` for form interactivity)
    - Email + password fields, "Sign In" button

22. **`/Users/sheltonmutambirwa/Desktop/medic/frontend/app/doctor/dashboard/page.tsx`**  
    - Dashboard placeholder with stat cards (Today's Consultations, Pending Consents, Recent Patients, Notifications)
    - Skeleton widgets for Schedule and Pending Consents

23. **`/Users/sheltonmutambirwa/Desktop/medic/frontend/app/doctor/patients/page.tsx`**  
    - Patient search placeholder with search input + skeleton patient rows

24. **`/Users/sheltonmutambirwa/Desktop/medic/frontend/app/doctor/consents/page.tsx`**  
    - Consent management placeholder with table header + skeleton rows

25. **`/Users/sheltonmutambirwa/Desktop/medic/frontend/app/doctor/consultations/page.tsx`**  
    - Consultations placeholder with Active Consultation + Upcoming skeleton widgets

26. **`/Users/sheltonmutambirwa/Desktop/medic/frontend/app/patient/login/page.tsx`**  
    - Patient login placeholder (`'use client'`)
    - National ID / Phone + PIN fields, "Continue" button

27. **`/Users/sheltonmutambirwa/Desktop/medic/frontend/app/patient/consent/page.tsx`**  
    - Patient consent approval placeholder
    - Doctor card, purpose, shared data list, expiry banner, Approve/Decline buttons

28. **`/Users/sheltonmutambirwa/Desktop/medic/frontend/app/not-found.tsx`** *(REWRITTEN)*  
    - 404 page styled with Mirage tokens

---

### Files Removed (Cleanup)

- `app/components/Header.tsx`, `app/components/Footer.tsx`
- `app/lib/api.ts`, `app/lib/auth.ts`, `app/lib/types.ts`
- `app/about/`, `app/chat/`, `app/contact/`, `app/login/`, `app/privacy/`, `app/settings/`
- Old `tailwind.config.js` (replaced by `.ts`)

---

### Build Result

✅ **Next.js 14.2.5 builds successfully** with all 12 routes pre-rendered:
- `/` (Landing)
- `/demo` (Split-screen)
- `/doctor/login`, `/doctor/dashboard`, `/doctor/patients`, `/doctor/consents`, `/doctor/consultations`
- `/patient/login`, `/patient/consent`
</task_result>
```

---

## Assistant (Build · Kimi)

_Thinking:_

 Phase 1 is complete for both subagents. Now I need to launch Phase 2 (Shared Core) and Phase 3 (Auth Layer) in parallel. Both depend on Phase 1 (done), and Phase 4+ steps depend on Phase 2 and 3.

Let me dispatch Phase 2 and Phase 3 now.

 Phase 1 is complete. Now launching Phase 2 (Shared Core) and Phase 3 (Authentication Layer) in parallel. 

**Tool: task**

**Input:**
```json
{
  "description": "Phase 2: Shared Core Backend",
  "prompt": "You are building the shared core backend layer for the Mirage healthcare platform. BEFORE writing any code, you MUST read the following documentation files IN ORDER:\n\n1. /Users/sheltonmutambirwa/Desktop/medic/AGENTS.md — Development instructions\n2. /Users/sheltonmutambirwa/Desktop/medic/docs/02_Technical_Architecture.md — 5-layer architecture, tech stack\n3. /Users/sheltonmutambirwa/Desktop/medic/docs/06_Database_Schema.md — **Authoritative source for ALL table definitions, columns, types, indexes, foreign keys, constraints. UUID PKs, UTC timestamps.**\n4. /Users/sheltonmutambirwa/Desktop/medic/docs/08_Coding_Standards.md — Python 3.12+, strict typing, SQLAlchemy patterns\n5. /Users/sheltonmutambirwa/Desktop/medic/docs/05_API_Contract.md — REST API patterns, base response envelope, error codes, WebSocket event types\n\nAfter reading these, inspect the existing backend skeleton at /Users/sheltonmutambirwa/Desktop/medic/backend/ to understand what was created in Phase 1.\n\nYOUR TASKS:\n\n1. **Database Models** (`/Users/sheltonmutambirwa/Desktop/medic/backend/app/db/models.py`):\n   - Implement ALL tables defined in the Database Schema doc using SQLAlchemy 2.0 declarative base (async style).\n   - Every table must use `UUID` primary keys with `default=uuid.uuid4`.\n   - Every model must have `created_at` and `updated_at` columns using `DateTime(timezone=True)` with server default `func.now()` / `onupdate=func.now()`.\n   - All `__tablename__` values must match the schema doc exactly.\n   - Define all indexes and unique constraints per the schema.\n   - Include relationships between tables where appropriate (e.g., User ↔ ConsentRequest, ConsentRequest ↔ PatientRecord).\n   - Use explicit `Mapped[...]` and `mapped_column(...)` syntax (SQLAlchemy 2.0 style).\n\n2. **Pydantic Schemas** (`/Users/sheltonmutambirwa/Desktop/medic/backend/app/shared/schemas.py`):\n   - Create base `MirageBaseModel` extending `BaseModel` with `ConfigDict(from_attributes=True)`.\n   - Create request/response schemas for every entity in the Database Schema.\n   - Use `UUID` type annotation for all ID fields.\n   - Include `datetime` fields with explicit `Field(...)` descriptions.\n   - Separate `Create`, `Update`, `Response`, and `ListResponse` variants where appropriate.\n   - Create a generic `Envelope[T]` generic model for API responses matching the API Contract (success, data, message, error_code).\n\n3. **Database Session & Engine** (`/Users/sheltonmutambirwa/Desktop/medic/backend/app/db/session.py`):\n   - Create async SQLAlchemy engine using `create_async_engine` with connection pool settings.\n   - Create `AsyncSessionLocal` using `async_sessionmaker`.\n   - Implement `get_db()` async dependency generator for FastAPI.\n   - Implement `init_db()` async function that creates all tables (used on startup during dev).\n   - Read database URL from environment (via Pydantic Settings from Phase 1 skeleton).\n\n4. **Database Migrations** (`/Users/sheltonmutambirwa/Desktop/medic/backend/alembic/env.py`):\n   - Update the existing alembic env.py to target the async SQLAlchemy engine.\n   - Import your Base and models so autogenerate works.\n   - Ensure it reads the database URL from the same settings source.\n\n5. **Settings / Config** (`/Users/sheltonmutambirwa/Desktop/medic/backend/app/shared/settings.py`):\n   - Pydantic-Settings `Settings` class reading from environment variables.\n   - Required fields: `DATABASE_URL`, `REDIS_URL`, `SECRET_KEY`, `JWT_ALGORITHM` (default HS256), `ACCESS_TOKEN_EXPIRE_MINUTES`, `REFRESH_TOKEN_EXPIRE_DAYS`, `DEMO_MODE_ENABLED`, `AI_PROVIDER` (default \"mock\").\n   - Use `model_config = SettingsConfigDict(env_file=\".env\", env_file_encoding=\"utf-8\")`.\n\n6. **Exception Handling** (`/Users/sheltonmutambirwa/Desktop/medic/backend/app/shared/exceptions.py`):\n   - Define custom exceptions: `MirageException`, `NotFoundException`, `ValidationException`, `UnauthorizedException`, `ForbiddenException`, `ConflictException`.\n   - Each should carry an optional `error_code` string for API Contract compliance.\n\n7. **Logging Configuration** (`/Users/sheltonmutambirwa/Desktop/medic/backend/app/shared/logging_config.py`):\n   - Set up Python `logging` with a consistent formatter.\n   - JSON formatter option for production.\n   - Default INFO level for app modules.\n\n8. **Redis Client Helper** (`/Users/sheltonmutambirwa/Desktop/medic/backend/app/shared/redis_client.py`):\n   - Async Redis client singleton using `redis.asyncio.Redis`.\n   - `get_redis()` function returning the shared client.\n   - Reads Redis URL from Settings.\n\nIMPORTANT CONSTRAINTS:\n- Do NOT use MongoDB anywhere.\n- Python 3.12+ with strict typing (`from __future__ import annotations`, `list[str]` not `List[str]`).\n- SQLAlchemy 2.0 style ONLY (no legacy `declarative_base()` or `Column(...)` without `mapped_column`).\n- UUID PKs everywhere. UTC timestamps everywhere.\n- All file paths absolute starting from `/Users/sheltonmutambirwa/Desktop/medic/`.\n\nReturn a summary of every file you created/modified and any schema tables you implemented.",
  "subagent_type": "general"
}
```

**Tool: task**

**Input:**
```json
{
  "description": "Phase 3: Authentication Layer",
  "prompt": "You are building the authentication layer for the Mirage healthcare platform. BEFORE writing any code, you MUST read the following documentation files IN ORDER:\n\n1. /Users/sheltonmutambirwa/Desktop/medic/AGENTS.md — Development instructions\n2. /Users/sheltonmutambirwa/Desktop/medic/docs/01_Product_Requirements_Document.md — Product behaviour authority, especially Demo Mode and JWT requirements\n3. /Users/sheltonmutambirwa/Desktop/medic/docs/02_Technical_Architecture.md — Auth stack (JWT, OAuth2-password-bearer, bcrypt)\n4. /Users/sheltonmutambirwa/Desktop/medic/docs/05_API_Contract.md — **Authoritative source for all auth endpoints, request/response shapes, error codes**\n5. /Users/sheltonmutambirwa/Desktop/medic/docs/06_Database_Schema.md — Users table definition (roles: doctor, patient, admin; password_hash; phone; national_id)\n6. /Users/sheltonmutambirwa/Desktop/medic/docs/08_Coding_Standards.md — Python 3.12+, strict typing, security patterns\n\nAfter reading these, inspect the existing backend at /Users/sheltonmutambirwa/Desktop/medic/backend/ to understand Phase 1 structure and what already exists.\n\nYOUR TASKS:\n\n1. **Password Hashing Utility** (`/Users/sheltonmutambirwa/Desktop/medic/backend/app/auth/password.py`):\n   - Use `passlib[bcrypt]` with bcrypt.\n   - `hash_password(plain: str) -> str`\n   - `verify_password(plain: str, hashed: str) -> bool`\n   - Configurable rounds via settings (default 12).\n\n2. **JWT Token Utilities** (`/Users/sheltonmutambirwa/Desktop/medic/backend/app/auth/jwt.py`):\n   - Use `python-jose[cryptography]` with HS256 (upgrade to RS256 later if specified).\n   - `create_access_token(subject: UUID, role: str, expires_delta: timedelta | None = None) -> str`\n   - `create_refresh_token(subject: UUID, expires_delta: timedelta | None = None) -> str`\n   - `decode_token(token: str) -> dict` raising `UnauthorizedException` on expired/invalid.\n   - Include `jti` (JWT ID) claim for future revocation support.\n   - Include `type` claim distinguishing \"access\" vs \"refresh\".\n\n3. **Auth Dependencies** (`/Users/sheltonmutambirwa/Desktop/medic/backend/app/auth/dependencies.py`):\n   - `get_current_user(token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)) -> User`\n   - `require_role(*roles: str)` dependency factory returning `Depends` that checks `current_user.role`.\n   - `get_current_doctor = require_role(\"doctor\", \"admin\")`\n   - `get_current_patient = require_role(\"patient\", \"admin\")`\n   - All dependencies must be async and raise `UnauthorizedException` / `ForbiddenException` appropriately.\n\n4. **Demo Mode Handler** (`/Users/sheltonmutambirwa/Desktop/medic/backend/app/auth/demo.py`):\n   - `DEMO_CREDENTIALS` hardcoded per the PRD: doctor email `dr.sarah.mirage@mirage.health`, password `Healthathon2024!`; patient national_id `ZIM-89-4567234`, PIN `2024`.\n   - `authenticate_demo_doctor(email: str, password: str) -> bool`\n   - `authenticate_demo_patient(national_id: str, pin: str) -> bool`\n   - On demo auth success, generate a real JWT token with a synthetic UUID subject (deterministically derived from the demo identifier so it's consistent across requests).\n   - `is_demo_token(token_payload: dict) -> bool` to flag demo sessions.\n\n5. **Auth Service** (`/Users/sheltonmutambirwa/Desktop/medic/backend/app/auth/service.py`):\n   - `login_doctor(email: str, password: str, db: AsyncSession) -> TokenPair` — checks real DB first, falls back to demo handler if `DEMO_MODE_ENABLED`.\n   - `login_patient(national_id: str, pin: str, db: AsyncSession) -> TokenPair` — same pattern.\n   - `refresh_access_token(refresh_token: str) -> str`\n   - `logout(token_jti: str)` — blacklist the JTI in Redis with TTL matching token expiry.\n   - Pydantic response model `TokenPair` with `access_token`, `refresh_token`, `token_type=\"bearer\"`, `expires_in`, `role`, `demo_mode: bool`.\n\n6. **Auth Router** (`/Users/sheltonmutambirwa/Desktop/medic/backend/app/auth/router.py`):\n   - POST `/api/v1/auth/doctor/login` — request body `{email, password}`, returns TokenPair.\n   - POST `/api/v1/auth/patient/login` — request body `{national_id, pin}`, returns TokenPair.\n   - POST `/api/v1/auth/refresh` — request body `{refresh_token}`, returns new access token.\n   - POST `/api/v1/auth/logout` — requires current token, blacklists JTI in Redis, returns success.\n   - GET `/api/v1/auth/me` — returns current user profile (from DB or synthetic demo user).\n   - All endpoints must return the standard API Envelope format from shared schemas.\n   - Include OpenAPI summary/description on each endpoint.\n\n7. **Demo Data Seeder** (`/Users/sheltonmutambirwa/Desktop/medic/backend/app/db/seeder.py`):\n   - Async function `seed_demo_data(db: AsyncSession)` that creates:\n     - The demo doctor user (Dr. Sarah Mirage) with role \"doctor\", specialty \"Internal Medicine\", if not exists.\n     - The demo patient user (Tendai Mutasa) with role \"patient\", national_id `ZIM-89-4567234`, date_of_birth `1989-05-14`, if not exists.\n     - A `PatientRecord` linked to the demo patient with a few synthetic conditions, allergies, medications.\n     - Use `get_or_create` pattern (query first, create if missing).\n     - Must hash passwords using the password utility above.\n   - This seeder runs automatically when backend starts if `DEMO_MODE_ENABLED=true`.\n\n8. **Register Auth Router in Main App** (`/Users/sheltonmutambirwa/Desktop/medic/backend/main.py`):\n   - Update the existing `main.py` (from Phase 1) to include `app.include_router(auth.router, prefix=\"/api/v1/auth\", tags=[\"Authentication\"])`.\n   - Add startup event handler that calls `init_db()` and `seed_demo_data()`.\n   - Ensure CORS allows localhost:3000.\n\nIMPORTANT CONSTRAINTS:\n- Do NOT use MongoDB anywhere.\n- Python 3.12+ strict typing. Use `from __future__ import annotations`.\n- Demo credentials MUST match the PRD exactly.\n- All JWT operations must handle expiry gracefully.\n- Redis blacklisting must use TTL so keys auto-expire.\n- Synthetic demo UUID must be deterministic (e.g., `uuid5(NAMESPACE_OID, demo_identifier)`).\n- Return `Envelope[TokenPair]` and `Envelope[UserResponse]` from all auth endpoints.\n- All file paths absolute starting from `/Users/sheltonmutambirwa/Desktop/medic/`.\n\nReturn a summary of every file you created/modified.",
  "subagent_type": "general"
}
```

**Output:**
```
task_id: ses_0cd2addebffeodtcIptJly8AWJ (for resuming to continue this task if needed)

<task_result>
 Here is the summary of every file created or modified for the Mirage authentication layer:

---

### **Core Infrastructure (Created)**

| File | Purpose |
|------|---------|
| `/Users/sheltonmutambirwa/Desktop/medic/backend/app/core/__init__.py` | Package marker for core utilities. |
| `/Users/sheltonmutambirwa/Desktop/medic/backend/app/core/config.py` | Pydantic-settings configuration object (`Settings`) for `database_url`, `redis_url`, JWT secrets, `demo_mode_enabled`, `bcrypt_rounds`, etc. |
| `/Users/sheltonmutambirwa/Desktop/medic/backend/app/core/exceptions.py` | Domain exceptions: `MirageException`, `UnauthorizedException`, `ForbiddenException`. |
| `/Users/sheltonmutambirwa/Desktop/medic/backend/app/core/database.py` | SQLAlchemy 2.x async engine/session factory, `Base`, `get_db()` dependency, and `init_db()` startup helper. |
| `/Users/sheltonmutambirwa/Desktop/medic/backend/app/core/redis.py` | Singleton async `Redis` client factory via `Redis.from_url`. |

---

### **Schemas (Created)**

| File | Purpose |
|------|---------|
| `/Users/sheltonmutambirwa/Desktop/medic/backend/app/schemas/__init__.py` | Exports `Envelope`, `TokenPair`, `UserResponse`. |
| `/Users/sheltonmutambirwa/Desktop/medic/backend/app/schemas/envelope.py` | Generic `Envelope[T]` with `success`, `data`, `errors`, `meta` (requestId + timestamp). |
| `/Users/sheltonmutambirwa/Desktop/medic/backend/app/schemas/token.py` | Pydantic `TokenPair` — `access_token`, `refresh_token`, `token_type`, `expires_in`, `role`, `demo_mode`. |
| `/Users/sheltonmutambirwa/Desktop/medic/backend/app/schemas/user.py` | Pydantic `UserResponse` — `id`, `role`, `first_name`, `last_name`, `email`, `avatar_url`. |

---

### **Models (Created / Modified)**

| File | Purpose |
|------|---------|
| `/Users/sheltonmutambirwa/Desktop/medic/backend/app/models/__init__.py` | **Modified** — added `Doctor` import/export. |
| `/Users/sheltonmutambirwa/Desktop/medic/backend/app/models/user.py` | SQLAlchemy `User` model with `id` (UUID), `email`, `password_hash`, `role`, `first_name`, `last_name`, etc. |
| `/Users/sheltonmutambirwa/Desktop/medic/backend/app/models/doctor.py` | SQLAlchemy `Doctor` model linked to `User` with `registration_number`, `specialty`, `facility_id`, etc. |
| `/Users/sheltonmutambirwa/Desktop/medic/backend/app/models/patient_record.py` | SQLAlchemy models: `Patient`, `MedicalRecord`, `Allergy`, `ChronicCondition`, `Medication` with relationships. |

---

### **Auth Layer (Created / Modified)**

| File | Purpose |
|------|---------|
| `/Users/sheltonmutambirwa/Desktop/medic/backend/app/auth/__init__.py` | **Modified** — exports `router`. |
| `/Users/sheltonmutambirwa/Desktop/medic/backend/app/auth/password.py` | `hash_password(plain) -> str` and `verify_password(plain, hashed) -> bool` using `passlib[bcrypt]` with configurable rounds. |
| `/Users/sheltonmutambirwa/Desktop/medic/backend/app/auth/jwt.py` | `create_access_token`, `create_refresh_token`, `decode_token`, `decode_refresh_token`. HS256 via `python-jose[cryptography]`. Includes `jti` and `type` claims. |
| `/Users/sheltonmutambirwa/Desktop/medic/backend/app/auth/demo.py` | `DEMO_CREDENTIALS`, `authenticate_demo_doctor`, `authenticate_demo_patient`, `generate_demo_tokens`, `is_demo_token`. Uses deterministic `uuid5` for synthetic demo subjects. |
| `/Users/sheltonmutambirwa/Desktop/medic/backend/app/auth/dependencies.py` | `get_current_user`, `get_current_active_user`, `require_role(*roles)` factory, `get_current_doctor`, `get_current_patient`. All async; raise `UnauthorizedException`/`ForbiddenException`. |
| `/Users/sheltonmutambirwa/Desktop/medic/backend/app/auth/service.py` | `login_doctor`, `login_patient` (real DB → demo fallback), `refresh_access_token`, `logout` (Redis JTI blacklist with TTL). |
| `/Users/sheltonmutambirwa/Desktop/medic/backend/app/auth/router.py` | FastAPI router with endpoints: `POST /doctor/login`, `POST /patient/login`, `POST /refresh`, `POST /logout`, `GET /me`. Returns `Envelope[...]` on every endpoint. |

---

### **Seeder (Created)**

| File | Purpose |
|------|---------|
| `/Users/sheltonmutambirwa/Desktop/medic/backend/app/db/seeder.py` | `seed_demo_data(db)` — idempotent get-or-create for demo doctor (Dr. Sarah Mirage), demo patient (Tendai Mutasa), linked `MedicalRecord`, plus synthetic `ChronicCondition`, `Allergy`, and `Medication` rows. |

---

### **Application Entrypoint (Modified)**

| File | Purpose |
|------|---------|
| `/Users/sheltonmutambirwa/Desktop/medic/backend/main.py` | **Modified** — includes `CORSMiddleware` (allowing `localhost:3000`), mounts auth router under `/api/v1/auth`, and adds `startup_event` calling `init_db()` and `seed_demo_data()` when demo mode is enabled. |

---

All files are written with Python 3.12+ strict typing (`from __future__ import annotations`), no MongoDB, and conform to the PRD / API Contract / Database Schema / Coding Standards.
</task_result>
```

---

