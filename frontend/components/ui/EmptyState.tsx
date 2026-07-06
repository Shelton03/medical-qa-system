import React from 'react'
import { cn } from '@/lib/utils'

interface EmptyStateProps {
  icon?: React.ReactNode
  title: string
  description?: string
  action?: React.ReactNode
  className?: string
}

export function EmptyState({ icon, title, description, action, className }: EmptyStateProps): React.ReactElement {
  return (
    <div className={cn('flex flex-col items-center justify-center text-center p-6', className)}>
      {icon && (
        <div className="w-16 h-16 rounded-full bg-clinicalGrey/10 flex items-center justify-center mb-4">
          {icon}
        </div>
      )}
      <h3 className="text-card-title font-medium text-mirageBlack mb-1">{title}</h3>
      {description && <p className="text-caption text-clinicalGrey max-w-[240px] mb-4">{description}</p>}
      {action && <div className="mt-2">{action}</div>}
    </div>
  )
}
