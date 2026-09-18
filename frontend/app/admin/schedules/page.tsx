"use client";

import React from "react";
import { motion } from "framer-motion";
import Link from "next/link";
import { useQuery } from "@tanstack/react-query";
import { CalendarDays, ChevronRight, Clock, MapPin } from "lucide-react";
import { adminApi } from "@/lib/api";

const spring = { type: "spring", stiffness: 380, damping: 32 };

export default function AdminSchedulesPage(): React.ReactElement {
  const { data: doctors, isLoading } = useQuery({
    queryKey: ["admin", "doctors"],
    queryFn: () => adminApi.listDoctors({ limit: 100 }),
  });

  return (
    <div className="space-y-6">
      <motion.div initial={{ opacity: 0, y: 12 }} animate={{ opacity: 1, y: 0 }} transition={spring}>
        <h1 className="text-2xl font-bold text-mirageBlack">Schedules</h1>
        <p className="text-clinicalGrey">Manage doctor weekly schedules</p>
      </motion.div>

      <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-4">
        {isLoading
          ? Array.from({ length: 6 }).map((_, i) => (
              <div key={i} className="bg-white rounded-xl border border-border p-5 animate-shimmer">
                <div className="h-5 w-1/2 bg-clinicalGrey/20 rounded mb-2" />
                <div className="h-4 w-1/3 bg-clinicalGrey/20 rounded mb-4" />
                <div className="space-y-2">
                  <div className="h-3 w-full bg-clinicalGrey/20 rounded" />
                  <div className="h-3 w-2/3 bg-clinicalGrey/20 rounded" />
                </div>
              </div>
            ))
          : doctors?.map((doctor, i) => (
              <motion.div
                key={doctor.id}
                initial={{ opacity: 0, y: 12 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ ...spring, delay: i * 0.04 }}
                className="bg-white rounded-xl border border-border p-5 hover:shadow-elevation-2 transition-shadow"
              >
                <div className="flex items-start justify-between mb-3">
                  <div>
                    <h3 className="font-semibold text-mirageBlack">
                      Dr. {doctor.first_name} {doctor.last_name}
                    </h3>
                    <p className="text-xs text-clinicalGrey flex items-center gap-1 mt-0.5">
                      <MapPin className="w-3 h-3" />
                      {doctor.facility_name}
                    </p>
                  </div>
                </div>
                <div className="space-y-2 mb-4">
                  <div className="flex items-center gap-2 text-sm text-clinicalGrey">
                    <CalendarDays className="w-4 h-4" />
                    <span>{doctor.working_days?.join(", ") ?? "—"}</span>
                  </div>
                  <div className="flex items-center gap-2 text-sm text-clinicalGrey">
                    <Clock className="w-4 h-4" />
                    <span>
                      {doctor.schedule_start_time} – {doctor.schedule_end_time}
                    </span>
                  </div>
                  <div className="text-sm text-clinicalGrey">
                    Specialty: <span className="text-mirageBlack font-medium">{doctor.specialty}</span>
                  </div>
                </div>
                <div className="flex gap-2">
                  <Link
                    href={`/admin/schedules/${doctor.id}`}
                    className="inline-flex items-center gap-1 px-3 py-1.5 bg-celestialBlue/10 text-celestialBlue rounded-lg text-xs font-medium hover:bg-celestialBlue/20 transition-colors"
                  >
                    Edit Schedule
                    <ChevronRight className="w-3 h-3" />
                  </Link>
                  <Link
                    href={`/admin/doctors/${doctor.id}/time-off`}
                    className="inline-flex items-center gap-1 px-3 py-1.5 bg-white border border-border text-mirageBlack rounded-lg text-xs font-medium hover:bg-secondary transition-colors"
                  >
                    Leave
                  </Link>
                </div>
              </motion.div>
            ))}
        {!isLoading && (!doctors || doctors.length === 0) && (
          <div className="col-span-full text-center text-clinicalGrey py-12">
            No doctors found.
          </div>
        )}
      </div>
    </div>
  );
}
