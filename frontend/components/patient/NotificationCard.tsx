'use client'

import React from 'react'
import { motion } from 'framer-motion'
import { Bell, Check, ShieldCheck, FileText, Activity, Info } from 'lucide-react'
import { cn } from '@/lib/utils'

export interface NotificationItem {
  id: string
  type: string
  title: string
  body: string | null
  is_read: boolean
  created_at: string
}

interface NotificationCardProps {
  notification: NotificationItem
  onClick?: () => void
}

const typeIconMap: Record<string, React.ElementType> = {
  consent: ShieldCheck,
  medical_record: FileText,
  reminder: Bell,
  system: Info,
  ai: Activity,
}

const typeColorMap: Record<string, string> = {
  consent: 'bg-celestialBlue/10 text-celestialBlue',
  medical_record: 'bg-healthGreen/10 text-healthGreen',
  reminder: 'bg-alertOrange/10 text-alertOrange',
  system: 'bg-clinicalGrey/10 text-clinicalGrey',
  ai: 'bg-mirageBlack/10 text-mirageBlack',
}

export function NotificationCard({ notification, onClick }: NotificationCardProps): React.ReactElement {
  const Icon = typeIconMap[notification.type] || Bell
  const colorClass = typeColorMap[notification.type] || 'bg-clinicalGrey/10 text-clinicalGrey'

  const timeAgo = (dateStr: string): string => {
    const date = new Date(dateStr)
    const now = new Date()
    const seconds = Math.floor((now.getTime() - date.getTime()) / 1000)
    if (seconds < 60) return 'Just now'
    const minutes = Math.floor(seconds / 60)
    if (minutes < 60) return `${minutes}m ago`
    const hours = Math.floor(minutes / 60)
    if (hours < 24) return `${hours}h ago`
    const days = Math.floor(hours / 24)
    return `${days}d ago`
  }

  return (
    <motion.button
      whileTap={{ scale: 0.98 }}
      onClick={onClick}
      className={cn(
        'relative w-full flex items-start gap-3 p-3 rounded-card text-left transition-colors',
        notification.is_read
          ? 'bg-white border border-border'
          : 'bg-celestialBlue-50 border border-celestialBlue/20'
      )}
    >
      {!notification.is_read && (
        <span className="absolute top-3 right-3 w-2 h-2 bg-celestialBlue rounded-full">
          <span className="absolute inset-0 w-2 h-2 bg-celestialBlue rounded-full animate-ping opacity-60" />
        </span>
      )}
      <div className={cn('w-9 h-9 rounded-lg flex items-center justify-center shrink-0 mt-0.5', colorClass)}>
        <Icon className="w-4 h-4" />
      </div>
      <div className="flex-1 min-w-0">
        <div className="flex items-center justify-between gap-2">
          <p className={cn('text-body truncate', notification.is_read ? 'text-mirageBlack' : 'font-medium text-mirageBlack')}>
            {notification.title}
          </p>
        </div>
        {notification.body && (
          <p className="text-caption text-clinicalGrey line-clamp-2 mt-0.5">{notification.body}</p>
        )}
        <p className="text-micro text-clinicalGrey mt-1">{timeAgo(notification.created_at)}</p>
      </div>
    </motion.button>
  )
}
