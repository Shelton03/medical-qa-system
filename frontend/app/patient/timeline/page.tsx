"use client";

import React, { useMemo } from "react";
import { motion } from "framer-motion";
import { useQuery } from "@tanstack/react-query";
import {
  Stethoscope,
  Pill,
  ClipboardList,
  ChevronDown,
  ChevronUp,
  Sparkles,
  AlertTriangle,
  HeartPulse,
  Activity,
} from "lucide-react";
import { patientsApi } from "@/lib/api";
import type { TimelineEvent } from "@/lib/types";
import { LoadingSkeleton } from "@/components/ui/LoadingSkeleton";
import { EmptyState } from "@/components/ui/EmptyState";
import { cn } from "@/lib/utils";

interface TimelineEntry {
  id: string;
  date: string;
  type: string;
  title: string;
  subtitle?: string | null;
  status?: string | null;
  details?: Record<string, string | null>;
}

function useTimelineData() {
  return useQuery({
    queryKey: ["patient-timeline"],
    queryFn: () => patientsApi.getMyTimeline(),
  });
}

function formatDate(dateStr: string): string {
  const d = new Date(dateStr);
  return d.toLocaleDateString("en-US", {
    month: "short",
    day: "numeric",
    year: "numeric",
  });
}

function formatTime(dateStr: string): string {
  const d = new Date(dateStr);
  return d.toLocaleTimeString("en-US", { hour: "2-digit", minute: "2-digit" });
}

const iconMap: Record<string, React.ElementType> = {
  VISIT: Stethoscope,
  DIAGNOSIS: ClipboardList,
  PRESCRIPTION: Pill,
  ALLERGY_UPDATE: AlertTriangle,
  CONDITION: HeartPulse,
  AI_SESSION: Sparkles,
};

const colorMap: Record<string, string> = {
  VISIT: "bg-celestialBlue/10 text-celestialBlue border-celestialBlue/20",
  DIAGNOSIS: "bg-alertOrange/10 text-alertOrange border-alertOrange/20",
  PRESCRIPTION: "bg-healthGreen/10 text-healthGreen border-healthGreen/20",
  ALLERGY_UPDATE: "bg-errorRed/10 text-errorRed border-errorRed/20",
  CONDITION: "bg-mirageBlack/10 text-mirageBlack border-mirageBlack/20",
  AI_SESSION: "bg-violet-500/10 text-violet-600 border-violet-500/20",
};

const statusBadge: Record<string, { label: string; classes: string }> = {
  suspected: { label: "Suspected", classes: "bg-alertOrange/10 text-alertOrange border-alertOrange/20" },
  confirmed: { label: "Confirmed", classes: "bg-healthGreen/10 text-healthGreen border-healthGreen/20" },
  active: { label: "Active", classes: "bg-healthGreen/10 text-healthGreen border-healthGreen/20" },
  completed: { label: "Completed", classes: "bg-clinicalGrey/10 text-clinicalGrey border-clinicalGrey/20" },
};

function mapEvent(e: TimelineEvent): TimelineEntry {
  const iconKey = e.event_type in iconMap ? e.event_type : "VISIT";

  // Build details object from whatever extra fields the event carries
  const details: Record<string, string | null> = {};
  if (e.description) details.description = e.description;
  if (e.facility_name) details.facility = e.facility_name;
  if (e.doctor_name) details.doctor = e.doctor_name;
  if (e.status) details.status = e.status;

  return {
    id: e.event_id,
    date: e.date,
    type: iconKey,
    title: e.title || "Unknown Event",
    subtitle: e.description || null,
    status: e.status || null,
    details,
  };
}

function TimelineEventCard({ event }: { event: TimelineEntry }): React.ReactElement {
  const [expanded, setExpanded] = React.useState(false);
  const Icon = iconMap[event.type] || Stethoscope;
  const colorClass = colorMap[event.type] || "bg-celestialBlue/10 text-celestialBlue border-celestialBlue/20";
  const statusConfig = event.status ? statusBadge[event.status.toLowerCase()] : null;

  return (
    <div className="relative flex gap-3">
      <div className="flex flex-col items-center">
        <div className={cn("w-9 h-9 rounded-full flex items-center justify-center border", colorClass)}>
          <Icon className="w-4 h-4" />
        </div>
        <div className="w-px flex-1 bg-border my-1" />
      </div>
      <div className="flex-1 pb-4">
        <button
          onClick={() => setExpanded(!expanded)}
          className="w-full text-left bg-white border border-border rounded-card p-3 hover:shadow-elevation-1 transition-shadow"
        >
          <div className="flex items-start justify-between gap-2">
            <div className="flex-1 min-w-0">
              <div className="flex items-center gap-2 flex-wrap">
                <p className="text-caption text-clinicalGrey">
                  {formatDate(event.date)} · {formatTime(event.date)}
                </p>
                {statusConfig && (
                  <span className={cn("px-2 py-0.5 rounded-full text-[10px] font-medium border", statusConfig.classes)}>
                    {statusConfig.label}
                  </span>
                )}
              </div>
              <h3 className="text-body font-medium text-mirageBlack mt-0.5">{event.title}</h3>
              {event.subtitle && (
                <p className="text-caption text-clinicalGrey mt-0.5 line-clamp-2">{event.subtitle}</p>
              )}
              {(event.details?.doctor || event.details?.facility) && (
                <p className="text-micro text-clinicalGrey mt-1">
                  {event.details?.doctor && <span className="text-mirageBlack">{event.details.doctor}</span>}
                  {event.details?.doctor && event.details?.facility && <span className="mx-1">·</span>}
                  {event.details?.facility && <span>{event.details.facility}</span>}
                </p>
              )}
            </div>
            {event.details && Object.keys(event.details).length > 0 && (
              <div className="shrink-0 mt-1">
                {expanded ? (
                  <ChevronUp className="w-4 h-4 text-clinicalGrey" />
                ) : (
                  <ChevronDown className="w-4 h-4 text-clinicalGrey" />
                )}
              </div>
            )}
          </div>
          {expanded && event.details && Object.keys(event.details).length > 0 && (
            <motion.div
              initial={{ height: 0, opacity: 0 }}
              animate={{ height: "auto", opacity: 1 }}
              className="overflow-hidden"
            >
              <div className="mt-3 pt-3 border-t border-border space-y-2">
                {Object.entries(event.details).map(([key, value]) =>
                  value && key !== "doctor" && key !== "facility" && key !== "status" ? (
                    <div key={key} className="flex justify-between items-start">
                      <span className="text-caption text-clinicalGrey capitalize">
                        {key.replace(/_/g, " ")}
                      </span>
                      <span className="text-caption text-mirageBlack text-right max-w-[60%]">
                        {value}
                      </span>
                    </div>
                  ) : null
                )}
              </div>
            </motion.div>
          )}
        </button>
      </div>
    </div>
  );
}

export default function PatientTimelinePage(): React.ReactElement {
  const { data: events, isLoading, error } = useTimelineData();

  const entries: TimelineEntry[] = useMemo(() => {
    if (!events) return [];
    return events.map(mapEvent).sort(
      (a, b) => new Date(b.date).getTime() - new Date(a.date).getTime()
    );
  }, [events]);

  return (
    <div className="p-4 space-y-4 pb-20">
      <motion.div
        initial={{ opacity: 0, y: 8 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.3 }}
      >
        <h1 className="text-page-title font-heading text-mirageBlack">Health Timeline</h1>
        <p className="text-caption text-clinicalGrey">Your chronological health history</p>
      </motion.div>

      {isLoading && <LoadingSkeleton type="timeline" count={4} />}

      {!isLoading && error && (
        <EmptyState
          icon={<Stethoscope className="w-8 h-8 text-clinicalGrey" />}
          title="Could not load timeline"
          description="Something went wrong while fetching your timeline. Please try again later."
        />
      )}

      {!isLoading && !error && entries.length === 0 && (
        <EmptyState
          icon={<ClipboardList className="w-8 h-8 text-clinicalGrey" />}
          title="No timeline events"
          description="Your health timeline will appear here after your first visit or activity."
        />
      )}

      {!isLoading && !error && entries.length > 0 && (
        <div className="pl-1">
          {entries.map((event, index) => (
            <motion.div
              key={event.id}
              initial={{ opacity: 0, y: 8 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: index * 0.05, duration: 0.3 }}
            >
              <TimelineEventCard event={event} />
            </motion.div>
          ))}
        </div>
      )}
    </div>
  );
}
