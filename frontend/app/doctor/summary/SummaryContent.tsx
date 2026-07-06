"use client";

import React, { useState, useEffect } from "react";
import { motion } from "framer-motion";
import { useSearchParams, useRouter } from "next/navigation";
import { useQuery, useMutation } from "@tanstack/react-query";
import { FileText, ArrowLeft } from "lucide-react";
import Link from "next/link";
import { aiApi, consultationsApi } from "@/lib/api";
import { useToast } from "@/hooks/useToast";
import { SOAPEditor } from "@/components/doctor/SOAPEditor";
import type { ClinicalSummary } from "@/lib/types";

const EMPTY_SUMMARY: ClinicalSummary = {
  subjective: "",
  objective: "",
  assessment: "",
  plan: "",
};

export default function SummaryContent(): React.ReactElement {
  const searchParams = useSearchParams();
  const router = useRouter();
  const sessionId = searchParams.get("sessionId");
  const visitId = searchParams.get("visitId");
  const { showToast } = useToast();
  const [summary, setSummary] = useState<ClinicalSummary>(EMPTY_SUMMARY);

  const { data: generatedSummary, isLoading } = useQuery({
    queryKey: ["summary", sessionId],
    queryFn: () => aiApi.getClinicalSummary(sessionId!),
    enabled: !!sessionId,
  });

  useEffect(() => {
    if (generatedSummary) {
      setSummary(generatedSummary);
    }
  }, [generatedSummary]);

  const regenerate = useMutation({
    mutationFn: () => aiApi.getClinicalSummary(sessionId!),
    onSuccess: (data) => {
      setSummary(data);
      showToast({ title: "Regenerated", message: "Clinical summary updated.", type: "success" });
    },
  });

  const saveSummary = useMutation({
    mutationFn: async (data: ClinicalSummary) => {
      // If visitId is available, save notes to the visit
      if (visitId) {
        await Promise.all([
          data.subjective ? consultationsApi.addNote(visitId, { note_type: "subjective", content: data.subjective }) : Promise.resolve(),
          data.objective ? consultationsApi.addNote(visitId, { note_type: "objective", content: data.objective }) : Promise.resolve(),
          data.assessment ? consultationsApi.addNote(visitId, { note_type: "assessment", content: data.assessment }) : Promise.resolve(),
          data.plan ? consultationsApi.addNote(visitId, { note_type: "plan", content: data.plan }) : Promise.resolve(),
        ]);
      }
    },
    onSuccess: () => {
      showToast({ title: "Saved", message: "Clinical summary saved to consultation record.", type: "success" });
      if (visitId) {
        router.push(`/doctor/consultations/${visitId}`);
      }
    },
    onError: (err: unknown) => {
      const msg = err instanceof Error ? err.message : "Failed to save summary";
      showToast({ title: "Error", message: msg, type: "error" });
    },
  });

  if (!sessionId) {
    return (
      <div className="text-center py-12">
        <p className="text-clinicalGrey">No AI session specified.</p>
        <Link href="/doctor/ai-consultation" className="text-celestialBlue text-sm hover:underline mt-2 inline-block">
          Start AI Consultation
        </Link>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Breadcrumb */}
      <div className="flex items-center gap-2 text-sm text-clinicalGrey">
        <Link href="/doctor/ai-consultation" className="hover:text-mirageBlack transition-colors">
          AI Consultation
        </Link>
        <span>/</span>
        <span className="text-mirageBlack">Clinical Summary</span>
      </div>

      <motion.div initial={{ opacity: 0, y: 12 }} animate={{ opacity: 1, y: 0 }}>
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-full bg-mirageBlack/5 flex items-center justify-center">
              <FileText className="w-5 h-5 text-mirageBlack" />
            </div>
            <div>
              <h1 className="text-2xl font-bold text-mirageBlack">Clinical Summary</h1>
              <p className="text-sm text-clinicalGrey">Review and edit the SOAP summary before saving</p>
            </div>
          </div>
          <Link
            href={`/doctor/ai-consultation?sessionId=${sessionId}`}
            className="inline-flex items-center gap-1.5 px-3 py-2 rounded-lg text-sm font-medium bg-secondary text-mirageBlack hover:bg-secondary/80 transition-colors"
          >
            <ArrowLeft className="w-3.5 h-3.5" />
            Back
          </Link>
        </div>
      </motion.div>

      {isLoading && !generatedSummary ? (
        <div className="space-y-4">
          <div className="skeleton h-48 w-full rounded-card" />
          <div className="skeleton h-48 w-full rounded-card" />
          <div className="skeleton h-48 w-full rounded-card" />
          <div className="skeleton h-48 w-full rounded-card" />
        </div>
      ) : (
        <SOAPEditor
          summary={summary}
          onChange={setSummary}
          onSave={(s) => saveSummary.mutate(s)}
          onRegenerate={() => regenerate.mutate()}
        />
      )}
    </div>
  );
}
