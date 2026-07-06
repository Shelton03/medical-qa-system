import { describe, it, expect } from 'vitest';
import { render, screen } from '@testing-library/react';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import DoctorDashboardPage from '@/app/doctor/dashboard/page';

function createTestQueryClient() {
  return new QueryClient({
    defaultOptions: {
      queries: { retry: false },
      mutations: { retry: false },
    },
  });
}

describe('Doctor Dashboard', () => {
  it('renders dashboard heading', () => {
    const queryClient = createTestQueryClient();
    render(
      <QueryClientProvider client={queryClient}>
        <DoctorDashboardPage />
      </QueryClientProvider>
    );
    expect(screen.getByRole('heading', { name: /Dashboard/i })).toBeInTheDocument();
  });

  it('renders stat cards labels', () => {
    const queryClient = createTestQueryClient();
    render(
      <QueryClientProvider client={queryClient}>
        <DoctorDashboardPage />
      </QueryClientProvider>
    );
    expect(screen.getByText("Today's Consultations")).toBeInTheDocument();
    expect(screen.getByText('Pending Consents')).toBeInTheDocument();
    expect(screen.getByText('Recent Patients')).toBeInTheDocument();
    expect(screen.getByText('Notifications')).toBeInTheDocument();
  });

  it('renders quick action buttons', () => {
    const queryClient = createTestQueryClient();
    render(
      <QueryClientProvider client={queryClient}>
        <DoctorDashboardPage />
      </QueryClientProvider>
    );
    expect(screen.getByText('Start Consultation')).toBeInTheDocument();
    expect(screen.getByText('Search Patient')).toBeInTheDocument();
  });
});
