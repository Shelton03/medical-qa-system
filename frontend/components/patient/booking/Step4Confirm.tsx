"use client";

import React from "react";
import { motion } from "framer-motion";
import {
  MapPin,
  CalendarDays,
  Clock,
  Stethoscope,
  CheckCircle2,
  Loader2,
  ShieldCheck,
  AlertTriangle,
} from "lucide-react";
import { useRouter } from "next/navigation";
import { cn } from "@/lib/utils";
import type { AppointmentPriority } from "@/lib/types";

interface Step4ConfirmProps {
  facilityName: string;
  facilityCity: string;
  date: string;
  symptoms: string;
  reason: string;
  duration: number;
  priority: AppointmentPriority;
  doctorName: string | null;
  doctorSpecialty: string | null;
  isSubmitting: boolean;
  isSuccess: boolean;
  onConfirm: () => void;
}

function formatDateLabel(iso: string): string {
  const d = new Date(iso + "T00:00:00");
  return d.toLocaleDateString("en-US", {
    weekday: "long",
    month: "long",
    day: "numeric",
    year: "numeric",
  });
}

const priorityLabel: Record<AppointmentPriority, string> = {
  NORMAL: "Normal",
  URGENT: "Urgent",
  EMERGENCY: "Emergency",
  LOW: "Low",
};

const priorityColor: Record<AppointmentPriority, string> = {
  NORMAL: "bg-celestialBlue/10 text-celestialBlue border-celestialBlue/20",
  URGENT: "bg-alertOrange/10 text-alertOrange border-alertOrange/20",
  EMERGENCY: "bg-[#EF4444]/10 text-[#EF4444] border-[#EF4444]/20",
  LOW: "bg-clinicalGrey/10 text-clinicalGrey border-clinicalGrey/20",
};

export function Step4Confirm({
  facilityName,
  facilityCity,
  date,
  symptoms,
  reason,
  duration,
  priority,
  doctorName,
  doctorSpecialty,
  isSubmitting,
  isSuccess,
  onConfirm,
}: Step4ConfirmProps): React.ReactElement {
  const router = useRouter();

  if (isSuccess) {
    return (
      <motion.div
        variants={{
          hidden: { x: 24, opacity: 0 },
          visible: { x: 0, opacity: 1, transition: { type: "spring", stiffness: 380, damping: 32 } },
          exit: { x: -24, opacity: 0, transition: { duration: 0.2, ease: "easeIn" } },
        }}
        initial="hidden"
        animate="visible"
        exit="exit"
        className="flex flex-col items-center justify-center h-full px-6 text-center"
      >
        <motion.div
          initial={{ scale: 0.8, opacity: 0 }}
          animate={{ scale: 1, opacity: 1 }}
          transition={{ type: "spring", stiffness: 380, damping: 32 }}
          className="w-16 h-16 rounded-full bg-healthGreen/10 flex items-center justify-center mb-4"
        >
          <CheckCircle2 className="w-8 h-8 text-healthGreen" />
        </motion.div>
        <h3 className="text-section-title font-semibold text-mirageBlack mb-2">
          Appointment Booked!
        </h3>
        <p className="text-caption text-clinicalGrey max-w-[280px] mb-6">
          Your appointment has been confirmed. You can view it in My
          Appointments.
        </p>
        <button
          onClick={() => router.push("/patient/appointments")}
          className="px-6 py-3 bg-celestialBlue text-white rounded-button text-body font-medium hover:bg-celestialBlue-600 transition-colors min-h-[44px]"
        >
          Go to My Appointments
        </button>
      </motion.div>
    );
  }

  return (
    <motion.div
      variants={{
        hidden: { x: 24, opacity: 0 },
        visible: { x: 0, opacity: 1, transition: { type: "spring", stiffness: 380, damping: 32 } },
        exit: { x: -24, opacity: 0, transition: { duration: 0.2, ease: "easeIn" } },
      }}
      initial="hidden"
      animate="visible"
      exit="exit"
      className="flex flex-col h-full px-4 pt-3"
    >
      <h3 className="text-section-title font-semibold text-mirageBlack mb-1">
        Review & Confirm
      </h3>
      <p className="text-caption text-clinicalGrey mb-4">
        Please review your appointment details before confirming.
      </p>

      <div className="flex-1 overflow-y-auto space-y-3 pb-4">
        {/* Summary card */}
        <div className="bg-white border border-border rounded-card p-4 space-y-3">
          <div className="flex items-start gap-3">
            <div className="w-9 h-9 rounded-lg bg-celestialBlue/10 flex items-center justify-center shrink-0">
              <MapPin className="w-4.5 h-4.5 text-celestialBlue" />
            </div>
            <div>
              <p className="text-caption text-clinicalGrey">Facility</p>
              <p className="text-body font-medium text-mirageBlack">
                {facilityName}
              </p>
              <p className="text-caption text-clinicalGrey">{facilityCity}</p>
            </div>
          </div>

          <div className="flex items-start gap-3">
            <div className="w-9 h-9 rounded-lg bg-celestialBlue/10 flex items-center justify-center shrink-0">
              <CalendarDays className="w-4.5 h-4.5 text-celestialBlue" />
            </div>
            <div>
              <p className="text-caption text-clinicalGrey">Date</p>
              <p className="text-body font-medium text-mirageBlack">
                {formatDateLabel(date)}
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
                {duration} minutes
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
                  priorityColor[priority]
                )}
              >
                {priorityLabel[priority]}
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
            {symptoms}
          </p>
        </div>

        {/* Reason */}
        {reason && (
          <div className="bg-white border border-border rounded-card p-4">
            <p className="text-caption font-medium text-mirageBlack mb-1">
              Reason
            </p>
            <p className="text-body text-mirageBlack">{reason}</p>
          </div>
        )}

        {/* Auto-routed doctor */}
        {doctorName && (
          <motion.div
            initial={{ opacity: 0, y: 8 }}
            animate={{ opacity: 1, y: 0 }}
            className="bg-celestialBlue-50 border border-celestialBlue/20 rounded-card p-4"
          >
            <div className="flex items-center gap-2 mb-2">
              <Stethoscope className="w-4 h-4 text-celestialBlue" />
              <p className="text-caption font-medium text-celestialBlue">
                Assigned Doctor
              </p>
            </div>
            <p className="text-body font-semibold text-mirageBlack">
              {doctorName}
            </p>
            {doctorSpecialty && (
              <p className="text-caption text-clinicalGrey">
                {doctorSpecialty}
              </p>
            )}
          </motion.div>
        )}

        {!doctorName && !isSubmitting && (
          <div className="bg-stellarWhite-100 border border-border rounded-card p-4 text-center">
            <p className="text-caption text-clinicalGrey">
              A doctor will be assigned after confirmation.
            </p>
          </div>
        )}
      </div>

      {/* Confirm Button */}
      <div className="shrink-0 py-3 bg-white border-t border-border">
        <button
          onClick={onConfirm}
          disabled={isSubmitting}
          className="w-full py-3 bg-celestialBlue text-white rounded-button text-body font-medium hover:bg-celestialBlue-600 transition-colors disabled:opacity-50 flex items-center justify-center gap-2 min-h-[44px]"
        >
          {isSubmitting ? (
            <>
              <Loader2 className="w-4 h-4 animate-spin" />
              Booking...
            </>
          ) : (
            "Confirm Booking"
          )}
        </button>
      </div>
    </motion.div>
  );
}
