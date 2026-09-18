"use client";

import React from "react";
import { motion } from "framer-motion";
import Link from "next/link";
import { useQuery } from "@tanstack/react-query";
import { CalendarDays, ChevronRight, MapPin } from "lucide-react";
import { adminApi } from "@/lib/api";

const spring = { type: "spring", stiffness: 380, damping: 32 };

export default function AdminDoctorsPage(): React.ReactElement {
  const { data: doctors, isLoading } = useQuery({
    queryKey: ["admin", "doctors"],
    queryFn: () => adminApi.listDoctors({ limit: 100 }),
  });

  return (
    <div className="space-y-6">
      <motion.div initial={{ opacity: 0, y: 12 }} animate={{ opacity: 1, y: 0 }} transition={spring}>
        <h1 className="text-2xl font-bold text-mirageBlack">Doctors</h1>
        <p className="text-clinicalGrey">View and manage all practitioners</p>
      </motion.div>

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
                <th className="px-6 py-3">Name</th>
                <th className="px-6 py-3">Specialty</th>
                <th className="px-6 py-3">Facility</th>
                <th className="px-6 py-3">Working Days</th>
                <th className="px-6 py-3">Schedule</th>
                <th className="px-6 py-3 text-right">Actions</th>
              </tr>
            </thead>
            <tbody>
              {isLoading ? (
                Array.from({ length: 5 }).map((_, i) => (
                  <tr key={i} className="border-b border-border animate-shimmer">
                    <td className="px-6 py-4"><div className="h-4 w-24 bg-clinicalGrey/20 rounded" /></td>
                    <td className="px-6 py-4"><div className="h-4 w-20 bg-clinicalGrey/20 rounded" /></td>
                    <td className="px-6 py-4"><div className="h-4 w-28 bg-clinicalGrey/20 rounded" /></td>
                    <td className="px-6 py-4"><div className="h-4 w-32 bg-clinicalGrey/20 rounded" /></td>
                    <td className="px-6 py-4"><div className="h-4 w-16 bg-clinicalGrey/20 rounded" /></td>
                    <td className="px-6 py-4 text-right"><div className="h-4 w-16 bg-clinicalGrey/20 rounded ml-auto" /></td>
                  </tr>
                ))
              ) : doctors && doctors.length > 0 ? (
                doctors.map((doctor) => (
                  <tr key={doctor.id} className="border-b border-border hover:bg-stellarWhite/50 transition-colors">
                    <td className="px-6 py-4 font-medium text-mirageBlack whitespace-nowrap">
                      Dr. {doctor.first_name} {doctor.last_name}
                    </td>
                    <td className="px-6 py-4 text-clinicalGrey">{doctor.specialty}</td>
                    <td className="px-6 py-4 text-clinicalGrey">
                      <div className="flex items-center gap-1.5">
                        <MapPin className="w-3.5 h-3.5" />
                        {doctor.facility_name}
                      </div>
                    </td>
                    <td className="px-6 py-4 text-clinicalGrey">
                      {doctor.working_days?.slice(0, 3).join(", ") ?? "—"}
                      {doctor.working_days && doctor.working_days.length > 3 && (
                        <span className="text-xs text-clinicalGrey ml-1">+{doctor.working_days.length - 3} more</span>
                      )}
                    </td>
                    <td className="px-6 py-4 text-clinicalWhitespace whitespace-nowrap">
                      {doctor.schedule_start_time} – {doctor.schedule_end_time}
                    </td>
                    <td className="px-6 py-4 text-right">
                      <Link
                        href={`/admin/schedules/${doctor.id}`}
                        className="inline-flex items-center gap-1 text-xs text-celestialBlue hover:underline font-medium"
                      >
                        <CalendarDays className="w-3.5 h-3.5" />
                        Edit Schedule
                        <ChevronRight className="w-3 h-3" />
                      </Link>
                    </td>
                  </tr>
                ))
              ) : (
                <tr>
                  <td colSpan={6} className="px-6 py-8 text-center text-clinicalGrey">
                    No doctors found.
                  </td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
      </motion.div>
    </div>
  );
}
