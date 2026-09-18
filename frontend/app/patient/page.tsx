"use client";

import React, { useMemo } from "react";
import Link from "next/link";
import { motion } from "framer-motion";
import { useQuery } from "@tanstack/react-query";
import {
  ShieldCheck,
  FileText,
  ChevronRight,
  Bell,
  User,
  AlertTriangle,
  CalendarPlus,
  Pill,
  Stethoscope,
} from "lucide-react";
import { patientsApi, notificationsApi } from "@/lib/api";
import { LoadingSkeleton } from "@/components/ui/LoadingSkeleton";
import { EmptyState } from "@/components/ui/EmptyState";

function getGreeting(): string {
  const hour = new Date().getHours();
  if (hour >= 5 && hour < 12) return "Good morning";
  if (hour >= 12 && hour < 17) return "Good afternoon";
  if (hour >= 17 && hour < 21) return "Good evening";
  return "Good night";
}

export default function PatientHomePage(): React.ReactElement {
  const {
    data: profile,
    isLoading: profileLoading,
    error: profileError,
  } = useQuery({
    queryKey: ["patient-me"],
    queryFn: () => patientsApi.getMyProfile(),
  });

  const { data: unreadCount } = useQuery({
    queryKey: ["notifications-unread"],
    queryFn: () => notificationsApi.getUnreadCount(),
  });

  const patientName = profile
    ? `${profile.first_name ?? ""} ${profile.last_name ?? ""}`.trim()
    : null;

  const allergies = profile?.medical_record?.allergies ?? [];
  const chronicConditions = profile?.medical_record?.chronic_conditions ?? [];
  const medications = profile?.medical_record?.medications ?? [];
  const visits = profile?.medical_record?.visits ?? [];
  const today = new Date();
  today.setHours(0, 0, 0, 0);
  const activeMedications = medications.filter((m) => {
    if (!m.end_date) return true;
    const end = new Date(m.end_date);
    end.setHours(0, 0, 0, 0);
    return end >= today;
  });

  const stats = [
    {
      label: "Conditions",
      value: chronicConditions.length,
      icon: ShieldCheck,
      color: "text-celestialBlue",
      bg: "bg-celestialBlue-50 border-celestialBlue/20",
    },
    {
      label: "Active Meds",
      value: activeMedications.length,
      icon: Pill,
      color: "text-healthGreen",
      bg: "bg-healthGreen-50 border-healthGreen/20",
    },
    {
      label: "Visits",
      value: visits.length,
      icon: Stethoscope,
      color: "text-alertOrange",
      bg: "bg-alertOrange-50 border-alertOrange/20",
    },
    {
      label: "Allergies",
      value: allergies.length,
      icon: AlertTriangle,
      color: "text-errorRed",
      bg: "bg-errorRed-50 border-errorRed/20",
    },
  ];

  const quickActions = [
    {
      href: "/patient/book-appointment",
      label: "Book Appointment",
      description: "Schedule a visit with a doctor",
      icon: CalendarPlus,
      color: "bg-celestialBlue/10 text-celestialBlue",
    },
    {
      href: "/patient/consent",
      label: "Pending Consents",
      description: "Review and approve requests",
      icon: ShieldCheck,
      color: "bg-alertOrange/10 text-alertOrange",
    },
    {
      href: "/patient/records",
      label: "My Health Records",
      description: "View your medical history",
      icon: FileText,
      color: "bg-celestialBlue/10 text-celestialBlue",
    },
    {
      href: "/patient/notifications",
      label: "Notifications",
      description: unreadCount && unreadCount.count > 0
        ? `${unreadCount.count} unread`
        : "Stay updated",
      icon: Bell,
      color: "bg-mirageBlack/10 text-mirageBlack",
    },
  ];

  return (
    <div className="p-4 space-y-5 pb-20">
      {/* Greeting */}
      <motion.div
        initial={{ opacity: 0, y: 8 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.3 }}
      >
        <p className="text-caption text-clinicalGrey">{getGreeting()},</p>
        {profileLoading ? (
          <div className="mt-1 h-7 w-40 bg-mirageBlack-200 rounded animate-pulse" />
        ) : (
          <h1 className="text-page-title font-heading text-mirageBlack">
            {patientName || "Welcome"}
          </h1>
        )}
      </motion.div>

      {/* Health Summary */}
      <motion.div
        initial={{ opacity: 0, y: 8 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.1, duration: 0.3 }}
        className="grid grid-cols-2 gap-3"
      >
        {stats.map((stat) => {
          const Icon = stat.icon;
          return (
            <div
              key={stat.label}
              className={`border rounded-card p-3 ${stat.bg}`}
            >
              <Icon className={`w-5 h-5 ${stat.color} mb-1.5`} />
              <p className="text-section-title font-semibold text-mirageBlack">
                {profileLoading ? "—" : stat.value}
              </p>
              <p className="text-micro text-clinicalGrey">{stat.label}</p>
            </div>
          );
        })}
      </motion.div>

      {/* Critical Allergies Alert */}
      {allergies.length > 0 && (
        <motion.div
          initial={{ opacity: 0, y: 8 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.15, duration: 0.3 }}
          className="bg-errorRed-50 border border-errorRed/20 rounded-card p-3 flex items-start gap-3"
        >
          <AlertTriangle className="w-5 h-5 text-errorRed shrink-0 mt-0.5" />
          <div>
            <p className="text-body font-medium text-errorRed">Critical Allergies</p>
            <div className="flex flex-wrap gap-1.5 mt-1.5">
              {allergies.map((a) => (
                <span
                  key={a.id}
                  className="text-micro px-2 py-0.5 bg-errorRed/10 text-errorRed rounded-full border border-errorRed/20"
                >
                  {a.allergen} ({a.severity})
                </span>
              ))}
            </div>
          </div>
        </motion.div>
      )}

      {/* Quick Actions */}
      <motion.div
        initial={{ opacity: 0, y: 8 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.2, duration: 0.3 }}
      >
        <div className="flex items-center justify-between mb-2">
          <h2 className="text-body font-semibold text-mirageBlack">Quick Actions</h2>
        </div>
        <div className="grid grid-cols-1 gap-2">
          {quickActions.map((action) => (
            <Link key={action.href} href={action.href}>
              <div className="bg-white border border-border rounded-card p-3 flex items-center gap-3 hover:shadow-elevation-1 transition-shadow">
                <div
                  className={`w-9 h-9 rounded-lg flex items-center justify-center shrink-0 ${action.color}`}
                >
                  <action.icon className="w-4 h-4" />
                </div>
                <div className="flex-1">
                  <p className="text-body font-medium text-mirageBlack">{action.label}</p>
                  <p className="text-micro text-clinicalGrey">{action.description}</p>
                </div>
                <ChevronRight className="w-4 h-4 text-clinicalGrey" />
              </div>
            </Link>
          ))}
        </div>
      </motion.div>

      {/* Recent Activity */}
      <motion.div
        initial={{ opacity: 0, y: 8 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.3, duration: 0.3 }}
        className="bg-white border border-border rounded-card p-4"
      >
        <h2 className="text-body font-semibold text-mirageBlack mb-2">Recent Activity</h2>
        {profileLoading ? (
          <LoadingSkeleton type="text" count={3} />
        ) : profileError ? (
          <p className="text-caption text-clinicalGrey text-center py-4">
            Unable to load recent activity.
          </p>
        ) : (
          <div className="space-y-3">
            <div className="flex items-start gap-2">
              <div className="w-1.5 h-1.5 rounded-full bg-celestialBlue mt-1.5 shrink-0" />
              <div>
                <p className="text-caption text-mirageBlack">
                  Dr. Mirage requested access to your records
                </p>
                <p className="text-micro text-clinicalGrey">Today, 10:23 AM</p>
              </div>
            </div>
            <div className="flex items-start gap-2">
              <div className="w-1.5 h-1.5 rounded-full bg-healthGreen mt-1.5 shrink-0" />
              <div>
                <p className="text-caption text-mirageBlack">Your consent was approved</p>
                <p className="text-micro text-clinicalGrey">Today, 10:25 AM</p>
              </div>
            </div>
            <div className="flex items-start gap-2">
              <div className="w-1.5 h-1.5 rounded-full bg-clinicalGrey mt-1.5 shrink-0" />
              <div>
                <p className="text-caption text-mirageBlack">Consultation completed</p>
                <p className="text-micro text-clinicalGrey">Today, 10:45 AM</p>
              </div>
            </div>
          </div>
        )}
      </motion.div>
    </div>
  );
}
