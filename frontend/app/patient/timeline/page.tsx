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
} from "lucide-react";
import { patientsApi } from "@/lib/api";
import type { VisitResponse, DiagnosisResponse, MedicationResponse } from "@/lib/types";
import { LoadingSkeleton } from "@/components/ui/LoadingSkeleton";
import { EmptyState } from "@/components/ui/EmptyState";
import { cn } from "@/lib/utils";

interface TimelineEntry {
  id: string;
  date: string;
  type: "visit" | "diagnosis" | "medication";
  title: string;
  subtitle?: string;
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

const typeConfig = {
  visit: { icon: Stethoscope, color: "bg-celestialBlue/10 text-celestialBlue", label: "Visit" },
  diagnosis: { icon: ClipboardList, color: "bg-alertOrange/10 text-alertOrange", label: "Diagnosis" },
  medication: { icon: Pill, color: "bg-healthGreen/10 text-healthGreen", label: "Medication" },
};

function TimelineEventCard({ event }: { event: TimelineEntry }): React.ReactElement {
  const [expanded, setExpanded] = React.useState(false);
  const config = typeConfig[event.type];
  const Icon = config.icon;

  return (
    <div className="relative flex gap-3">
      <div className="flex flex-col items-center">
        <div className={cn("w-8 h-8 rounded-full flex items-center justify-center", config.color)}>
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
            <div className="flex-1">
              <p className="text-caption text-clinicalGrey">
                {formatDate(event.date)} · {formatTime(event.date)}
              </p>
              <h3 className="text-body font-medium text-mirageBlack mt-0.5">{event.title}</h3>
              {event.subtitle && (
                <p className="text-caption text-clinicalGrey mt-0.5">{event.subtitle}</p>
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
                  value ? (
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
  const { data: visits, isLoading, error } = useTimelineData();

  const entries: TimelineEntry[] = useMemo(() => {
    if (!visits) return [];
    const result: TimelineEntry[] = [];
    for (const visit of visits) {
      result.push({
        id: `visit-${visit.id}`,
        date: visit.visit_date,
        type: "visit",
        title: visit.chief_complaint || visit.reason || "Medical Visit",
        subtitle: visit.status,
        details: {
          summary: visit.summary,
          ai_summary: visit.ai_summary,
          follow_up: visit.follow_up_required ? "Required" : "Not required",
        },
      });
    }
    // Sort newest first
    return result.sort(
      (a, b) => new Date(b.date).getTime() - new Date(a.date).getTime()
    );
  }, [visits]);

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
          description="Your health timeline will appear here after your first visit."
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
