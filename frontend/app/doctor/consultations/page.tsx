"use client";

import React, { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { useRouter } from "next/navigation";
import Link from "next/link";
import { Stethoscope, Plus, Check, X, Search, User, Sparkles } from "lucide-react";
import { consultationsApi, patientsApi } from "@/lib/api";
import type { VisitResponse, PatientResponse } from "@/lib/types";
import { useToast } from "@/hooks/useToast";

export default function DoctorConsultationsPage(): React.ReactElement {
  const { showToast } = useToast();
  const queryClient = useQueryClient();
  const router = useRouter();
  const [showNewModal, setShowNewModal] = useState(false);
  const [searchQuery, setSearchQuery] = useState("");
  const [selectedPatient, setSelectedPatient] = useState<PatientResponse | null>(null);
  const [chiefComplaint, setChiefComplaint] = useState("");

  const { data: visits, isLoading } = useQuery({
    queryKey: ["consultations"],
    queryFn: () => consultationsApi.listConsultations({ limit: 50 }),
  });

  const { data: patients } = useQuery({
    queryKey: ["patients", "search", searchQuery],
    queryFn: () => patientsApi.searchPatients(searchQuery, 10, 0),
    enabled: searchQuery.length > 1,
  });

  const startMutation = useMutation({
    mutationFn: (data: { patient_id: string; chief_complaint: string }) =>
      consultationsApi.startConsultation(data),
    onSuccess: (visit) => {
      showToast({ title: "Started", message: "New consultation started.", type: "success" });
      setShowNewModal(false);
      setSelectedPatient(null);
      setChiefComplaint("");
      queryClient.invalidateQueries({ queryKey: ["consultations"] });
      // Navigate to consultation detail
      router.push(`/doctor/consultations/${visit.id}`);
    },
    onError: (err: unknown) => {
      const msg = err instanceof Error ? err.message : "Failed to start consultation";
      showToast({ title: "Error", message: msg, type: "error" });
    },
  });

  return (
    <div className="space-y-6">
      <motion.div initial={{ opacity: 0, y: 12 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.4 }}>
            <div className="flex items-center justify-between">
              <div>
                <h1 className="text-2xl font-bold text-mirageBlack">Consultations</h1>
                <p className="text-clinicalGrey">Manage patient consultations</p>
              </div>
              <div className="flex items-center gap-2">
                <Link
                  href="/doctor/ai-consultation"
                  className="inline-flex items-center gap-2 px-4 py-2 bg-celestialBlue text-white rounded-lg text-sm font-medium hover:bg-celestialBlue/90 transition-colors"
                >
                  <Sparkles className="w-4 h-4" />
                  AI Consultation
                </Link>
                <button
                  onClick={() => setShowNewModal(true)}
                  className="inline-flex items-center gap-2 px-4 py-2 bg-mirageBlack text-white rounded-lg text-sm font-medium hover:bg-mirageBlack/90 transition-colors"
                >
                  <Plus className="w-4 h-4" />
                  New Consultation
                </button>
              </div>
            </div>
      </motion.div>

      {isLoading ? (
        <p className="text-sm text-clinicalGrey">Loading consultations...</p>
      ) : visits && visits.length > 0 ? (
        <div className="space-y-3">
          {visits.map((visit: VisitResponse, i: number) => (
            <motion.div
              key={visit.id}
              initial={{ opacity: 0, y: 8 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: i * 0.03, duration: 0.3 }}
              className="bg-white rounded-xl border border-border p-4 hover:shadow-sm transition-shadow cursor-pointer group"
              onClick={() => router.push(`/doctor/consultations/${visit.id}`)}
            >
              <div className="flex items-center justify-between">
                <div>
                  <p className="font-medium text-mirageBlack">{visit.reason || visit.chief_complaint || "Consultation"}</p>
                  <p className="text-xs text-clinicalGrey">
                    {new Date(visit.visit_date).toLocaleDateString()} · {new Date(visit.visit_date).toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" })}
                  </p>
                </div>
                <div className="flex items-center gap-2" onClick={(e) => e.stopPropagation()}>
                  <Link
                    href={`/doctor/ai-consultation?visitId=${visit.id}&patientId=${visit.patient_id || ""}`}
                    className="opacity-0 group-hover:opacity-100 transition-opacity inline-flex items-center gap-1 px-2 py-1 rounded-lg text-[10px] font-medium bg-celestialBlue text-white hover:bg-celestialBlue/90"
                  >
                    <Sparkles className="w-3 h-3" />
                    AI
                  </Link>
                  <span className={`text-xs px-2.5 py-1 rounded-full font-medium ${
                    visit.status === "completed" ? "bg-healthGreen/10 text-healthGreen" :
                    visit.status === "in_progress" ? "bg-celestialBlue/10 text-celestialBlue" :
                    "bg-clinicalGrey/10 text-clinicalGrey"
                  }`}>
                    {visit.status.replace("_", " ")}
                  </span>
                </div>
              </div>
            </motion.div>
          ))}
        </div>
      ) : (
        <div className="text-center py-12 bg-white rounded-xl border border-border">
          <Stethoscope className="w-10 h-10 text-clinicalGrey mx-auto mb-2" />
          <p className="text-sm text-mirageBlack font-medium">No consultations yet</p>
          <p className="text-xs text-clinicalGrey">Start a new consultation to begin</p>
        </div>
      )}

      {/* New Consultation Modal */}
      <AnimatePresence>
        {showNewModal && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="fixed inset-0 bg-black/40 flex items-center justify-center z-50 p-4"
            onClick={() => setShowNewModal(false)}
          >
            <motion.div
              initial={{ scale: 0.95, opacity: 0 }}
              animate={{ scale: 1, opacity: 1 }}
              exit={{ scale: 0.95, opacity: 0 }}
              onClick={(e) => e.stopPropagation()}
              className="bg-white rounded-xl w-full max-w-md p-6 shadow-xl"
            >
              <h2 className="text-lg font-bold text-mirageBlack mb-1">Start Consultation</h2>
              <p className="text-sm text-clinicalGrey mb-4">Search and select a patient</p>

              <div className="relative mb-3">
                <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-clinicalGrey" />
                <input
                  type="text"
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  placeholder="Search by name or ID..."
                  className="w-full pl-9 pr-4 py-2 rounded-lg border border-border bg-white text-sm text-mirageBlack focus:outline-none focus:ring-2 focus:ring-celestialBlue/30 focus:border-celestialBlue transition-all"
                />
              </div>

              {patients && patients.length > 0 && (
                <div className="space-y-2 max-h-48 overflow-y-auto mb-3">
                  {patients.map((patient) => (
                    <button
                      key={patient.id}
                      onClick={() => setSelectedPatient(patient)}
                      className={`w-full flex items-center gap-2 p-2 rounded-lg text-left transition-colors ${
                        selectedPatient?.id === patient.id
                          ? "bg-celestialBlue/10 border border-celestialBlue/30"
                          : "hover:bg-secondary"
                      }`}
                    >
                      <User className="w-4 h-4 text-clinicalGrey" />
                      <div>
                        <p className="text-sm font-medium text-mirageBlack">{patient.first_name} {patient.last_name}</p>
                        <p className="text-[10px] text-clinicalGrey">{patient.national_identifier}</p>
                      </div>
                    </button>
                  ))}
                </div>
              )}

              {selectedPatient && (
                <div className="mb-3">
                  <label className="block text-sm font-medium text-mirageBlack mb-1">Chief Complaint</label>
                  <textarea
                    value={chiefComplaint}
                    onChange={(e) => setChiefComplaint(e.target.value)}
                    placeholder="Patient's primary complaint..."
                    className="w-full px-3 py-2 rounded-lg border border-border bg-white text-sm text-mirageBlack focus:outline-none focus:ring-2 focus:ring-celestialBlue/30 focus:border-celestialBlue transition-all resize-none h-16"
                  />
                </div>
              )}

              <div className="flex gap-3">
                <button
                  onClick={() => setShowNewModal(false)}
                  className="flex-1 py-2 border border-border rounded-lg text-sm font-medium text-mirageBlack hover:bg-secondary transition-colors"
                >
                  Cancel
                </button>
                <button
                  onClick={() => {
                    if (selectedPatient) {
                      startMutation.mutate({
                        patient_id: selectedPatient.id,
                        chief_complaint: chiefComplaint || "General consultation",
                      });
                    }
                  }}
                  disabled={!selectedPatient || startMutation.isPending}
                  className="flex-1 py-2 bg-celestialBlue text-white rounded-lg text-sm font-medium hover:bg-celestialBlue/90 transition-colors disabled:opacity-50"
                >
                  {startMutation.isPending ? "Starting..." : "Start"}
                </button>
              </div>
            </motion.div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}
