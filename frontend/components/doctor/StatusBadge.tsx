import React from 'react';
import { cn } from '@/lib/utils';

interface StatusBadgeProps {
  status: string;
  className?: string;
}

export function StatusBadge({ status, className }: StatusBadgeProps): React.ReactElement {
  const normalized = status.toLowerCase().trim();

  let colorClass = 'bg-clinicalGrey/10 text-clinicalGrey';
  if (normalized === 'completed' || normalized === 'approved' || normalized === 'success') {
    colorClass = 'bg-healthGreen/10 text-healthGreen';
  } else if (normalized === 'in_progress' || normalized === 'active' || normalized === 'pending') {
    colorClass = 'bg-celestialBlue/10 text-celestialBlue';
  } else if (normalized === 'cancelled' || normalized === 'declined' || normalized === 'error') {
    colorClass = 'bg-alertOrange/10 text-alertOrange';
  }

  return (
    <span
      className={cn(
        'inline-flex items-center px-2.5 py-1 rounded-full text-xs font-medium capitalize',
        colorClass,
        className
      )}
      data-testid="status-badge"
    >
      {status.replace(/_/g, ' ')}
    </span>
  );
}
