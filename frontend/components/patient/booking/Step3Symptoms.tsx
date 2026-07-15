"use client";

import React from "react";
import { motion } from "framer-motion";
import {
  AlertTriangle,
  Clock,
} from "lucide-react";
import { cn } from "@/lib/utils";
import { AppointmentPriority } from "@/lib/types";

const DURATION_OPTIONS = [15, 30, 45, 60] as const;

const PROMPTS = [
  "I have chest pain",
  "I have a headache",
  "I feel dizzy and nauseous",
  "I have a fever and sore throat",
  "I have pain in my back",
  "I have a skin rash",
];

interface Step3SymptomsProps {
  symptoms: string;
  reason: string;
  duration: number;
  priority: AppointmentPriority;
  onSymptomsChange: (v: string) => void;
  onReasonChange: (v: string) => void;
  onDurationChange: (v: number) => void;
  onPriorityChange: (v: AppointmentPriority) => void;
}

export function Step3Symptoms({
  symptoms,
  reason,
  duration,
  priority,
  onSymptomsChange,
  onReasonChange,
  onDurationChange,
  onPriorityChange,
}: Step3SymptomsProps): React.ReactElement {
  const symptomCount = symptoms.length;
  const isOverLimit = symptomCount > 2000;
  const isUnderLimit = symptomCount > 0 && symptomCount < 10;

  const isEmergency = priority === "EMERGENCY";

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
        Describe Your Symptoms
      </h3>
      <p className="text-caption text-clinicalGrey mb-3">
        Tell us what is bothering you so we can route you to the right care.
      </p>

      <div className="flex-1 overflow-y-auto space-y-4 pb-4">
        {/* Symptom textarea */}
        <div>
          <label className="text-caption font-medium text-mirageBlack mb-1.5 block">
            Symptoms <span className="text-alertOrange">*</span>
          </label>
          <textarea
            value={symptoms}
            onChange={(e) => {
              if (e.target.value.length <= 2000) onSymptomsChange(e.target.value);
            }}
            placeholder="Describe what you are feeling..."
            rows={4}
            className={cn(
              "w-full bg-stellarWhite-100 border rounded-input px-3 py-2.5 text-body text-mirageBlack placeholder:text-clinicalGrey focus:outline-none focus:ring-2 focus:ring-celestialBlue/30 resize-none",
              isOverLimit ? "border-alertOrange" : "border-border"
            )}
          />
          <div className="flex items-center justify-between mt-1">
            <p
              className={cn(
                "text-micro",
                isUnderLimit || isOverLimit ? "text-alertOrange" : "text-clinicalGrey"
              )}
            >
              {isUnderLimit
                ? "Please enter at least 10 characters"
                : isOverLimit
                ? "Maximum 2000 characters"
                : ""}
            </p>
            <p className="text-micro text-clinicalGrey">
              {symptomCount}/2000
            </p>
          </div>
        </div>

        {/* Duration selector */}
        <div>
          <label className="text-caption font-medium text-mirageBlack mb-2 block flex items-center gap-1.5">
            <Clock className="w-4 h-4 text-clinicalGrey" />
            Estimated Duration
          </label>
          <div className="grid grid-cols-4 gap-2">
            {DURATION_OPTIONS.map((min) => (
              <button
                key={min}
                onClick={() => onDurationChange(min)}
                className={cn(
                  "py-2.5 rounded-button text-body font-medium transition-colors min-h-[44px]",
                  duration === min
                    ? "bg-celestialBlue text-white shadow-elevation-1"
                    : "bg-white border border-border text-mirageBlack hover:bg-stellarWhite-200"
                )}
              >
                {min}m
              </button>
            ))}
          </div>
        </div>

        {/* Reason */}
        <div>
          <label className="text-caption font-medium text-mirageBlack mb-1.5 block">
            Reason for Visit <span className="text-clinicalGrey">(optional)</span>
          </label>
          <input
            type="text"
            value={reason}
            onChange={(e) => {
              if (e.target.value.length <= 500) onReasonChange(e.target.value);
            }}
            placeholder="e.g., Routine check-up, follow-up, referral..."
            className="w-full bg-stellarWhite-100 border border-border rounded-input px-3 py-2.5 text-body text-mirageBlack placeholder:text-clinicalGrey focus:outline-none focus:ring-2 focus:ring-celestialBlue/30"
          />
          <p className="text-micro text-clinicalGrey mt-1 text-right">
            {reason.length}/500
          </p>
        </div>

        {/* Guided prompts */}
        <div>
          <p className="text-caption font-medium text-mirageBlack mb-2">
            Quick prompts
          </p>
          <div className="flex flex-wrap gap-2">
            {PROMPTS.map((prompt) => (
              <button
                key={prompt}
                onClick={() => onSymptomsChange(prompt)}
                className="px-3 py-1.5 bg-white border border-border rounded-button text-caption text-mirageBlack hover:border-celestialBlue/30 hover:shadow-elevation-1 transition-all"
              >
                {prompt}
              </button>
            ))}
          </div>
        </div>

        {/* Emergency toggle */}
        <div
          className={cn(
            "rounded-card p-4 border transition-colors",
            isEmergency
              ? "bg-alertOrange-50 border-alertOrange/30"
              : "bg-white border-border"
          )}
        >
          <label className="flex items-start gap-3 cursor-pointer min-h-[44px]">
            <input
              type="checkbox"
              checked={isEmergency}
              onChange={(e) =>
                onPriorityChange(
                  e.target.checked ? "EMERGENCY" : "NORMAL"
                )
              }
              className="mt-1 w-5 h-5 accent-alertOrange shrink-0"
            />
            <div className="flex-1">
              <div className="flex items-center gap-2">
                <AlertTriangle
                  className={cn(
                    "w-4 h-4",
                    isEmergency ? "text-alertOrange" : "text-clinicalGrey"
                  )}
                />
                <span
                  className={cn(
                    "text-body font-medium",
                    isEmergency ? "text-alertOrange" : "text-mirageBlack"
                  )}
                >
                  This is an emergency
                </span>
              </div>
              {isEmergency && (
                <motion.p
                  initial={{ opacity: 0, height: 0 }}
                  animate={{ opacity: 1, height: "auto" }}
                  className="text-caption text-alertOrange mt-1"
                >
                  If you are experiencing a life-threatening emergency, call
                  emergency services immediately.
                </motion.p>
              )}
            </div>
          </label>
        </div>
      </div>
    </motion.div>
  );
}
