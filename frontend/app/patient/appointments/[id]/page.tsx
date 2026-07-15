"use client";

import React, { useState } from "react";
import { useRouter, useParams } from "next/navigation";
import { motion, AnimatePresence } from "framer-motion";
import {
  Stethoscope,
  MapPin,
  CalendarDays,
  Clock,
  ShieldCheck,
  AlertTriangle,
  ChevronLeft,
  X,
  Loader2,
} from "lucide-react";
import { useAppointment, useCancelAppointment } from "@/hooks/useAppointments";
import { LoadingSkeleton } from "@/components/ui/LoadingSkeleton";
import { EmptyState } from "@/components/ui/EmptyState";
import { useToast } from "@/hooks/useToast";
import { cn } from "@/lib/utils";
import type { AppointmentStatus, AppointmentPriority, AppointmentResponse } from "@/lib/types";

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

const priorityBadge: Record<AppointmentPriority, { label: string; classes: string }> = {
  NORMAL: {
    label: "Normal",
    classes: "bg-celestialBlue/10 text-celestialBlue border-celestialBlue/20",
  },
  URGENT: {
    label: "Urgent",
    classes: "bg-alertOrange/10 text-alertOrange border-alertOrange/20",
  },
  EMERGENCY: {
    label: "Emergency",
    classes: "bg-[#EF4444]/10 text-[#EF4444] border-[#EF4444]/20",
  },
  LOW: {
    label: "Low",
    classes: "bg-clinicalGrey/10 text-clinicalGrey border-clinicalGrey/20",
  },
};

function parseDateTime(iso: string): { date: string; time: string | null } {
  const hasTime = iso.includes("T");
  const d = new Date(iso);
  if (isNaN(d.getTime())) {
    return { date: iso, time: null };
  }
  return {
    date: d.toLocaleDateString("en-US", {
      weekday: "long",
      month: "long",
      day: "numeric",
      year: "numeric",
    }),
    time: hasTime
      ? d.toLocaleTimeString("en-US", { hour: "2-digit", minute: "2-digit" })
      : null,
  };
}

export default function AppointmentDetailPage(): React.ReactElement {
  const params = useParams();
  const id = typeof params.id === "string" ? params.id : null;
  const router = useRouter();
  const { showToast } = useToast();

  const { data, isLoading, error } = useAppointment(id);
  const cancelMutation = useCancelAppointment();

  const [showCancelModal, setShowCancelModal] = useState(false);

  const appointment = data ?? null;
  const todayStr = new Date().toISOString().split("T")[0];

  const canStartAssessment =
    appointment?.status === "CONFIRMED" &&
    appointment?.appointment_date === todayStr;

  const within3Days = (() => {
    if (!appointment) return true;
    const today = new Date(todayStr + "T00:00:00");
    const apptDate = new Date(appointment.appointment_date + "T00:00:00");
    const diffMs = apptDate.getTime() - today.getTime();
    const diffDays = diffMs / (1000 * 60 * 60 * 24);
    return diffDays < 3;
  })();

  const canCancel =
    appointment &&
    appointment.status !== "CANCELLED" &&
    appointment.status !== "COMPLETED" &&
    !within3Days;

  const dt = appointment ? parseDateTime(appointment.appointment_date) : null;

  const handleStartAssessment = () => {
    if (!appointment) return;
    router.push(`/patient/symptom-check?appointmentId=${appointment.id}`);
  };

  const handleCancel = async () => {
    if (!appointment) return;
    try {
      await cancelMutation.mutateAsync({
        id: appointment.id,
        reason: "Patient cancelled via app",
      });
      setShowCancelModal(false);
      showToast({
        title: "Cancelled",
        message: "Your appointment has been cancelled.",
        type: "info",
      });
      router.push("/patient/appointments");
    } catch (err) {
      const msg =
        err instanceof Error ? err.message : "Failed to cancel appointment.";
      showToast({ title: "Error", message: msg, type: "error" });
    }
  };

  return (
    <div className="relative">
      {/* Header */}
      <div className="sticky top-0 z-10 bg-stellarWhite/80 backdrop-blur-glass border-b border-border px-4 py-3 flex items-center gap-3">
        <button
          onClick={() => router.push("/patient/appointments")}
          className="w-10 h-10 rounded-full bg-white border border-border flex items-center justify-center active:scale-95 transition-transform"
          aria-label="Back"
        >
          <ChevronLeft className="w-5 h-5 text-mirageBlack" />
        </button>
        <h1 className="text-body font-semibold text-mirageBlack flex-1">
          Appointment
        </h1>
      </div>

      <div className="p-4 space-y-4 pb-20">
        {isLoading && <LoadingSkeleton type="card" count={2} />}

        {!isLoading && error && (
          <EmptyState
            icon={<Stethoscope className="w-8 h-8 text-clinicalGrey" />}
            title="Could not load appointment"
            description="Something went wrong. Please try again later."
          />
        )}

        {!isLoading && !error && !appointment && (
          <EmptyState
            icon={<Stethoscope className="w-8 h-8 text-clinicalGrey" />}
            title="Appointment not found"
            description="The appointment you are looking for does not exist."
          />
        )}

        {!isLoading && !error && appointment && (
          <motion.div
            initial={{ opacity: 0, y: 8 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.3 }}
            className="space-y-3"
          >
            {/* Status card */}
            <div className="bg-white border border-border rounded-card p-4">
              <div className="flex items-center justify-between mb-3">
                <span
                  className={cn(
                    "px-2.5 py-0.5 rounded-full border text-micro font-medium",
                    statusBadge[appointment.status].classes
                  )}
                >
                  {statusBadge[appointment.status].label}
                </span>
                <span
                  className={cn(
                    "px-2.5 py-0.5 rounded-full border text-micro font-medium",
                    priorityBadge[appointment.priority].classes
                  )}
                >
                  {priorityBadge[appointment.priority].label}
                </span>
              </div>
              <h2 className="text-section-title font-semibold text-mirageBlack">
                {appointment.facility_name || "Healthcare Facility"}
              </h2>
              <p className="text-caption text-clinicalGrey mt-0.5">
                {dt?.date}
                {dt?.time ? ` · ${dt.time}` : " · Time to be confirmed"}
              </p>
            </div>

            {/* Details */}
            <div className="bg-white border border-border rounded-card p-4 space-y-4">
              <div className="flex items-start gap-3">
                <div className="w-9 h-9 rounded-lg bg-celestialBlue/10 flex items-center justify-center shrink-0">
                  <MapPin className="w-4.5 h-4.5 text-celestialBlue" />
                </div>
                <div>
                  <p className="text-caption text-clinicalGrey">Facility</p>
                  <p className="text-body font-medium text-mirageBlack">
                    {appointment.facility_name || "—"}
                  </p>
                </div>
              </div>

              <div className="flex items-start gap-3">
                <div className="w-9 h-9 rounded-lg bg-celestialBlue/10 flex items-center justify-center shrink-0">
                  <Stethoscope className="w-4.5 h-4.5 text-celestialBlue" />
                </div>
                <div>
                  <p className="text-caption text-clinicalGrey">Doctor</p>
                  <p className="text-body font-medium text-mirageBlack">
                    {appointment.doctor_name
                      ? `Dr. ${appointment.doctor_name}`
                      : "To be assigned"}
                  </p>
                  {appointment.doctor_specialty && (
                    <p className="text-caption text-clinicalGrey">
                      {appointment.doctor_specialty}
                    </p>
                  )}
                </div>
              </div>

              <div className="flex items-start gap-3">
                <div className="w-9 h-9 rounded-lg bg-celestialBlue/10 flex items-center justify-center shrink-0">
                  <CalendarDays className="w-4.5 h-4.5 text-celestialBlue" />
                </div>
                <div>
                  <p className="text-caption text-clinicalGrey">Date</p>
                  <p className="text-body font-medium text-mirageBlack">
                    {dt?.date}
                  </p>
                </div>
              </div>

              <div className="flex items-start gap-3">
                <div className="w-9 h-9 rounded-lg bg-celestialBlue/10 flex items-center justify-center shrink-0">
                  <Clock className="w-4.5 h-4.5 text-celestialBlue" />
                </div>
                <div>
                  <p className="text-caption text-clinicalGrey">Duration</p>
                  <p className="text-body font-medium text-mirageBlack">
                    {appointment.desired_duration_minutes} minutes
                  </p>
                </div>
              </div>

              <div className="flex items-start gap-3">
                <div className="w-9 h-9 rounded-lg bg-celestialBlue/10 flex items-center justify-center shrink-0">
                  <ShieldCheck className="w-4.5 h-4.5 text-celestialBlue" />
                </div>
                <div>
                  <p className="text-caption text-clinicalGrey">Priority</p>
                  <span
                    className={cn(
                      "inline-flex items-center px-2.5 py-0.5 rounded-full border text-micro font-medium mt-0.5",
                      priorityBadge[appointment.priority].classes
                    )}
                  >
                    {priorityBadge[appointment.priority].label}
                  </span>
                </div>
              </div>
            </div>

            {/* Symptoms */}
            <div className="bg-white border border-border rounded-card p-4">
              <p className="text-caption font-medium text-mirageBlack mb-1.5">
                Symptoms
              </p>
              <p className="text-body text-mirageBlack whitespace-pre-wrap">
                {appointment.symptoms || "Not provided"}
              </p>
            </div>

            {/* Reason */}
            {appointment.reason && (
              <div className="bg-white border border-border rounded-card p-4">
                <p className="text-caption font-medium text-mirageBlack mb-1">
                  Reason
                </p>
                <p className="text-body text-mirageBlack">{appointment.reason}</p>
              </div>
            )}

            {/* Actions */}
            <div className="space-y-3 pt-2">
              {canStartAssessment && (
                <button
                  onClick={handleStartAssessment}
                  className="w-full py-3 bg-healthGreen text-white rounded-button text-body font-medium hover:bg-healthGreen-600 transition-colors flex items-center justify-center gap-2 min-h-[44px]"
                >
                  <Stethoscope className="w-5 h-5" />
                  Start Initial Assessment
                </button>
              )}

              {canCancel ? (
                <button
                  onClick={() => setShowCancelModal(true)}
                  className="w-full py-3 border border-alertOrange/30 text-alertOrange rounded-button text-body font-medium hover:bg-alertOrange-50 transition-colors min-h-[44px]"
                >
                  Cancel Appointment
                </button>
              ) : appointment &&
                appointment.status !== "CANCELLED" &&
                appointment.status !== "COMPLETED" ? (
                <div className="text-center">
                  <p className="text-caption text-clinicalGrey">
                    Cancellations require 3 days notice.
                  </p>
                </div>
              ) : null}
            </div>
          </motion.div>
        )}
      </div>

      {/* Cancel Confirmation Modal */}
      <AnimatePresence>
        {showCancelModal && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="fixed inset-0 z-50 bg-black/40 backdrop-blur-sm flex items-center justify-center px-4"
          >
            <motion.div
              initial={{ scale: 0.96, opacity: 0 }}
              animate={{ scale: 1, opacity: 1 }}
              exit={{ scale: 0.96, opacity: 0 }}
              transition={{ type: "spring", stiffness: 380, damping: 32 }}
              className="bg-white rounded-dialog p-5 max-w-sm w-full shadow-elevation-4"
            >
              <div className="flex items-center justify-between mb-3">
                <h3 className="text-section-title font-semibold text-mirageBlack">
                  Cancel Appointment?
                </h3>
                <button
                  onClick={() => setShowCancelModal(false)}
                  className="w-8 h-8 rounded-full flex items-center justify-center hover:bg-stellarWhite-200 transition-colors"
                  aria-label="Close"
                >
                  <X className="w-4 h-4 text-clinicalGrey" />
                </button>
              </div>
              <p className="text-body text-clinicalGrey mb-6">
                Are you sure you want to cancel this appointment? This action
                cannot be undone.
              </p>
              <div className="flex gap-3">
                <button
                  onClick={() => setShowCancelModal(false)}
                  className="flex-1 py-3 border border-border text-mirageBlack rounded-button text-body font-medium hover:bg-stellarWhite-200 transition-colors min-h-[44px]"
                >
                  Keep Appointment
                </button>
                <button
                  onClick={handleCancel}
                  disabled={cancelMutation.isPending}
                  className="flex-1 py-3 bg-alertOrange text-white rounded-button text-body font-medium hover:bg-alertOrange-600 transition-colors disabled:opacity-50 flex items-center justify-center gap-2 min-h-[44px]"
                >
                  {cancelMutation.isPending ? (
                    <Loader2 className="w-4 h-4 animate-spin" />
                  ) : (
                    <AlertTriangle className="w-4 h-4" />
                  )}
                  Cancel
                </button>
              </div>
            </motion.div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}
