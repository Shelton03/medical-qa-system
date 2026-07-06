import { describe, it, expect } from 'vitest';
import { render, screen } from '@testing-library/react';
import { AIChatPanel } from '@/components/doctor/AIChatPanel';

describe('AIChatPanel', () => {
  it('renders chat panel header', () => {
    render(<AIChatPanel sessionId="test-session-123" />);
    expect(screen.getByText('AI Clinical Assistant')).toBeInTheDocument();
  });

  it('renders input placeholder', () => {
    render(<AIChatPanel sessionId="test-session-123" />);
    expect(screen.getByPlaceholderText('Ask the AI assistant...')).toBeInTheDocument();
  });

  it('renders send button', () => {
    render(<AIChatPanel sessionId="test-session-123" />);
    expect(screen.getByLabelText('Send message')).toBeInTheDocument();
  });

  it('displays session info', () => {
    render(<AIChatPanel sessionId="test-session-123" patientId="patient-456" />);
    expect(screen.getByText(/test-session-123/)).toBeInTheDocument();
  });

  it('renders initial messages if provided', () => {
    const messages = [
      {
        id: 'msg-1',
        session_id: 'test-session-123',
        role: 'assistant',
        content: 'Hello doctor, how can I help?',
        model_name: null,
        token_count: null,
        created_at: new Date().toISOString(),
      },
    ];
    render(<AIChatPanel sessionId="test-session-123" initialMessages={messages} />);
    expect(screen.getByText('Hello doctor, how can I help?')).toBeInTheDocument();
  });
});
