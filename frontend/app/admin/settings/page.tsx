"use client";

import React, { useState, useEffect } from "react";
import { motion } from "framer-motion";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import {
  Clock,
  AlertTriangle,
  Bell,
  CalendarCheck,
  Save,
  Loader2,
} from "lucide-react";
import { adminApi } from "@/lib/api";
import type { SystemConfigItem, UpdateSystemConfigPayload } from "@/lib/types";
import { cn } from "@/lib/utils";
import { useToast } from "@/hooks/useToast";

const spring = { type: "spring", stiffness: 380, damping: 32 };

interface SectionDef {
  title: string;
  icon: React.ElementType;
  keys: string[];
}

const SECTIONS: SectionDef[] = [
  {
    title: "Facility Defaults",
    icon: Clock,
    keys: ["facility_open_time", "facility_close_time", "default_slot_duration"],
  },
  {
    title: "Triage Rules",
    icon: AlertTriangle,
    keys: ["emergency_triage_threshold"],
  },
  {
    title: "Notifications",
    icon: Bell,
    keys: ["auto_reminder_hours"],
  },
  {
    title: "Booking Limits",
    icon: CalendarCheck,
    keys: ["max_daily_appointments_per_doctor"],
  },
];

const LABELS: Record<string, string> = {
  facility_open_time: "Opening Time",
  facility_close_time: "Closing Time",
  default_slot_duration: "Slot Duration (minutes)",
  emergency_triage_threshold: "Emergency Threshold Score",
  auto_reminder_hours: "Reminder Hours Before",
  max_daily_appointments_per_doctor: "Max Daily Appointments / Doctor",
};

const INPUT_TYPES: Record<string, string> = {
  facility_open_time: "time",
  facility_close_time: "time",
  default_slot_duration: "number",
  emergency_triage_threshold: "number",
  auto_reminder_hours: "number",
  max_daily_appointments_per_doctor: "number",
};

export default function AdminSettingsPage(): React.ReactElement {
  const { showToast } = useToast();
  const queryClient = useQueryClient();

  const { data: settings, isLoading } = useQuery({
    queryKey: ["admin", "settings"],
    queryFn: () => adminApi.listSettings(),
  });

  const [localValues, setLocalValues] = useState<Record<string, string>>({});

  useEffect(() => {
    if (settings) {
      const map: Record<string, string> = {};
      for (const s of settings) {
        map[s.key] = s.value;
      }
      setLocalValues(map);
    }
  }, [settings]);

  const updateMutation = useMutation({
    mutationFn: ({ key, data }: { key: string; data: UpdateSystemConfigPayload }) =>
      adminApi.updateSetting(key, data),
    onSuccess: (_data, variables) => {
      queryClient.invalidateQueries({ queryKey: ["admin", "settings"] });
      showToast({
        title: `Setting saved`,
        message: `${LABELS[variables.key] ?? variables.key} updated.`,
        type: "success",
      });
    },
    onError: (err: unknown) => {
      const message = err instanceof Error ? err.message : "Failed to save setting.";
      showToast({ title: message, message: "", type: "error" });
    },
  });

  function handleChange(key: string, value: string) {
    setLocalValues((prev) => ({ ...prev, [key]: value }));
  }

  function handleSaveSection(section: SectionDef) {
    if (!settings) return;
    for (const key of section.keys) {
      const newValue = localValues[key];
      const original = settings.find((s) => s.key === key)?.value;
      if (newValue !== undefined && newValue !== original) {
        updateMutation.mutate({ key, data: { value: newValue } });
      }
    }
  }

  function getSectionHasChanges(section: SectionDef): boolean {
    if (!settings) return false;
    return section.keys.some((key) => {
      const newValue = localValues[key];
      const original = settings.find((s) => s.key === key)?.value;
      return newValue !== undefined && newValue !== original;
    });
  }

  return (
    <div className="space-y-6">
      <motion.div
        initial={{ opacity: 0, y: 12 }}
        animate={{ opacity: 1, y: 0 }}
        transition={spring}
      >
        <div>
          <h1 className="text-2xl font-bold text-mirageBlack">Settings</h1>
          <p className="text-clinicalGrey">
            Manage hospital-wide configuration defaults
          </p>
        </div>
      </motion.div>

      {isLoading ? (
        <div className="bg-white rounded-xl border border-border p-8 flex items-center justify-center">
          <Loader2 className="w-6 h-6 text-celestialBlue animate-spin" />
        </div>
      ) : (
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {SECTIONS.map((section, index) => {
            const Icon = section.icon;
            const hasChanges = getSectionHasChanges(section);
            return (
              <motion.div
                key={section.title}
                initial={{ opacity: 0, y: 12 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ ...spring, delay: index * 0.05 }}
                className="bg-white rounded-xl border border-border p-6 space-y-4"
              >
                <div className="flex items-center gap-3">
                  <div className="w-9 h-9 rounded-lg bg-celestialBlue/10 flex items-center justify-center">
                    <Icon className="w-5 h-5 text-celestialBlue" />
                  </div>
                  <h2 className="text-base font-bold text-mirageBlack">
                    {section.title}
                  </h2>
                </div>

                <div className="space-y-4">
                  {section.keys.map((key) => {
                    const setting = settings?.find((s) => s.key === key);
                    if (!setting) return null;
                    return (
                      <div key={key} className="space-y-1.5">
                        <label className="text-xs font-medium text-clinicalGrey block">
                          {LABELS[key] ?? key}
                        </label>
                        <input
                          type={INPUT_TYPES[key] ?? "text"}
                          value={localValues[key] ?? setting.value}
                          onChange={(e) => handleChange(key, e.target.value)}
                          className="w-full px-3 py-2 rounded-lg border border-border text-sm text-mirageBlack focus:outline-none focus:ring-2 focus:ring-celestialBlue/30 transition-all"
                        />
                        {setting.description && (
                          <p className="text-xs text-clinicalGrey">
                            {setting.description}
                          </p>
                        )}
                      </div>
                    );
                  })}
                </div>

                <div className="flex items-center justify-end pt-2">
                  <button
                    onClick={() => handleSaveSection(section)}
                    disabled={!hasChanges || updateMutation.isPending}
                    className={cn(
                      "inline-flex items-center gap-2 px-4 py-2 rounded-lg text-sm font-medium transition-colors",
                      hasChanges
                        ? "bg-celestialBlue text-white hover:bg-celestialBlue/90"
                        : "bg-stellarWhite text-clinicalGrey cursor-not-allowed"
                    )}
                  >
                    {updateMutation.isPending ? (
                      <Loader2 className="w-4 h-4 animate-spin" />
                    ) : (
                      <Save className="w-4 h-4" />
                    )}
                    Save Changes
                  </button>
                </div>
              </motion.div>
            );
          })}
        </div>
      )}
    </div>
  );
}
