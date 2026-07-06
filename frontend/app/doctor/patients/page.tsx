"use client";

import React, { useState, useCallback } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { useRouter } from "next/navigation";
import { Search, User, Clock, ShieldCheck, ShieldAlert, FileText } from "lucide-react";
import { patientsApi, consentsApi } from "@/lib/api";
import type { PatientResponse } from "@/lib/types";
import { useToast } from "@/hooks/useToast";

export default function DoctorPatientsPage(): React.ReactElement {
  const router = useRouter();
  const [query, setQuery] = useState("");
  const [selectedPatient, setSelectedPatient] = useState<PatientResponse | null>(null);
  const [showConsentModal, setShowConsentModal] = useState(false);
  const [consentPurpose, setConsentPurpose] = useState("");
  const [sharedData, setSharedData] = useState<string[]>(["allergies", "medications", "diagnoses"]);
  const { showToast } = useToast();
  const queryClient = useQueryClient();

  const { data: patients, isLoading } = useQuery({
    queryKey: ["patients", "search", query],
    queryFn: () => patientsApi.searchPatients(query, 20, 0),
    enabled: query.length > 1,
  });

  const requestConsent = useMutation({
    mutationFn: (data: { patient_id: string; purpose: string; shared_data: string[] }) =>
      consentsApi.createConsent({
        doctor_id: "00000000-0000-0000-0000-000000000000", // Backend resolves from JWT
        patient_id: data.patient_id,
        purpose: data.purpose,
        shared_data: data.shared_data,
        expiry_hours: 24,
      }),
    onSuccess: () => {
      showToast({ title: "Success", message: "Consent request sent to patient.", type: "success" });
      setShowConsentModal(false);
      setConsentPurpose("");
      queryClient.invalidateQueries({ queryKey: ["consents"] });
    },
    onError: (err: unknown) => {
      const msg = err instanceof Error ? err.message : "Failed to send consent request";
      showToast({ title: "Error", message: msg, type: "error" });
    },
  });

  const handleSearch = useCallback((e: React.ChangeEvent<HTMLInputElement>) => {
    setQuery(e.target.value);
  }, []);

  const toggleDataType = (type: string) => {
    setSharedData((prev) =>
      prev.includes(type) ? prev.filter((t) => t !== type) : [...prev, type]
    );
  };

  const dataTypes = [
    { key: "allergies", label: "Allergies" },
    { key: "medications", label: "Medications" },
    { key: "diagnoses", label: "Diagnoses" },
    { key: "lab_results", label: "Lab Results" },
    { key: "imaging", label: "Imaging" },
  ];

  return (
    <div className="space-y-6">
      <motion.div initial={{ opacity: 0, y: 12 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.4 }}>
        <h1 className="text-2xl font-bold text-mirageBlack">Patient Search</h1>
        <p className="text-clinicalGrey">Search patients by name, ID, or phone</p>
      </motion.div>

      <div className="relative">
        <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-clinicalGrey" />
        <input
          type="text"
          value={query}
          onChange={handleSearch}
          placeholder="Search patients..."
          className="w-full pl-10 pr-4 py-2.5 rounded-lg border border-border bg-white text-mirageBlack focus:outline-none focus:ring-2 focus:ring-celestialBlue/30 focus:border-celestialBlue transition-all"
        />
      </div>

      {isLoading && <p className="text-sm text-clinicalGrey">Searching...</p>}

      <div className="space-y-3">
        <AnimatePresence>
          {patients?.map((patient) => (
            <motion.div
              key={patient.id}
              initial={{ opacity: 0, y: 8 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0 }}
              className="bg-white rounded-xl border border-border p-4 hover:shadow-sm transition-shadow cursor-pointer group"
              onClick={() => router.push(`/doctor/patients/${patient.id}`)}
            >
              <div className="flex items-center gap-3">
                <div className="w-10 h-10 rounded-full bg-mirageBlack-100 flex items-center justify-center shrink-0">
                  <User className="w-5 h-5 text-mirageBlack" />
                </div>
                <div className="flex-1 min-w-0">
                  <p className="font-medium text-mirageBlack truncate">
                    {patient.first_name} {patient.last_name}
                  </p>
                  <p className="text-xs text-clinicalGrey">
                    {patient.national_identifier} · {patient.gender} · {patient.phone}
                  </p>
                </div>
                <div className="flex items-center gap-2" onClick={(e) => e.stopPropagation()}>
                  <button
                    onClick={() => router.push(`/doctor/patients/${patient.id}`)}
                    className="opacity-0 group-hover:opacity-100 transition-opacity inline-flex items-center gap-1 px-2.5 py-1.5 bg-secondary text-mirageBlack text-xs font-medium rounded-lg hover:bg-secondary/80 transition-colors"
                  >
                    <FileText className="w-3 h-3" />
                    View Record
                  </button>
                  <button
                    onClick={() => {
                      setSelectedPatient(patient);
                      setShowConsentModal(true);
                    }}
                    className="px-3 py-1.5 bg-celestialBlue text-white text-xs font-medium rounded-lg hover:bg-celestialBlue/90 transition-colors"
                  >
                    Request Consent
                  </button>
                </div>
              </div>
            </motion.div>
          ))}
        </AnimatePresence>

        {!isLoading && query.length > 1 && (!patients || patients.length === 0) && (
          <p className="text-sm text-clinicalGrey text-center py-8">No patients found.</p>
        )}
      </div>

      {/* Consent Request Modal */}
      <AnimatePresence>
        {showConsentModal && selectedPatient && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="fixed inset-0 bg-black/40 flex items-center justify-center z-50 p-4"
            onClick={() => setShowConsentModal(false)}
          >
            <motion.div
              initial={{ scale: 0.95, opacity: 0 }}
              animate={{ scale: 1, opacity: 1 }}
              exit={{ scale: 0.95, opacity: 0 }}
              onClick={(e) => e.stopPropagation()}
              className="bg-white rounded-xl w-full max-w-md p-6 shadow-xl"
            >
              <h2 className="text-lg font-bold text-mirageBlack mb-1">Request Consent</h2>
              <p className="text-sm text-clinicalGrey mb-4">
                Ask {selectedPatient.first_name} {selectedPatient.last_name} for access to their records
              </p>

              <div className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-mirageBlack mb-1">Purpose</label>
                  <textarea
                    value={consentPurpose}
                    onChange={(e) => setConsentPurpose(e.target.value)}
                    placeholder="e.g., Reviewing patient history for follow-up consultation"
                    className="w-full px-3 py-2 rounded-lg border border-border bg-white text-sm text-mirageBlack focus:outline-none focus:ring-2 focus:ring-celestialBlue/30 focus:border-celestialBlue transition-all resize-none h-20"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-mirageBlack mb-2">Data to access</label>
                  <div className="flex flex-wrap gap-2">
                    {dataTypes.map((dt) => (
                      <button
                        key={dt.key}
                        onClick={() => toggleDataType(dt.key)}
                        className={`px-3 py-1.5 rounded-lg text-xs font-medium transition-colors ${
                          sharedData.includes(dt.key)
                            ? "bg-celestialBlue text-white"
                            : "bg-secondary text-clinicalGrey hover:bg-secondary/70"
                        }`}
                      >
                        {dt.label}
                      </button>
                    ))}
                  </div>
                </div>

                <div className="flex gap-3 pt-2">
                  <button
                    onClick={() => setShowConsentModal(false)}
                    className="flex-1 py-2 border border-border rounded-lg text-sm font-medium text-mirageBlack hover:bg-secondary transition-colors"
                  >
                    Cancel
                  </button>
                  <button
                    onClick={() =>
                      requestConsent.mutate({
                        patient_id: selectedPatient.id,
                        purpose: consentPurpose || "Medical record access",
                        shared_data: sharedData,
                      })
                    }
                    disabled={requestConsent.isPending || sharedData.length === 0}
                    className="flex-1 py-2 bg-celestialBlue text-white rounded-lg text-sm font-medium hover:bg-celestialBlue/90 transition-colors disabled:opacity-50"
                  >
                    {requestConsent.isPending ? "Sending..." : "Send Request"}
                  </button>
                </div>
              </div>
            </motion.div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}
