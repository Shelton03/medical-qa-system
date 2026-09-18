"use client";

import React, { useEffect, useState } from "react";
import { motion } from "framer-motion";
import { useSearchParams, useRouter } from "next/navigation";
import { useQuery, useMutation } from "@tanstack/react-query";
import { Sparkles, AlertTriangle, Activity, Pill } from "lucide-react";
import { aiApi, doctorApi } from "@/lib/api";
import { useToast } from "@/hooks/useToast";
import { AIChatPanel } from "@/components/doctor/AIChatPanel";

export default function AIConsultationContent(): React.ReactElement {
  const searchParams = useSearchParams();
  const router = useRouter();
  const patientId = searchParams.get("patientId");
  const visitId = searchParams.get("visitId");
  const { showToast } = useToast();
  const [sessionId, setSessionId] = useState<string | null>(null);

  const { data: patient } = useQuery({
    queryKey: ["doctor-patient-overview", patientId],
    queryFn: () => doctorApi.getDoctorPatientOverview(patientId!),
    enabled: !!patientId,
  });

  const { data: session, isLoading: sessionLoading } = useQuery({
    queryKey: ["ai-session", sessionId],
    queryFn: () => aiApi.getSession(sessionId!),
    enabled: !!sessionId,
  });

  const createSession = useMutation({
    mutationFn: () => aiApi.createSession({ patient_id: patientId || undefined }),
    onSuccess: (data) => {
      setSessionId(data.id);
      showToast({ title: "AI Session Started", message: "You can now chat with the AI assistant.", type: "success" });
    },
    onError: (err: unknown) => {
      const msg = err instanceof Error ? err.message : "Failed to start AI session";
      showToast({ title: "Error", message: msg, type: "error" });
    },
  });

  useEffect(() => {
    if (!sessionId) {
      createSession.mutate();
    }
  }, []);

  return (
    <div className="h-[calc(100vh-64px)] flex gap-4 -m-8 p-8">
      {/* Left Panel — Patient Context (30%) */}
      <motion.div
        initial={{ opacity: 0, x: -12 }}
        animate={{ opacity: 1, x: 0 }}
        className="w-[30%] min-w-[280px] max-w-[360px] flex flex-col gap-4 overflow-y-auto scrollbar-thin"
      >
        <div className="bg-white rounded-card border border-border p-4">
          <h2 className="font-semibold text-mirageBlack mb-3">Patient Context</h2>
          {patient ? (
            <div className="space-y-3">
              <div>
                <p className="text-micro text-clinicalGrey uppercase tracking-wider">Name</p>
                <p className="text-sm font-medium text-mirageBlack">{patient.full_name}</p>
              </div>
              <div className="grid grid-cols-2 gap-2">
                <div>
                  <p className="text-micro text-clinicalGrey uppercase tracking-wider">MRN</p>
                  <p className="text-sm text-mirageBlack">{patient.medical_record_number}</p>
                </div>
                <div>
                  <p className="text-micro text-clinicalGrey uppercase tracking-wider">Gender</p>
                  <p className="text-sm text-mirageBlack capitalize">{patient.gender}</p>
                </div>
              </div>
              {patient.blood_type && (
                <div>
                  <p className="text-micro text-clinicalGrey uppercase tracking-wider">Blood Type</p>
                  <p className="text-sm text-mirageBlack">{patient.blood_type}</p>
                </div>
              )}
            </div>
          ) : patientId ? (
            <div className="space-y-2">
              <div className="skeleton h-4 w-32" />
              <div className="skeleton h-4 w-24" />
            </div>
          ) : (
            <p className="text-sm text-clinicalGrey">No patient linked. General AI consultation mode.</p>
          )}
        </div>

        {/* Allergies */}
        {patient?.allergies && patient.allergies.length > 0 && (
          <div className="bg-alertOrange/5 border border-alertOrange/15 rounded-card p-4">
            <div className="flex items-center gap-2 mb-2">
              <AlertTriangle className="w-4 h-4 text-alertOrange" />
              <h3 className="text-sm font-semibold text-alertOrange">Allergies</h3>
            </div>
            <div className="space-y-1.5">
              {patient.allergies.map((a) => (
                <div key={a.id} className="flex items-center justify-between text-sm">
                  <span className="text-mirageBlack">{a.allergen}</span>
                  <span className={`text-[10px] px-1.5 py-0.5 rounded-full font-medium ${
                    a.severity === "severe" ? "bg-alertOrange/15 text-alertOrange" : "bg-clinicalGrey/10 text-clinicalGrey"
                  }`}>
                    {a.severity}
                  </span>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Conditions */}
        {patient?.conditions && patient.conditions.length > 0 && (
          <div className="bg-white rounded-card border border-border p-4">
            <div className="flex items-center gap-2 mb-2">
              <Activity className="w-4 h-4 text-celestialBlue" />
              <h3 className="text-sm font-semibold text-mirageBlack">Conditions</h3>
            </div>
            <div className="space-y-1.5">
              {patient.conditions.map((c) => (
                <div key={c.id} className="flex items-center justify-between text-sm">
                  <span className="text-mirageBlack">{c.condition_name}</span>
                  <span className="text-[10px] px-1.5 py-0.5 rounded-full font-medium bg-celestialBlue/10 text-celestialBlue">
                    {c.status}
                  </span>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Medications */}
        {patient?.current_medications && patient.current_medications.length > 0 && (
          <div className="bg-white rounded-card border border-border p-4">
            <div className="flex items-center gap-2 mb-2">
              <Pill className="w-4 h-4 text-healthGreen" />
              <h3 className="text-sm font-semibold text-mirageBlack">Medications</h3>
            </div>
            <div className="space-y-1.5">
              {patient.current_medications.map((m) => (
                <div key={m.id} className="text-sm">
                  <span className="text-mirageBlack font-medium">{m.name}</span>
                  <span className="text-clinicalGrey text-xs"> {m.dosage} · {m.frequency}</span>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Quick Actions */}
        <div className="bg-white rounded-card border border-border p-4 space-y-2">
          <button
            onClick={() => sessionId && router.push(`/doctor/differential?sessionId=${sessionId}`)}
            disabled={!sessionId}
            className="w-full flex items-center justify-center gap-2 px-3 py-2 rounded-lg bg-celestialBlue text-white text-sm font-medium hover:bg-celestialBlue/90 transition-colors disabled:opacity-50"
          >
            <Sparkles className="w-3.5 h-3.5" />
            Differential Diagnosis
          </button>
          <button
            onClick={() => sessionId && router.push(`/doctor/summary?sessionId=${sessionId}`)}
            disabled={!sessionId}
            className="w-full flex items-center justify-center gap-2 px-3 py-2 rounded-lg bg-secondary text-mirageBlack text-sm font-medium hover:bg-secondary/80 transition-colors disabled:opacity-50"
          >
            <Sparkles className="w-3.5 h-3.5" />
            Generate Summary
          </button>
        </div>
      </motion.div>

      {/* Center Panel — Chat (50%) */}
      <div className="flex-1 min-w-0">
        {sessionLoading || !sessionId ? (
          <div className="h-full bg-white rounded-card border border-border flex items-center justify-center">
            <div className="text-center">
              <Sparkles className="w-8 h-8 text-celestialBlue mx-auto mb-2 animate-pulse" />
              <p className="text-sm text-clinicalGrey">Starting AI session...</p>
            </div>
          </div>
        ) : (
          <AIChatPanel
            sessionId={sessionId}
            visitId={visitId || undefined}
            patientId={patientId || undefined}
            initialMessages={session?.messages || []}
          />
        )}
      </div>

      {/* Right Panel — Current Assessment (20%) */}
      <motion.div
        initial={{ opacity: 0, x: 12 }}
        animate={{ opacity: 1, x: 0 }}
        className="w-[20%] min-w-[220px] max-w-[280px] bg-white rounded-card border border-border p-4 overflow-y-auto scrollbar-thin"
      >
        <h2 className="font-semibold text-mirageBlack mb-3">Current Assessment</h2>
        <div className="space-y-4">
          <div>
            <p className="text-micro text-clinicalGrey uppercase tracking-wider mb-1">Symptoms</p>
            <div className="space-y-1.5">
              <p className="text-sm text-clinicalGrey italic">No symptoms recorded yet.</p>
            </div>
          </div>
          <div>
            <p className="text-micro text-clinicalGrey uppercase tracking-wider mb-1">Suspected Conditions</p>
            <div className="space-y-1.5">
              <p className="text-sm text-clinicalGrey italic">Use differential diagnosis to generate.</p>
            </div>
          </div>
          <div>
            <p className="text-micro text-clinicalGrey uppercase tracking-wider mb-1">Notes</p>
            <p className="text-sm text-clinicalGrey italic">
              Chat with the AI to build an assessment. The assistant will update this panel as the consultation progresses.
            </p>
          </div>
        </div>
      </motion.div>
    </div>
  );
}
