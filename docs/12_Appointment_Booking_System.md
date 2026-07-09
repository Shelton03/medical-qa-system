# Mirage
# Appointment Booking System Specification

Version: 1.0
Status: Ready for Implementation
Last Updated: 2024-07-08

---

# Table of Contents

1. Overview & Purpose
2. Design Decisions
3. Database Schema Changes
4. Auto-Routing Algorithm
5. Backend Architecture
6. API Contract
7. Frontend Architecture
8. Admin UI Specification
9. Integration Points
10. Notification Events
11. Bug Fixes & Improvements
12. Implementation Timeline

---

# 1. Overview & Purpose

The Appointment Booking System enables patients to schedule healthcare appointments at facilities. Key capabilities:

- **Patient Booking:** Book at a facility (not specific doctor) for a chosen date
- **Intelligent Auto-Routing:** System assigns optimal doctor based on:
  - Patient's historical doctor relationships
  - Symptom-to-specialty matching
  - Doctor availability and current workload
  - Priority/triage level
- **Day-of Consultation:** On appointment day, patient starts AI pre-assessment
- **Doctor Schedule View:** Doctors see daily/weekly appointment schedules
- **Admin Management:** Admins configure doctor schedules, leave, and facility settings

### Why This Feature Exists

Previously, only doctors could initiate consultations. Patients could not start symptom checking before seeing a doctor. This system bridges that gap by allowing patients to book, then begin their AI-assisted assessment on the appointment day.

---

# 2. Design Decisions

| Decision | Choice | Rationale |
|---|---|---|
| Facility vs Doctor booking | Book at facility | Auto-routing selects best doctor |
| Date/Time selection | Date only + desired duration | Time slot auto-calculated via triage |
| Preferred doctor | Optional request | If unavailable, auto-routes to next best |
| No doctor available | Explicit message | "No doctor available" shown to patient |
| Emergency handling | Bypass queue | First available doctor, urgent priority |
| Cancellation notice | 3 days prior | Medical scheduling standard |
| Admin manages schedules | Yes + default hours | Doctors can have leave, admin oversight |
| Buffer between appointments | 3 minutes | Prevents back-to-back overload |
| Demo mode for admin | Yes | Admin UI has demo-login for testing |
| Calendar view | Doctor can choose week or day | Flexibility in viewing schedule |
| Notifications | Both in-app and WebSocket | Real-time plus persistent notifications |
| Priority levels | Emergency, Urgent, Normal, Low | Based on patient history + self-reported urgency |

---


# 3. Database Schema Changes

## 3.1 Modified Tables

### `doctors` — Extended Fields

```sql
ALTER TABLE doctors ADD COLUMN IF NOT EXISTS
    max_daily_appointments INT DEFAULT 20,
    is_accepting_appointments BOOLEAN DEFAULT TRUE,
    next_available_date DATE,
    created_by UUID REFERENCES users(id),
    updated_by UUID REFERENCES users(id);
```

**Updated columns:**
| Column | Type | Constraints | Description |
|---|---|---|---|
| specialty | VARCHAR(255) | nullable=True | Required for routing (e.g., "Cardiology", "Pediatrics") |
| max_daily_appointments | INT | DEFAULT 20 | Max appointments per day |
| is_accepting_appointments | BOOLEAN | DEFAULT TRUE | Toggle availability |
| next_available_date | DATE | nullable | Pre-computed for quick lookup |

**Existing columns preserved:**
`id`, `user_id`, `registration_number`, `facility_id`, `department`, `license_expiry`, `years_experience`, `created_at`, `updated_at`

### `users` — No changes (role already supports "admin")

## 3.2 New Tables

### `appointments`

```sql
CREATE TABLE appointments (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    patient_id UUID NOT NULL REFERENCES patients(id),
    facility_id UUID NOT NULL REFERENCES facilities(id),
    doctor_id UUID REFERENCES doctors(id),
    visit_id UUID REFERENCES visits(id),
    
    appointment_date DATE NOT NULL,
    desired_duration_minutes INT DEFAULT 30,
    allocated_start_time TIME,
    allocated_end_time TIME,
    
    status VARCHAR(20) NOT NULL DEFAULT 'PENDING',
    reason TEXT,
    symptoms TEXT,
    priority VARCHAR(20) DEFAULT 'NORMAL',
    is_emergency BOOLEAN DEFAULT FALSE,
    triage_score INT DEFAULT 0,
    
    preferred_doctor_id UUID REFERENCES doctors(id),
    
    patient_confirmed_at TIMESTAMP,
    doctor_confirmed_at TIMESTAMP,
    cancelled_at TIMESTAMP,
    cancelled_by VARCHAR(20),
    cancellation_reason TEXT,
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
```

Indexes: `patient_id`, `facility_id`, `doctor_id`, `appointment_date`, `status`, `priority`

### `doctor_schedules` (Admin-managed)

```sql
CREATE TABLE doctor_schedules (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    doctor_id UUID NOT NULL REFERENCES doctors(id),
    day_of_week INT NOT NULL CHECK (day_of_week BETWEEN 0 AND 6),
    start_time TIME NOT NULL DEFAULT '08:00',
    end_time TIME NOT NULL DEFAULT '17:00',
    is_working_day BOOLEAN DEFAULT TRUE,
    default_slot_duration INT DEFAULT 30,
    max_daily_appointments INT DEFAULT 20,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    
    UNIQUE(doctor_id, day_of_week)
);
```

### `doctor_time_offs` (Leave / Unavailability)

```sql
CREATE TABLE doctor_time_offs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    doctor_id UUID NOT NULL REFERENCES doctors(id),
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    type VARCHAR(20) DEFAULT 'LEAVE',
    reason TEXT,
    status VARCHAR(20) DEFAULT 'APPROVED',
    requested_by UUID REFERENCES users(id),
    approved_by UUID REFERENCES users(id),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
```

### `appointment_slot_allocations`

```sql
CREATE TABLE appointment_slot_allocations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    appointment_id UUID NOT NULL REFERENCES appointments(id),
    doctor_id UUID NOT NULL REFERENCES doctors(id),
    slot_date DATE NOT NULL,
    start_time TIME NOT NULL,
    end_time TIME NOT NULL,
    buffer_after_minutes INT DEFAULT 3,
    status VARCHAR(20) DEFAULT 'ALLOCATED',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
```

## 3.3 SQLAlchemy Model Additions

Add to existing models:

**Doctor model additions:**
```python
max_daily_appointments: Mapped[int | None] = mapped_column(Integer, default=20)
is_accepting_appointments: Mapped[bool] = mapped_column(Boolean, default=True)
next_available_date: Mapped[date | None] = mapped_column(Date(), nullable=True)

appointments: Mapped[List["Appointment"]] = relationship("Appointment", foreign_keys="Appointment.doctor_id")
schedules: Mapped[List["DoctorSchedule"]] = relationship("DoctorSchedule")
time_offs: Mapped[List["DoctorTimeOff"]] = relationship("DoctorTimeOff")
```

**Patient model additions:**
```python
appointments: Mapped[List["Appointment"]] = relationship("Appointment", back_populates="patient")
```

**Facility model additions:**
```python
appointments: Mapped[List["Appointment"]] = relationship("Appointment", back_populates="facility")
```

**Visit model additions:**
```python
appointment: Mapped["Appointment"] = relationship("Appointment", back_populates="visit", uselist=False)
```

**New Appointment model:**
```python
class Appointment(Base):
    __tablename__ = "appointments"
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    patient_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("patients.id"), nullable=False)
    facility_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("facilities.id"), nullable=False)
    doctor_id: Mapped[uuid.UUID | None] = mapped_column(ForeignKey("doctors.id"), nullable=True)
    visit_id: Mapped[uuid.UUID | None] = mapped_column(ForeignKey("visits.id"), nullable=True)
    appointment_date: Mapped[date] = mapped_column(Date(), nullable=False)
    desired_duration_minutes: Mapped[int] = mapped_column(Integer, default=30)
    allocated_start_time: Mapped[time | None] = mapped_column(Time(), nullable=True)
    allocated_end_time: Mapped[time | None] = mapped_column(Time(), nullable=True)
    status: Mapped[str] = mapped_column(String(20), default="PENDING")
    reason: Mapped[str | None] = mapped_column(Text, nullable=True)
    symptoms: Mapped[str | None] = mapped_column(Text, nullable=True)
    priority: Mapped[str] = mapped_column(String(20), default="NORMAL")
    is_emergency: Mapped[bool] = mapped_column(Boolean, default=False)
    triage_score: Mapped[int] = mapped_column(Integer, default=0)
    preferred_doctor_id: Mapped[uuid.UUID | None] = mapped_column(ForeignKey("doctors.id"), nullable=True)
    patient_confirmed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    doctor_confirmed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    cancelled_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    cancelled_by: Mapped[str | None] = mapped_column(String(20), nullable=True)
    cancellation_reason: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
```


---

# 4. Auto-Routing Algorithm

## 4.1 Input Parameters

- `facility_id`: UUID — Selected facility
- `patient_id`: UUID — Authenticated patient
- `symptoms`: str — Patient symptom description
- `appointment_date`: date — Selected date
- `desired_duration`: int — Minutes (15, 30, 45, 60)
- `is_emergency`: bool — Emergency flag
- `preferred_doctor_id`: UUID | None — Optional preference

## 4.2 Scoring System (100-point scale)

### Prerequisite Checks (Must pass all)
- Doctor belongs to facility
- Doctor is working on selected day
- Doctor is not on leave
- Doctor has capacity (appointments < max_daily_appointments)
- Doctor is accepting appointments

### Scoring Factors

**1. Patient History Match** (max 35 points)
| Condition | Points |
|---|---|
| Exact doctor seen in past visits | +35 |
| Same specialty as previous visit doctor | +20 |
| Any history with this facility | +10 |

**2. Specialty-Symptom Match** (max 25 points)
| Condition | Points |
|---|---|
| Direct keyword match with specialty | +25 |
| Partial match | +15 |
| Related specialty | +5 |

**3. Availability & Workload** (max 25 points)
| Condition | Points |
|---|---|
| < 30% capacity used | +25 |
| 30-60% capacity used | +15 |
| 60-80% capacity used | +5 |
| > 80% capacity | 0 |

**4. Preferred Doctor** (max 15 points)
| Condition | Points |
|---|---|
| Matches patient preference | +15 |

### Emergency Override

If `is_emergency = TRUE`: bypass scoring, select first available doctor, notify ALL doctors in facility.

## 4.3 Algorithm Flow

```python
async def auto_route_to_doctor(
    db, facility_id, patient_id, symptoms, 
    appointment_date, desired_duration=30,
    is_emergency=False, preferred_doctor_id=None
) -> uuid.UUID | None:
    
    # 1. Get available doctors at facility
    doctors = await get_available_doctors(db, facility_id, appointment_date)
    if not doctors:
        return None
    
    # Emergency: bypass scoring
    if is_emergency:
        for doctor in doctors:
            if await has_capacity(db, doctor.id, appointment_date, desired_duration):
                await notify_all_doctors(db, facility_id, "EMERGENCY appointment")
                return doctor.id
        return None
    
    # 2. Score each doctor
    scored = []
    for doctor in doctors:
        if not await has_capacity(db, doctor.id, appointment_date, desired_duration):
            continue
        
        score = 0
        score += await calculate_history_score(db, patient_id, doctor.id)      # 0-35
        score += await calculate_specialty_score(symptoms, doctor.specialty)   # 0-25
        score += await calculate_workload_score(db, doctor.id, appointment_date) # 0-25
        
        if preferred_doctor_id and doctor.id == preferred_doctor_id:
            score += 15
        
        scored.append((doctor, score))
    
    if not scored:
        return None
    
    # 3. Sort by score desc, return best
    scored.sort(key=lambda x: x[1], reverse=True)
    return scored[0][0].id
```

## 4.4 Specialty Keyword Mapping

```python
SPECIALTY_KEYWORDS = {
    "cardiology": ["heart", "chest pain", "chest", "blood pressure", "hypertension", "cardiac", "palpitations"],
    "pediatrics": ["child", "baby", "infant", "toddler", "fever", "cough", "vaccination", "growth"],
    "obstetrics and gynaecology": ["pregnancy", "pregnant", "menstrual", "period", "ovary", "fertility", "birth"],
    "internal medicine": ["diabetes", "thyroid", "hormone", "chronic", "fatigue", "weight loss"],
    "general practice": ["cold", "flu", "headache", "rash", "checkup", "review", "general"],
    "dermatology": ["skin", "rash", "acne", "eczema", "psoriasis", "lesion", "mole", "itching"],
    "orthopedics": ["bone", "fracture", "joint", "knee", "back pain", "shoulder", "sprain", "arthritis"],
    "neurology": ["headache", "migraine", "seizure", "tremor", "numbness", "memory", "dizziness", "stroke"],
    "psychiatry": ["anxiety", "depression", "stress", "insomnia", "mood", "mental health", "panic"],
    "gastroenterology": ["stomach", "abdominal pain", "nausea", "vomiting", "diarrhea", "liver", "digestion"],
    "urology": ["urinary", "kidney", "bladder", "prostate", "urination"],
    "pulmonology": ["cough", "breathing", "asthma", "pneumonia", "tb", "tuberculosis", "shortness of breath"],
    "endocrinology": ["diabetes", "thyroid", "hormone", "metabolism", "weight", "growth", "pituitary"],
    "nephrology": ["kidney", "renal", "dialysis", "proteinuria", "creatinine"],
    "hematology": ["anemia", "bleeding", "clotting", "blood", "transfusion"],
    "infectious disease": ["infection", "fever", "malaria", "hiv", "tb", "sepsis"],
    "oncology": ["cancer", "tumor", "mass", "chemotherapy", "radiation"],
    "ophthalmology": ["eye", "vision", "blurred", "cataract", "glaucoma", "retinopathy"],
    "ent": ["ear", "nose", "throat", "sinus", "hearing", "tonsils"],
}
```

## 4.5 Time Slot Allocation with Buffer

```python
async def allocate_time_slot(
    db, doctor_id, appointment_date, desired_duration, buffer_minutes=3
) -> tuple[time, time] | None:
    
    schedule = await get_doctor_schedule(db, doctor_id, appointment_date)
    if not schedule or not schedule.is_working_day:
        return None
    
    existing = await get_existing_allocations(db, doctor_id, appointment_date)
    current_time = schedule.start_time
    total_needed = timedelta(minutes=desired_duration + buffer_minutes)
    
    for allocation in existing:
        gap = datetime.combine(appointment_date, allocation.start_time) - \
              datetime.combine(appointment_date, current_time)
        
        if gap >= total_needed:
            start = current_time
            end = (datetime.combine(appointment_date, current_time) + 
                   timedelta(minutes=desired_duration)).time()
            return (start, end)
        
        current_time = (datetime.combine(appointment_date, allocation.end_time) +
                       timedelta(minutes=buffer_minutes)).time()
    
    # Check remaining time
    if (datetime.combine(appointment_date, schedule.end_time) - 
        datetime.combine(appointment_date, current_time)) >= total_needed:
        start = current_time
        end = (datetime.combine(appointment_date, current_time) + 
               timedelta(minutes=desired_duration)).time()
        return (start, end)
    
    return None
```


---

# 5. Backend Architecture

## 5.1 Directory Structure

```
backend/app/appointment/
  __init__.py          # Router export
  router.py            # REST endpoints
  service.py           # Business logic + auto-routing
  repository.py        # Database queries
  schemas.py           # Pydantic DTOs
  enums.py             # Status & priority enums

backend/app/facility/
  __init__.py
  router.py
  service.py
  repository.py
  schemas.py

backend/app/schedule/
  __init__.py
  router.py            # Admin schedule management
  service.py
  repository.py
  schemas.py
```

## 5.2 Enums

```python
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
```

## 5.3 Key Schemas

```python
class AppointmentCreateRequest(BaseModel):
    facility_id: uuid.UUID
    appointment_date: date
    desired_duration_minutes: int = Field(default=30, ge=15, le=120)
    symptoms: str = Field(..., min_length=10, max_length=2000)
    reason: Optional[str] = Field(default=None, max_length=500)
    is_emergency: bool = False
    preferred_doctor_id: Optional[uuid.UUID] = None

class AppointmentResponse(BaseModel):
    id: uuid.UUID
    patient_id: uuid.UUID
    facility_id: uuid.UUID
    doctor_id: Optional[uuid.UUID] = None
    visit_id: Optional[uuid.UUID] = None
    appointment_date: date
    desired_duration_minutes: int
    allocated_start_time: Optional[time] = None
    allocated_end_time: Optional[time] = None
    status: AppointmentStatus
    reason: Optional[str] = None
    symptoms: Optional[str] = None
    priority: Priority
    is_emergency: bool
    preferred_doctor_id: Optional[uuid.UUID] = None
    triage_score: int
    facility: Optional[dict] = None
    doctor: Optional[dict] = None
    created_at: datetime

class DoctorScheduleResponse(BaseModel):
    id: uuid.UUID
    doctor_id: uuid.UUID
    day_of_week: int
    start_time: time
    end_time: time
    is_working_day: bool
    default_slot_duration: int
    max_daily_appointments: int

class TimeOffRequest(BaseModel):
    doctor_id: uuid.UUID
    start_date: date
    end_date: date
    type: str = "LEAVE"
    reason: Optional[str] = None
```

## 5.4 Service Layer Interface

```python
class AppointmentService:
    async def create_booking(self, db, patient_id, data: AppointmentCreateRequest) -> Appointment
    async def cancel_appointment(self, db, appointment_id, cancelled_by, user_id, reason=None) -> Appointment
    async def confirm_appointment(self, db, appointment_id, confirmed_by) -> Appointment
    async def start_consultation_from_appointment(self, db, appointment_id, patient_id) -> Visit
    async def get_patient_appointments(self, db, patient_id, status=None, limit=50, offset=0) -> tuple[list[Appointment], int]
    async def get_doctor_schedule(self, db, doctor_id, date=None) -> list[Appointment]
    async def update_doctor_schedule(self, db, doctor_id, schedules) -> list[DoctorSchedule]
    async def add_time_off(self, db, data: TimeOffRequest, requested_by) -> DoctorTimeOff

class AutoRoutingService:
    async def find_optimal_doctor(self, db, facility_id, patient_id, symptoms, appointment_date, 
                                  desired_duration=30, is_emergency=False, preferred_doctor_id=None) -> uuid.UUID | None
    async def calculate_history_score(self, db, patient_id, doctor_id) -> int  # 0-35
    async def calculate_specialty_score(self, symptoms, specialty) -> int        # 0-25
    async def calculate_workload_score(self, db, doctor_id, appointment_date) -> int  # 0-25
```


---

# 6. API Contract

## 6.1 Patient Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| POST | `/appointments` | Patient | Create booking |
| GET | `/appointments/my` | Patient | List my appointments |
| GET | `/appointments/{id}` | Patient | Get appointment details |
| PUT | `/appointments/{id}/cancel` | Patient | Cancel (3-day notice enforced) |
| POST | `/appointments/{id}/confirm` | Patient | Confirm booking |
| POST | `/appointments/{id}/start-consultation` | Patient | Start day-of consultation |

## 6.2 Doctor Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/doctor/schedule` | Doctor | View my schedule |
| GET | `/doctor/appointments/today` | Doctor | Today's appointments |
| PUT | `/doctor/appointments/{id}/status` | Doctor | Update status |
| GET | `/doctor/availability` | Doctor | My availability settings |

## 6.3 Facility Endpoints (Public/Authenticated)

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/facilities` | Any | Search/list facilities |
| GET | `/facilities/{id}` | Any | Facility details |
| GET | `/facilities/{id}/doctors` | Any | Doctors at facility |

## 6.4 Admin Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/admin/dashboard` | Admin | Dashboard stats |
| GET | `/admin/doctors/{id}/schedule` | Admin | View doctor schedule |
| PUT | `/admin/doctors/{id}/schedule` | Admin | Update schedule |
| POST | `/admin/doctors/{id}/time-off` | Admin | Add leave |
| GET | `/admin/appointments` | Admin | All appointments |
| GET | `/admin/doctors` | Admin | Manage doctors |

## 6.5 Request/Response Example

**POST /api/v1/appointments**
```json
// Request
{
    "facility_id": "550e8400-e29b-41d4-a716-446655440000",
    "appointment_date": "2024-07-15",
    "desired_duration_minutes": 30,
    "symptoms": "chest pain and shortness of breath when walking upstairs",
    "reason": "Follow-up for hypertension",
    "is_emergency": false,
    "preferred_doctor_id": null
}

// Response 200
{
    "statusCode": 200,
    "message": "Appointment booked successfully",
    "success": true,
    "data": {
        "id": "660e8400-e29b-41d4-a716-446655440001",
        "patient_id": "770e8400-e29b-41d4-a716-446655440002",
        "facility_id": "550e8400-e29b-41d4-a716-446655440000",
        "doctor_id": "880e8400-e29b-41d4-a716-446655440003",
        "appointment_date": "2024-07-15",
        "allocated_start_time": "09:00:00",
        "allocated_end_time": "09:30:00",
        "status": "CONFIRMED",
        "priority": "NORMAL",
        "triage_score": 72,
        "doctor": {
            "id": "880e8400-e29b-41d4-a716-446655440003",
            "name": "Dr. Sarah Mutasa",
            "specialty": "Cardiology"
        },
        "facility": {
            "id": "550e8400-e29b-41d4-a716-446655440000",
            "name": "Harare Central Hospital"
        }
    }
}
```


---

# 7. Frontend Architecture

## 7.1 New Pages

### Patient Pages
```
app/patient/book-appointment/
  page.tsx                    # Step 1: Select facility
  date/
    page.tsx                  # Step 2: Select date
  symptoms/
    page.tsx                  # Step 3: Describe symptoms
  confirm/
    page.tsx                  # Step 4: Review & confirm

app/patient/appointments/
  page.tsx                    # My appointments list
  [id]/
    page.tsx                  # Appointment detail
```

### Doctor Pages
```
app/doctor/schedule/
  page.tsx                    # Schedule view (calendar + list)
  availability/
    page.tsx                  # Manage availability settings
```

### Admin Pages
```
app/admin/
  layout.tsx                  # Admin shell with sidebar
  login/
    page.tsx                  # Admin login with demo
  dashboard/
    page.tsx                  # Admin overview
  doctors/
    page.tsx                  # Manage doctors
  schedules/
    page.tsx                  # All doctor schedules
    [doctorId]/
      page.tsx                # Edit specific schedule
  appointments/
    page.tsx                  # View all appointments
```

## 7.2 Updated Navigation

### Patient Sidebar
- Dashboard
- My Consultations
- **Book Appointment** (NEW)
- **My Appointments** (NEW)
- Timeline
- Notifications
- Settings

### Doctor Sidebar
- Dashboard
- Patients
- **Schedule** (NEW)
- Consultations
- Consents
- Notifications
- Settings

### Admin Sidebar
- Dashboard
- Facilities
- Doctors
- Schedules
- Appointments
- Reports
- Settings

## 7.3 Key Components

### FacilitySearch
- Search bar with city filter
- Facility cards with details
- Availability summary
- Distance indicator (future)

### AppointmentCalendar
- Month view with available dates
- Disabled dates (fully booked, weekends)
- Emergency indicator
- Quick date selection

### SymptomInput
- Textarea with guided prompts
- Duration selector (15/30/45/60 min)
- Emergency toggle with warning
- Character counter

### DoctorMatchCard
- Shows auto-assigned doctor
- Match score indicator
- Specialty badge
- "Request Different Doctor" option
- Preferred doctor toggle

### TriageBadge
- Priority level display
- Color coded (red=emergency, orange=urgent, blue=normal, grey=low)
- Estimated wait time
- Queue position

### ScheduleCalendar (Doctor)
- Week/day toggle
- Appointment blocks with patient info
- Time slots with buffer gaps visible
- Status colors

### AdminDoctorScheduleEditor
- Weekly grid (Mon-Sun)
- Time pickers per day
- Working day toggle
- Max appointments input
- Bulk copy/paste

## 7.4 API Client Additions

```typescript
export const appointmentsApi = {
  create: (data: CreateAppointmentPayload) => 
    request<AppointmentResponse>('/appointments', {
      method: 'POST', body: JSON.stringify(data),
    }),
  listMy: () => 
    request<AppointmentListResponse>('/appointments/my', { method: 'GET' }),
  getById: (id: string) => 
    request<AppointmentResponse>(`/appointments/${id}`, { method: 'GET' }),
  cancel: (id: string, reason: string) => 
    request<void>(`/appointments/${id}/cancel`, {
      method: 'PUT', body: JSON.stringify({ reason }),
    }),
  confirm: (id: string) => 
    request<void>(`/appointments/${id}/confirm`, { method: 'POST' }),
  startConsultation: (id: string) => 
    request<VisitResponse>(`/appointments/${id}/start-consultation`, { method: 'POST' }),
};

export const facilitiesApi = {
  search: (params?: { q?: string; city?: string }) => {
    const search = new URLSearchParams();
    if (params?.q) search.set('q', params.q);
    if (params?.city) search.set('city', params.city);
    return request<FacilityListResponse>(`/facilities?${search}`, { method: 'GET' });
  },
  getById: (id: string) => 
    request<FacilityResponse>(`/facilities/${id}`, { method: 'GET' }),
  getDoctors: (id: string) => 
    request<DoctorListResponse>(`/facilities/${id}/doctors`, { method: 'GET' }),
};

export const scheduleApi = {
  getMySchedule: (date?: string) => 
    request<ScheduleResponse>(`/doctor/schedule${date ? `?date=${date}` : ''}`, { method: 'GET' }),
  getMyAvailability: () => 
    request<AvailabilityResponse>('/doctor/availability', { method: 'GET' }),
  updateAvailability: (data: AvailabilitySettings) => 
    request<void>('/doctor/availability', { method: 'PUT', body: JSON.stringify(data) }),
};

export const adminApi = {
  getDashboard: () => 
    request<AdminDashboardResponse>('/admin/dashboard', { method: 'GET' }),
  getDoctorSchedule: (doctorId: string) => 
    request<DoctorScheduleResponse>(`/admin/doctors/${doctorId}/schedule`, { method: 'GET' }),
  updateDoctorSchedule: (doctorId: string, data: ScheduleUpdatePayload) => 
    request<void>(`/admin/doctors/${doctorId}/schedule`, { method: 'PUT', body: JSON.stringify(data) }),
  addTimeOff: (doctorId: string, data: TimeOffPayload) => 
    request<TimeOffResponse>(`/admin/doctors/${doctorId}/time-off`, { method: 'POST', body: JSON.stringify(data) }),
  listAllAppointments: (params?: { status?: string; date?: string }) => {
    const search = new URLSearchParams();
    if (params?.status) search.set('status', params.status);
    if (params?.date) search.set('date', params.date);
    return request<AppointmentListResponse>(`/admin/appointments?${search}`, { method: 'GET' });
  },
};
```


---

# 8. Admin UI Specification

## 8.1 Admin Login Page (`/admin/login`)

- Admin-specific login form (email + password)
- **Demo login button** with hardcoded credentials:
  - Email: `admin@mirage.health`
  - Password: `Admin2024!`
- Auto-fill on `?demo=1` query param
- Auto-submit after 1.5 seconds
- Redirect to `/admin/dashboard` on success
- Link to main login pages

## 8.2 Admin Dashboard (`/admin/dashboard`)

Statistics cards:
- Total appointments today
- Pending confirmations
- Doctors on leave
- Facility occupancy rate

Quick actions:
- "Manage Schedules"
- "View All Appointments"
- "Add Doctor Leave"

Recent activity feed with timestamps

## 8.3 Doctor Schedule Management (`/admin/schedules`)

List view:
- All doctors with current schedule summary
- Working days indicator
- Time range per doctor
- Quick edit button

Weekly editor (per doctor):
- Grid: Mon-Sun
- Time pickers per day (start/end)
- Working day toggle
- Max appointments input
- Slot duration selector
- Bulk actions:
  - Copy to next week
  - Apply template
  - Reset to defaults

## 8.4 Leave Management (`/admin/doctors/[id]/time-off`)

Calendar view:
- Leave marked in red
- Existing appointments shown
- Conflicts highlighted

Add leave form:
- Start date, end date
- Type: LEAVE, SICK, TRAINING, OTHER
- Reason textarea
- Status: PENDING, APPROVED, REJECTED

Approval workflow:
- List pending requests
- Approve/Reject actions
- Automatic notifications

## 8.5 Appointment Overview (`/admin/appointments`)

Filterable table:
- Date range picker
- Facility dropdown
- Status filter
- Priority filter
- Doctor filter
- Patient search

Columns:
- Date/Time
- Patient name
- Doctor name
- Facility
- Status (badge)
- Priority (badge)
- Actions (view, cancel, reassign)

Bulk actions:
- Cancel multiple
- Reassign doctor
- Export to CSV

---

# 9. Integration Points

## 9.1 Booking to Consultation Flow

```
Patient                                    Backend                              Doctor
  |                                          |                                      |
  |-- 1. Book Appointment ------------------>|                                      |
  |   (facility, date, symptoms)             |                                      |
  |                                          |-- 2. Auto-route to doctor            |
  |                                          |   (history + specialty + workload)   |
  |                                          |                                      |
  |<-- 3. Confirmed Booking -----------------|                                      |
  |   (doctor assigned, time allocated)      |                                      |
  |                                          |-- 4. Notify Doctor ----------------->|
  |                                          |   "New appointment on [date]"        |
  |                                          |                                      |
  |-- 5. (On appointment day)                |                                      |
  |   "Start Consultation" activates         |                                      |
  |                                          |                                      |
  |-- 6. Start Consultation --------------->|                                      |
  |                                          |-- 7. Create Visit                     |
  |                                          |   (linked to appointment)            |
  |                                          |                                      |
  |<-- 8. AI Session Created ----------------|                                      |
  |                                          |                                      |
  |-- 9. Complete AI pre-assessment --------------------------------------------->|
  |   (symptoms, answers, differential)      |-- 10. Notify Doctor                  |
  |                                          |   "Patient ready for consultation"   |
  |                                          |                                      |
  |<-- 11. Live consultation -------------->|                                      |
```

## 9.2 Modified Existing Endpoints

**POST /api/v1/doctor/consultations** (existing)
- Now accepts `appointment_id` in VisitCreate
- Links created visit to appointment
- Sets appointment status to COMPLETED

**GET /api/v1/doctor** (existing)
- Enhanced to show appointment-linked visits
- Shows appointment status alongside visit status

## 9.3 New WebSocket Events

```
APPOINTMENT_CREATED       → Doctor notified
APPOINTMENT_CONFIRMED     → Patient notified
APPOINTMENT_CANCELLED     → Both parties notified
APPOINTMENT_REMINDER      → Patient (24h before)
EMERGENCY_APPOINTMENT     → All facility doctors
CONSULTATION_READY        → Doctor notified
DOCTOR_SCHEDULE_UPDATED   → Affected doctors
DOCTOR_TIME_OFF_ADDED     → Admin dashboard
```

---

# 10. Notification Events

## 10.1 Trigger Points

| Event | Recipient | Channel | Content |
|---|---|---|---|
| Appointment Created | Assigned Doctor | In-app + WebSocket | "New appointment on [date] at [time]" |
| Appointment Confirmed | Patient | In-app | "Your appointment is confirmed" |
| Appointment Cancelled | Both parties | In-app + WebSocket | "Appointment cancelled: [reason]" |
| 24h Reminder | Patient | In-app + Email | "Reminder: Appointment tomorrow" |
| Emergency Booked | All facility doctors | WebSocket (urgent) | "EMERGENCY: New urgent appointment" |
| Doctor Reassigned | Patient | In-app | "Your doctor changed to [name]" |
| Consultation Ready | Doctor | WebSocket | "Patient started pre-assessment" |
| Day-of Activation | Patient | In-app | "Your appointment is today. Start?" |

## 10.2 Priority Levels

- **CRITICAL**: Emergency appointments, cancellations < 24h
- **HIGH**: Doctor reassignment, day-of reminder
- **NORMAL**: Confirmations, 24h reminders
- **LOW**: General updates, schedule changes


---

# 11. Bug Fixes & Improvements

## 11.1 Timeline 403 Forbidden (Patient)

**Root Cause:** `get_current_patient` dependency requires `role="patient"`, but patient login may not be setting role correctly in the JWT token.

**Fix:**
1. Verify `/api/v1/auth/patient/login` returns token with `role="patient"` in payload
2. Check `get_current_user` dependency extracts role correctly
3. Ensure patient login service queries database user and includes role in token
4. Add debug logging to trace: login → token generation → token decode → role check

**Files:**
- `backend/app/auth/service.py` - `login_patient()`
- `backend/app/auth/jwt.py` - Token generation
- `backend/app/auth/dependencies.py` - `get_current_user()`, `get_current_patient()`

## 11.2 Notifications 401/429 Infinite Loop

**Root Cause:** Frontend polls notifications when not authenticated, causing infinite 401 → retry → 429 (rate limit).

**Fix (Frontend):**
1. Only start notification polling when `isAuthenticated === true`
2. Stop polling on 401 error (redirect to login, do not retry)
3. Add exponential backoff for failed requests
4. Debounce or deduplicate rapid requests

**Fix (Backend):**
1. Do not rate-limit 401 responses (they're already rejected)
2. Return proper 401 without triggering rate limit counter

**Files:**
- `frontend/providers/WebSocketProvider.tsx`
- `frontend/hooks/useNotifications.ts` or `layout.tsx`
- `frontend/lib/api.ts`
- `backend/app/middleware/rate_limit.py`

## 11.3 Consultations 404 Error

**Root Cause:** Frontend calls `/api/v1/consultations` but backend has this endpoint mounted at `/api/v1/doctor` (with empty path).

**Fix:** Update frontend API client to call correct endpoint.

```typescript
// BEFORE (incorrect)
listConsultations: (params) =>
  request<VisitResponse[]>(`/consultations?${search}`, { method: "GET" })

// AFTER (correct)
listConsultations: (params) =>
  request<VisitResponse[]>(`/doctor?${search}`, { method: "GET" })
```

**File:** `frontend/lib/api.ts`

---

# 12. Implementation Timeline

## Phase 1: Foundation & Bug Fixes (Week 1)

### Days 1-2: Authentication & Bug Fixes
- [ ] Fix timeline 403 for patients
  - Debug token role assignment
  - Verify `get_current_patient` dependency
  - Test with demo login
- [ ] Fix notifications 401/429 loop
  - Add auth check before polling
  - Stop polling on 401
  - Test no-retry behavior
- [ ] Fix consultations 404
  - Update frontend API path
  - Verify backend endpoint

### Days 3-4: Database Schema
- [ ] Create Alembic migration
  - `appointments` table
  - `doctor_schedules` table
  - `doctor_time_offs` table
  - `appointment_slot_allocations` table
- [ ] Extend `doctors` table
  - `max_daily_appointments`
  - `is_accepting_appointments`
  - `next_available_date`
- [ ] Update SQLAlchemy models with relationships
- [ ] Run migration and verify

### Day 5: Seed Data
- [ ] Update seeder to create doctor schedules
- [ ] Add sample time-off records
- [ ] Create test appointments
- [ ] Verify data integrity

## Phase 2: Backend Core (Week 2)

### Days 6-7: Services
- [ ] Implement `AppointmentService`
  - create_booking
  - cancel_appointment (with 3-day validation)
  - confirm_appointment
  - list_appointments
- [ ] Implement `AutoRoutingService`
  - History score calculation
  - Specialty matching with keyword map
  - Workload scoring
  - Emergency bypass
- [ ] Implement `ScheduleService`
  - Doctor schedules CRUD
  - Time-off management
  - Slot allocation algorithm

### Days 8-9: API Endpoints
- [ ] Patient appointment endpoints
- [ ] Doctor schedule endpoints
- [ ] Facility endpoints
- [ ] Admin endpoints
- [ ] Integration with existing visits (start_consultation_from_appointment)

### Day 10: Backend Testing
- [ ] Unit tests for auto-routing algorithm
- [ ] Unit tests for slot allocation with buffer
- [ ] Unit tests for cancellation logic
- [ ] Integration tests for full booking flow

## Phase 3: Frontend Patient Flow (Week 3)

### Days 11-12: Booking Wizard
- [ ] Facility search page
- [ ] Date selection calendar
- [ ] Symptom input form
- [ ] Review & confirm page
- [ ] Booking success screen

### Days 13-14: Patient Appointments
- [ ] My appointments list
- [ ] Appointment detail view
- [ ] Cancel appointment flow
- [ ] Day-of consultation trigger button

### Day 15: Integration
- [ ] Connect booking wizard to API
- [ ] Handle loading states
- [ ] Error handling
- [ ] Empty states

## Phase 4: Frontend Doctor & Admin (Week 4)

### Days 16-17: Doctor Schedule
- [ ] Schedule calendar view (week/day toggle)
- [ ] Availability settings
- [ ] Appointment notifications
- [ ] Day-of patient list

### Days 18-19: Admin UI
- [ ] Admin login with demo button
- [ ] Dashboard overview
- [ ] Doctor schedule editor (weekly grid)
- [ ] Leave management
- [ ] Appointment overview table

### Day 20: Polish
- [ ] Responsive design
- [ ] Loading skeletons
- [ ] Error boundaries
- [ ] Accessibility checks

## Phase 5: Testing & Deployment (Week 5)

### Days 21-22: E2E Testing
- [ ] Full booking flow end-to-end
- [ ] Auto-routing validation with different scenarios
- [ ] Cancellation with and without notice
- [ ] Day-of consultation start
- [ ] Admin schedule management

### Days 23-24: Performance
- [ ] API response optimization
- [ ] Frontend bundle size checks
- [ ] Database query optimization
- [ ] Redis caching strategy

### Day 25: Deployment
- [ ] Final testing
- [ ] Documentation update
- [ ] Deploy to staging
- [ ] User acceptance testing

---

# 13. Success Criteria

The Appointment Booking System is complete when:

- [ ] Patient can book appointment at facility with date selection
- [ ] Auto-routing assigns appropriate doctor based on history/specialty/workload
- [ ] Patient can request preferred doctor with fallback
- [ ] Emergency appointments bypass queue immediately
- [ ] 3-day cancellation notice is enforced
- [ ] Doctor can view daily schedule with appointments
- [ ] Admin can manage doctor schedules and leave
- [ ] Admin UI has demo login functionality
- [ ] Day-of consultation flow works (booking → visit → AI assessment)
- [ ] Notifications sent at all key points
- [ ] Timeline 403 error is resolved
- [ ] Notifications 401/429 loop is fixed
- [ ] Consultations 404 error is fixed
- [ ] All tests pass
- [ ] Documentation is updated

---

# 14. Future Iterations

1. **Calendar Sync:** Google Calendar / Outlook integration for doctors
2. **Recurring Appointments:** Book follow-up sequences
3. **Waitlist:** Add to waitlist when no slots available
4. **Telemedicine:** Distinguish in-person vs virtual appointments
5. **Patient Preferences:** Save preferred facilities/doctors
6. **SMS Notifications:** SMS reminders (requires provider integration)
7. **QR Check-in:** Scan QR code at facility on arrival
8. **AI Triage:** Use AI to better match symptoms to specialties

---

# End of Appointment Booking System Specification

