import React from 'react'
import { cn } from '@/lib/utils'

interface LoadingSkeletonProps {
  type: 'card' | 'list' | 'text' | 'timeline'
  count?: number
  className?: string
}

export function LoadingSkeleton({ type, count = 3, className }: LoadingSkeletonProps): React.ReactElement {
  if (type === 'card') {
    return (
      <div className={cn('space-y-3', className)}>
        {Array.from({ length: count }).map((_, i) => (
          <div key={i} className="bg-white border border-border rounded-card p-4 space-y-3 animate-pulse">
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 rounded-full bg-mirageBlack-200" />
              <div className="flex-1 space-y-1.5">
                <div className="h-3.5 bg-mirageBlack-200 rounded w-3/4" />
                <div className="h-2.5 bg-mirageBlack-200 rounded w-1/2" />
              </div>
            </div>
            <div className="h-2.5 bg-mirageBlack-200 rounded w-full" />
            <div className="h-2.5 bg-mirageBlack-200 rounded w-2/3" />
          </div>
        ))}
      </div>
    )
  }

  if (type === 'list') {
    return (
      <div className={cn('space-y-2', className)}>
        {Array.from({ length: count }).map((_, i) => (
          <div key={i} className="bg-white border border-border rounded-card p-3 flex items-center gap-3 animate-pulse">
            <div className="w-9 h-9 rounded-lg bg-mirageBlack-200 shrink-0" />
            <div className="flex-1 space-y-1.5">
              <div className="h-3 bg-mirageBlack-200 rounded w-2/3" />
              <div className="h-2 bg-mirageBlack-200 rounded w-1/2" />
            </div>
          </div>
        ))}
      </div>
    )
  }

  if (type === 'text') {
    return (
      <div className={cn('space-y-2', className)}>
        {Array.from({ length: count }).map((_, i) => (
          <div
            key={i}
            className={cn(
              'h-3 bg-mirageBlack-200 rounded animate-pulse',
              i % 3 === 0 ? 'w-full' : i % 3 === 1 ? 'w-3/4' : 'w-1/2'
            )}
          />
        ))}
      </div>
    )
  }

  // timeline
  return (
    <div className={cn('space-y-4 pl-3', className)}>
      {Array.from({ length: count }).map((_, i) => (
        <div key={i} className="relative flex gap-3 animate-pulse">
          <div className="flex flex-col items-center">
            <div className="w-3 h-3 rounded-full bg-mirageBlack-200" />
            {i < count - 1 && <div className="w-px h-full bg-mirageBlack-200 my-1" />}
          </div>
          <div className="flex-1 space-y-2 pb-4">
            <div className="h-3 bg-mirageBlack-200 rounded w-1/3" />
            <div className="h-3.5 bg-mirageBlack-200 rounded w-3/4" />
            <div className="h-2.5 bg-mirageBlack-200 rounded w-1/2" />
          </div>
        </div>
      ))}
    </div>
  )
}
