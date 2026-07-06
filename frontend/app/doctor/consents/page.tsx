"use client";

import React, { useState } from "react";
import { motion } from "framer-motion";
import { useQuery } from "@tanstack/react-query";
import { consentsApi } from "@/lib/api";
import type { ConsentRequestResponse } from "@/lib/types";

const statusColors: Record<string, string> = {
  pending: "bg-alertOrange/10 text-alertOrange",
  approved: "bg-healthGreen/10 text-healthGreen",
  declined: "bg-red-100 text-red-600",
  expired: "bg-clinicalGrey/10 text-clinicalGrey",
  revoked: "bg-clinicalGrey/10 text-clinicalGrey",
};

const statusLabels: Record<string, string> = {
  pending: "Pending",
  approved: "Approved",
  declined: "Declined",
  expired: "Expired",
  revoked: "Revoked",
};

export default function DoctorConsentsPage(): React.ReactElement {
  const [activeFilter, setActiveFilter] = useState<string | null>(null);

  const { data: consentData, isLoading } = useQuery({
    queryKey: ["consents", activeFilter],
    queryFn: () => consentsApi.listConsents(activeFilter ? { status: activeFilter, limit: 50 } : { limit: 50 }),
  });

  const consents = consentData?.items ?? [];
  const filters = ["All", "pending", "approved", "declined", "expired"];

  return (
    <div className="space-y-6">
      <motion.div initial={{ opacity: 0, y: 12 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.4 }}>
        <h1 className="text-2xl font-bold text-mirageBlack">Consent Management</h1>
        <p className="text-clinicalGrey">Track and manage patient consent requests</p>
      </motion.div>

      <div className="flex gap-2 flex-wrap">
        {filters.map((filter) => (
          <button
            key={filter}
            onClick={() => setActiveFilter(filter === "All" ? null : filter)}
            className={`px-3 py-1.5 rounded-lg text-xs font-medium transition-colors ${
              (filter === "All" && !activeFilter) || activeFilter === filter
                ? "bg-mirageBlack text-white"
                : "bg-white border border-border text-clinicalGrey hover:bg-secondary"
            }`}
          >
            {filter === "All" ? "All" : statusLabels[filter]}
          </button>
        ))}
      </div>

      {isLoading ? (
        <p className="text-sm text-clinicalGrey">Loading consents...</p>
      ) : consents.length > 0 ? (
        <div className="space-y-3">
          {consents.map((consent: ConsentRequestResponse, i: number) => (
            <motion.div
              key={consent.id}
              initial={{ opacity: 0, y: 8 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: i * 0.03, duration: 0.3 }}
              className="bg-white rounded-xl border border-border p-4"
            >
              <div className="flex items-start justify-between">
                <div>
                  <p className="font-medium text-mirageBlack">{consent.purpose || "Record access request"}</p>
                  <p className="text-xs text-clinicalGrey mt-0.5">
                    {consent.doctor_name || "Dr. Mirage"} · {new Date(consent.created_at).toLocaleDateString()}
                  </p>
                  {consent.shared_data && consent.shared_data.length > 0 && (
                    <div className="flex flex-wrap gap-1.5 mt-2">
                      {consent.shared_data.map((dt) => (
                        <span key={dt} className="px-2 py-0.5 bg-secondary rounded text-[10px] text-clinicalGrey capitalize">
                          {dt.replace("_", " ")}
                        </span>
                      ))}
                    </div>
                  )}
                </div>
                <span className={`text-xs px-2.5 py-1 rounded-full font-medium ${statusColors[consent.status] || "bg-clinicalGrey/10 text-clinicalGrey"}`}>
                  {statusLabels[consent.status] || consent.status}
                </span>
              </div>
              {consent.expiry_date && consent.status === "pending" && (
                <p className="text-xs text-alertOrange mt-2">
                  Expires {new Date(consent.expiry_date).toLocaleDateString()} {new Date(consent.expiry_date).toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" })}
                </p>
              )}
            </motion.div>
          ))}
        </div>
      ) : (
        <div className="text-center py-12">
          <p className="text-sm text-clinicalGrey">No consent requests found.</p>
        </div>
      )}
    </div>
  );
}
