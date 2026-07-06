"use client";

import React from "react";
import { motion } from "framer-motion";
import { useQuery } from "@tanstack/react-query";
import { Shield, Clock, CheckCircle, AlertTriangle } from "lucide-react";
import { auditApi } from "@/lib/api";
import type { AuditLogEntry } from "@/lib/types";

export default function AccessHistoryPage(): React.ReactElement {
  const { data, isLoading } = useQuery({
    queryKey: ["audit"],
    queryFn: () => auditApi.getAccessHistory({ limit: 50 }),
  });

  const entries = data?.items ?? [];

  return (
    <div className="space-y-6">
      <motion.div initial={{ opacity: 0, y: 12 }} animate={{ opacity: 1, y: 0 }}>
        <h1 className="text-2xl font-bold text-mirageBlack">Access History</h1>
        <p className="text-clinicalGrey">Audit trail of patient record access</p>
      </motion.div>

      {isLoading ? (
        <div className="space-y-3">
          {[1, 2, 3, 4].map((i) => (
            <div key={i} className="skeleton h-16 w-full rounded-card" />
          ))}
        </div>
      ) : entries.length > 0 ? (
        <div className="bg-white rounded-card border border-border overflow-hidden">
          <div className="overflow-x-auto">
            <table className="w-full text-sm">
              <thead>
                <tr className="border-b border-border bg-secondary/30">
                  <th className="text-left px-5 py-3 text-micro text-clinicalGrey uppercase tracking-wider font-semibold">
                    Patient
                  </th>
                  <th className="text-left px-5 py-3 text-micro text-clinicalGrey uppercase tracking-wider font-semibold">
                    Facility
                  </th>
                  <th className="text-left px-5 py-3 text-micro text-clinicalGrey uppercase tracking-wider font-semibold">
                    Time
                  </th>
                  <th className="text-left px-5 py-3 text-micro text-clinicalGrey uppercase tracking-wider font-semibold">
                    Purpose
                  </th>
                  <th className="text-left px-5 py-3 text-micro text-clinicalGrey uppercase tracking-wider font-semibold">
                    Duration
                  </th>
                  <th className="text-left px-5 py-3 text-micro text-clinicalGrey uppercase tracking-wider font-semibold">
                    Outcome
                  </th>
                </tr>
              </thead>
              <tbody>
                {entries.map((entry: AuditLogEntry, i: number) => (
                  <motion.tr
                    key={entry.id}
                    initial={{ opacity: 0, y: 4 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: i * 0.02 }}
                    className="border-b border-border last:border-b-0 hover:bg-secondary/20 transition-colors"
                  >
                    <td className="px-5 py-3.5">
                      <div className="flex items-center gap-2">
                        <Shield className="w-3.5 h-3.5 text-celestialBlue shrink-0" />
                        <span className="font-medium text-mirageBlack">{entry.patient_name}</span>
                      </div>
                    </td>
                    <td className="px-5 py-3.5 text-clinicalGrey">{entry.facility}</td>
                    <td className="px-5 py-3.5 text-clinicalGrey">
                      {new Date(entry.access_time).toLocaleString()}
                    </td>
                    <td className="px-5 py-3.5 text-mirageBlack">{entry.purpose}</td>
                    <td className="px-5 py-3.5 text-clinicalGrey">
                      <span className="inline-flex items-center gap-1">
                        <Clock className="w-3 h-3" />
                        {entry.duration_minutes}m
                      </span>
                    </td>
                    <td className="px-5 py-3.5">
                      <span
                        className={`inline-flex items-center gap-1 text-[11px] font-medium px-2 py-0.5 rounded-full ${
                          entry.outcome === "success"
                            ? "bg-healthGreen/10 text-healthGreen"
                            : entry.outcome === "denied"
                            ? "bg-alertOrange/10 text-alertOrange"
                            : "bg-clinicalGrey/10 text-clinicalGrey"
                        }`}
                      >
                        {entry.outcome === "success" ? (
                          <CheckCircle className="w-3 h-3" />
                        ) : entry.outcome === "denied" ? (
                          <AlertTriangle className="w-3 h-3" />
                        ) : null}
                        {entry.outcome}
                      </span>
                    </td>
                  </motion.tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      ) : (
        <div className="text-center py-16 bg-white rounded-card border border-border">
          <Shield className="w-10 h-10 text-clinicalGrey mx-auto mb-3" />
          <p className="text-sm text-mirageBlack font-medium">No access history</p>
          <p className="text-xs text-clinicalGrey mt-1">Patient access events will be logged here.</p>
        </div>
      )}
    </div>
  );
}
