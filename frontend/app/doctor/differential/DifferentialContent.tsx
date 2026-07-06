"use client";

import React, { useState, useEffect } from "react";
import { motion } from "framer-motion";
import { useSearchParams, useRouter } from "next/navigation";
import { useQuery } from "@tanstack/react-query";
import { Sparkles, CheckCircle, ArrowLeft } from "lucide-react";
import Link from "next/link";
import { aiApi } from "@/lib/api";
import { useToast } from "@/hooks/useToast";
import { DifferentialList } from "@/components/doctor/DifferentialList";
import type { DifferentialDiagnosis } from "@/lib/types";

export default function DifferentialContent(): React.ReactElement {
  const searchParams = useSearchParams();
  const router = useRouter();
  const sessionId = searchParams.get("sessionId");
  const { showToast } = useToast();
  const [diagnoses, setDiagnoses] = useState<DifferentialDiagnosis[]>([]);

  const { data: differentialData, isLoading } = useQuery({
    queryKey: ["differential", sessionId],
    queryFn: () => aiApi.getDifferentialDiagnosis(sessionId!),
    enabled: !!sessionId,
  });

  useEffect(() => {
    if (differentialData) {
      setDiagnoses(differentialData);
    }
  }, [differentialData]);

  const handleConfirm = (id: string) => {
    setDiagnoses((prev) =>
      prev.map((d) => (d.id === id ? { ...d, status: "confirmed" as const } : d))
    );
    showToast({ title: "Confirmed", message: "Diagnosis marked as confirmed.", type: "success" });
  };

  const handleIgnore = (id: string) => {
    setDiagnoses((prev) =>
      prev.map((d) => (d.id === id ? { ...d, status: "ignored" as const } : d))
    );
  };

  const confirmAll = () => {
    const confirmed = diagnoses.filter((d) => d.status === "confirmed");
    if (confirmed.length === 0) {
      showToast({ title: "No Selection", message: "Please confirm at least one diagnosis first.", type: "warning" });
      return;
    }
    showToast({ title: "Finalized", message: `${confirmed.length} diagnosis(es) confirmed.`, type: "success" });
    // Navigate back or to summary
    router.push(`/doctor/summary?sessionId=${sessionId}`);
  };

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
        <span className="text-mirageBlack">Differential Diagnosis</span>
      </div>

      <motion.div initial={{ opacity: 0, y: 12 }} animate={{ opacity: 1, y: 0 }}>
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-full bg-celestialBlue/10 flex items-center justify-center">
              <Sparkles className="w-5 h-5 text-celestialBlue" />
            </div>
            <div>
              <h1 className="text-2xl font-bold text-mirageBlack">Differential Diagnosis</h1>
              <p className="text-sm text-clinicalGrey">AI-generated ranked list — review and confirm</p>
            </div>
          </div>
          <div className="flex items-center gap-2">
            <Link
              href={`/doctor/ai-consultation?sessionId=${sessionId}`}
              className="inline-flex items-center gap-1.5 px-3 py-2 rounded-lg text-sm font-medium bg-secondary text-mirageBlack hover:bg-secondary/80 transition-colors"
            >
              <ArrowLeft className="w-3.5 h-3.5" />
              Back
            </Link>
            <button
              onClick={confirmAll}
              className="inline-flex items-center gap-2 px-4 py-2 bg-healthGreen text-white rounded-lg text-sm font-medium hover:bg-healthGreen/90 transition-colors"
            >
              <CheckCircle className="w-4 h-4" />
              Confirm Diagnosis
            </button>
          </div>
        </div>
      </motion.div>

      {isLoading ? (
        <div className="space-y-4">
          {[1, 2, 3].map((i) => (
            <div key={i} className="skeleton h-28 w-full rounded-card" />
          ))}
        </div>
      ) : (
        <DifferentialList
          diagnoses={diagnoses}
          onConfirm={handleConfirm}
          onIgnore={handleIgnore}
        />
      )}
    </div>
  );
}
