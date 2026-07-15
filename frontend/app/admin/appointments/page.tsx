"use client";

import React, { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import Link from "next/link";
import { useQuery } from "@tanstack/react-query";
import {
  CalendarCheck,
  Filter,
  Search,
  ChevronLeft,
  ChevronRight,
  X,
  AlertTriangle,
  Stethoscope,
} from "lucide-react";
import { adminApi } from "@/lib/api";
import type { AppointmentAdminItem, AppointmentAdminFilters } from "@/lib/types";
import { cn } from "@/lib/utils";
import { useToast } from "@/hooks/useToast";

const spring = { type: "spring", stiffness: 380, damping: 32 };

const statusStyles: Record<string, string> = {
  PENDING: "bg-alertOrange/10 text-alertOrange border-alertOrange/20",
  CONFIRMED: "bg-celestialBlue/10 text-celestialBlue border-celestialBlue/20",
  COMPLETED: "bg-healthGreen/10 text-healthGreen border-healthGreen/20",
  CANCELLED: "bg-clinicalGrey/10 text-clinicalGrey border-clinicalGrey/20",
};

const priorityStyles: Record<string, string> = {
  EMERGENCY: "bg-[#EF4444]/10 text-[#EF4444] border-[#EF4444]/20",
  URGENT: "bg-alertOrange/10 text-alertOrange border-alertOrange/20",
  NORMAL: "bg-celestialBlue/10 text-celestialBlue border-celestialBlue/20",
  LOW: "bg-clinicalGrey/10 text-clinicalGrey border-clinicalGrey/20",
};

export default function AdminAppointmentsPage(): React.ReactElement {
  const { showToast } = useToast();
  const [filters, setFilters] = useState<AppointmentAdminFilters>({
    page: 1,
    page_size: 20,
  });
  const [showFilters, setShowFilters] = useState(false);

  const { data, isLoading } = useQuery({
    queryKey: ["admin", "appointments", filters],
    queryFn: () => adminApi.listAppointments(filters),
  });

  const appointments = data?.items ?? [];
  const totalPages = data?.total_pages ?? 1;

  return (
    <div className="space-y-6">
      <motion.div initial={{ opacity: 0, y: 12 }} animate={{ opacity: 1, y: 0 }} transition={spring}>
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-2xl font-bold text-mirageBlack">Appointments</h1>
            <p className="text-clinicalGrey">View and manage all appointments</p>
          </div>
          <button
            onClick={() => setShowFilters(!showFilters)}
            className="inline-flex items-center gap-2 px-3 py-2 bg-white border border-border text-mirageBlack rounded-lg text-sm font-medium hover:bg-secondary transition-colors"
          >
            <Filter className="w-4 h-4" />
            Filters
          </button>
        </div>
      </motion.div>

      {/* Filters */}
      <AnimatePresence>
        {showFilters && (
          <motion.div
            initial={{ opacity: 0, height: 0 }}
            animate={{ opacity: 1, height: "auto" }}
            exit={{ opacity: 0, height: 0 }}
            className="bg-white rounded-xl border border-border p-4 space-y-3"
          >
            <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
              <div>
                <label className="text-xs text-clinicalGrey block mb-1">Status</label>
                <select
                  value={filters.status ?? ""}
                  onChange={(e) =>
                    setFilters((f) => ({ ...f, status: e.target.value || undefined, page: 1 }))
                  }
                  className="w-full px-3 py-2 rounded-lg border border-border text-sm text-mirageBlack focus:outline-none focus:ring-2 focus:ring-celestialBlue/30"
                >
                  <option value="">All</option>
                  <option value="PENDING">Pending</option>
                  <option value="CONFIRMED">Confirmed</option>
                  <option value="COMPLETED">Completed</option>
                  <option value="CANCELLED">Cancelled</option>
                </select>
              </div>
              <div>
                <label className="text-xs text-clinicalGrey block mb-1">Priority</label>
                <select
                  value={filters.priority ?? ""}
                  onChange={(e) =>
                    setFilters((f) => ({ ...f, priority: e.target.value || undefined, page: 1 }))
                  }
                  className="w-full px-3 py-2 rounded-lg border border-border text-sm text-mirageBlack focus:outline-none focus:ring-2 focus:ring-celestialBlue/30"
                >
                  <option value="">All</option>
                  <option value="EMERGENCY">Emergency</option>
                  <option value="URGENT">Urgent</option>
                  <option value="NORMAL">Normal</option>
                  <option value="LOW">Low</option>
                </select>
              </div>
              <div>
                <label className="text-xs text-clinicalGrey block mb-1">Search</label>
                <div className="relative">
                  <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-clinicalGrey" />
                  <input
                    type="text"
                    placeholder="Patient or doctor..."
                    value={filters.patient_search ?? ""}
                    onChange={(e) =>
                      setFilters((f) => ({
                        ...f,
                        patient_search: e.target.value || undefined,
                        page: 1,
                      }))
                    }
                    className="w-full pl-9 pr-4 py-2 rounded-lg border border-border text-sm text-mirageBlack focus:outline-none focus:ring-2 focus:ring-celestialBlue/30"
                  />
                </div>
              </div>
            </div>
            <div className="flex gap-3">
              <div>
                <label className="text-xs text-clinicalGrey block mb-1">From</label>
                <input
                  type="date"
                  value={filters.date_from ?? ""}
                  onChange={(e) =>
                    setFilters((f) => ({ ...f, date_from: e.target.value || undefined, page: 1 }))
                  }
                  className="px-3 py-2 rounded-lg border border-border text-sm text-mirageBlack focus:outline-none focus:ring-2 focus:ring-celestialBlue/30"
                />
              </div>
              <div>
                <label className="text-xs text-clinicalGrey block mb-1">To</label>
                <input
                  type="date"
                  value={filters.date_to ?? ""}
                  onChange={(e) =>
                    setFilters((f) => ({ ...f, date_to: e.target.value || undefined, page: 1 }))
                  }
                  className="px-3 py-2 rounded-lg border border-border text-sm text-mirageBlack focus:outline-none focus:ring-2 focus:ring-celestialBlue/30"
                />
              </div>
              <div className="flex items-end">
                <button
                  onClick={() =>
                    setFilters({ page: 1, page_size: 20 })
                  }
                  className="px-3 py-2 text-sm text-clinicalGrey hover:text-mirageBlack transition-colors"
                >
                  Clear all
                </button>
              </div>
            </div>
          </motion.div>
        )}
      </AnimatePresence>

      {/* Table */}
      <motion.div
        initial={{ opacity: 0, y: 12 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ ...spring, delay: 0.1 }}
        className="bg-white rounded-xl border border-border overflow-hidden"
      >
        <div className="overflow-x-auto">
          <table className="w-full text-sm text-left">
            <thead className="text-xs text-clinicalGrey uppercase bg-stellarWhite border-b border-border">
              <tr>
                <th className="px-6 py-3">Date/Time</th>
                <th className="px-6 py-3">Patient</th>
                <th className="px-6 py-3">Doctor</th>
                <th className="px-6 py-3">Facility</th>
                <th className="px-6 py-3">Status</th>
                <th className="px-6 py-3">Priority</th>
                <th className="px-6 py-3">Reason</th>
              </tr>
            </thead>
            <tbody>
              {isLoading ? (
                Array.from({ length: 5 }).map((_, i) => (
                  <tr key={i} className="border-b border-border animate-shimmer">
                    <td className="px-6 py-4"><div className="h-4 w-24 bg-clinicalGrey/20 rounded" /></td>
                    <td className="px-6 py-4"><div className="h-4 w-20 bg-clinicalGrey/20 rounded" /></td>
                    <td className="px-6 py-4"><div className="h-4 w-20 bg-clinicalGrey/20 rounded" /></td>
                    <td className="px-6 py-4"><div className="h-4 w-24 bg-clinicalGrey/20 rounded" /></td>
                    <td className="px-6 py-4"><div className="h-4 w-16 bg-clinicalGrey/20 rounded" /></td>
                    <td className="px-6 py-4"><div className="h-4 w-16 bg-clinicalGrey/20 rounded" /></td>
                    <td className="px-6 py-4"><div className="h-4 w-32 bg-clinicalGrey/20 rounded" /></td>
                  </tr>
                ))
              ) : appointments.length > 0 ? (
                appointments.map((appt: AppointmentAdminItem) => (
                  <tr key={appt.id} className="border-b border-border hover:bg-stellarWhite/50 transition-colors">
                    <td className="px-6 py-4 whitespace-nowrap">
                      <p className="text-mirageBlack font-medium">
                        {new Date(appt.date_time).toLocaleDateString()}
                      </p>
                      <p className="text-xs text-clinicalGrey">
                        {new Date(appt.date_time).toLocaleTimeString([], {
                          hour: "2-digit",
                          minute: "2-digit",
                        })}
                      </p>
                    </td>
                    <td className="px-6 py-4 text-mirageBlack">{appt.patient_name}</td>
                    <td className="px-6 py-4 text-mirageBlack">{appt.doctor_name}</td>
                    <td className="px-6 py-4 text-clinicalGrey">{appt.facility_name}</td>
                    <td className="px-6 py-4">
                      <span
                        className={cn(
                          "px-2 py-0.5 rounded-full border text-micro font-medium",
                          statusStyles[appt.status] ?? "bg-clinicalGrey/10 text-clinicalGrey"
                        )}
                      >
                        {appt.status}
                      </span>
                    </td>
                    <td className="px-6 py-4">
                      <span
                        className={cn(
                          "px-2 py-0.5 rounded-full border text-micro font-medium",
                          priorityStyles[appt.priority] ?? "bg-clinicalGrey/10 text-clinicalGrey"
                        )}
                      >
                        {appt.priority}
                      </span>
                    </td>
                    <td className="px-6 py-4 text-clinicalGrey truncate max-w-[200px]">
                      {appt.reason || "—"}
                    </td>
                  </tr>
                ))
              ) : (
                <tr>
                  <td colSpan={7} className="px-6 py-12 text-center text-clinicalGrey">
                    No appointments found.
                  </td>
                </tr>
              )}
            </tbody>
          </table>
        </div>

        {/* Pagination */}
        {totalPages > 1 && (
          <div className="flex items-center justify-between px-6 py-4 border-t border-border">
            <p className="text-xs text-clinicalGrey">
              Page {filters.page} of {totalPages}
            </p>
            <div className="flex gap-2">
              <button
                onClick={() => setFilters((f) => ({ ...f, page: Math.max(1, (f.page ?? 1) - 1) }))}
                disabled={(filters.page ?? 1) <= 1}
                className="px-3 py-1.5 border border-border rounded-lg text-sm text-mirageBlack hover:bg-secondary transition-colors disabled:opacity-50"
              >
                <ChevronLeft className="w-4 h-4" />
              </button>
              <button
                onClick={() => setFilters((f) => ({ ...f, page: Math.min(totalPages, (f.page ?? 1) + 1) }))}
                disabled={(filters.page ?? 1) >= totalPages}
                className="px-3 py-1.5 border border-border rounded-lg text-sm text-mirageBlack hover:bg-secondary transition-colors disabled:opacity-50"
              >
                <ChevronRight className="w-4 h-4" />
              </button>
            </div>
          </div>
        )}
      </motion.div>
    </div>
  );
}
