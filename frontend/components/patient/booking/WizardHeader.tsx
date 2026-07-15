"use client";

import React from "react";
import { motion } from "framer-motion";
import { ChevronLeft } from "lucide-react";
import { pageTransition } from "@/lib/animations";

interface WizardHeaderProps {
  step: number;
  totalSteps: number;
  onBack: () => void;
}

export function WizardHeader({
  step,
  totalSteps,
  onBack,
}: WizardHeaderProps): React.ReactElement {
  const progress = (step / totalSteps) * 100;

  return (
    <div className="shrink-0">
      <div className="flex items-center gap-3 px-4 py-3 bg-white">
        <button
          onClick={onBack}
          className="w-10 h-10 rounded-full bg-stellarWhite-200 flex items-center justify-center active:scale-95 transition-transform"
          aria-label="Go back"
        >
          <ChevronLeft className="w-5 h-5 text-mirageBlack" />
        </button>
        <div className="flex-1">
          <div className="flex items-center justify-between mb-1.5">
            <h2 className="text-body font-semibold text-mirageBlack">
              Book Appointment
            </h2>
            <span className="text-micro text-clinicalGrey">
              {step}/{totalSteps}
            </span>
          </div>
          <div className="h-1.5 bg-stellarWhite-200 rounded-full overflow-hidden">
            <motion.div
              className="h-full bg-celestialBlue rounded-full"
              initial={{ width: 0 }}
              animate={{ width: `${progress}%` }}
              transition={{ type: "spring", stiffness: 380, damping: 32 }}
            />
          </div>
        </div>
      </div>
    </div>
  );
}
