"use client";

import React from "react";
import { motion } from "framer-motion";
import Link from "next/link";
import { useQuery } from "@tanstack/react-query";
import {
  CalendarDays,
  ChevronLeft,
  ChevronRight,
  Clock,
  Stethoscope,
  ArrowRight,
} from "lucide-react";
import { useMySchedule, useMyAppointmentsToday } from "@/hooks/useSchedule";
import { LoadingSkeleton } from "@/components/ui/LoadingSkeleton";
import { EmptyState } from "@/components/ui/EmptyState";
import type { ScheduleAppointment } from "@/lib/types";
import { cn } from "@/lib/utils";

const spring = { type: "spring", stiffness: 380, damping: 32 };

const TIME_SLOTS = Array.from({ length: 19 }, (_, i) => {
  const hour = 8 + Math.floor(i / 2);
  const minute = (i % 2) * 30;
  return `${String(hour).padStart(2, "0")}:${String(minute).padStart(2, "0")}`;
});

const DAYS = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"];

function AppointmentBlock({
  appt,
  onClick,
}: {
  appt: ScheduleAppointment;
  onClick?: () => void;
}) {
  const statusColors: Record<string, string> = {
    PENDING: "bg-alertOrange/20 border-alertOrange/40 text-alertOrange",
    CONFIRMED: "bg-celestialBlue/20 border-celestialBlue/40 text-celestialBlue",
    COMPLETED: "bg-healthGreen/20 border-healthGreen/40 text-healthGreen",
    CANCELLED: "bg-clinicalGrey/20 border-clinicalGrey/40 text-clinicalGrey",
  };

  const startHour = parseInt(appt.start_time.split(":")[0], 10);
  const startMin = parseInt(appt.start_time.split(":")[1], 10);
  const endHour = parseInt(appt.end_time.split(":")[0], 10);
  const endMin = parseInt(appt.end_time.split(":")[1], 10);

  const startSlot = (startHour - 8) * 2 + (startMin >= 30 ? 1 : 0);
  const endSlot = (endHour - 8) * 2 + (endMin >= 30 ? 1 : 0);
  const durationSlots = Math.max(1, endSlot - startSlot);

  return (
    <motion.div
      initial={{ opacity: 0, scale: 0.9 }}
      animate={{ opacity: 1, scale: 1 }}
      transition={{ duration: 0.2 }}
      onClick={onClick}
      className={cn(
        "absolute left-1 right-1 rounded-md border px-2 py-1 cursor-pointer hover:brightness-95 transition-all overflow-hidden",
        statusColors[appt.status] ?? statusColors.PENDING
      )}
      style={{
        top: `${startSlot * 48 + 4}px`,
        height: `${durationSlots * 48 - 8}px`,
      }}
    >
      <p className="text-xs font-semibold truncate">
        {appt.patient_name || "Patient"}
      </p>
      <p className="text-[10px] opacity-80">
        {appt.start_time} – {appt.end_time}
      </p>
    </motion.div>
  );
}

export default function DoctorSchedulePage(): React.ReactElement {
  const { data: scheduleData, isLoading: scheduleLoading } = useMySchedule();
  const { data: todayAppointments, isLoading: apptsLoading } = useMyAppointmentsToday();

  const isLoading = scheduleLoading || apptsLoading;

  // Get today's day index (0=Sun, 1=Mon... convert to 0=Mon for our display)
  const today = new Date();
  const todayDayIndex = (today.getDay() + 6) % 7; // Convert to Mon=0

  return (
    <div className="space-y-6">
      <motion.div initial={{ opacity: 0, y: 12 }} animate={{ opacity: 1, y: 0 }} transition={spring}>
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-2xl font-bold text-mirageBlack">Schedule</h1>
            <p className="text-clinicalGrey">Your weekly appointment calendar</p>
          </div>
          <Link
            href="/doctor/schedule/availability"
            className="inline-flex items-center gap-2 px-4 py-2 bg-white border border-border text-mirageBlack rounded-lg text-sm font-medium hover:bg-secondary transition-colors"
          >
            <Clock className="w-4 h-4" />
            Availability
          </Link>
        </div>
      </motion.div>

      {isLoading ? (
        <LoadingSkeleton type="card" count={2} />
      ) : (
        <>
          {/* Week View */}
          <motion.div
            initial={{ opacity: 0, y: 12 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ ...spring, delay: 0.1 }}
            className="bg-white rounded-xl border border-border overflow-hidden"
          >
            {/* Day headers */}
            <div className="grid grid-cols-8 border-b border-border">
              <div className="px-3 py-3 text-xs font-medium text-clinicalGrey border-r border-border">
                Time
              </div>
              {DAYS.map((day, idx) => (
                <div
                  key={day}
                  className={cn(
                    "px-2 py-3 text-center text-xs font-medium border-r border-border last:border-r-0",
                    idx === todayDayIndex
                      ? "bg-celestialBlue/5 text-celestialBlue"
                      : "text-clinicalGrey"
                  )}
                >
                  <span className="block">{day}</span>
                  <span className="block text-[10px] opacity-70">
                    {idx === todayDayIndex ? "Today" : ""}
                  </span>
                </div>
              ))}
            </div>

            {/* Time grid */}
            <div className="relative" style={{ height: `${TIME_SLOTS.length * 48}px` }}>
              {/* Time labels */}
              <div className="absolute left-0 top-0 w-16 h-full border-r border-border">
                {TIME_SLOTS.map((time, idx) => (
                  <div
                    key={time}
                    className="absolute left-0 right-0 text-[10px] text-clinicalGrey text-right pr-2"
                    style={{ top: `${idx * 48}px`, transform: "translateY(-50%)" }}
                  >
                    {time}
                  </div>
                ))}
              </div>

              {/* Grid lines */}
              <div className="absolute left-16 right-0 h-full">
                {TIME_SLOTS.map((_, idx) => (
                  <div
                    key={idx}
                    className="absolute left-0 right-0 border-b border-border/50"
                    style={{ top: `${idx * 48}px` }}
                  />
                ))}
              </div>

              {/* Day columns */}
              <div className="absolute left-16 right-0 top-0 h-full grid grid-cols-7">
                {DAYS.map((_, dayIdx) => (
                  <div
                    key={dayIdx}
                    className={cn(
                      "relative border-r border-border/50 last:border-r-0",
                      dayIdx === todayDayIndex ? "bg-celestialBlue/[0.02]" : ""
                    )}
                  >
                    {/* Render today's appointments */}
                    {dayIdx === todayDayIndex &&
                      todayAppointments?.map((appt) => (
                        <AppointmentBlock
                          key={appt.id}
                          appt={appt}
                          onClick={() => {
                            if (appt.visit_id) {
                              window.location.href = `/doctor/consultations/${appt.visit_id}`;
                            }
                          }}
                        />
                      ))}
                  </div>
                ))}
              </div>
            </div>
          </motion.div>

          {/* Today's Appointments List */}
          <motion.div
            initial={{ opacity: 0, y: 12 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ ...spring, delay: 0.2 }}
            className="bg-white rounded-xl border border-border p-5"
          >
            <h2 className="font-semibold text-mirageBlack mb-4 flex items-center gap-2">
              <CalendarDays className="w-4 h-4" />
              Today&apos;s Appointments
            </h2>
            {todayAppointments && todayAppointments.length > 0 ? (
              <div className="space-y-2">
                {todayAppointments.map((appt) => (
                  <div
                    key={appt.id}
                    className="flex items-center justify-between p-3 bg-stellarWhite rounded-lg border border-border"
                  >
                    <div className="flex items-center gap-3">
                      <div className="w-10 h-10 rounded-lg bg-celestialBlue/10 flex items-center justify-center shrink-0">
                        <Stethoscope className="w-5 h-5 text-celestialBlue" />
                      </div>
                      <div>
                        <p className="text-sm font-medium text-mirageBlack">
                          {appt.patient_name || "Patient"}
                        </p>
                        <p className="text-xs text-clinicalGrey">
                          {appt.start_time} – {appt.end_time} · {appt.duration_minutes} min
                        </p>
                      </div>
                    </div>
                    <div className="flex items-center gap-2">
                      <span
                        className={cn(
                          "px-2 py-0.5 rounded-full border text-micro font-medium",
                           {
                             PENDING: "bg-alertOrange/10 text-alertOrange border-alertOrange/20",
                             CONFIRMED: "bg-celestialBlue/10 text-celestialBlue border-celestialBlue/20",
                             COMPLETED: "bg-healthGreen/10 text-healthGreen border-healthGreen/20",
                             CANCELLED: "bg-clinicalGrey/10 text-clinicalGrey border-clinicalGrey/20",
                             NO_SHOW: "bg-clinicalGrey/10 text-clinicalGrey border-clinicalGrey/20",
                           }[appt.status]
                        )}
                      >
                        {appt.status}
                      </span>
                      {appt.visit_id && (
                        <Link
                          href={`/doctor/consultations/${appt.visit_id}`}
                          className="p-2 rounded-lg hover:bg-secondary transition-colors"
                        >
                          <ArrowRight className="w-4 h-4 text-clinicalGrey" />
                        </Link>
                      )}
                    </div>
                  </div>
                ))}
              </div>
            ) : (
              <EmptyState
                icon={<CalendarDays className="w-8 h-8 text-clinicalGrey" />}
                title="No appointments today"
                description="You have no scheduled appointments for today."
              />
            )}
          </motion.div>
        </>
      )}
    </div>
  );
}
