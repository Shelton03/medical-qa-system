# Mirage Frontend

Next.js 14 application for the Mirage healthcare platform. Provides the Doctor Portal (desktop) and Patient Application (mobile-frame).

---

## Quick Start

```bash
npm install
npm run dev          # http://localhost:3000
npm run build        # Production build (standalone)
npm run test         # Run Vitest suite
```

---

## Design Token Reference

### Colors

| Token | Hex | Usage |
|---|---|---|
| `celestialBlue` | `#2563EB` | Primary actions, links, active states |
| `stellarWhite` | `#FAFAF8` | Page backgrounds |
| `mirageBlack` | `#0A3828` | Text, primary buttons, headings |
| `healthGreen` | `#18A358` | Success, confirmed, approved states |
| `alertOrange` | `#EA580C` | Warnings, errors, destructive actions |
| `clinicalGrey` | `#6B6760` | Secondary text, borders, disabled |
| `deepSpace` | `#0A0A0F` | Demo chrome, dark backgrounds |

### Typography

| Token | Size | Weight | Usage |
|---|---|---|---|
| `display` | 36px | 700 | Hero headlines |
| `page-title` | 28px | 700 | Page headings |
| `section-title` | 22px | 600 | Section headings |
| `card-title` | 18px | 600 | Card headings |
| `body` | 16px | 400 | Body text |
| `caption` | 12px | 400 | Captions, metadata |
| `micro` | 10px | 500 | Labels, overlines |

### Spacing Scale

`4px, 8px, 12px, 16px, 20px, 24px, 32px, 40px, 48px, 64px`

### Radius Scale

| Token | Value | Usage |
|---|---|---|
| `button` | 9999px | Buttons |
| `card` | 16px | Cards |
| `sheet` | 32px | Bottom sheets |
| `input` | 16px | Inputs |
| `dialog` | 24px | Dialogs |

---

## Component Library

### Doctor Components

| Component | Path | Props |
|---|---|---|
| `PatientOverviewCard` | `components/doctor/PatientOverviewCard.tsx` | `patient`, `compact?` |
| `DiagnosisCard` | `components/doctor/DiagnosisCard.tsx` | `diagnosis`, `onConfirm?`, `onIgnore?` |
| `PrescriptionCard` | `components/doctor/PrescriptionCard.tsx` | `medication` |
| `AIChatPanel` | `components/doctor/AIChatPanel.tsx` | `sessionId`, `patientId?`, `initialMessages?` |
| `DifferentialList` | `components/doctor/DifferentialList.tsx` | `diagnoses`, `onConfirm?`, `onIgnore?`, `onEdit?` |
| `SOAPEditor` | `components/doctor/SOAPEditor.tsx` | `summary`, `onChange?`, `onSave?`, `onRegenerate?`, `readOnly?` |
| `StatusBadge` | `components/doctor/StatusBadge.tsx` | `status`, `className?` |

### Shared

| Component | Path | Description |
|---|---|---|
| `PhoneFrame` | `components/phone-frame/PhoneFrame.tsx` | Simulated smartphone wrapper for patient app |

---

## Route Map

### Doctor Portal (`/doctor/*`)

| Route | Purpose |
|---|---|
| `/doctor/dashboard` | Landing page, stats, recent consultations, pending consents |
| `/doctor/patients` | Patient search with fuzzy query |
| `/doctor/patients/[id]` | Full patient record, conditions, meds, visits, consent request |
| `/doctor/consultations` | List consultations, start new, AI quick-start |
| `/doctor/consultations/[id]` | Visit detail — diagnoses, meds, notes, AI summary, finalize |
| `/doctor/consents` | Consent management list |
| `/doctor/ai-consultation` | Interactive AI workspace — 3-panel layout with chat |
| `/doctor/differential` | AI differential diagnosis review and confirmation |
| `/doctor/summary` | Clinical SOAP summary editor |
| `/doctor/notifications` | Doctor inbox — mark read, mark all read |
| `/doctor/settings` | Profile, notification prefs, theme, logout |
| `/doctor/access-history` | Audit trail table |

### Patient Application (`/patient/*`)

| Route | Purpose |
|---|---|
| `/patient/login` | Patient authentication |
| `/patient/consent` | Consent request review / approval |
| `/patient/records` | Health record timeline |
| `/patient/profile` | Patient profile |

### Demo & Shared

| Route | Purpose |
|---|---|
| `/` | Landing / marketing page |
| `/demo` | Split-screen demo with PhoneFrame + Doctor Portal |

---

## API Integration Guide

### Adding a New Endpoint

1. **Add types** in `lib/types.ts`
2. **Add API method** in `lib/api.ts` inside the appropriate namespace object
3. **Create a feature hook** or use `useQuery` / `useMutation` directly in components
4. **Use the typed API client** — never call `fetch` directly in components

Example pattern:

```tsx
import { useQuery } from '@tanstack/react-query';
import { someApi } from '@/lib/api';

const { data, isLoading } = useQuery({
  queryKey: ['resource', id],
  queryFn: () => someApi.getResource(id),
  enabled: !!id,
});
```

### Auth

Tokens are stored in `localStorage` (`mirage_access_token`, `mirage_refresh_token`).
The API client automatically attaches the `Authorization` header and refreshes expired tokens.

### WebSocket

Real-time notifications via `WebSocketProvider` at `ws://localhost:8002/ws/notifications`.
Events: `CONSENT_REQUESTED`, `CONSENT_APPROVED`, `NOTIFICATION_CREATED`, etc.

---

## Testing

```bash
npm run test           # Run all tests
npm run test -- --watch  # Watch mode
```

- **Vitest** for runner
- **@testing-library/react** for component rendering
- **jsdom** for DOM environment
- **@testing-library/jest-dom** for DOM matchers

Test files: `__tests__/**/*.test.tsx`

---

## Docker Notes

The frontend Docker build uses Next.js `output: 'standalone'`.

- `Dockerfile`: Multi-stage build — installs deps, builds, then copies standalone output
- `docker-compose.yml`: Frontend service exposes port 3000
- The bind mount `./frontend:/app` is **disabled** in compose to avoid shadowing `server.js`

For local development outside Docker, `npm run dev` is preferred.

---

## Project Structure

```
frontend/
├── app/                  # Next.js App Router pages
│   ├── doctor/           # Doctor portal pages
│   ├── patient/          # Patient app pages
│   ├── demo/             # Split-screen demo
│   └── layout.tsx        # Root layout with providers
├── components/           # React components
│   ├── doctor/           # Doctor-specific components
│   ├── patient/          # Patient-specific components
│   └── phone-frame/      # PhoneFrame component
├── lib/
│   ├── api.ts            # Typed API client
│   ├── types.ts          # TypeScript types
│   └── utils.ts          # Tailwind class utilities
├── providers/            # React context providers
│   ├── AuthProvider.tsx
│   ├── QueryProvider.tsx
│   ├── ToastProvider.tsx
│   └── WebSocketProvider.tsx
├── hooks/                # Shared hooks
│   ├── useAuth.ts
│   ├── useToast.ts
│   └── useWebSocket.ts
├── __tests__/            # Test files
├── public/               # Static assets
├── vitest.config.ts      # Vitest configuration
└── vitest.setup.ts       # Test setup (jest-dom)
```
