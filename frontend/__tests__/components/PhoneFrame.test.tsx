import { describe, it, expect } from 'vitest';
import { render, screen } from '@testing-library/react';
import { PhoneFrame } from '@/components/phone-frame/PhoneFrame';

describe('PhoneFrame', () => {
  it('renders children', () => {
    render(
      <PhoneFrame>
        <div data-testid="child">Hello Mirage</div>
      </PhoneFrame>
    );
    expect(screen.getByTestId('child')).toHaveTextContent('Hello Mirage');
  });

  it('has aria-label for accessibility', () => {
    render(
      <PhoneFrame>
        <div>Content</div>
      </PhoneFrame>
    );
    expect(screen.getByLabelText(/Simulated mobile device/i)).toBeInTheDocument();
  });

  it('renders status bar elements', () => {
    render(
      <PhoneFrame>
        <div>Content</div>
      </PhoneFrame>
    );
    expect(screen.getByText('9:41')).toBeInTheDocument();
    expect(screen.getByText('5G')).toBeInTheDocument();
  });
});
