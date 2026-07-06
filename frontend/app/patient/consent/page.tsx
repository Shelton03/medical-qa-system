"use client";

import React, { useState, useEffect } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { Check, X, Clock, User, ShieldCheck, ShieldX } from "lucide-react";
import { consentsApi } from "@/lib/api";
import type { ConsentRequestResponse } from "@/lib/types";
import { useToast } from "@/hooks/useToast";

const statusConfig: Record<string, { icon: React.ElementType; color: string; label: string }> = {
  pending: { icon: Clock, color: "text-alertOrange", label: "Pending" },
  approved: { icon: ShieldCheck, color: "text-healthGreen", label: "Approved" },
  declined: { icon: ShieldX, color: "text-red-500", label: "Declined" },
  expired: { icon: Clock, color: "text-clinicalGrey", label: "Expired" },
  revoked: { icon: ShieldX, color: "text-clinicalGrey", label: "Revoked" },
};

export default function PatientConsentPage(): React.ReactElement {
  const { showToast } = useToast();
  const queryClient = useQueryClient();
  const [activeTab, setActiveTab] = useState<"pending" | "history">("pending");

  const { data: consentData, isLoading } = useQuery({
    queryKey: ["patient-consents"],
    queryFn: () => consentsApi.listConsents({ limit: 50 }),
  });

  const allConsents = consentData?.items ?? [];
  const pendingConsents = allConsents.filter((c) => c.status === "pending");
  const historyConsents = allConsents.filter((c) => c.status !== "pending");

  // Demo mode: auto-approve first pending consent after delay
  useEffect(() => {
    const params = new URLSearchParams(window.location.search);
    if (params.get("demo") === "1" && pendingConsents.length > 0 && !approveMutation.isPending) {
      const timer = setTimeout(() => {
        approveMutation.mutate(pendingConsents[0].id);
      }, 2000);
      return () => clearTimeout(timer);
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [pendingConsents.length]);

  const approveMutation = useMutation({
    mutationFn: (consentId: string) => consentsApi.approveConsent(consentId),
    onSuccess: () => {
      showToast({ title: "Approved", message: "You have approved the consent request.", type: "success" });
      queryClient.invalidateQueries({ queryKey: ["patient-consents"] });
    },
    onError: (err: unknown) => {
      const msg = err instanceof Error ? err.message : "Failed to approve";
      showToast({ title: "Error", message: msg, type: "error" });
    },
  });

  const declineMutation = useMutation({
    mutationFn: (consentId: string) => consentsApi.declineConsent(consentId),
    onSuccess: () => {
      showToast({ title: "Declined", message: "You have declined the consent request.", type: "info" });
      queryClient.invalidateQueries({ queryKey: ["patient-consents"] });
    },
    onError: (err: unknown) => {
      const msg = err instanceof Error ? err.message : "Failed to decline";
      showToast({ title: "Error", message: msg, type: "error" });
    },
  });

  return (
    <div className="p-4 space-y-4">
      <motion.div initial={{ opacity: 0, y: 8 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.3 }}>
        <h1 className="text-xl font-bold text-mirageBlack">Consent Requests</h1>
        <p className="text-xs text-clinicalGrey">Manage who can access your health records</p>
      </motion.div>

      <div className="flex bg-secondary/50 rounded-lg p-0.5">
        <button
          onClick={() => setActiveTab("pending")}
          className={`flex-1 py-1.5 text-xs font-medium rounded-md transition-colors ${
            activeTab === "pending" ? "bg-white text-mirageBlack shadow-sm" : "text-clinicalGrey"
          }`}
        >
          Pending ({pendingConsents.length})
        </button>
        <button
          onClick={() => setActiveTab("history")}
          className={`flex-1 py-1.5 text-xs font-medium rounded-md transition-colors ${
            activeTab === "history" ? "bg-white text-mirageBlack shadow-sm" : "text-clinicalGrey"
          }`}
        >
          History ({historyConsents.length})
        </button>
      </div>

      {isLoading ? (
        <p className="text-xs text-clinicalGrey text-center py-8">Loading...</p>
      ) : (
        <AnimatePresence mode="wait">
          {activeTab === "pending" ? (
            <motion.div key="pending" initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }} className="space-y-3">
              {pendingConsents.length > 0 ? (
                pendingConsents.map((consent) => (
                  <ConsentCard
                    key={consent.id}
                    consent={consent}
                    onApprove={() => approveMutation.mutate(consent.id)}
                    onDecline={() => declineMutation.mutate(consent.id)}
                    isLoading={approveMutation.isPending || declineMutation.isPending}
                  />
                ))
              ) : (
                <div className="text-center py-12">
                  <ShieldCheck className="w-10 h-10 text-healthGreen mx-auto mb-2" />
                  <p className="text-sm text-mirageBlack font-medium">No pending requests</p>
                  <p className="text-xs text-clinicalGrey">You have no pending consent requests</p>
                </div>
              )}
            </motion.div>
          ) : (
            <motion.div key="history" initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }} className="space-y-3">
              {historyConsents.length > 0 ? (
                historyConsents.map((consent) => (
                  <HistoryCard key={consent.id} consent={consent} />
                ))
              ) : (
                <div className="text-center py-12">
                  <p className="text-xs text-clinicalGrey">No consent history yet</p>
                </div>
              )}
            </motion.div>
          )}
        </AnimatePresence>
      )}
    </div>
  );
}

function ConsentCard({
  consent,
  onApprove,
  onDecline,
  isLoading,
}: {
  consent: ConsentRequestResponse;
  onApprove: () => void;
  onDecline: () => void;
  isLoading: boolean;
}): React.ReactElement {
  return (
    <motion.div
      layout
      initial={{ opacity: 0, scale: 0.97 }}
      animate={{ opacity: 1, scale: 1 }}
      exit={{ opacity: 0, scale: 0.97 }}
      className="bg-white rounded-xl border border-border p-4 shadow-sm"
    >
      <div className="flex items-center gap-3 mb-3">
        <div className="w-10 h-10 rounded-full bg-celestialBlue/10 flex items-center justify-center shrink-0">
          <User className="w-5 h-5 text-celestialBlue" />
        </div>
        <div>
          <p className="text-sm font-medium text-mirageBlack">{consent.doctor_name || "Dr. Mirage"}</p>
          <p className="text-[10px] text-clinicalGrey">General Practice · Harare Hospital</p>
        </div>
        <span className="ml-auto text-[10px] px-2 py-0.5 rounded-full bg-alertOrange/10 text-alertOrange font-medium">
          Pending
        </span>
      </div>

      <div className="bg-secondary/30 rounded-lg p-3 mb-3">
        <p className="text-xs font-medium text-mirageBlack mb-1">Purpose</p>
        <p className="text-xs text-clinicalGrey">{consent.purpose || "Requesting access to your medical records"}</p>
      </div>

      {consent.shared_data && consent.shared_data.length > 0 && (
        <div className="mb-3">
          <p className="text-[10px] font-medium text-clinicalGrey mb-1.5">Data requested</p>
          <div className="flex flex-wrap gap-1.5">
            {consent.shared_data.map((dt) => (
              <span key={dt} className="px-2 py-0.5 bg-mirageBlack/5 rounded text-[10px] text-mirageBlack capitalize">
                {dt.replace("_", " ")}
              </span>
            ))}
          </div>
        </div>
      )}

      {consent.expiry_date && (
        <div className="flex items-center gap-1.5 mb-3">
          <Clock className="w-3 h-3 text-alertOrange" />
          <p className="text-[10px] text-alertOrange">
            Expires {new Date(consent.expiry_date).toLocaleDateString()} {new Date(consent.expiry_date).toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" })}
          </p>
        </div>
      )}

      <div className="flex gap-2">
        <button
          onClick={onDecline}
          disabled={isLoading}
          className="flex-1 py-2 border border-red-200 text-red-600 rounded-lg text-xs font-medium hover:bg-red-50 transition-colors disabled:opacity-50"
        >
          <X className="w-3.5 h-3.5 inline mr-1" />
          Decline
        </button>
        <button
          onClick={onApprove}
          disabled={isLoading}
          className="flex-1 py-2 bg-healthGreen text-white rounded-lg text-xs font-medium hover:bg-healthGreen/90 transition-colors disabled:opacity-50"
        >
          <Check className="w-3.5 h-3.5 inline mr-1" />
          Approve
        </button>
      </div>
    </motion.div>
  );
}

function HistoryCard({ consent }: { consent: ConsentRequestResponse }): React.ReactElement {
  const config = statusConfig[consent.status] || statusConfig.expired;
  const Icon = config.icon;

  return (
    <div className="bg-white rounded-xl border border-border p-3 flex items-center gap-3">
      <div className={`w-8 h-8 rounded-full flex items-center justify-center shrink-0 ${config.color.replace("text-", "bg-").replace("500", "100").replace("clinicalGrey", "clinicalGrey/10")}`}>
        <Icon className={`w-4 h-4 ${config.color}`} />
      </div>
      <div className="flex-1 min-w-0">
        <p className="text-xs font-medium text-mirageBlack truncate">{consent.purpose || "Record access"}</p>
        <p className="text-[10px] text-clinicalGrey">{new Date(consent.created_at).toLocaleDateString()}</p>
      </div>
      <span className={`text-[10px] px-2 py-0.5 rounded-full font-medium ${config.color.replace("text-", "bg-").replace("500", "100").replace("clinicalGrey", "clinicalGrey/10")}`}>
        {config.label}
      </span>
    </div>
  );
}
