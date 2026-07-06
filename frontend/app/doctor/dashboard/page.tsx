"use client";

import React from "react";
import { motion } from "framer-motion";
import Link from "next/link";
import { useQuery } from "@tanstack/react-query";
import { Stethoscope, Users, FileCheck, Activity } from "lucide-react";
import { consultationsApi, consentsApi } from "@/lib/api";

export default function DoctorDashboardPage(): React.ReactElement {
  const { data: visits, isLoading: visitsLoading } = useQuery({
    queryKey: ["consultations"],
    queryFn: () => consultationsApi.listConsultations({ limit: 5 }),
  });

  const { data: consentData, isLoading: consentsLoading } = useQuery({
    queryKey: ["consents"],
    queryFn: () => consentsApi.listConsents({ limit: 5 }),
  });

  const pendingConsents = consentData?.items?.filter((c) => c.status === "pending") ?? [];

  const stats = [
    { label: "Today's Consultations", value: visits?.length ?? 0, icon: Stethoscope, color: "text-celestialBlue" },
    { label: "Pending Consents", value: pendingConsents.length, icon: FileCheck, color: "text-alertOrange" },
    { label: "Recent Patients", value: "—", icon: Users, color: "text-healthGreen" },
    { label: "Notifications", value: "—", icon: Activity, color: "text-clinicalGrey" },
  ];

  return (
    <div className="space-y-6">
      <motion.div
        initial={{ opacity: 0, y: 12 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.4 }}
      >
        <h1 className="text-2xl font-bold text-mirageBlack">Dashboard</h1>
        <p className="text-clinicalGrey">Welcome back, Dr. Mirage</p>
      </motion.div>

      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
        {stats.map((stat, i) => (
          <motion.div
            key={stat.label}
            initial={{ opacity: 0, y: 12 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: i * 0.05, duration: 0.4 }}
            className="glass-card p-4 rounded-xl bg-white border border-border"
          >
            <div className="flex items-center gap-3 mb-2">
              <stat.icon className={`w-5 h-5 ${stat.color}`} />
              <span className="text-xs text-clinicalGrey">{stat.label}</span>
            </div>
            <p className="text-2xl font-bold text-mirageBlack">
              {visitsLoading && i === 0 ? "..." : stat.value}
            </p>
          </motion.div>
        ))}
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <motion.div
          initial={{ opacity: 0, y: 12 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2, duration: 0.4 }}
          className="bg-white rounded-xl border border-border p-5"
        >
          <div className="flex items-center justify-between mb-4">
            <h2 className="font-semibold text-mirageBlack">Recent Consultations</h2>
            <Link href="/doctor/consultations" className="text-xs text-celestialBlue hover:underline">
              View all
            </Link>
          </div>
          {visitsLoading ? (
            <p className="text-sm text-clinicalGrey">Loading...</p>
          ) : visits && visits.length > 0 ? (
            <div className="space-y-3">
              {visits.map((visit) => (
                <div key={visit.id} className="flex items-center justify-between p-3 bg-secondary/50 rounded-lg">
                  <div>
                    <p className="text-sm font-medium text-mirageBlack">{visit.reason || "Consultation"}</p>
                    <p className="text-xs text-clinicalGrey">{new Date(visit.visit_date).toLocaleDateString()}</p>
                  </div>
                  <span className={`text-xs px-2 py-1 rounded-full font-medium ${
                    visit.status === "completed" ? "bg-healthGreen/10 text-healthGreen" :
                    visit.status === "in_progress" ? "bg-celestialBlue/10 text-celestialBlue" :
                    "bg-clinicalGrey/10 text-clinicalGrey"
                  }`}>
                    {visit.status}
                  </span>
                </div>
              ))}
            </div>
          ) : (
            <p className="text-sm text-clinicalGrey">No consultations yet.</p>
          )}
        </motion.div>

        <motion.div
          initial={{ opacity: 0, y: 12 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.3, duration: 0.4 }}
          className="bg-white rounded-xl border border-border p-5"
        >
          <div className="flex items-center justify-between mb-4">
            <h2 className="font-semibold text-mirageBlack">Pending Consents</h2>
            <Link href="/doctor/consents" className="text-xs text-celestialBlue hover:underline">
              View all
            </Link>
          </div>
          {consentsLoading ? (
            <p className="text-sm text-clinicalGrey">Loading...</p>
          ) : pendingConsents.length > 0 ? (
            <div className="space-y-3">
              {pendingConsents.map((consent) => (
                <div key={consent.id} className="flex items-center justify-between p-3 bg-alertOrange/5 rounded-lg border border-alertOrange/10">
                  <div>
                    <p className="text-sm font-medium text-mirageBlack">{consent.purpose || "Record access request"}</p>
                    <p className="text-xs text-clinicalGrey">Waiting for patient approval</p>
                  </div>
                  <span className="text-xs px-2 py-1 rounded-full bg-alertOrange/10 text-alertOrange font-medium">
                    Pending
                  </span>
                </div>
              ))}
            </div>
          ) : (
            <p className="text-sm text-clinicalGrey">No pending consent requests.</p>
          )}
        </motion.div>
      </div>

      <div className="flex gap-3">
        <Link
          href="/doctor/consultations"
          className="inline-flex items-center gap-2 px-4 py-2 bg-mirageBlack text-white rounded-lg text-sm font-medium hover:bg-mirageBlack/90 transition-colors"
        >
          <Stethoscope className="w-4 h-4" />
          Start Consultation
        </Link>
        <Link
          href="/doctor/patients"
          className="inline-flex items-center gap-2 px-4 py-2 bg-white border border-border text-mirageBlack rounded-lg text-sm font-medium hover:bg-secondary transition-colors"
        >
          <Users className="w-4 h-4" />
          Search Patient
        </Link>
      </div>
    </div>
  );
}
