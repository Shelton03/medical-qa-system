"use client";

import React, { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { Check, X, ChevronDown, ChevronUp, AlertTriangle, TestTube, Pill } from "lucide-react";
import type { DifferentialDiagnosis } from "@/lib/types";

interface DifferentialListProps {
  diagnoses: DifferentialDiagnosis[];
  onConfirm?: (id: string) => void;
  onIgnore?: (id: string) => void;
  onEdit?: (id: string) => void;
}

export function DifferentialList({ diagnoses, onConfirm, onIgnore, onEdit }: DifferentialListProps): React.ReactElement {
  const [expandedId, setExpandedId] = useState<string | null>(null);

  const toggleExpanded = (id: string) => {
    setExpandedId((prev) => (prev === id ? null : id));
  };

  if (!diagnoses || diagnoses.length === 0) {
    return (
      <div className="bg-white rounded-card border border-border p-8 text-center">
        <p className="text-sm text-clinicalGrey">No differential diagnoses available.</p>
      </div>
    );
  }

  return (
    <div className="space-y-3">
      {diagnoses.map((dx, index) => {
        const isExpanded = expandedId === dx.id;
        const isConfirmed = dx.status === "confirmed";
        const isIgnored = dx.status === "ignored";
        const probability = Math.round((dx.probability ?? 0) * 100);

        return (
          <motion.div
            key={dx.id}
            initial={{ opacity: 0, y: 8 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: index * 0.05 }}
            className={`bg-white rounded-card border ${isConfirmed ? "border-healthGreen" : isIgnored ? "border-clinicalGrey/30" : "border-border"} overflow-hidden`}
          >
            {/* Header */}
            <div className="p-4">
              <div className="flex items-start justify-between gap-3">
                <div className="flex items-center gap-3">
                  <div
                    className={`w-8 h-8 rounded-full flex items-center justify-center text-xs font-bold shrink-0 ${
                      index === 0
                        ? "bg-healthGreen/10 text-healthGreen"
                        : index === 1
                        ? "bg-celestialBlue/10 text-celestialBlue"
                        : "bg-clinicalGrey/10 text-clinicalGrey"
                    }`}
                  >
                    {index + 1}
                  </div>
                  <div>
                    <div className="flex items-center gap-2">
                      <h3 className={`text-sm font-semibold ${isIgnored ? "text-clinicalGrey line-through" : "text-mirageBlack"}`}>
                        {dx.diagnosis_name}
                      </h3>
                      {isConfirmed && (
                        <span className="inline-flex items-center gap-1 px-2 py-0.5 rounded-full text-[10px] font-semibold bg-healthGreen-50 text-healthGreen">
                          <Check className="w-3 h-3" />
                          Confirmed
                        </span>
                      )}
                      {isIgnored && (
                        <span className="inline-flex items-center gap-1 px-2 py-0.5 rounded-full text-[10px] font-semibold bg-clinicalGrey/10 text-clinicalGrey">
                          Ignored
                        </span>
                      )}
                    </div>
                    {dx.icd10_code && (
                      <p className="text-[11px] text-clinicalGrey mt-0.5">ICD-10: {dx.icd10_code}</p>
                    )}
                  </div>
                </div>

                <div className="flex items-center gap-1 shrink-0">
                  {onConfirm && !isConfirmed && !isIgnored && (
                    <button
                      onClick={() => onConfirm(dx.id)}
                      className="p-1.5 rounded-lg hover:bg-healthGreen-50 text-clinicalGrey hover:text-healthGreen transition-colors"
                      title="Confirm"
                      aria-label="Confirm diagnosis"
                    >
                      <Check className="w-4 h-4" />
                    </button>
                  )}
                  {onIgnore && !isConfirmed && !isIgnored && (
                    <button
                      onClick={() => onIgnore(dx.id)}
                      className="p-1.5 rounded-lg hover:bg-alertOrange/5 text-clinicalGrey hover:text-alertOrange transition-colors"
                      title="Ignore"
                      aria-label="Ignore diagnosis"
                    >
                      <X className="w-4 h-4" />
                    </button>
                  )}
                  {onEdit && (
                    <button
                      onClick={() => onEdit(dx.id)}
                      className="p-1.5 rounded-lg hover:bg-secondary text-clinicalGrey hover:text-mirageBlack transition-colors"
                      title="Edit"
                      aria-label="Edit diagnosis"
                    >
                      <ChevronDown className="w-4 h-4" />
                    </button>
                  )}
                </div>
              </div>

              {/* Probability Bar */}
              {dx.probability !== undefined && dx.probability !== null && (
                <div className="mt-3">
                  <div className="flex items-center justify-between mb-1">
                    <span className="text-[11px] text-clinicalGrey">Confidence</span>
                    <span className="text-[11px] font-medium text-mirageBlack">{probability}%</span>
                  </div>
                  <div className="h-1.5 w-full bg-secondary rounded-full overflow-hidden">
                    <motion.div
                      initial={{ width: 0 }}
                      animate={{ width: `${probability}%` }}
                      transition={{ duration: 0.6, ease: "easeOut" }}
                      className={`h-full rounded-full ${
                        probability >= 70
                          ? "bg-healthGreen"
                          : probability >= 40
                          ? "bg-celestialBlue"
                          : "bg-clinicalGrey"
                      }`}
                    />
                  </div>
                </div>
              )}

              {/* Expand toggle */}
              {(dx.reasoning || dx.supporting_evidence?.length || dx.suggested_investigations?.length) && (
                <button
                  onClick={() => toggleExpanded(dx.id)}
                  className="flex items-center gap-1 mt-2 text-[11px] text-celestialBlue hover:underline"
                >
                  {isExpanded ? <ChevronUp className="w-3 h-3" /> : <ChevronDown className="w-3 h-3" />}
                  {isExpanded ? "Hide details" : "Show details"}
                </button>
              )}
            </div>

            {/* Expanded details */}
            <AnimatePresence>
              {isExpanded && (
                <motion.div
                  initial={{ height: 0, opacity: 0 }}
                  animate={{ height: "auto", opacity: 1 }}
                  exit={{ height: 0, opacity: 0 }}
                  transition={{ duration: 0.3 }}
                  className="overflow-hidden"
                >
                  <div className="px-4 pb-4 pt-0 space-y-3 border-t border-border">
                    {dx.reasoning && (
                      <div className="pt-3">
                        <p className="text-micro text-clinicalGrey uppercase tracking-wider mb-1">Reasoning</p>
                        <p className="text-caption text-mirageBlack leading-relaxed">{dx.reasoning}</p>
                      </div>
                    )}

                    {dx.supporting_evidence && dx.supporting_evidence.length > 0 && (
                      <div>
                        <p className="text-micro text-clinicalGrey uppercase tracking-wider mb-1">Supporting Evidence</p>
                        <ul className="space-y-1">
                          {dx.supporting_evidence.map((ev, i) => (
                            <li key={i} className="flex items-start gap-1.5 text-caption text-mirageBlack">
                              <span className="text-healthGreen mt-1">•</span>
                              {ev}
                            </li>
                          ))}
                        </ul>
                      </div>
                    )}

                    {dx.contradictory_evidence && dx.contradictory_evidence.length > 0 && (
                      <div>
                        <p className="text-micro text-clinicalGrey uppercase tracking-wider mb-1">Contradictory Evidence</p>
                        <ul className="space-y-1">
                          {dx.contradictory_evidence.map((ev, i) => (
                            <li key={i} className="flex items-start gap-1.5 text-caption text-mirageBlack">
                              <AlertTriangle className="w-3 h-3 text-alertOrange mt-0.5 shrink-0" />
                              {ev}
                            </li>
                          ))}
                        </ul>
                      </div>
                    )}

                    {dx.suggested_investigations && dx.suggested_investigations.length > 0 && (
                      <div>
                        <p className="text-micro text-clinicalGrey uppercase tracking-wider mb-1">Suggested Tests</p>
                        <div className="flex flex-wrap gap-2">
                          {dx.suggested_investigations.map((test, i) => (
                            <span
                              key={i}
                              className="inline-flex items-center gap-1 px-2 py-0.5 rounded-full text-[10px] font-medium bg-celestialBlue/5 text-celestialBlue border border-celestialBlue/10"
                            >
                              <TestTube className="w-2.5 h-2.5" />
                              {test}
                            </span>
                          ))}
                        </div>
                      </div>
                    )}

                    {dx.medication_risks && dx.medication_risks.length > 0 && (
                      <div>
                        <p className="text-micro text-clinicalGrey uppercase tracking-wider mb-1">Medication Risks</p>
                        <div className="flex flex-wrap gap-2">
                          {dx.medication_risks.map((risk, i) => (
                            <span
                              key={i}
                              className="inline-flex items-center gap-1 px-2 py-0.5 rounded-full text-[10px] font-medium bg-alertOrange/5 text-alertOrange border border-alertOrange/10"
                            >
                              <Pill className="w-2.5 h-2.5" />
                              {risk}
                            </span>
                          ))}
                        </div>
                      </div>
                    )}
                  </div>
                </motion.div>
              )}
            </AnimatePresence>
          </motion.div>
        );
      })}
    </div>
  );
}
