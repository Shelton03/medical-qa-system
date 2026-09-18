"use client";

import React, { useState, useMemo } from "react";
import Link from "next/link";
import { motion } from "framer-motion";
import {
  CalendarPlus,
  Stethoscope,
  MapPin,
  Clock,
  ChevronRight,
} from "lucide-react";
import { useAppointments } from "@/hooks/useAppointments";
import { LoadingSkeleton } from "@/components/ui/LoadingSkeleton";
import { EmptyState } from "@/components/ui/EmptyState";
import type { Appointment, AppointmentResponse, AppointmentStatus } from "@/lib/types";
import { cn } from "@/lib/utils";

const statusBadge: Record<AppointmentStatus, { label: string; classes: string }> = {
  PENDING: {
    label: "Pending",
    classes: "bg-alertOrange/10 text-alertOrange border-alertOrange/20",
  },
  CONFIRMED: {
    label: "Confirmed",
    classes: "bg-celestialBlue/10 text-celestialBlue border-celestialBlue/20",
  },
  COMPLETED: {
    label: "Completed",
    classes: "bg-healthGreen/10 text-healthGreen border-healthGreen/20",
  },
  CANCELLED: {
    label: "Cancelled",
    classes: "bg-clinicalGrey/10 text-clinicalGrey border-clinicalGrey/20",
  },
  NO_SHOW: {
    label: "No Show",
    classes: "bg-clinicalGrey/10 text-clinicalGrey border-clinicalGrey/20",
  },
};

function formatDate(iso: string): string {
  const d = new Date(iso + "T00:00:00");
  return d.toLocaleDateString("en-US", {
    month: "short",
    day: "numeric",
    year: "numeric",
  });
}

function isUpcoming(appointmentDate: string, status: AppointmentStatus): boolean {
  if (status === "CANCELLED" || status === "COMPLETED") return false;
  const d = new Date(appointmentDate + "T00:00:00");
  d.setHours(0, 0, 0, 0);
  const today = new Date();
  today.setHours(0, 0, 0, 0);
  return d.getTime() >= today.getTime();
}

function AppointmentCard({ appointment, index }: { appointment: Appointment; index: number }) {
  const status = statusBadge[appointment.status];
  return (
    <motion.div
      initial={{ opacity: 0, y: 8 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay: index * 0.05, duration: 0.3 }}
    >
      <Link href={`/patient/appointments/${appointment.id}`}>
        <div className="bg-white border border-border rounded-card p-3.5 flex items-center gap-3 hover:shadow-elevation-1 transition-shadow active:scale-[0.99]">
          <div className="w-10 h-10 rounded-lg bg-celestialBlue/10 flex items-center justify-center shrink-0">
            <Stethoscope className="w-5 h-5 text-celestialBlue" />
          </div>
          <div className="flex-1 min-w-0">
            <div className="flex items-center justify-between gap-2">
              <p className="text-body font-medium text-mirageBlack truncate">
                {appointment.facility_name || "Facility"}
              </p>
              <span
                className={cn(
                  "shrink-0 px-2 py-0.5 rounded-full border text-micro font-medium",
                  status.classes
                )}
              >
                {status.label}
              </span>
            </div>
            <div className="flex items-center gap-3 mt-1">
              <span className="text-caption text-clinicalGrey flex items-center gap-1">
                <Clock className="w-3 h-3" />
                {formatDate(appointment.appointment_date)}
              </span>
              {appointment.doctor_name && (
                <span className="text-caption text-clinicalGrey truncate">
                  Dr. {appointment.doctor_name}
                </span>
              )}
            </div>
          </div>
          <ChevronRight className="w-4 h-4 text-clinicalGrey shrink-0" />
        </div>
      </Link>
    </motion.div>
  );
}

export default function AppointmentsListPage(): React.ReactElement {
  const [tab, setTab] = useState<"upcoming" | "past">("upcoming");
  const { data, isLoading, error } = useAppointments();

  const appointments: AppointmentResponse[] = useMemo(() => data?.items ?? [], [data]);

  const filtered = useMemo(() => {
    if (tab === "upcoming") {
      return appointments.filter((a: AppointmentResponse) => isUpcoming(a.appointment_date, a.status));
    }
    return appointments.filter((a: AppointmentResponse) => !isUpcoming(a.appointment_date, a.status));
  }, [appointments, tab]);

  return (
    <div className="p-4 space-y-4 pb-20">
      <motion.div
        initial={{ opacity: 0, y: 8 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.3 }}
        className="flex items-end justify-between gap-4"
      >
        <div>
          <h1 className="text-page-title font-heading text-mirageBlack">
            My Appointments
          </h1>
          <p className="text-caption text-clinicalGrey">
            View and manage your appointments
          </p>
        </div>
        <Link href="/patient/book-appointment">
          <button className="px-4 py-2 bg-celestialBlue text-white rounded-button text-caption font-medium hover:bg-celestialBlue-600 transition-colors min-h-[40px] whitespace-nowrap">
            + Book
          </button>
        </Link>
      </motion.div>

      {/* Tabs */}
      <div className="flex bg-white border border-border rounded-button p-1">
        <button
          onClick={() => setTab("upcoming")}
          className={cn(
            "flex-1 py-2 text-caption font-medium rounded-button transition-colors min-h-[36px]",
            tab === "upcoming"
              ? "bg-celestialBlue text-white"
              : "text-clinicalGrey hover:text-mirageBlack"
          )}
        >
          Upcoming
        </button>
        <button
          onClick={() => setTab("past")}
          className={cn(
            "flex-1 py-2 text-caption font-medium rounded-button transition-colors min-h-[36px]",
            tab === "past"
              ? "bg-celestialBlue text-white"
              : "text-clinicalGrey hover:text-mirageBlack"
          )}
        >
          Past
        </button>
      </div>

      {isLoading && <LoadingSkeleton type="list" count={4} />}

      {!isLoading && error && (
        <EmptyState
          icon={<Stethoscope className="w-8 h-8 text-clinicalGrey" />}
          title="Could not load appointments"
          description="Something went wrong. Please try again later."
        />
      )}

      {!isLoading && !error && filtered.length === 0 && (
        <EmptyState
          icon={<CalendarPlus className="w-8 h-8 text-clinicalGrey" />}
          title="No appointments yet"
          description={
            tab === "upcoming"
              ? "You have no upcoming appointments. Book one now."
              : "No past appointments to show."
          }
          action={
            tab === "upcoming" ? (
              <Link href="/patient/book-appointment">
                <button className="px-5 py-2.5 bg-celestialBlue text-white rounded-button text-body font-medium hover:bg-celestialBlue-600 transition-colors min-h-[44px]">
                  Book Appointment
                </button>
              </Link>
            ) : null
          }
        />
      )}

      {!isLoading && !error && filtered.length > 0 && (
        <div className="space-y-2">
          {filtered.map((appointment, index) => (
            <AppointmentCard
              key={appointment.id}
              appointment={appointment}
              index={index}
            />
          ))}
        </div>
      )}
    </div>
  );
}
