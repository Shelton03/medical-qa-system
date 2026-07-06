"use client";

import React from "react";
import Link from "next/link";
import { motion } from "framer-motion";
import { useQuery } from "@tanstack/react-query";
import {
  ArrowLeft,
  Stethoscope,
  ClipboardList,
  Pill,
  FileText,
  Calendar,
  Building2,
  User,
  AlertCircle,
} from "lucide-react";
import { patientsApi } from "@/lib/api";
import { StatusBadge } from "@/components/ui/StatusBadge";
import { LoadingSkeleton } from "@/components/ui/LoadingSkeleton";
import { EmptyState } from "@/components/ui/EmptyState";
import type { VisitWithDetailsResponse } from "@/lib/types";

interface VisitDetailPageProps {
  params: { id: string };
}

function useVisitDetail(visitId: string) {
  return useQuery<VisitWithDetailsResponse, Error>({
    queryKey: ["patient-visit", visitId],
    queryFn: () => patientsApi.getMyVisit(visitId),
    enabled: !!visitId,
  });
}

function formatDate(dateStr: string): string {
  const d = new Date(dateStr);
  return d.toLocaleDateString("en-US", {
    weekday: "short",
    month: "short",
    day: "numeric",
    year: "numeric",
  });
}

export default function VisitDetailPage({ params }: VisitDetailPageProps): React.ReactElement {
  const visitId = params.id;
  const { data: visit, isLoading, error } = useVisitDetail(visitId);

  const statusVariant =
    visit?.status === "completed"
      ? "completed"
      : visit?.status === "in_progress"
      ? "active"
      : visit?.status === "cancelled"
      ? "expired"
      : "pending";

  return (
    <div className="p-4 space-y-4 pb-20">
      {/* Header */}
      <motion.div
        initial={{ opacity: 0, y: 8 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.3 }}
        className="flex items-center gap-3"
      >
        <Link
          href="/patient/timeline"
          className="touch-target flex items-center justify-center rounded-full hover:bg-mirageBlack-100 transition-colors"
        >
          <ArrowLeft className="w-5 h-5 text-mirageBlack" />
        </Link>
        <div>
          <h1 className="text-page-title font-heading text-mirageBlack">Visit Details</h1>
        </div>
      </motion.div>

      {isLoading && <LoadingSkeleton type="card" count={2} />}

      {error && (
        <EmptyState
          icon={<AlertCircle className="w-8 h-8 text-errorRed" />}
          title="Could not load visit"
          description={error.message || "Something went wrong while fetching the visit details."}
          action={
            <Link
              href="/patient/timeline"
              className="inline-flex items-center gap-1.5 px-4 py-2 bg-mirageBlack text-white rounded-button text-body font-medium"
            >
              <ArrowLeft className="w-4 h-4" />
              Back to Timeline
            </Link>
          }
        />
      )}

      {!isLoading && !error && visit && (
        <>
          {/* Visit Info Card */}
          <motion.div
            initial={{ opacity: 0, y: 8 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.1, duration: 0.3 }}
            className="bg-white border border-border rounded-card p-4 space-y-3"
          >
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-2">
                <div className="w-8 h-8 rounded-lg bg-celestialBlue/10 flex items-center justify-center">
                  <Stethoscope className="w-4 h-4 text-celestialBlue" />
                </div>
                <span className="text-body font-medium text-mirageBlack">Visit #{visit.id.slice(-6)}</span>
              </div>
              <StatusBadge variant={statusVariant}>{visit.status}</StatusBadge>
            </div>

            <div className="space-y-2 pt-2 border-t border-border">
              <div className="flex items-center gap-2 text-caption text-clinicalGrey">
                <Calendar className="w-3.5 h-3.5" />
                <span>{formatDate(visit.visit_date)}</span>
              </div>
              {visit.facility_id && (
                <div className="flex items-center gap-2 text-caption text-clinicalGrey">
                  <Building2 className="w-3.5 h-3.5" />
                  <span>Facility ID: {visit.facility_id}</span>
                </div>
              )}
              {visit.doctor_id && (
                <div className="flex items-center gap-2 text-caption text-clinicalGrey">
                  <User className="w-3.5 h-3.5" />
                  <span>Doctor ID: {visit.doctor_id}</span>
                </div>
              )}
            </div>

            {visit.chief_complaint && (
              <div className="pt-2 border-t border-border">
                <p className="text-caption text-clinicalGrey mb-1">Chief Complaint</p>
                <p className="text-body text-mirageBlack">{visit.chief_complaint}</p>
              </div>
            )}

            {visit.reason && (
              <div className="pt-2 border-t border-border">
                <p className="text-caption text-clinicalGrey mb-1">Reason</p>
                <p className="text-body text-mirageBlack">{visit.reason}</p>
              </div>
            )}
          </motion.div>

          {/* Diagnoses */}
          {visit.diagnoses && visit.diagnoses.length > 0 && (
            <motion.div
              initial={{ opacity: 0, y: 8 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.2, duration: 0.3 }}
              className="bg-white border border-border rounded-card p-4"
            >
              <div className="flex items-center gap-2 mb-3">
                <ClipboardList className="w-4 h-4 text-alertOrange" />
                <h2 className="text-body font-semibold text-mirageBlack">Diagnoses</h2>
              </div>
              <div className="space-y-2">
                {visit.diagnoses.map((dx) => (
                  <div
                    key={dx.id}
                    className="flex items-start justify-between gap-2 p-2 bg-alertOrange-50 rounded-lg border border-alertOrange/10"
                  >
                    <div>
                      <p className="text-body font-medium text-mirageBlack">{dx.diagnosis_name}</p>
                      {dx.notes && <p className="text-caption text-clinicalGrey mt-0.5">{dx.notes}</p>}
                    </div>
                    {dx.icd10_code && (
                      <span className="text-micro px-2 py-0.5 bg-alertOrange/10 text-alertOrange rounded-full border border-alertOrange/20 shrink-0">
                        {dx.icd10_code}
                      </span>
                    )}
                  </div>
                ))}
              </div>
            </motion.div>
          )}

          {/* Medications */}
          {visit.medications && visit.medications.length > 0 && (
            <motion.div
              initial={{ opacity: 0, y: 8 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.3, duration: 0.3 }}
              className="bg-white border border-border rounded-card p-4"
            >
              <div className="flex items-center gap-2 mb-3">
                <Pill className="w-4 h-4 text-healthGreen" />
                <h2 className="text-body font-semibold text-mirageBlack">Medications</h2>
              </div>
              <div className="space-y-2">
                {visit.medications.map((med) => (
                  <div
                    key={med.id}
                    className="flex items-start justify-between gap-2 p-2 bg-healthGreen-50 rounded-lg border border-healthGreen/10"
                  >
                    <div>
                      <p className="text-body font-medium text-mirageBlack">{med.name}</p>
                      <p className="text-caption text-clinicalGrey mt-0.5">
                        {med.dosage || "—"} · {med.frequency || "As directed"}
                      </p>
                      {med.instructions && (
                        <p className="text-micro text-clinicalGrey mt-0.5">{med.instructions}</p>
                      )}
                    </div>
                  </div>
                ))}
              </div>
            </motion.div>
          )}

          {/* Clinical Notes */}
          {visit.clinical_notes && visit.clinical_notes.length > 0 && (
            <motion.div
              initial={{ opacity: 0, y: 8 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.4, duration: 0.3 }}
              className="bg-white border border-border rounded-card p-4"
            >
              <div className="flex items-center gap-2 mb-3">
                <FileText className="w-4 h-4 text-celestialBlue" />
                <h2 className="text-body font-semibold text-mirageBlack">Clinical Notes</h2>
              </div>
              <div className="space-y-2">
                {visit.clinical_notes.map((note) => (
                  <div key={note.id} className="p-2 bg-celestialBlue-50 rounded-lg border border-celestialBlue/10">
                    <div className="flex items-center justify-between">
                      <p className="text-caption font-medium text-mirageBlack capitalize">
                        {note.note_type || "Note"}
                      </p>
                      {note.is_finalized && (
                        <StatusBadge variant="completed">Finalized</StatusBadge>
                      )}
                    </div>
                    <p className="text-caption text-clinicalGrey mt-1">{note.content ?? `${note.subjective ?? note.objective ?? note.assessment ?? note.plan ?? "—"}`}</p>
                  </div>
                ))}
              </div>
            </motion.div>
          )}
        </>
      )}
    </div>
  );
}
