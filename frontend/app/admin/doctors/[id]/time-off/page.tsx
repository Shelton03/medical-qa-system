"use client";

import React, { useState } from "react";
import { motion } from "framer-motion";
import Link from "next/link";
import { useParams } from "next/navigation";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { ArrowLeft, CalendarPlus, Check, X } from "lucide-react";
import { adminApi } from "@/lib/api";
import type { TimeOffAdminRequest } from "@/lib/types";
import { useToast } from "@/hooks/useToast";

const spring = { type: "spring", stiffness: 380, damping: 32 };

const LEAVE_TYPES = ["LEAVE", "SICK", "TRAINING", "OTHER"] as const;

function getDaysInMonth(year: number, month: number): number {
  return new Date(year, month + 1, 0).getDate();
}

function getFirstDayOfMonth(year: number, month: number): number {
  return new Date(year, month, 1).getDay();
}

export default function AdminDoctorTimeOffPage(): React.ReactElement {
  const params = useParams();
  const doctorId = params.id as string;
  const queryClient = useQueryClient();
  const { showToast } = useToast();

  const today = new Date();
  const [viewYear, setViewYear] = useState(today.getFullYear());
  const [viewMonth, setViewMonth] = useState(today.getMonth());

  const { data: timeOffList, isLoading } = useQuery({
    queryKey: ["admin", "time-off", doctorId],
    queryFn: () => adminApi.listDoctorTimeOff(doctorId),
  });

  const addMutation = useMutation({
    mutationFn: (data: TimeOffAdminRequest) => adminApi.addTimeOff(doctorId, data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["admin", "time-off", doctorId] });
      showToast({ title: "Success", message: "Leave request added.", type: "success" });
    },
    onError: (err: unknown) => {
      const msg = err instanceof Error ? err.message : "Failed to add leave";
      showToast({ title: "Error", message: msg, type: "error" });
    },
  });

  const approveMutation = useMutation({
    mutationFn: (id: string) => adminApi.approveTimeOff(id),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["admin", "time-off", doctorId] });
      showToast({ title: "Approved", message: "Leave approved.", type: "success" });
    },
    onError: (err: unknown) => {
      const msg = err instanceof Error ? err.message : "Failed";
      showToast({ title: "Error", message: msg, type: "error" });
    },
  });

  const rejectMutation = useMutation({
    mutationFn: (id: string) => adminApi.rejectTimeOff(id),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["admin", "time-off", doctorId] });
      showToast({ title: "Rejected", message: "Leave rejected.", type: "success" });
    },
    onError: (err: unknown) => {
      const msg = err instanceof Error ? err.message : "Failed";
      showToast({ title: "Error", message: msg, type: "error" });
    },
  });

  const [form, setForm] = useState<TimeOffAdminRequest>({
    start_date: "",
    end_date: "",
    type: "LEAVE",
    reason: "",
  });

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    addMutation.mutate(form);
  };

  // Calendar helpers
  const daysInMonth = getDaysInMonth(viewYear, viewMonth);
  const firstDay = getFirstDayOfMonth(viewYear, viewMonth);

  const dayCells = Array.from({ length: firstDay }, () => null as number | null).concat(
    Array.from({ length: daysInMonth }, (_, i) => i + 1)
  );

  const monthName = new Date(viewYear, viewMonth).toLocaleString("default", { month: "long" });

  const isLeaveDay = (day: number): { status: "approved" | "pending"; type: string } | null => {
    const dateStr = `${viewYear}-${String(viewMonth + 1).padStart(2, "0")}-${String(day).padStart(2, "0")}`;
    for (const entry of timeOffList ?? []) {
      if (entry.start_date <= dateStr && entry.end_date >= dateStr) {
        return { status: entry.status as "approved" | "pending", type: entry.type };
      }
    }
    return null;
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
          href="/admin/doctors"
          className="inline-flex items-center gap-1 text-sm text-clinicalGrey hover:text-mirageBlack transition-colors"
        >
          <ArrowLeft className="w-4 h-4" />
          Back
        </Link>
        <div>
          <h1 className="text-2xl font-bold text-mirageBlack">Time Off</h1>
          <p className="text-clinicalGrey">Doctor ID: {doctorId}</p>
        </div>
      </motion.div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Calendar */}
        <motion.div
          initial={{ opacity: 0, y: 12 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ ...spring, delay: 0.1 }}
          className="lg:col-span-2 bg-white rounded-xl border border-border p-5"
        >
          <div className="flex items-center justify-between mb-4">
            <h2 className="font-semibold text-mirageBlack">
              {monthName} {viewYear}
            </h2>
            <div className="flex gap-2">
              <button
                onClick={() => {
                  if (viewMonth === 0) {
                    setViewMonth(11);
                    setViewYear((y) => y - 1);
                  } else {
                    setViewMonth((m) => m - 1);
                  }
                }}
                className="px-2 py-1 rounded-md border border-border text-sm text-mirageBlack hover:bg-secondary"
              >
                Prev
              </button>
              <button
                onClick={() => {
                  if (viewMonth === 11) {
                    setViewMonth(0);
                    setViewYear((y) => y + 1);
                  } else {
                    setViewMonth((m) => m + 1);
                  }
                }}
                className="px-2 py-1 rounded-md border border-border text-sm text-mirageBlack hover:bg-secondary"
              >
                Next
              </button>
            </div>
          </div>

          <div className="grid grid-cols-7 gap-1 text-center mb-2">
            {["Su", "Mo", "Tu", "We", "Th", "Fr", "Sa"].map((d) => (
              <div key={d} className="text-xs font-medium text-clinicalGrey py-1">
                {d}
              </div>
            ))}
          </div>
          <div className="grid grid-cols-7 gap-1">
            {dayCells.map((day, idx) => {
              if (day === null) return <div key={idx} />;
              const leave = isLeaveDay(day);
              const isToday =
                today.getDate() === day &&
                today.getMonth() === viewMonth &&
                today.getFullYear() === viewYear;
              return (
                <div
                  key={idx}
                  className={`
                    aspect-square flex items-center justify-center rounded-lg text-sm font-medium
                    ${isToday ? "ring-2 ring-celestialBlue" : ""}
                    ${leave?.status === "approved" ? "bg-alertOrange/10 text-alertOrange" : ""}
                    ${leave?.status === "pending" ? "bg-alertOrange/5 text-alertOrange border border-alertOrange/20" : ""}
                    ${!leave ? "text-mirageBlack hover:bg-secondary" : ""}
                  `}
                  title={leave ? `${leave.type} (${leave.status})` : undefined}
                >
                  {day}
                </div>
              );
            })}
          </div>

          <div className="flex items-center gap-4 mt-4 text-xs">
            <div className="flex items-center gap-1.5">
              <span className="w-3 h-3 rounded-sm bg-alertOrange/20 border border-alertOrange/40" />
              <span className="text-clinicalGrey">Approved</span>
            </div>
            <div className="flex items-center gap-1.5">
              <span className="w-3 h-3 rounded-sm bg-alertOrange/5 border border-alertOrange/20" />
              <span className="text-clinicalGrey">Pending</span>
            </div>
          </div>
        </motion.div>

        {/* Add leave form */}
        <motion.div
          initial={{ opacity: 0, y: 12 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ ...spring, delay: 0.15 }}
          className="bg-white rounded-xl border border-border p-5"
        >
          <h2 className="font-semibold text-mirageBlack mb-4 flex items-center gap-2">
            <CalendarPlus className="w-4 h-4" />
            Add Leave
          </h2>
          <form onSubmit={handleSubmit} className="space-y-3">
            <div>
              <label className="text-xs text-clinicalGrey block mb-1">Start Date</label>
              <input
                type="date"
                required
                value={form.start_date}
                onChange={(e) => setForm((f) => ({ ...f, start_date: e.target.value }))}
                className="w-full px-3 py-2 rounded-lg border border-border text-sm text-mirageBlack focus:outline-none focus:ring-2 focus:ring-celestialBlue/30 focus:border-celestialBlue"
              />
            </div>
            <div>
              <label className="text-xs text-clinicalGrey block mb-1">End Date</label>
              <input
                type="date"
                required
                value={form.end_date}
                onChange={(e) => setForm((f) => ({ ...f, end_date: e.target.value }))}
                className="w-full px-3 py-2 rounded-lg border border-border text-sm text-mirageBlack focus:outline-none focus:ring-2 focus:ring-celestialBlue/30 focus:border-celestialBlue"
              />
            </div>
            <div>
              <label className="text-xs text-clinicalGrey block mb-1">Type</label>
              <select
                value={form.type}
                onChange={(e) => setForm((f) => ({ ...f, type: e.target.value as typeof LEAVE_TYPES[number] }))}
                className="w-full px-3 py-2 rounded-lg border border-border text-sm text-mirageBlack focus:outline-none focus:ring-2 focus:ring-celestialBlue/30 focus:border-celestialBlue"
              >
                {LEAVE_TYPES.map((t) => (
                  <option key={t} value={t}>
                    {t}
                  </option>
                ))}
              </select>
            </div>
            <div>
              <label className="text-xs text-clinicalGrey block mb-1">Reason</label>
              <textarea
                rows={3}
                value={form.reason}
                onChange={(e) => setForm((f) => ({ ...f, reason: e.target.value }))}
                className="w-full px-3 py-2 rounded-lg border border-border text-sm text-mirageBlack focus:outline-none focus:ring-2 focus:ring-celestialBlue/30 focus:border-celestialBlue resize-none"
                placeholder="Enter reason..."
              />
            </div>
            <button
              type="submit"
              disabled={addMutation.isPending}
              className="w-full py-2 bg-deepSpace text-white rounded-lg text-sm font-medium hover:bg-deepSpace-50 transition-colors disabled:opacity-50"
            >
              {addMutation.isPending ? "Submitting..." : "Submit Leave"}
            </button>
          </form>
        </motion.div>
      </div>

      {/* Pending requests */}
      <motion.div
        initial={{ opacity: 0, y: 12 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ ...spring, delay: 0.2 }}
        className="bg-white rounded-xl border border-border p-5"
      >
        <h2 className="font-semibold text-mirageBlack mb-4">Leave Requests</h2>
        {isLoading ? (
          <div className="space-y-3">
            {Array.from({ length: 3 }).map((_, i) => (
              <div key={i} className="animate-shimmer h-12 bg-stellarWhite rounded-lg" />
            ))}
          </div>
        ) : timeOffList && timeOffList.length > 0 ? (
          <div className="space-y-3">
            {timeOffList.map((entry) => (
              <div
                key={entry.id}
                className="flex items-center justify-between p-3 bg-stellarWhite rounded-lg border border-border"
              >
                <div>
                  <p className="text-sm font-medium text-mirageBlack">
                    {entry.start_date} – {entry.end_date}
                  </p>
                  <p className="text-xs text-clinicalGrey">
                    {entry.type} &middot; {entry.reason || "No reason"} &middot; {entry.doctor_name}
                  </p>
                </div>
                <div className="flex items-center gap-2">
                  {entry.status === "pending" ? (
                    <>
                      <button
                        onClick={() => approveMutation.mutate(entry.id)}
                        disabled={approveMutation.isPending}
                        className="inline-flex items-center gap-1 px-3 py-1.5 bg-healthGreen/10 text-healthGreen rounded-lg text-xs font-medium hover:bg-healthGreen/20 transition-colors"
                      >
                        <Check className="w-3.5 h-3.5" />
                        Approve
                      </button>
                      <button
                        onClick={() => rejectMutation.mutate(entry.id)}
                        disabled={rejectMutation.isPending}
                        className="inline-flex items-center gap-1 px-3 py-1.5 bg-alertOrange/10 text-alertOrange rounded-lg text-xs font-medium hover:bg-alertOrange/20 transition-colors"
                      >
                        <X className="w-3.5 h-3.5" />
                        Reject
                      </button>
                    </>
                  ) : (
                    <span
                      className={`text-xs px-2 py-1 rounded-full font-medium ${
                        entry.status === "approved"
                          ? "bg-healthGreen/10 text-healthGreen"
                          : "bg-clinicalGrey/10 text-clinicalGrey"
                      }`}
                    >
                      {entry.status}
                    </span>
                  )}
                </div>
              </div>
            ))}
          </div>
        ) : (
          <p className="text-sm text-clinicalGrey">No leave requests.</p>
        )}
      </motion.div>
    </div>
  );
}
