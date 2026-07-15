"use client";

import React, { useState } from "react";
import { motion } from "framer-motion";
import Link from "next/link";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import {
  ArrowLeft,
  Clock,
  CalendarDays,
  Users,
  Timer,
  CalendarPlus,
} from "lucide-react";
import { useMySchedule } from "@/hooks/useSchedule";
import { scheduleApi } from "@/lib/api";
import type { TimeOffRequest, DoctorScheduleDay, TimeOffResponse } from "@/lib/types";
import { useToast } from "@/hooks/useToast";
import { LoadingSkeleton } from "@/components/ui/LoadingSkeleton";
import { cn } from "@/lib/utils";

const spring = { type: "spring", stiffness: 380, damping: 32 };
const DAYS = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"];

export default function DoctorAvailabilityPage(): React.ReactElement {
  const { showToast } = useToast();
  const queryClient = useQueryClient();
  const { data: schedule, isLoading } = useMySchedule();

  const [showLeaveForm, setShowLeaveForm] = useState(false);
  const [leaveForm, setLeaveForm] = useState<TimeOffRequest>({
    start_date: "",
    end_date: "",
    type: "LEAVE",
    reason: "",
  });

  const requestLeaveMutation = useMutation({
    mutationFn: (data: TimeOffRequest) => scheduleApi.requestLeave(data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["doctor", "schedule"] });
      setShowLeaveForm(false);
      setLeaveForm({ start_date: "", end_date: "", type: "LEAVE", reason: "" });
      showToast({ title: "Success", message: "Leave request submitted.", type: "success" });
    },
    onError: (err: unknown) => {
      const msg = err instanceof Error ? err.message : "Failed to submit leave request";
      showToast({ title: "Error", message: msg, type: "error" });
    },
  });

  const handleSubmitLeave = (e: React.FormEvent) => {
    e.preventDefault();
    requestLeaveMutation.mutate(leaveForm);
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
          href="/doctor/schedule"
          className="inline-flex items-center gap-1 text-sm text-clinicalGrey hover:text-mirageBlack transition-colors"
        >
          <ArrowLeft className="w-4 h-4" />
          Back
        </Link>
        <div>
          <h1 className="text-2xl font-bold text-mirageBlack">Availability</h1>
          <p className="text-clinicalGrey">Your schedule settings and leave requests</p>
        </div>
      </motion.div>

      {isLoading ? (
        <LoadingSkeleton type="card" count={2} />
      ) : (
        <>
          {/* Schedule Overview */}
          <motion.div
            initial={{ opacity: 0, y: 12 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ ...spring, delay: 0.1 }}
            className="bg-white rounded-xl border border-border p-5"
          >
            <h2 className="font-semibold text-mirageBlack mb-4 flex items-center gap-2">
              <Clock className="w-4 h-4" />
              Weekly Schedule
            </h2>
            <div className="space-y-3">
              {schedule?.days?.map((day: DoctorScheduleDay) => (
                <div
                  key={day.day_of_week}
                  className={cn(
                    "flex items-center justify-between p-3 rounded-lg border",
                    day.is_working
                      ? "bg-stellarWhite border-border"
                      : "bg-clinicalGrey/5 border-border/50"
                  )}
                >
                  <div className="flex items-center gap-3">
                    <div
                      className={cn(
                        "w-2 h-2 rounded-full",
                        day.is_working ? "bg-healthGreen" : "bg-clinicalGrey/40"
                      )}
                    />
                    <span className="text-sm font-medium text-mirageBlack w-24">
                      {DAYS[day.day_of_week]}
                    </span>
                  </div>
                  <div className="flex items-center gap-4 text-sm text-clinicalGrey">
                    {day.is_working ? (
                      <>
                        <span className="flex items-center gap-1">
                          <Clock className="w-3.5 h-3.5" />
                          {day.start_time} – {day.end_time}
                        </span>
                        <span className="flex items-center gap-1">
                          <Users className="w-3.5 h-3.5" />
                          Max {day.max_appointments} appts
                        </span>
                        <span className="flex items-center gap-1">
                          <Timer className="w-3.5 h-3.5" />
                          {day.slot_duration_minutes} min slots
                        </span>
                      </>
                    ) : (
                      <span className="text-clinicalGrey/60 italic">Off</span>
                    )}
                  </div>
                </div>
              )) ?? (
                <p className="text-sm text-clinicalGrey">No schedule configured.</p>
              )}
            </div>
            <div className="mt-4 p-3 bg-celestialBlue/5 rounded-lg border border-celestialBlue/20">
              <p className="text-xs text-celestialBlue">
                Your schedule is managed by the administration team. Contact them if you need changes.
              </p>
            </div>
          </motion.div>

          {/* Leave Request Section */}
          <motion.div
            initial={{ opacity: 0, y: 12 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ ...spring, delay: 0.2 }}
            className="bg-white rounded-xl border border-border p-5"
          >
            <div className="flex items-center justify-between mb-4">
              <h2 className="font-semibold text-mirageBlack flex items-center gap-2">
                <CalendarPlus className="w-4 h-4" />
                Request Leave
              </h2>
              <button
                onClick={() => setShowLeaveForm(!showLeaveForm)}
                className="px-3 py-1.5 bg-deepSpace text-white rounded-lg text-sm font-medium hover:bg-deepSpace-50 transition-colors"
              >
                {showLeaveForm ? "Cancel" : "New Request"}
              </button>
            </div>

            {showLeaveForm && (
              <motion.form
                initial={{ opacity: 0, height: 0 }}
                animate={{ opacity: 1, height: "auto" }}
                exit={{ opacity: 0, height: 0 }}
                onSubmit={handleSubmitLeave}
                className="space-y-3 border-t border-border pt-4 mt-4"
              >
                <div className="grid grid-cols-2 gap-3">
                  <div>
                    <label className="text-xs text-clinicalGrey block mb-1">Start Date</label>
                    <input
                      type="date"
                      required
                      value={leaveForm.start_date}
                      onChange={(e) =>
                        setLeaveForm((f) => ({ ...f, start_date: e.target.value }))
                      }
                      className="w-full px-3 py-2 rounded-lg border border-border text-sm text-mirageBlack focus:outline-none focus:ring-2 focus:ring-celestialBlue/30"
                    />
                  </div>
                  <div>
                    <label className="text-xs text-clinicalGrey block mb-1">End Date</label>
                    <input
                      type="date"
                      required
                      value={leaveForm.end_date}
                      onChange={(e) =>
                        setLeaveForm((f) => ({ ...f, end_date: e.target.value }))
                      }
                      className="w-full px-3 py-2 rounded-lg border border-border text-sm text-mirageBlack focus:outline-none focus:ring-2 focus:ring-celestialBlue/30"
                    />
                  </div>
                </div>
                <div>
                  <label className="text-xs text-clinicalGrey block mb-1">Type</label>
                  <select
                    value={leaveForm.type}
                    onChange={(e) =>
                      setLeaveForm((f) => ({ ...f, type: e.target.value as TimeOffRequest["type"] }))
                    }
                    className="w-full px-3 py-2 rounded-lg border border-border text-sm text-mirageBlack focus:outline-none focus:ring-2 focus:ring-celestialBlue/30"
                  >
                    <option value="LEAVE">Leave</option>
                    <option value="SICK">Sick</option>
                    <option value="TRAINING">Training</option>
                    <option value="OTHER">Other</option>
                  </select>
                </div>
                <div>
                  <label className="text-xs text-clinicalGrey block mb-1">Reason</label>
                  <textarea
                    rows={3}
                    value={leaveForm.reason}
                    onChange={(e) =>
                      setLeaveForm((f) => ({ ...f, reason: e.target.value }))
                    }
                    className="w-full px-3 py-2 rounded-lg border border-border text-sm text-mirageBlack focus:outline-none focus:ring-2 focus:ring-celestialBlue/30 resize-none"
                    placeholder="Enter reason for leave..."
                  />
                </div>
                <button
                  type="submit"
                  disabled={requestLeaveMutation.isPending}
                  className="w-full py-2.5 bg-deepSpace text-white rounded-lg text-sm font-medium hover:bg-deepSpace-50 transition-colors disabled:opacity-50"
                >
                  {requestLeaveMutation.isPending ? "Submitting..." : "Submit Leave Request"}
                </button>
              </motion.form>
            )}

            {/* Existing leave requests */}
            {schedule?.time_off_requests && schedule.time_off_requests.length > 0 && (
              <div className="mt-4 space-y-2">
                <h3 className="text-sm font-medium text-mirageBlack">Your Leave Requests</h3>
                {schedule.time_off_requests.map((req: TimeOffResponse) => (
                  <div
                    key={req.id}
                    className="flex items-center justify-between p-3 bg-stellarWhite rounded-lg border border-border"
                  >
                    <div>
                      <p className="text-sm text-mirageBlack">
                        {req.start_date} – {req.end_date}
                      </p>
                      <p className="text-xs text-clinicalGrey">
                        {req.type} · {req.reason || "No reason"}
                      </p>
                    </div>
                    <span
                      className={cn(
                        "px-2 py-0.5 rounded-full border text-micro font-medium",
                        req.status === "APPROVED"
                          ? "bg-healthGreen/10 text-healthGreen border-healthGreen/20"
                          : req.status === "PENDING"
                          ? "bg-alertOrange/10 text-alertOrange border-alertOrange/20"
                          : "bg-clinicalGrey/10 text-clinicalGrey border-clinicalGrey/20"
                      )}
                    >
                      {req.status}
                    </span>
                  </div>
                ))}
              </div>
            )}
          </motion.div>
        </>
      )}
    </div>
  );
}
