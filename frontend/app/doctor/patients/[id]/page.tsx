"use client";

export const dynamic = "force-dynamic";

import React, { useState } from "react";
import { motion } from "framer-motion";
import { useParams, useRouter } from "next/navigation";
import { useQuery, useMutation } from "@tanstack/react-query";
import Link from "next/link";
import {
  User,
  AlertTriangle,
  Activity,
  Pill,
  Calendar,
  Clock,
  ChevronRight,
  Stethoscope,
  ShieldCheck,
  FileText,
  Phone,
  Droplets,
} from "lucide-react";
import { doctorApi, consultationsApi, consentsApi } from "@/lib/api";
import { useToast } from "@/hooks/useToast";
import type { DoctorPatientOverview } from "@/lib/types";

export default function PatientDetailPage(): React.ReactElement {
  const params = useParams();
  const router = useRouter();
  const patientId = params.id as string;
  const { showToast } = useToast();
  const [showConsentModal, setShowConsentModal] = useState(false);
  const [consentPurpose, setConsentPurpose] = useState("");

  const {
    data: patient,
    isLoading,
    error,
  } = useQuery<DoctorPatientOverview>({
    queryKey: ["doctor-patient-overview", patientId],
    queryFn: () => doctorApi.getDoctorPatientOverview(patientId),
  });

  const startConsultation = useMutation({
    mutationFn: () =>
      consultationsApi.startConsultation({
        patient_id: patientId,
        chief_complaint: "General consultation",
      }),
    onSuccess: (visit) => {
      showToast({ title: "Consultation Started", message: "Redirecting to consultation workspace.", type: "success" });
      router.push(`/doctor/consultations/${visit.id}`);
    },
    onError: (err: unknown) => {
      const msg = err instanceof Error ? err.message : "Failed to start consultation";
      showToast({ title: "Error", message: msg, type: "error" });
    },
  });

  const requestConsent = useMutation({
    mutationFn: () =>
      consentsApi.createConsent({
        doctor_id: "00000000-0000-0000-0000-000000000000",
        patient_id: patientId,
        purpose: consentPurpose || "Medical record access",
        shared_data: ["allergies", "medications", "diagnoses"],
        expiry_hours: 24,
      }),
    onSuccess: () => {
      showToast({ title: "Success", message: "Consent request sent to patient.", type: "success" });
      setShowConsentModal(false);
      setConsentPurpose("");
    },
    onError: (err: unknown) => {
      const msg = err instanceof Error ? err.message : "Failed to send consent request";
      showToast({ title: "Error", message: msg, type: "error" });
    },
  });

  // Consent required state
  const isConsentRequired = error instanceof Error && error.message.includes("403");

  if (isLoading) {
    return (
      <div className="space-y-6">
        <div className="skeleton h-8 w-48" />
        <div className="skeleton h-40 w-full rounded-card" />
        <div className="skeleton h-32 w-full rounded-card" />
      </div>
    );
  }

  if (isConsentRequired || !patient) {
    return (
      <div className="space-y-6">
        <div className="flex items-center gap-2 text-sm text-clinicalGrey">
          <Link href="/doctor/patients" className="hover:text-mirageBlack transition-colors">
            Patients
          </Link>
          <ChevronRight className="w-3.5 h-3.5" />
          <span className="text-mirageBlack">Patient Record</span>
        </div>

        <motion.div
          initial={{ opacity: 0, y: 12 }}
          animate={{ opacity: 1, y: 0 }}
          className="bg-white rounded-card border border-border p-8 text-center"
        >
          <div className="w-16 h-16 rounded-full bg-clinicalGrey/10 flex items-center justify-center mx-auto mb-4">
            <ShieldCheck className="w-8 h-8 text-clinicalGrey" />
          </div>
          <h2 className="text-lg font-semibold text-mirageBlack mb-2">Consent Required</h2>
          <p className="text-sm text-clinicalGrey max-w-sm mx-auto mb-6">
            You need the patient&apos;s consent to view their full medical record. Request consent to continue.
          </p>
          <button
            onClick={() => setShowConsentModal(true)}
            className="inline-flex items-center gap-2 px-4 py-2 bg-celestialBlue text-white rounded-lg text-sm font-medium hover:bg-celestialBlue/90 transition-colors"
          >
            <ShieldCheck className="w-4 h-4" />
            Request Consent
          </button>
        </motion.div>

        {/* Consent Modal */}
        {showConsentModal && (
          <div className="fixed inset-0 bg-black/40 flex items-center justify-center z-50 p-4" onClick={() => setShowConsentModal(false)}>
            <motion.div
              initial={{ scale: 0.95, opacity: 0 }}
              animate={{ scale: 1, opacity: 1 }}
              onClick={(e) => e.stopPropagation()}
              className="bg-white rounded-xl w-full max-w-md p-6 shadow-xl"
            >
              <h2 className="text-lg font-bold text-mirageBlack mb-1">Request Consent</h2>
              <p className="text-sm text-clinicalGrey mb-4">
                Ask the patient for record access
              </p>
              <textarea
                value={consentPurpose}
                onChange={(e) => setConsentPurpose(e.target.value)}
                placeholder="Reason for access..."
                className="w-full px-3 py-2 rounded-lg border border-border bg-white text-sm text-mirageBlack focus:outline-none focus:ring-2 focus:ring-celestialBlue/30 focus:border-celestialBlue transition-all resize-none h-20 mb-4"
              />
              <div className="flex gap-3">
                <button onClick={() => setShowConsentModal(false)} className="flex-1 py-2 border border-border rounded-lg text-sm font-medium text-mirageBlack hover:bg-secondary transition-colors">
                  Cancel
                </button>
                <button
                  onClick={() => requestConsent.mutate()}
                  disabled={requestConsent.isPending}
                  className="flex-1 py-2 bg-celestialBlue text-white rounded-lg text-sm font-medium hover:bg-celestialBlue/90 transition-colors disabled:opacity-50"
                >
                  {requestConsent.isPending ? "Sending..." : "Send Request"}
                </button>
              </div>
            </motion.div>
          </div>
        )}
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Breadcrumb */}
      <div className="flex items-center gap-2 text-sm text-clinicalGrey">
        <Link href="/doctor/patients" className="hover:text-mirageBlack transition-colors">
          Patients
        </Link>
        <ChevronRight className="w-3.5 h-3.5" />
        <span className="text-mirageBlack">{patient.full_name}</span>
      </div>

      {/* Critical Allergies Banner */}
      {patient.allergies.some((a) => a.severity === "severe") && (
        <motion.div
          initial={{ opacity: 0, y: -8 }}
          animate={{ opacity: 1, y: 0 }}
          className="bg-alertOrange/10 border border-alertOrange/20 rounded-card p-4 flex items-center gap-3 sticky top-0 z-10"
        >
          <AlertTriangle className="w-5 h-5 text-alertOrange shrink-0" />
          <div>
            <p className="text-sm font-semibold text-alertOrange">Critical Allergies</p>
            <p className="text-caption text-alertOrange/80">
              {patient.allergies
                .filter((a) => a.severity === "severe")
                .map((a) => `${a.allergen} (${a.reaction || "unknown reaction"})`)
                .join(", ")}
            </p>
          </div>
        </motion.div>
      )}

      {/* Patient Header Card */}
      <motion.div
        initial={{ opacity: 0, y: 12 }}
        animate={{ opacity: 1, y: 0 }}
        className="bg-white rounded-card border border-border p-6"
      >
        <div className="flex items-start justify-between gap-4">
          <div className="flex items-center gap-4">
            <div className="w-16 h-16 rounded-full bg-mirageBlack-100 flex items-center justify-center">
              <User className="w-8 h-8 text-mirageBlack" />
            </div>
            <div>
              <h1 className="text-page-title font-bold text-mirageBlack">{patient.full_name}</h1>
              <p className="text-sm text-clinicalGrey mt-0.5">
                MRN: {patient.medical_record_number} · ID: {patient.national_identifier || "—"}
              </p>
              <div className="flex flex-wrap items-center gap-3 mt-2">
                {patient.blood_type && (
                  <span className="inline-flex items-center gap-1 px-2.5 py-1 rounded-full text-xs font-medium bg-healthGreen/10 text-healthGreen">
                    <Droplets className="w-3 h-3" />
                    {patient.blood_type}
                  </span>
                )}
                <span className="text-xs text-clinicalGrey">{patient.gender || "—"}</span>
                <span className="text-xs text-clinicalGrey">
                  DOB: {patient.date_of_birth ? new Date(patient.date_of_birth).toLocaleDateString() : "—"}
                </span>
              </div>
            </div>
          </div>
          <div className="flex flex-col gap-2 shrink-0">
            <button
              onClick={() => startConsultation.mutate()}
              disabled={startConsultation.isPending}
              className="inline-flex items-center gap-2 px-4 py-2 bg-mirageBlack text-white rounded-lg text-sm font-medium hover:bg-mirageBlack/90 transition-colors disabled:opacity-50"
            >
              <Stethoscope className="w-4 h-4" />
              {startConsultation.isPending ? "Starting..." : "Start Consultation"}
            </button>
            <button
              onClick={() => setShowConsentModal(true)}
              className="inline-flex items-center gap-2 px-4 py-2 bg-white border border-border text-mirageBlack rounded-lg text-sm font-medium hover:bg-secondary transition-colors"
            >
              <ShieldCheck className="w-4 h-4" />
              Request Consent
            </button>
          </div>
        </div>

        {/* Contact Info */}
        <div className="grid grid-cols-2 gap-4 mt-5 pt-4 border-t border-border">
          {patient.phone && (
            <div className="flex items-center gap-2 text-sm text-clinicalGrey">
              <Phone className="w-4 h-4" />
              {patient.phone}
            </div>
          )}
          {patient.email && (
            <div className="text-sm text-clinicalGrey">{patient.email}</div>
          )}
          <div className="text-sm text-clinicalGrey">
            Emergency: {patient.emergency_contact_name || "—"} {patient.emergency_contact_phone || ""}
          </div>
        </div>
      </motion.div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Active Conditions */}
        <motion.div
          initial={{ opacity: 0, y: 12 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.1 }}
          className="bg-white rounded-card border border-border p-5"
        >
          <div className="flex items-center gap-2 mb-4">
            <Activity className="w-4 h-4 text-celestialBlue" />
            <h2 className="font-semibold text-mirageBlack">Active Conditions</h2>
          </div>
          {patient.conditions.length > 0 ? (
            <div className="space-y-2.5">
              {patient.conditions.map((condition) => (
                <div key={condition.id} className="flex items-center justify-between p-3 bg-secondary/50 rounded-lg">
                  <div>
                    <p className="text-sm font-medium text-mirageBlack">{condition.condition_name}</p>
                    {condition.icd10_code && <p className="text-[11px] text-clinicalGrey">ICD-10: {condition.icd10_code}</p>}
                  </div>
                  <span
                    className={`text-[10px] px-2 py-0.5 rounded-full font-medium ${
                      condition.status === "active"
                        ? "bg-healthGreen/10 text-healthGreen"
                        : condition.status === "managed"
                        ? "bg-celestialBlue/10 text-celestialBlue"
                        : "bg-clinicalGrey/10 text-clinicalGrey"
                    }`}
                  >
                    {condition.status}
                  </span>
                </div>
              ))}
            </div>
          ) : (
            <p className="text-sm text-clinicalGrey">No active conditions recorded.</p>
          )}
        </motion.div>

        {/* Current Medications */}
        <motion.div
          initial={{ opacity: 0, y: 12 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.15 }}
          className="bg-white rounded-card border border-border p-5"
        >
          <div className="flex items-center gap-2 mb-4">
            <Pill className="w-4 h-4 text-healthGreen" />
            <h2 className="font-semibold text-mirageBlack">Current Medications</h2>
          </div>
          {patient.current_medications.length > 0 ? (
            <div className="space-y-2.5">
              {patient.current_medications.map((med) => (
                <div key={med.id} className="flex items-center justify-between p-3 bg-secondary/50 rounded-lg">
                  <div>
                    <p className="text-sm font-medium text-mirageBlack">{med.name}</p>
                    <p className="text-[11px] text-clinicalGrey">
                      {med.dosage} · {med.frequency}
                    </p>
                  </div>
                  <span className="text-[10px] px-2 py-0.5 rounded-full font-medium bg-celestialBlue/10 text-celestialBlue">
                    active
                  </span>
                </div>
              ))}
            </div>
          ) : (
            <p className="text-sm text-clinicalGrey">No current medications.</p>
          )}
        </motion.div>
      </div>

      {/* Recent Visits */}
      <motion.div
        initial={{ opacity: 0, y: 12 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.2 }}
        className="bg-white rounded-card border border-border p-5"
      >
        <div className="flex items-center justify-between mb-4">
          <div className="flex items-center gap-2">
            <Calendar className="w-4 h-4 text-clinicalGrey" />
            <h2 className="font-semibold text-mirageBlack">Recent Visits</h2>
          </div>
        </div>
        {patient.recent_visits.length > 0 ? (
          <div className="space-y-3">
            {patient.recent_visits.map((visit) => (
              <div key={visit.id} className="flex items-center gap-3 p-3 bg-secondary/50 rounded-lg">
                <div className="w-8 h-8 rounded-full bg-mirageBlack-100 flex items-center justify-center shrink-0">
                  <Clock className="w-3.5 h-3.5 text-clinicalGrey" />
                </div>
                <div className="flex-1 min-w-0">
                  <p className="text-sm font-medium text-mirageBlack">{visit.reason || visit.chief_complaint || "Consultation"}</p>
                  <p className="text-[11px] text-clinicalGrey">
                    {visit.visit_date ? new Date(visit.visit_date).toLocaleDateString() : "—"}
                    {visit.doctor_name ? ` · ${visit.doctor_name}` : ""}
                    {visit.facility_name ? ` · ${visit.facility_name}` : ""}
                  </p>
                </div>
                <span
                  className={`text-[10px] px-2 py-0.5 rounded-full font-medium ${
                    visit.status === "completed"
                      ? "bg-healthGreen/10 text-healthGreen"
                      : visit.status === "in_progress"
                      ? "bg-celestialBlue/10 text-celestialBlue"
                      : "bg-clinicalGrey/10 text-clinicalGrey"
                  }`}
                >
                  {visit.status}
                </span>
              </div>
            ))}
          </div>
        ) : (
          <div className="flex items-center gap-3 p-3 bg-secondary/50 rounded-lg">
            <FileText className="w-4 h-4 text-clinicalGrey" />
            <p className="text-sm text-clinicalGrey">No recent visits available. Start a consultation to create one.</p>
          </div>
        )}
      </motion.div>

      {/* Consent Modal */}
      {showConsentModal && (
        <div className="fixed inset-0 bg-black/40 flex items-center justify-center z-50 p-4" onClick={() => setShowConsentModal(false)}>
          <motion.div
            initial={{ scale: 0.95, opacity: 0 }}
            animate={{ scale: 1, opacity: 1 }}
            onClick={(e) => e.stopPropagation()}
            className="bg-white rounded-xl w-full max-w-md p-6 shadow-xl"
          >
            <h2 className="text-lg font-bold text-mirageBlack mb-1">Request Consent</h2>
            <p className="text-sm text-clinicalGrey mb-4">
              Ask {patient.full_name} for record access
            </p>
            <textarea
              value={consentPurpose}
              onChange={(e) => setConsentPurpose(e.target.value)}
              placeholder="Reason for access..."
              className="w-full px-3 py-2 rounded-lg border border-border bg-white text-sm text-mirageBlack focus:outline-none focus:ring-2 focus:ring-celestialBlue/30 focus:border-celestialBlue transition-all resize-none h-20 mb-4"
            />
            <div className="flex gap-3">
              <button onClick={() => setShowConsentModal(false)} className="flex-1 py-2 border border-border rounded-lg text-sm font-medium text-mirageBlack hover:bg-secondary transition-colors">
                Cancel
              </button>
              <button
                onClick={() => requestConsent.mutate()}
                disabled={requestConsent.isPending}
                className="flex-1 py-2 bg-celestialBlue text-white rounded-lg text-sm font-medium hover:bg-celestialBlue/90 transition-colors disabled:opacity-50"
              >
                {requestConsent.isPending ? "Sending..." : "Send Request"}
              </button>
            </div>
          </motion.div>
        </div>
      )}
    </div>
  );
}
