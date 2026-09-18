"use client";

export const dynamic = "force-dynamic";

import React, { useState } from "react";
import { motion } from "framer-motion";
import { useParams, useRouter } from "next/navigation";
import { useQuery, useMutation } from "@tanstack/react-query";
import Link from "next/link";
import {
  ChevronRight,
  Edit3,
  Plus,
  CheckCircle,
  Loader2,
  FileText,
  Sparkles,
  User,
} from "lucide-react";
import { consultationsApi } from "@/lib/api";
import { useToast } from "@/hooks/useToast";
import { DiagnosisCard } from "@/components/doctor/DiagnosisCard";
import { PrescriptionCard } from "@/components/doctor/PrescriptionCard";
import type { ClinicalNoteCreatePayload, PreAssessmentResponse } from "@/lib/types";

export default function ConsultationDetailPage(): React.ReactElement {
  const params = useParams();
  const router = useRouter();
  const visitId = params.id as string;
  const { showToast } = useToast();
  const [noteType, setNoteType] = useState<ClinicalNoteCreatePayload["note_type"]>("subjective");
  const [noteContent, setNoteContent] = useState("");
  const [showAddDiagnosis, setShowAddDiagnosis] = useState(false);
  const [showAddMedication, setShowAddMedication] = useState(false);
  const [diagName, setDiagName] = useState("");
  const [diagCode, setDiagCode] = useState("");
  const [medName, setMedName] = useState("");
  const [medDosage, setMedDosage] = useState("");
  const [medFrequency, setMedFrequency] = useState("");

  const { data: visit, isLoading } = useQuery({
    queryKey: ["consultation", visitId],
    queryFn: () => consultationsApi.getConsultation(visitId),
  });

  const { data: preAssessment } = useQuery<PreAssessmentResponse>({
    queryKey: ["pre-assessment", visitId],
    queryFn: () => consultationsApi.getPreAssessment(visitId),
    enabled: !!visitId,
  });

  const addNote = useMutation({
    mutationFn: (data: ClinicalNoteCreatePayload) => consultationsApi.addNote(visitId, data),
    onSuccess: () => {
      showToast({ title: "Note Added", message: "Clinical note saved.", type: "success" });
      setNoteContent("");
    },
  });

  const addDiagnosis = useMutation({
    mutationFn: () =>
      consultationsApi.addDiagnosis(visitId, {
        diagnosis_name: diagName,
        icd10_code: diagCode || undefined,
        type: "secondary",
        status: "suspected",
      }),
    onSuccess: () => {
      showToast({ title: "Added", message: "Diagnosis added to visit.", type: "success" });
      setShowAddDiagnosis(false);
      setDiagName("");
      setDiagCode("");
    },
  });

  const addMedication = useMutation({
    mutationFn: () =>
      consultationsApi.addMedication(visitId, {
        name: medName,
        dosage: medDosage || undefined,
        frequency: medFrequency || undefined,
      }),
    onSuccess: () => {
      showToast({ title: "Added", message: "Medication added to visit.", type: "success" });
      setShowAddMedication(false);
      setMedName("");
      setMedDosage("");
      setMedFrequency("");
    },
  });

  const finalize = useMutation({
    mutationFn: () => consultationsApi.completeConsultation(visitId),
    onSuccess: () => {
      showToast({ title: "Finalized", message: "Consultation completed.", type: "success" });
    },
  });

  if (isLoading) {
    return (
      <div className="space-y-6">
        <div className="skeleton h-8 w-64" />
        <div className="skeleton h-40 w-full rounded-card" />
        <div className="skeleton h-32 w-full rounded-card" />
      </div>
    );
  }

  if (!visit) {
    return (
      <div className="text-center py-12">
        <p className="text-clinicalGrey">Consultation not found.</p>
        <Link href="/doctor/consultations" className="text-celestialBlue text-sm hover:underline mt-2 inline-block">
          Back to Consultations
        </Link>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Breadcrumb */}
      <div className="flex items-center gap-2 text-sm text-clinicalGrey">
        <Link href="/doctor/consultations" className="hover:text-mirageBlack transition-colors">
          Consultations
        </Link>
        <ChevronRight className="w-3.5 h-3.5" />
        <span className="text-mirageBlack">Visit {visitId.slice(0, 8)}</span>
      </div>

      {/* Header */}
      <motion.div
        initial={{ opacity: 0, y: 12 }}
        animate={{ opacity: 1, y: 0 }}
        className="bg-white rounded-card border border-border p-6"
      >
        <div className="flex items-start justify-between gap-4">
          <div>
            <div className="flex items-center gap-2 flex-wrap">
              <h1 className="text-page-title font-bold text-mirageBlack">
                {visit.reason || visit.chief_complaint || "Consultation"}
              </h1>
              <span className={`text-xs px-2.5 py-1 rounded-full font-medium ${
                visit.status === "completed" ? "bg-healthGreen/10 text-healthGreen" :
                visit.status === "in_progress" ? "bg-celestialBlue/10 text-celestialBlue" :
                "bg-clinicalGrey/10 text-clinicalGrey"
              }`}>
                {visit.status.replace("_", " ")}
              </span>
            </div>
            <p className="text-sm text-clinicalGrey mt-1">
              {new Date(visit.visit_date).toLocaleDateString()} · {new Date(visit.visit_date).toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" })}
            </p>
          </div>
          <div className="flex items-center gap-2 shrink-0">
            {visit.status !== "completed" && (
              <button
                onClick={() => finalize.mutate()}
                disabled={finalize.isPending}
                className="inline-flex items-center gap-2 px-4 py-2 bg-healthGreen text-white rounded-lg text-sm font-medium hover:bg-healthGreen/90 transition-colors disabled:opacity-50"
              >
                <CheckCircle className="w-4 h-4" />
                {finalize.isPending ? "Finalizing..." : "Finalize"}
              </button>
            )}
            <Link
              href={`/doctor/ai-consultation?visitId=${visitId}`}
              className="inline-flex items-center gap-2 px-4 py-2 bg-celestialBlue text-white rounded-lg text-sm font-medium hover:bg-celestialBlue/90 transition-colors"
            >
              <Sparkles className="w-4 h-4" />
              AI Consultation
            </Link>
          </div>
        </div>

        {/* Visit Info */}
        <div className="grid grid-cols-2 lg:grid-cols-4 gap-4 mt-5 pt-4 border-t border-border">
          <div>
            <p className="text-micro text-clinicalGrey uppercase tracking-wider">Chief Complaint</p>
            <p className="text-sm text-mirageBlack mt-0.5">{visit.chief_complaint || "—"}</p>
          </div>
          <div>
            <p className="text-micro text-clinicalGrey uppercase tracking-wider">Facility</p>
            <p className="text-sm text-mirageBlack mt-0.5">{visit.facility_id || "General Hospital"}</p>
          </div>
          <div>
            <p className="text-micro text-clinicalGrey uppercase tracking-wider">Patient ID</p>
            <p className="text-sm text-mirageBlack mt-0.5">{visit.patient_id || "—"}</p>
          </div>
          <div>
            <p className="text-micro text-clinicalGrey uppercase tracking-wider">Doctor ID</p>
            <p className="text-sm text-mirageBlack mt-0.5">{visit.doctor_id.slice(0, 8)}...</p>
          </div>
        </div>
      </motion.div>

      {/* Patient Pre-Assessment */}
      {preAssessment && (
        <motion.div
          initial={{ opacity: 0, y: 12 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.05 }}
          className="bg-white rounded-card border border-border p-5"
        >
          <div className="flex items-center gap-2 mb-3">
            <Sparkles className="w-4 h-4 text-healthGreen" />
            <h2 className="font-semibold text-mirageBlack">Patient Pre-Assessment</h2>
          </div>
          {preAssessment.available ? (
            <div className="space-y-3">
              {preAssessment.summary && (
                <div className="p-3 bg-healthGreen/5 border border-healthGreen/20 rounded-lg">
                  <p className="text-[10px] uppercase font-semibold text-healthGreen tracking-wider mb-1">AI Summary</p>
                  <p className="text-sm text-mirageBlack">{preAssessment.summary}</p>
                </div>
              )}
              {preAssessment.messages && preAssessment.messages.length > 0 && (
                <div className="space-y-2">
                  <p className="text-micro text-clinicalGrey uppercase tracking-wider">Patient Responses</p>
                  {preAssessment.messages
                    .filter((m) => m.role.toLowerCase() === "user")
                    .map((m) => (
                      <div key={m.id} className="p-3 bg-secondary/50 rounded-lg">
                        <p className="text-sm text-mirageBlack whitespace-pre-wrap">{m.content}</p>
                      </div>
                    ))}
                </div>
              )}
            </div>
          ) : (
            <div className="flex items-start gap-3 p-3 bg-secondary/50 rounded-lg">
              <FileText className="w-4 h-4 text-clinicalGrey mt-0.5" />
              <p className="text-sm text-clinicalGrey">{preAssessment.reason || "No pre-assessment available."}</p>
            </div>
          )}
        </motion.div>
      )}

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Diagnoses */}
        <motion.div
          initial={{ opacity: 0, y: 12 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.1 }}
          className="bg-white rounded-card border border-border p-5"
        >
          <div className="flex items-center justify-between mb-4">
            <h2 className="font-semibold text-mirageBlack">Diagnoses</h2>
            <button
              onClick={() => setShowAddDiagnosis(true)}
              className="inline-flex items-center gap-1 px-2.5 py-1.5 rounded-lg text-xs font-medium bg-secondary text-mirageBlack hover:bg-secondary/80 transition-colors"
            >
              <Plus className="w-3 h-3" />
              Add
            </button>
          </div>
          {visit.diagnoses && visit.diagnoses.length > 0 ? (
            <div className="space-y-3">
              {visit.diagnoses.map((dx) => (
                <DiagnosisCard key={dx.id} diagnosis={dx} />
              ))}
            </div>
          ) : (
            <p className="text-sm text-clinicalGrey">No diagnoses recorded.</p>
          )}
        </motion.div>

        {/* Medications */}
        <motion.div
          initial={{ opacity: 0, y: 12 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.15 }}
          className="bg-white rounded-card border border-border p-5"
        >
          <div className="flex items-center justify-between mb-4">
            <h2 className="font-semibold text-mirageBlack">Medications</h2>
            <button
              onClick={() => setShowAddMedication(true)}
              className="inline-flex items-center gap-1 px-2.5 py-1.5 rounded-lg text-xs font-medium bg-secondary text-mirageBlack hover:bg-secondary/80 transition-colors"
            >
              <Plus className="w-3 h-3" />
              Add
            </button>
          </div>
          {visit.medications && visit.medications.length > 0 ? (
            <div className="space-y-3">
              {visit.medications.map((med) => (
                <PrescriptionCard key={med.id} medication={med} />
              ))}
            </div>
          ) : (
            <p className="text-sm text-clinicalGrey">No medications prescribed.</p>
          )}
        </motion.div>
      </div>

      {/* Clinical Notes */}
      <motion.div
        initial={{ opacity: 0, y: 12 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.2 }}
        className="bg-white rounded-card border border-border p-5"
      >
        <h2 className="font-semibold text-mirageBlack mb-4">Clinical Notes</h2>
        {visit.clinical_notes && visit.clinical_notes.length > 0 ? (
          <div className="space-y-3 mb-4">
            {visit.clinical_notes.map((note) => (
              <div key={note.id} className="p-3 bg-secondary/50 rounded-lg">
                <div className="flex items-center gap-2 mb-1">
                  <span className="text-[10px] uppercase font-semibold text-celestialBlue tracking-wider">Clinical Note</span>
                  {note.is_finalized && (
                    <span className="text-[10px] uppercase font-semibold text-healthGreen tracking-wider">Finalized</span>
                  )}
                </div>
                <div className="space-y-2 text-sm text-mirageBlack">
                  {note.subjective && (
                    <div>
                      <span className="text-[10px] font-semibold uppercase text-clinicalGrey tracking-wider">Subjective:</span>
                      <p className="whitespace-pre-wrap">{note.subjective}</p>
                    </div>
                  )}
                  {note.objective && (
                    <div>
                      <span className="text-[10px] font-semibold uppercase text-clinicalGrey tracking-wider">Objective:</span>
                      <p className="whitespace-pre-wrap">{note.objective}</p>
                    </div>
                  )}
                  {note.assessment && (
                    <div>
                      <span className="text-[10px] font-semibold uppercase text-clinicalGrey tracking-wider">Assessment:</span>
                      <p className="whitespace-pre-wrap">{note.assessment}</p>
                    </div>
                  )}
                  {note.plan && (
                    <div>
                      <span className="text-[10px] font-semibold uppercase text-clinicalGrey tracking-wider">Plan:</span>
                      <p className="whitespace-pre-wrap">{note.plan}</p>
                    </div>
                  )}
                </div>
              </div>
            ))}
          </div>
        ) : (
          <p className="text-sm text-clinicalGrey mb-4">No notes yet.</p>
        )}

        {/* Add Note */}
        {visit.status !== "completed" && (
          <div className="border-t border-border pt-4">
            <div className="flex items-center gap-2 mb-2">
              {(["subjective", "objective", "assessment", "plan"] as const).map((type) => (
                <button
                  key={type}
                  onClick={() => setNoteType(type)}
                  className={`px-2.5 py-1 rounded-lg text-[10px] font-semibold uppercase tracking-wider transition-colors ${
                    noteType === type
                      ? "bg-celestialBlue text-white"
                      : "bg-secondary text-clinicalGrey hover:bg-secondary/80"
                  }`}
                >
                  {type}
                </button>
              ))}
            </div>
            <div className="flex gap-2">
              <textarea
                value={noteContent}
                onChange={(e) => setNoteContent(e.target.value)}
                placeholder={`Enter ${noteType} note...`}
                rows={2}
                className="flex-1 px-3 py-2 rounded-input border border-border bg-white text-sm text-mirageBlack focus:outline-none focus:ring-2 focus:ring-celestialBlue/20 focus:border-celestialBlue transition-all resize-none"
              />
              <button
                onClick={() => addNote.mutate({ note_type: noteType, content: noteContent })}
                disabled={!noteContent.trim() || addNote.isPending}
                className="px-3 py-2 bg-mirageBlack text-white rounded-lg text-sm font-medium hover:bg-mirageBlack/90 transition-colors disabled:opacity-50"
              >
                {addNote.isPending ? <Loader2 className="w-4 h-4 animate-spin" /> : <Edit3 className="w-4 h-4" />}
              </button>
            </div>
          </div>
        )}
      </motion.div>

      {/* AI Summary */}
      {visit.ai_summary && (
        <motion.div
          initial={{ opacity: 0, y: 12 }}
          animate={{ opacity: 1, y: 0 }}
          className="bg-celestialBlue/5 border border-celestialBlue/20 rounded-card p-5"
        >
          <div className="flex items-center gap-2 mb-2">
            <Sparkles className="w-4 h-4 text-celestialBlue" />
            <h2 className="font-semibold text-mirageBlack">AI Summary</h2>
          </div>
          <p className="text-sm text-mirageBlack leading-relaxed">{visit.ai_summary}</p>
        </motion.div>
      )}

      {/* Add Diagnosis Modal */}
      {showAddDiagnosis && (
        <div className="fixed inset-0 bg-black/40 flex items-center justify-center z-50 p-4" onClick={() => setShowAddDiagnosis(false)}>
          <motion.div
            initial={{ scale: 0.95, opacity: 0 }}
            animate={{ scale: 1, opacity: 1 }}
            onClick={(e) => e.stopPropagation()}
            className="bg-white rounded-xl w-full max-w-md p-6 shadow-xl"
          >
            <h2 className="text-lg font-bold text-mirageBlack mb-4">Add Diagnosis</h2>
            <div className="space-y-3">
              <div>
                <label className="block text-sm font-medium text-mirageBlack mb-1">Diagnosis Name</label>
                <input
                  value={diagName}
                  onChange={(e) => setDiagName(e.target.value)}
                  placeholder="e.g., Type 2 Diabetes Mellitus"
                  className="w-full px-3 py-2 rounded-lg border border-border bg-white text-sm text-mirageBlack focus:outline-none focus:ring-2 focus:ring-celestialBlue/30 focus:border-celestialBlue transition-all"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-mirageBlack mb-1">ICD-10 Code (optional)</label>
                <input
                  value={diagCode}
                  onChange={(e) => setDiagCode(e.target.value)}
                  placeholder="e.g., E11.9"
                  className="w-full px-3 py-2 rounded-lg border border-border bg-white text-sm text-mirageBlack focus:outline-none focus:ring-2 focus:ring-celestialBlue/30 focus:border-celestialBlue transition-all"
                />
              </div>
            </div>
            <div className="flex gap-3 mt-4">
              <button onClick={() => setShowAddDiagnosis(false)} className="flex-1 py-2 border border-border rounded-lg text-sm font-medium text-mirageBlack hover:bg-secondary transition-colors">
                Cancel
              </button>
              <button
                onClick={() => addDiagnosis.mutate()}
                disabled={!diagName.trim() || addDiagnosis.isPending}
                className="flex-1 py-2 bg-mirageBlack text-white rounded-lg text-sm font-medium hover:bg-mirageBlack/90 transition-colors disabled:opacity-50"
              >
                {addDiagnosis.isPending ? "Adding..." : "Add"}
              </button>
            </div>
          </motion.div>
        </div>
      )}

      {/* Add Medication Modal */}
      {showAddMedication && (
        <div className="fixed inset-0 bg-black/40 flex items-center justify-center z-50 p-4" onClick={() => setShowAddMedication(false)}>
          <motion.div
            initial={{ scale: 0.95, opacity: 0 }}
            animate={{ scale: 1, opacity: 1 }}
            onClick={(e) => e.stopPropagation()}
            className="bg-white rounded-xl w-full max-w-md p-6 shadow-xl"
          >
            <h2 className="text-lg font-bold text-mirageBlack mb-4">Add Medication</h2>
            <div className="space-y-3">
              <div>
                <label className="block text-sm font-medium text-mirageBlack mb-1">Medication Name</label>
                <input
                  value={medName}
                  onChange={(e) => setMedName(e.target.value)}
                  placeholder="e.g., Metformin"
                  className="w-full px-3 py-2 rounded-lg border border-border bg-white text-sm text-mirageBlack focus:outline-none focus:ring-2 focus:ring-celestialBlue/30 focus:border-celestialBlue transition-all"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-mirageBlack mb-1">Dosage</label>
                <input
                  value={medDosage}
                  onChange={(e) => setMedDosage(e.target.value)}
                  placeholder="e.g., 500mg"
                  className="w-full px-3 py-2 rounded-lg border border-border bg-white text-sm text-mirageBlack focus:outline-none focus:ring-2 focus:ring-celestialBlue/30 focus:border-celestialBlue transition-all"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-mirageBlack mb-1">Frequency</label>
                <input
                  value={medFrequency}
                  onChange={(e) => setMedFrequency(e.target.value)}
                  placeholder="e.g., Twice daily"
                  className="w-full px-3 py-2 rounded-lg border border-border bg-white text-sm text-mirageBlack focus:outline-none focus:ring-2 focus:ring-celestialBlue/30 focus:border-celestialBlue transition-all"
                />
              </div>
            </div>
            <div className="flex gap-3 mt-4">
              <button onClick={() => setShowAddMedication(false)} className="flex-1 py-2 border border-border rounded-lg text-sm font-medium text-mirageBlack hover:bg-secondary transition-colors">
                Cancel
              </button>
              <button
                onClick={() => addMedication.mutate()}
                disabled={!medName.trim() || addMedication.isPending}
                className="flex-1 py-2 bg-mirageBlack text-white rounded-lg text-sm font-medium hover:bg-mirageBlack/90 transition-colors disabled:opacity-50"
              >
                {addMedication.isPending ? "Adding..." : "Add"}
              </button>
            </div>
          </motion.div>
        </div>
      )}
    </div>
  );
}
