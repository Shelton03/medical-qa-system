import { describe, it, expect } from 'vitest';
import { render, screen } from '@testing-library/react';
import { StatusBadge } from '@/components/doctor/StatusBadge';

describe('StatusBadge', () => {
  it('renders with correct text', () => {
    render(<StatusBadge status="completed" />);
    expect(screen.getByTestId('status-badge')).toHaveTextContent('completed');
  });

  it('renders success variant with green color classes', () => {
    render(<StatusBadge status="approved" />);
    const badge = screen.getByTestId('status-badge');
    expect(badge).toHaveClass('bg-healthGreen/10', 'text-healthGreen');
  });

  it('renders warning variant with blue color classes', () => {
    render(<StatusBadge status="in_progress" />);
    const badge = screen.getByTestId('status-badge');
    expect(badge).toHaveClass('bg-celestialBlue/10', 'text-celestialBlue');
  });

  it('renders error variant with orange color classes', () => {
    render(<StatusBadge status="cancelled" />);
    const badge = screen.getByTestId('status-badge');
    expect(badge).toHaveClass('bg-alertOrange/10', 'text-alertOrange');
  });

  it('replaces underscores with spaces', () => {
    render(<StatusBadge status="in_progress" />);
    expect(screen.getByTestId('status-badge')).toHaveTextContent('in progress');
  });

  it('applies custom className', () => {
    render(<StatusBadge status="pending" className="custom-class" />);
    expect(screen.getByTestId('status-badge')).toHaveClass('custom-class');
  });
});
