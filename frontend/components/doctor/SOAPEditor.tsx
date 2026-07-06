"use client";

import React, { useState, useCallback } from "react";
import { motion } from "framer-motion";
import { Save, RefreshCw, CheckCircle } from "lucide-react";
import type { ClinicalSummary } from "@/lib/types";

interface SOAPEditorProps {
  summary: ClinicalSummary;
  onChange?: (summary: ClinicalSummary) => void;
  onSave?: (summary: ClinicalSummary) => void;
  onRegenerate?: () => void;
  readOnly?: boolean;
}

const SECTIONS: { key: keyof ClinicalSummary; label: string; placeholder: string }[] = [
  {
    key: "subjective",
    label: "Subjective",
    placeholder: "Patient-reported symptoms, history, concerns...",
  },
  {
    key: "objective",
    label: "Objective",
    placeholder: "Physical exam findings, vitals, lab results, observations...",
  },
  {
    key: "assessment",
    label: "Assessment",
    placeholder: "Clinical assessment, differential diagnosis, analysis...",
  },
  {
    key: "plan",
    label: "Plan",
    placeholder: "Treatment plan, medications, follow-up, referrals...",
  },
];

export function SOAPEditor({ summary, onChange, onSave, onRegenerate, readOnly = false }: SOAPEditorProps): React.ReactElement {
  const [localSummary, setLocalSummary] = useState<ClinicalSummary>(summary);
  const [saving, setSaving] = useState(false);
  const [saved, setSaved] = useState(false);

  const handleChange = useCallback(
    (key: keyof ClinicalSummary, value: string) => {
      const updated = { ...localSummary, [key]: value };
      setLocalSummary(updated);
      setSaved(false);
      onChange?.(updated);
    },
    [localSummary, onChange]
  );

  const handleSave = useCallback(async () => {
    setSaving(true);
    try {
      await onSave?.(localSummary);
      setSaved(true);
      setTimeout(() => setSaved(false), 3000);
    } finally {
      setSaving(false);
    }
  }, [localSummary, onSave]);

  return (
    <motion.div
      initial={{ opacity: 0, y: 12 }}
      animate={{ opacity: 1, y: 0 }}
      className="bg-white rounded-card border border-border p-5 space-y-4"
    >
      <div className="flex items-center justify-between">
        <h3 className="text-card-title font-semibold text-mirageBlack">Clinical Summary (SOAP)</h3>
        {!readOnly && (
          <div className="flex items-center gap-2">
            {saved && (
              <motion.span
                initial={{ opacity: 0, scale: 0.9 }}
                animate={{ opacity: 1, scale: 1 }}
                className="flex items-center gap-1 text-xs text-healthGreen font-medium"
              >
                <CheckCircle className="w-3.5 h-3.5" />
                Saved
              </motion.span>
            )}
            {onRegenerate && (
              <button
                onClick={onRegenerate}
                className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-medium bg-secondary text-mirageBlack hover:bg-secondary/80 transition-colors"
              >
                <RefreshCw className="w-3.5 h-3.5" />
                Regenerate
              </button>
            )}
            {onSave && (
              <button
                onClick={handleSave}
                disabled={saving}
                className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-medium bg-mirageBlack text-white hover:bg-mirageBlack/90 transition-colors disabled:opacity-50"
              >
                <Save className="w-3.5 h-3.5" />
                {saving ? "Saving..." : "Approve & Save"}
              </button>
            )}
          </div>
        )}
      </div>

      <div className="space-y-4">
        {SECTIONS.map((section, i) => (
          <motion.div
            key={section.key}
            initial={{ opacity: 0, y: 8 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: i * 0.05 }}
          >
            <label className="block text-micro text-clinicalGrey uppercase tracking-wider mb-1.5">
              {section.label}
            </label>
            <textarea
              value={localSummary[section.key] || ""}
              onChange={(e) => handleChange(section.key, e.target.value)}
              placeholder={section.placeholder}
              readOnly={readOnly}
              rows={4}
              className={`w-full px-3 py-2.5 rounded-input text-sm leading-relaxed focus:outline-none focus:ring-2 focus:ring-celestialBlue/20 transition-all resize-y scrollbar-thin ${
                readOnly
                  ? "bg-secondary text-clinicalGrey cursor-not-allowed"
                  : "bg-white text-mirageBlack border border-border focus:border-celestialBlue"
              }`}
            />
          </motion.div>
        ))}
      </div>
    </motion.div>
  );
}
