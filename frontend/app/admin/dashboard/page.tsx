"use client";

import React from "react";
import { motion } from "framer-motion";
import Link from "next/link";
import { useQuery } from "@tanstack/react-query";
import { CalendarCheck, Clock, Users, Activity, CalendarDays, List, Plus } from "lucide-react";
import { adminApi } from "@/lib/api";

const spring = { type: "spring", stiffness: 380, damping: 32 };

function SkeletonCard() {
  return (
    <div className="bg-white rounded-xl border border-border p-4 animate-shimmer">
      <div className="flex items-center gap-3 mb-2">
        <div className="w-5 h-5 rounded bg-clinicalGrey/20" />
        <div className="w-20 h-3 rounded bg-clinicalGrey/20" />
      </div>
      <div className="w-12 h-8 rounded bg-clinicalGrey/20" />
    </div>
  );
}

export default function AdminDashboardPage(): React.ReactElement {
  const { data: stats, isLoading } = useQuery({
    queryKey: ["admin", "dashboard"],
    queryFn: () => adminApi.getDashboard(),
  });

  const cards = [
    {
      label: "Today's Appointments",
      value: stats?.total_appointments_today ?? 0,
      icon: CalendarCheck,
      color: "text-celestialBlue",
    },
    {
      label: "Pending Confirmations",
      value: stats?.pending_confirmations ?? 0,
      icon: Clock,
      color: "text-alertOrange",
    },
    {
      label: "Doctors on Leave",
      value: stats?.doctors_on_leave ?? 0,
      icon: Users,
      color: "text-healthGreen",
    },
    {
      label: "Facility Occupancy",
      value: stats?.facility_occupancy_rate != null ? `${stats.facility_occupancy_rate}%` : "—",
      icon: Activity,
      color: "text-clinicalGrey",
    },
  ];

  return (
    <div className="space-y-6">
      <motion.div
        initial={{ opacity: 0, y: 12 }}
        animate={{ opacity: 1, y: 0 }}
        transition={spring}
      >
        <h1 className="text-2xl font-bold text-mirageBlack">Dashboard</h1>
        <p className="text-clinicalGrey">Overview of the Mirage system</p>
      </motion.div>

      {/* Stats cards */}
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
        {isLoading
          ? Array.from({ length: 4 }).map((_, i) => <SkeletonCard key={i} />)
          : cards.map((stat, i) => (
              <motion.div
                key={stat.label}
                initial={{ opacity: 0, y: 12 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ ...spring, delay: i * 0.05 }}
                className="bg-white rounded-xl border border-border p-4"
              >
                <div className="flex items-center gap-3 mb-2">
                  <stat.icon className={`w-5 h-5 ${stat.color}`} />
                  <span className="text-xs text-clinicalGrey">{stat.label}</span>
                </div>
                <p className="text-2xl font-bold text-mirageBlack">{stat.value}</p>
              </motion.div>
            ))}
      </div>

      {/* Quick actions */}
      <motion.div
        initial={{ opacity: 0, y: 12 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ ...spring, delay: 0.2 }}
        className="flex flex-wrap gap-3"
      >
        <Link
          href="/admin/schedules"
          className="inline-flex items-center gap-2 px-4 py-2 bg-deepSpace text-white rounded-lg text-sm font-medium hover:bg-deepSpace-50 transition-colors"
        >
          <CalendarDays className="w-4 h-4" />
          Manage Schedules
        </Link>
        <Link
          href="/admin/appointments"
          className="inline-flex items-center gap-2 px-4 py-2 bg-white border border-border text-mirageBlack rounded-lg text-sm font-medium hover:bg-secondary transition-colors"
        >
          <List className="w-4 h-4" />
          View All Appointments
        </Link>
        <Link
          href="/admin/doctors"
          className="inline-flex items-center gap-2 px-4 py-2 bg-white border border-border text-mirageBlack rounded-lg text-sm font-medium hover:bg-secondary transition-colors"
        >
          <Plus className="w-4 h-4" />
          Add Doctor Leave
        </Link>
      </motion.div>

      {/* Recent activity */}
      <motion.div
        initial={{ opacity: 0, y: 12 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ ...spring, delay: 0.25 }}
        className="bg-white rounded-xl border border-border p-5"
      >
        <h2 className="font-semibold text-mirageBlack mb-4">Recent Activity</h2>
        {isLoading ? (
          <div className="space-y-3">
            {Array.from({ length: 4 }).map((_, i) => (
              <div key={i} className="flex items-center gap-3 p-3 bg-stellarWhite rounded-lg animate-shimmer">
                <div className="w-8 h-8 rounded-full bg-clinicalGrey/20" />
                <div className="flex-1 space-y-2">
                  <div className="w-1/2 h-3 rounded bg-clinicalGrey/20" />
                  <div className="w-1/3 h-2 rounded bg-clinicalGrey/20" />
                </div>
              </div>
            ))}
          </div>
        ) : stats?.recent_activity && stats.recent_activity.length > 0 ? (
          <div className="space-y-3">
            {stats.recent_activity.map((event) => (
              <div
                key={event.id}
                className="flex items-start gap-3 p-3 bg-stellarWhite rounded-lg"
              >
                <div className="w-2 h-2 rounded-full bg-celestialBlue mt-2 shrink-0" />
                <div className="flex-1 min-w-0">
                  <p className="text-sm text-mirageBlack">{event.description}</p>
                  <p className="text-xs text-clinicalGrey mt-0.5">
                    {new Date(event.timestamp).toLocaleString()} &middot;{" "}
                    {event.actor_name ?? "System"}
                  </p>
                </div>
              </div>
            ))}
          </div>
        ) : (
          <p className="text-sm text-clinicalGrey">No recent activity.</p>
        )}
      </motion.div>
    </div>
  );
}
