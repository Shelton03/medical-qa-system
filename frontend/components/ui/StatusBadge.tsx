import React from 'react'
import { cn } from '@/lib/utils'

type StatusBadgeVariant = 'pending' | 'approved' | 'denied' | 'expired' | 'active' | 'completed'

interface StatusBadgeProps {
  variant: StatusBadgeVariant
  children: React.ReactNode
  className?: string
}

const variantStyles: Record<StatusBadgeVariant, string> = {
  pending: 'bg-alertOrange/10 text-alertOrange border-alertOrange/20',
  approved: 'bg-healthGreen/10 text-healthGreen border-healthGreen/20',
  denied: 'bg-errorRed/10 text-errorRed border-errorRed/20',
  expired: 'bg-clinicalGrey/10 text-clinicalGrey border-clinicalGrey/20',
  active: 'bg-celestialBlue/10 text-celestialBlue border-celestialBlue/20',
  completed: 'bg-healthGreen/10 text-healthGreen border-healthGreen/20',
}

export function StatusBadge({ variant, children, className }: StatusBadgeProps): React.ReactElement {
  return (
    <span
      className={cn(
        'inline-flex items-center px-2.5 py-0.5 rounded-full text-micro font-medium border',
        variantStyles[variant],
        className
      )}
    >
      {children}
    </span>
  )
}
