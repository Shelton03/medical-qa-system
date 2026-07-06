"use client";

import React from "react";
import { motion } from "framer-motion";
import { Check, X, ChevronDown, ChevronUp } from "lucide-react";
import type { DiagnosisResponse } from "@/lib/types";

interface DiagnosisCardProps {
  diagnosis: DiagnosisResponse;
  onConfirm?: (id: string) => void;
  onIgnore?: (id: string) => void;
  className?: string;
}

function ConfidenceBadge({ confidence }: { confidence: string | null }): React.ReactElement {
  const value = confidence?.toLowerCase() ?? "";
  const isHigh = value.includes("high") || value.includes("confirmed");
  const isMedium = value.includes("medium") || value.includes("suspected");
  return (
    <span
      className={`inline-flex items-center px-2 py-0.5 rounded-full text-[10px] font-semibold tracking-wide uppercase ${
        isHigh
          ? "bg-healthGreen/10 text-healthGreen"
          : isMedium
          ? "bg-celestialBlue/10 text-celestialBlue"
          : "bg-clinicalGrey/10 text-clinicalGrey"
      }`}
    >
      {confidence || "Unknown"}
    </span>
  );
}

export function DiagnosisCard({ diagnosis, onConfirm, onIgnore, className = "" }: DiagnosisCardProps): React.ReactElement {
  const [expanded, setExpanded] = React.useState(false);

  return (
    <motion.div
      initial={{ opacity: 0, y: 8 }}
      animate={{ opacity: 1, y: 0 }}
      className={`bg-white rounded-card border border-border p-4 ${className}`}
    >
      <div className="flex items-start justify-between gap-3">
        <div className="flex-1 min-w-0">
          <div className="flex items-center gap-2 flex-wrap">
            <h3 className="text-sm font-semibold text-mirageBlack">{diagnosis.diagnosis_name}</h3>
            <ConfidenceBadge confidence={diagnosis.confidence} />
          </div>
          {diagnosis.icd10_code && (
            <p className="text-[11px] text-clinicalGrey mt-0.5">ICD-10: {diagnosis.icd10_code}</p>
          )}
        </div>
        <div className="flex items-center gap-1 shrink-0">
          {onConfirm && (
            <button
              onClick={() => onConfirm(diagnosis.id)}
              className="p-1.5 rounded-lg hover:bg-healthGreen-50 text-clinicalGrey hover:text-healthGreen transition-colors"
              aria-label="Confirm diagnosis"
              title="Confirm"
            >
              <Check className="w-4 h-4" />
            </button>
          )}
          {onIgnore && (
            <button
              onClick={() => onIgnore(diagnosis.id)}
              className="p-1.5 rounded-lg hover:bg-alertOrange/5 text-clinicalGrey hover:text-alertOrange transition-colors"
              aria-label="Ignore diagnosis"
              title="Ignore"
            >
              <X className="w-4 h-4" />
            </button>
          )}
        </div>
      </div>

      {diagnosis.notes && (
        <div className="mt-3">
          <button
            onClick={() => setExpanded((e) => !e)}
            className="flex items-center gap-1 text-[11px] text-celestialBlue hover:underline"
          >
            {expanded ? <ChevronUp className="w-3 h-3" /> : <ChevronDown className="w-3 h-3" />}
            {expanded ? "Hide notes" : "View notes"}
          </button>
          {expanded && (
            <motion.p
              initial={{ opacity: 0, height: 0 }}
              animate={{ opacity: 1, height: "auto" }}
              className="text-caption text-clinicalGrey mt-2 leading-relaxed"
            >
              {diagnosis.notes}
            </motion.p>
          )}
        </div>
      )}
    </motion.div>
  );
}
