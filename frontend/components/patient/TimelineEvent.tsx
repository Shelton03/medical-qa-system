'use client'

import React, { useState } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { ChevronDown, ChevronUp, Stethoscope, Pill, ClipboardList, ShieldCheck } from 'lucide-react'
import { cn } from '@/lib/utils'

export interface TimelineEventItem {
  id: string
  date: string
  facility?: string | null
  doctor?: string | null
  type: 'visit' | 'diagnosis' | 'medication' | 'consent'
  title: string
  subtitle?: string
  details?: Record<string, string | null>
}

interface TimelineEventProps {
  event: TimelineEventItem
}

const typeConfig = {
  visit: { icon: Stethoscope, color: 'bg-celestialBlue/10 text-celestialBlue' },
  diagnosis: { icon: ClipboardList, color: 'bg-alertOrange/10 text-alertOrange' },
  medication: { icon: Pill, color: 'bg-healthGreen/10 text-healthGreen' },
  consent: { icon: ShieldCheck, color: 'bg-clinicalGrey/10 text-clinicalGrey' },
}

export function TimelineEvent({ event }: TimelineEventProps): React.ReactElement {
  const [isExpanded, setIsExpanded] = useState(false)
  const config = typeConfig[event.type]
  const Icon = config.icon

  const dateObj = new Date(event.date)
  const dateStr = dateObj.toLocaleDateString('en-US', {
    month: 'short',
    day: 'numeric',
    year: 'numeric',
  })
  const timeStr = dateObj.toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit' })

  return (
    <div className="relative flex gap-3">
      {/* Timeline line */}
      <div className="flex flex-col items-center">
        <div className={cn('w-8 h-8 rounded-full flex items-center justify-center', config.color)}>
          <Icon className="w-4 h-4" />
        </div>
        <div className="w-px flex-1 bg-border my-1" />
      </div>

      {/* Content */}
      <div className="flex-1 pb-4">
        <button
          onClick={() => setIsExpanded(!isExpanded)}
          className="w-full text-left bg-white border border-border rounded-card p-3 hover:shadow-elevation-1 transition-shadow"
        >
          <div className="flex items-start justify-between gap-2">
            <div className="flex-1">
              <p className="text-caption text-clinicalGrey">
                {dateStr} · {timeStr}
              </p>
              <h3 className="text-body font-medium text-mirageBlack mt-0.5">{event.title}</h3>
              {event.subtitle && <p className="text-caption text-clinicalGrey mt-0.5">{event.subtitle}</p>}
              {(event.facility || event.doctor) && (
                <p className="text-micro text-clinicalGrey mt-1">
                  {event.doctor && `Dr. ${event.doctor}`}
                  {event.doctor && event.facility && ' · '}
                  {event.facility}
                </p>
              )}
            </div>
            {event.details && Object.keys(event.details).length > 0 && (
              <div className="shrink-0 mt-1">
                {isExpanded ? (
                  <ChevronUp className="w-4 h-4 text-clinicalGrey" />
                ) : (
                  <ChevronDown className="w-4 h-4 text-clinicalGrey" />
                )}
              </div>
            )}
          </div>

          <AnimatePresence>
            {isExpanded && event.details && Object.keys(event.details).length > 0 && (
              <motion.div
                initial={{ height: 0, opacity: 0 }}
                animate={{ height: 'auto', opacity: 1 }}
                exit={{ height: 0, opacity: 0 }}
                transition={{ duration: 0.2 }}
                className="overflow-hidden"
              >
                <div className="mt-3 pt-3 border-t border-border space-y-2">
                  {Object.entries(event.details).map(([key, value]) =>
                    value ? (
                      <div key={key} className="flex justify-between items-start">
                        <span className="text-caption text-clinicalGrey capitalize">{key.replace(/_/g, ' ')}</span>
                        <span className="text-caption text-mirageBlack text-right max-w-[60%]">{value}</span>
                      </div>
                    ) : null
                  )}
                </div>
              </motion.div>
            )}
          </AnimatePresence>
        </button>
      </div>
    </div>
  )
}
