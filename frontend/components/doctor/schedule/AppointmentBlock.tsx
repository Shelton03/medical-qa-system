"use client";

import React from "react";
import { motion } from "framer-motion";
import { useRouter } from "next/navigation";
import { Clock, User } from "lucide-react";
import { cn } from "@/lib/utils";
import type { ScheduleAppointment } from "@/lib/types";
import { springTransition } from "@/lib/animations";

const statusColorMap: Record<string, { bg: string; border: string; text: string; dot: string }> = {
  PENDING: {
    bg: "bg-alertOrange/10",
    border: "border-alertOrange/30",
    text: "text-alertOrange",
    dot: "bg-alertOrange",
  },
  CONFIRMED: {
    bg: "bg-celestialBlue/10",
    border: "border-celestialBlue/30",
    text: "text-celestialBlue",
    dot: "bg-celestialBlue",
  },
  COMPLETED: {
    bg: "bg-healthGreen/10",
    border: "border-healthGreen/30",
    text: "text-healthGreen",
    dot: "bg-healthGreen",
  },
  CANCELLED: {
    bg: "bg-clinicalGrey/10",
    border: "border-clinicalGrey/30",
    text: "text-clinicalGrey",
    dot: "bg-clinicalGrey",
  },
};

interface AppointmentBlockProps {
  appointment: ScheduleAppointment;
  top: number;
  height: number;
  onClick?: (appointment: ScheduleAppointment) => void;
}

export function AppointmentBlock({ appointment, top, height, onClick }: AppointmentBlockProps): React.ReactElement {
  const router = useRouter();
  const start = new Date(appointment.start_time);
  const end = new Date(appointment.end_time);
  const colors = statusColorMap[appointment.status] || statusColorMap.CONFIRMED;

  const handleClick = () => {
    if (onClick) {
      onClick(appointment);
    } else if (appointment.visit_id) {
      router.push(`/doctor/consultations/${appointment.visit_id}`);
    }
  };

  const timeLabel = `${start.toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" })} – ${end.toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" })}`;
  const durationMinutes = Math.round((end.getTime() - start.getTime()) / 60000);

  return (
    <motion.button
      type="button"
      initial={{ opacity: 0, scale: 0.96 }}
      animate={{ opacity: 1, scale: 1 }}
      transition={springTransition}
      onClick={handleClick}
      className={cn(
        "absolute left-1 right-1 rounded-lg border text-left overflow-hidden cursor-pointer",
        "hover:brightness-95 active:scale-[0.99] transition-transform",
        colors.bg,
        colors.border
      )}
      style={{ top, height: Math.max(height, 28) }}
      aria-label={`Appointment with ${appointment.patient_name || "Patient"} at ${timeLabel}, status ${appointment.status}`}
    >
      <div className="flex items-center gap-1.5 px-2 py-1">
        <span className={cn("w-1.5 h-1.5 rounded-full shrink-0", colors.dot)} />
        <span className={cn("text-[10px] font-semibold uppercase tracking-wide truncate", colors.text)}>
          {appointment.status}
        </span>
      </div>
      <div className="px-2 pb-1 space-y-0.5">
        <div className="flex items-center gap-1 text-mirageBlack">
          <User className="w-3 h-3 shrink-0 text-clinicalGrey" />
          <span className="text-xs font-medium truncate">{appointment.patient_name || "Patient"}</span>
        </div>
        <div className="flex items-center gap-1 text-clinicalGrey">
          <Clock className="w-3 h-3 shrink-0" />
          <span className="text-[10px] truncate">{timeLabel}</span>
        </div>
        <div className="text-[10px] text-clinicalGrey">{durationMinutes} min</div>
      </div>
    </motion.button>
  );
}
