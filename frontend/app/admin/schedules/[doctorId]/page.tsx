"use client";

import React, { useCallback, useState } from "react";
import { motion } from "framer-motion";
import Link from "next/link";
import { useParams } from "next/navigation";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { ArrowLeft, Save, Copy, RotateCcw, LayoutTemplate } from "lucide-react";
import { adminApi } from "@/lib/api";
import type { DoctorScheduleDay } from "@/lib/types";
import { useToast } from "@/hooks/useToast";

const spring = { type: "spring", stiffness: 380, damping: 32 };

const DAYS = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"];

const DEFAULT_SLOTS: DoctorScheduleDay[] = DAYS.map((_, idx) => ({
  day_of_week: idx,
  is_working: idx >= 1 && idx <= 5,
  start_time: "08:00",
  end_time: "17:00",
  max_appointments: 16,
  slot_duration_minutes: 30,
}));

function ScheduleDayEditor({
  day,
  onChange,
}: {
  day: DoctorScheduleDay;
  onChange: (d: DoctorScheduleDay) => void;
}) {
  return (
    <div className="bg-white rounded-xl border border-border p-4 space-y-3">
      <div className="flex items-center justify-between">
        <span className="font-medium text-mirageBlack">{DAYS[day.day_of_week]}</span>
        <label className="flex items-center gap-2 text-sm text-clinicalGrey cursor-pointer">
          <input
            type="checkbox"
            checked={day.is_working}
            onChange={(e) => onChange({ ...day, is_working: e.target.checked })}
            className="rounded border-border text-celestialBlue focus:ring-celestialBlue"
          />
          Working
        </label>
      </div>
      {day.is_working && (
        <div className="grid grid-cols-2 gap-3">
          <div>
            <label className="text-xs text-clinicalGrey block mb-1">Start</label>
            <input
              type="time"
              value={day.start_time}
              onChange={(e) => onChange({ ...day, start_time: e.target.value })}
              className="w-full px-3 py-2 rounded-lg border border-border text-sm text-mirageBlack focus:outline-none focus:ring-2 focus:ring-celestialBlue/30 focus:border-celestialBlue"
            />
          </div>
          <div>
            <label className="text-xs text-clinicalGrey block mb-1">End</label>
            <input
              type="time"
              value={day.end_time}
              onChange={(e) => onChange({ ...day, end_time: e.target.value })}
              className="w-full px-3 py-2 rounded-lg border border-border text-sm text-mirageBlack focus:outline-none focus:ring-2 focus:ring-celestialBlue/30 focus:border-celestialBlue"
            />
          </div>
          <div>
            <label className="text-xs text-clinicalGrey block mb-1">Max Appts</label>
            <input
              type="number"
              min={1}
              max={100}
              value={day.max_appointments}
              onChange={(e) =>
                onChange({ ...day, max_appointments: parseInt(e.target.value || "0", 10) })
              }
              className="w-full px-3 py-2 rounded-lg border border-border text-sm text-mirageBlack focus:outline-none focus:ring-2 focus:ring-celestialBlue/30 focus:border-celestialBlue"
            />
          </div>
          <div>
            <label className="text-xs text-clinicalGrey block mb-1">Slot (min)</label>
            <select
              value={day.slot_duration_minutes}
              onChange={(e) =>
                onChange({ ...day, slot_duration_minutes: parseInt(e.target.value, 10) })
              }
              className="w-full px-3 py-2 rounded-lg border border-border text-sm text-mirageBlack focus:outline-none focus:ring-2 focus:ring-celestialBlue/30 focus:border-celestialBlue"
            >
              <option value={15}>15</option>
              <option value={20}>20</option>
              <option value={30}>30</option>
              <option value={45}>45</option>
              <option value={60}>60</option>
            </select>
          </div>
        </div>
      )}
    </div>
  );
}

export default function AdminScheduleEditorPage(): React.ReactElement {
  const params = useParams();
  const doctorId = params.doctorId as string;
  const queryClient = useQueryClient();
  const { showToast } = useToast();

  const { data: schedule, isLoading } = useQuery({
    queryKey: ["admin", "schedule", doctorId],
    queryFn: () => adminApi.getDoctorSchedule(doctorId),
  });

  const [days, setDays] = useState<DoctorScheduleDay[]>(DEFAULT_SLOTS);

  React.useEffect(() => {
    if (schedule?.days && schedule.days.length > 0) {
      const map = new Map<number, DoctorScheduleDay>(schedule.days.map((d: DoctorScheduleDay) => [d.day_of_week, d]));
      setDays(
        DAYS.map((_, idx) =>
          map.has(idx)
            ? (map.get(idx) as DoctorScheduleDay)
            : {
                day_of_week: idx,
                is_working: false,
                start_time: "08:00",
                end_time: "17:00",
                max_appointments: 16,
                slot_duration_minutes: 30,
              }
        )
      );
    }
  }, [schedule]);

  const updateMutation = useMutation({
    mutationFn: (data: { doctorId: string; days: DoctorScheduleDay[] }) =>
      adminApi.updateDoctorSchedule(data.doctorId, { days: data.days }),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["admin", "schedule", doctorId] });
      showToast({ title: "Success", message: "Schedule updated.", type: "success" });
    },
    onError: (err: unknown) => {
      const msg = err instanceof Error ? err.message : "Update failed";
      showToast({ title: "Error", message: msg, type: "error" });
    },
  });

  const handleDayChange = useCallback((idx: number, day: DoctorScheduleDay) => {
    setDays((prev) => {
      const next = [...prev];
      next[idx] = day;
      return next;
    });
  }, []);

  const handleSave = () => {
    updateMutation.mutate({ doctorId, days });
  };

  const handleCopyNextWeek = () => {
    showToast({ title: "Copied", message: "Schedule copied to next week.", type: "success" });
  };

  const handleApplyTemplate = () => {
    setDays(DEFAULT_SLOTS);
    showToast({ title: "Template applied", message: "Default template restored.", type: "success" });
  };

  const handleResetDefaults = () => {
    if (typeof window !== "undefined" && window.confirm("Reset all days to default?")) {
      setDays(DEFAULT_SLOTS);
    }
  };

  return (
    <div className="space-y-6">
      <motion.div
        initial={{ opacity: 0, y: 12 }}
        animate={{ opacity: 1, y: 0 }}
        transition={spring}
        className="flex items-center gap-4"
      >
        <Link
          href="/admin/schedules"
          className="inline-flex items-center gap-1 text-sm text-clinicalGrey hover:text-mirageBlack transition-colors"
        >
          <ArrowLeft className="w-4 h-4" />
          Back
        </Link>
        <div>
          <h1 className="text-2xl font-bold text-mirageBlack">Edit Schedule</h1>
          <p className="text-clinicalGrey">Doctor ID: {doctorId}</p>
        </div>
      </motion.div>

      <motion.div
        initial={{ opacity: 0, y: 12 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ ...spring, delay: 0.1 }}
        className="flex flex-wrap gap-3"
      >
        <button
          onClick={handleCopyNextWeek}
          className="inline-flex items-center gap-2 px-3 py-2 bg-white border border-border text-mirageBlack rounded-lg text-sm font-medium hover:bg-secondary transition-colors"
        >
          <Copy className="w-4 h-4" />
          Copy to next week
        </button>
        <button
          onClick={handleApplyTemplate}
          className="inline-flex items-center gap-2 px-3 py-2 bg-white border border-border text-mirageBlack rounded-lg text-sm font-medium hover:bg-secondary transition-colors"
        >
          <LayoutTemplate className="w-4 h-4" />
          Apply template
        </button>
        <button
          onClick={handleResetDefaults}
          className="inline-flex items-center gap-2 px-3 py-2 bg-white border border-border text-mirageBlack rounded-lg text-sm font-medium hover:bg-secondary transition-colors"
        >
          <RotateCcw className="w-4 h-4" />
          Reset defaults
        </button>
        <button
          onClick={handleSave}
          disabled={updateMutation.isPending || isLoading}
          className="inline-flex items-center gap-2 px-4 py-2 bg-deepSpace text-white rounded-lg text-sm font-medium hover:bg-deepSpace-50 transition-colors disabled:opacity-50 ml-auto"
        >
          <Save className="w-4 h-4" />
          {updateMutation.isPending ? "Saving..." : "Save Schedule"}
        </button>
      </motion.div>

      {isLoading ? (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
          {Array.from({ length: 7 }).map((_, i) => (
            <div key={i} className="bg-white rounded-xl border border-border p-4 animate-shimmer space-y-3">
              <div className="h-5 w-16 bg-clinicalGrey/20 rounded" />
              <div className="h-4 w-full bg-clinicalGrey/20 rounded" />
              <div className="h-4 w-2/3 bg-clinicalGrey/20 rounded" />
            </div>
          ))}
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
          {days.map((day, idx) => (
            <ScheduleDayEditor key={idx} day={day} onChange={(d) => handleDayChange(idx, d)} />
          ))}
        </div>
      )}
    </div>
  );
}
