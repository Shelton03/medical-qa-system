"use client";

import React from "react";
import { motion } from "framer-motion";
import { Pill, Clock } from "lucide-react";
import type { MedicationResponse } from "@/lib/types";

interface PrescriptionCardProps {
  medication: MedicationResponse;
  className?: string;
}

export function PrescriptionCard({ medication, className = "" }: PrescriptionCardProps): React.ReactElement {
  return (
    <motion.div
      initial={{ opacity: 0, y: 8 }}
      animate={{ opacity: 1, y: 0 }}
      className={`bg-white rounded-card border border-border p-4 ${className}`}
    >
      <div className="flex items-start gap-3">
        <div className="w-9 h-9 rounded-lg bg-celestialBlue/10 flex items-center justify-center shrink-0">
          <Pill className="w-4.5 h-4.5 text-celestialBlue" />
        </div>
        <div className="flex-1 min-w-0">
          <h4 className="text-sm font-semibold text-mirageBlack">{medication.name}</h4>
          <div className="flex flex-wrap items-center gap-x-3 gap-y-1 mt-1">
            {medication.dosage && (
              <span className="text-caption text-clinicalGrey">{medication.dosage}</span>
            )}
            {medication.frequency && (
              <span className="inline-flex items-center gap-1 text-caption text-clinicalGrey">
                <Clock className="w-3 h-3" />
                {medication.frequency}
              </span>
            )}
            {medication.duration && (
              <span className="text-caption text-clinicalGrey">for {medication.duration}</span>
            )}
          </div>
          {medication.instructions && (
            <p className="text-[11px] text-clinicalGrey mt-2 leading-relaxed border-t border-border pt-2">
              {medication.instructions}
            </p>
          )}
          {(medication.start_date || medication.end_date) && (
            <p className="text-micro text-clinicalGrey mt-1.5">
              {medication.start_date && medication.end_date
                ? `${new Date(medication.start_date).toLocaleDateString()} – ${new Date(medication.end_date).toLocaleDateString()}`
                : medication.start_date
                ? `From ${new Date(medication.start_date).toLocaleDateString()}`
                : `Until ${new Date(medication.end_date!).toLocaleDateString()}`}
            </p>
          )}
        </div>
      </div>
    </motion.div>
  );
}
