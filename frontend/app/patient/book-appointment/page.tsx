"use client";

import React, { useState, useCallback } from "react";
import { AnimatePresence, motion } from "framer-motion";
import { useRouter } from "next/navigation";
import { ChevronRight } from "lucide-react";
import { WizardHeader } from "@/components/patient/booking/WizardHeader";
import { Step1Facility } from "@/components/patient/booking/Step1Facility";
import { Step2Date } from "@/components/patient/booking/Step2Date";
import { Step3Symptoms } from "@/components/patient/booking/Step3Symptoms";
import { Step4Confirm } from "@/components/patient/booking/Step4Confirm";
import { useCreateAppointment } from "@/hooks/useAppointments";
import { useToast } from "@/hooks/useToast";
import type { Facility, AppointmentPriority } from "@/lib/types";

const TOTAL_STEPS = 4;

export default function BookAppointmentPage(): React.ReactElement {
  const router = useRouter();
  const { showToast } = useToast();
  const createMutation = useCreateAppointment();

  const [step, setStep] = useState(1);
  const [direction, setDirection] = useState<1 | -1>(1);

  const [facility, setFacility] = useState<Facility | null>(null);
  const [selectedDate, setSelectedDate] = useState<string | null>(null);
  const [isEmergency, setIsEmergency] = useState(false);
  const [symptoms, setSymptoms] = useState("");
  const [reason, setReason] = useState("");
  const [duration, setDuration] = useState(30);
  const [priority, setPriority] = useState<AppointmentPriority>("NORMAL");

  const [isSuccess, setIsSuccess] = useState(false);

  const canProceed = useCallback(() => {
    switch (step) {
      case 1:
        return !!facility;
      case 2:
        return !!selectedDate;
      case 3:
        return symptoms.trim().length >= 10 && symptoms.trim().length <= 2000;
      case 4:
        return false; // handled by button
      default:
        return false;
    }
  }, [step, facility, selectedDate, symptoms]);

  const handleNext = useCallback(async () => {
    if (!canProceed()) return;

    if (step < TOTAL_STEPS) {
      setDirection(1);
      setStep((s) => s + 1);
    }
  }, [canProceed, step]);

  const handleBack = useCallback(() => {
    if (step > 1) {
      setDirection(-1);
      setStep((s) => s - 1);
    } else {
      router.push("/patient/services");
    }
  }, [step, router]);

  const handleConfirm = useCallback(async () => {
    if (isSuccess) return;
    if (!facility || !selectedDate) return;

    try {
      await createMutation.mutateAsync({
        facility_id: facility.id,
        appointment_date: selectedDate,
        symptoms: symptoms.trim(),
        reason: reason.trim() || undefined,
        duration_minutes: duration,
        priority,
      });
      setIsSuccess(true);
      showToast({
        title: "Appointment Confirmed",
        message: "Your appointment has been booked successfully.",
        type: "success",
      });
    } catch (err) {
      const msg = err instanceof Error ? err.message : "Failed to confirm booking.";
      showToast({ title: "Error", message: msg, type: "error" });
    }
  }, [isSuccess, facility, selectedDate, symptoms, reason, duration, priority, createMutation, showToast]);

  const slideVariants = {
    enter: (dir: number) => ({ x: dir > 0 ? 300 : -300, opacity: 0 }),
    center: {
      x: 0,
      opacity: 1,
      transition: { type: "spring", stiffness: 380, damping: 32 },
    },
    exit: (dir: number) => ({
      x: dir > 0 ? -300 : 300,
      opacity: 0,
      transition: { duration: 0.2, ease: "easeIn" },
    }),
  };

  return (
    <div className="flex flex-col h-[100dvh] bg-stellarWhite">
      <WizardHeader step={step} totalSteps={TOTAL_STEPS} onBack={handleBack} />

      <div className="flex-1 overflow-hidden relative">
        <AnimatePresence mode="wait" custom={direction}>
          {step === 1 && (
            <motion.div
              key="step1"
              custom={direction}
              variants={slideVariants}
              initial="enter"
              animate="center"
              exit="exit"
              className="absolute inset-0 flex flex-col"
            >
              <Step1Facility
                selectedFacilityId={facility?.id ?? null}
                onSelect={(f) => {
                  setFacility(f);
                  setDirection(1);
                  setStep(2);
                }}
              />
            </motion.div>
          )}

          {step === 2 && (
            <motion.div
              key="step2"
              custom={direction}
              variants={slideVariants}
              initial="enter"
              animate="center"
              exit="exit"
              className="absolute inset-0 flex flex-col"
            >
              <Step2Date
                selectedDate={selectedDate}
                isEmergency={isEmergency}
                onSelectDate={(d) => {
                  setSelectedDate(d);
                  setDirection(1);
                  setStep(3);
                }}
                onToggleEmergency={(v) => {
                  setIsEmergency(v);
                  if (v) setPriority("EMERGENCY");
                  else if (priority === "EMERGENCY") setPriority("NORMAL");
                }}
              />
            </motion.div>
          )}

          {step === 3 && (
            <motion.div
              key="step3"
              custom={direction}
              variants={slideVariants}
              initial="enter"
              animate="center"
              exit="exit"
              className="absolute inset-0 flex flex-col"
            >
              <div className="flex-1 min-h-0 overflow-y-auto">
                <Step3Symptoms
                  symptoms={symptoms}
                  reason={reason}
                  duration={duration}
                  priority={priority}
                  onSymptomsChange={setSymptoms}
                  onReasonChange={setReason}
                  onDurationChange={setDuration}
                  onPriorityChange={setPriority}
                />
              </div>
              {/* Next button for step 3 */}
              <div className="shrink-0 px-4 py-3 bg-white border-t border-border">
                <button
                  onClick={handleNext}
                  disabled={!canProceed()}
                  className="w-full py-3 bg-celestialBlue text-white rounded-button text-body font-medium hover:bg-celestialBlue-600 transition-colors disabled:opacity-50 flex items-center justify-center gap-2 min-h-[44px]"
                >
                  <>
                    Review & Confirm
                    <ChevronRight className="w-4 h-4" />
                  </>
                </button>
              </div>
            </motion.div>
          )}

          {step === 4 && (
            <motion.div
              key="step4"
              custom={direction}
              variants={slideVariants}
              initial="enter"
              animate="center"
              exit="exit"
              className="absolute inset-0 flex flex-col"
            >
              <Step4Confirm
                facilityName={facility?.name ?? ""}
                facilityCity={facility?.city ?? ""}
                date={selectedDate ?? ""}
                symptoms={symptoms}
                reason={reason}
                duration={duration}
                priority={priority}
                doctorName={null}
                doctorSpecialty={null}
                isSubmitting={createMutation.isPending}
                isSuccess={isSuccess}
                onConfirm={handleConfirm}
              />
            </motion.div>
          )}
        </AnimatePresence>
      </div>
    </div>
  );
}
