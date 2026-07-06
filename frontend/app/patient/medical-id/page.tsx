"use client";

import React from "react";
import { motion } from "framer-motion";
import { useQuery } from "@tanstack/react-query";
import {
  Heart,
  AlertTriangle,
  Stethoscope,
  User,
  Droplets,
  Phone,
  ClipboardList,
  Shield,
} from "lucide-react";
import { patientsApi } from "@/lib/api";
import { LoadingSkeleton } from "@/components/ui/LoadingSkeleton";
import { EmptyState } from "@/components/ui/EmptyState";

export default function PatientMedicalIdPage(): React.ReactElement {
  const {
    data: profile,
    isLoading,
    error,
  } = useQuery({
    queryKey: ["patient-me"],
    queryFn: () => patientsApi.getMyProfile(),
  });

  const patientName = profile
    ? `${profile.first_name ?? ""} ${profile.last_name ?? ""}`.trim()
    : null;

  const allergies = profile?.medical_record?.allergies ?? [];
  const chronicConditions = profile?.medical_record?.chronic_conditions ?? [];

  const formatDate = (dateStr: string | null): string => {
    if (!dateStr) return "—";
    const d = new Date(dateStr);
    return d.toLocaleDateString("en-US", {
      month: "short",
      day: "numeric",
      year: "numeric",
    });
  };

  return (
    <div className="p-4 space-y-4 pb-20">
      <motion.div
        initial={{ opacity: 0, y: 8 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.3 }}
      >
        <h1 className="text-page-title font-heading text-mirageBlack">Medical ID</h1>
        <p className="text-caption text-clinicalGrey">Emergency health information</p>
      </motion.div>

      {isLoading && <LoadingSkeleton type="card" count={3} />}

      {error && (
        <EmptyState
          icon={<Shield className="w-8 h-8 text-errorRed" />}
          title="Could not load medical ID"
          description="Something went wrong while fetching your medical information."
        />
      )}

      {!isLoading && !error && profile && (
        <>
          {/* Identity Card */}
          <motion.div
            initial={{ opacity: 0, y: 8 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.1, duration: 0.3 }}
            className="bg-white border border-border rounded-card p-4"
          >
            <div className="flex items-center gap-3 mb-4">
              <div className="w-12 h-12 rounded-full bg-mirageBlack flex items-center justify-center">
                <User className="w-6 h-6 text-white" />
              </div>
              <div>
                <h2 className="text-section-title font-semibold text-mirageBlack">
                  {patientName || "Patient"}
                </h2>
                <p className="text-caption text-clinicalGrey">
                  MRN: {profile.medical_record_number}
                </p>
              </div>
            </div>

            <div className="grid grid-cols-2 gap-3">
              <div className="bg-stellarWhite-100 rounded-lg p-2.5">
                <div className="flex items-center gap-1.5 mb-1">
                  <CalendarIcon className="w-3.5 h-3.5 text-celestialBlue" />
                  <span className="text-micro text-clinicalGrey">Date of Birth</span>
                </div>
                <p className="text-body font-medium text-mirageBlack">
                  {formatDate(profile.date_of_birth)}
                </p>
              </div>

              <div className="bg-stellarWhite-100 rounded-lg p-2.5">
                <div className="flex items-center gap-1.5 mb-1">
                  <Droplets className="w-3.5 h-3.5 text-healthGreen" />
                  <span className="text-micro text-clinicalGrey">Blood Type</span>
                </div>
                <p className="text-body font-medium text-mirageBlack">
                  {profile.blood_type || "Unknown"}
                </p>
              </div>

              <div className="bg-stellarWhite-100 rounded-lg p-2.5">
                <div className="flex items-center gap-1.5 mb-1">
                  <User className="w-3.5 h-3.5 text-clinicalGrey" />
                  <span className="text-micro text-clinicalGrey">Gender</span>
                </div>
                <p className="text-body font-medium text-mirageBlack capitalize">
                  {profile.gender || "—"}
                </p>
              </div>

              <div className="bg-stellarWhite-100 rounded-lg p-2.5">
                <div className="flex items-center gap-1.5 mb-1">
                  <Phone className="w-3.5 h-3.5 text-alertOrange" />
                  <span className="text-micro text-clinicalGrey">Emergency</span>
                </div>
                <p className="text-body font-medium text-mirageBlack truncate">
                  {profile.emergency_contact_name || "—"}
                </p>
                {profile.emergency_contact_phone && (
                  <p className="text-caption text-clinicalGrey">
                    {profile.emergency_contact_phone}
                  </p>
                )}
              </div>
            </div>
          </motion.div>

          {/* Allergies */}
          <motion.div
            initial={{ opacity: 0, y: 8 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.2, duration: 0.3 }}
            className="bg-white border border-border rounded-card p-4"
          >
            <div className="flex items-center gap-2 mb-3">
              <AlertTriangle className="w-4 h-4 text-errorRed" />
              <h2 className="text-body font-semibold text-mirageBlack">Allergies</h2>
              {allergies.length > 0 && (
                <span className="ml-auto text-micro px-2 py-0.5 bg-errorRed-50 text-errorRed rounded-full border border-errorRed/20">
                  {allergies.length} Active
                </span>
              )}
            </div>

            {allergies.length === 0 ? (
              <p className="text-caption text-clinicalGrey">No known allergies recorded.</p>
            ) : (
              <div className="space-y-2">
                {allergies.map((allergy) => (
                  <div
                    key={allergy.id}
                    className="flex items-start gap-2 p-2 bg-errorRed-50 rounded-lg border border-errorRed/10"
                  >
                    <AlertTriangle className="w-4 h-4 text-errorRed shrink-0 mt-0.5" />
                    <div>
                      <p className="text-body font-medium text-mirageBlack">{allergy.allergen}</p>
                      <p className="text-caption text-errorRed">{allergy.severity}</p>
                      {allergy.reaction && (
                        <p className="text-micro text-clinicalGrey mt-0.5">
                          Reaction: {allergy.reaction}
                        </p>
                      )}
                    </div>
                  </div>
                ))}
              </div>
            )}
          </motion.div>

          {/* Chronic Conditions */}
          <motion.div
            initial={{ opacity: 0, y: 8 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.3, duration: 0.3 }}
            className="bg-white border border-border rounded-card p-4"
          >
            <div className="flex items-center gap-2 mb-3">
              <Stethoscope className="w-4 h-4 text-alertOrange" />
              <h2 className="text-body font-semibold text-mirageBlack">Chronic Conditions</h2>
              {chronicConditions.length > 0 && (
                <span className="ml-auto text-micro px-2 py-0.5 bg-alertOrange-50 text-alertOrange rounded-full border border-alertOrange/20">
                  {chronicConditions.length} Active
                </span>
              )}
            </div>

            {chronicConditions.length === 0 ? (
              <p className="text-caption text-clinicalGrey">No chronic conditions recorded.</p>
            ) : (
              <div className="space-y-2">
                {chronicConditions.map((condition) => (
                  <div
                    key={condition.id}
                    className="flex items-start gap-2 p-2 bg-alertOrange-50 rounded-lg border border-alertOrange/10"
                  >
                    <ClipboardList className="w-4 h-4 text-alertOrange shrink-0 mt-0.5" />
                    <div className="flex-1">
                      <div className="flex items-center justify-between">
                        <p className="text-body font-medium text-mirageBlack">
                          {condition.condition_name}
                        </p>
                        {condition.icd10_code && (
                          <span className="text-micro px-2 py-0.5 bg-alertOrange/10 text-alertOrange rounded-full border border-alertOrange/20">
                            {condition.icd10_code}
                          </span>
                        )}
                      </div>
                      <p className="text-caption text-clinicalGrey capitalize">
                        Status: {condition.status}
                      </p>
                      {condition.diagnosed_date && (
                        <p className="text-micro text-clinicalGrey">
                          Diagnosed: {formatDate(condition.diagnosed_date)}
                        </p>
                      )}
                    </div>
                  </div>
                ))}
              </div>
            )}
          </motion.div>

          {/* Emergency Note */}
          <motion.div
            initial={{ opacity: 0, y: 8 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.4, duration: 0.3 }}
            className="bg-errorRed-50 border border-errorRed/20 rounded-card p-4"
          >
            <div className="flex items-start gap-2">
              <Heart className="w-5 h-5 text-errorRed shrink-0 mt-0.5" />
              <div>
                <p className="text-body font-medium text-errorRed">Emergency Use Only</p>
                <p className="text-caption text-clinicalGrey mt-0.5">
                  This information is intended for emergency medical personnel. Always carry a physical medical ID card as well.
                </p>
              </div>
            </div>
          </motion.div>
        </>
      )}
    </div>
  );
}

function CalendarIcon({ className }: { className?: string }): React.ReactElement {
  return (
    <svg
      xmlns="http://www.w3.org/2000/svg"
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth="2"
      strokeLinecap="round"
      strokeLinejoin="round"
      className={className}
    >
      <rect width="18" height="18" x="3" y="4" rx="2" ry="2" />
      <line x1="16" x2="16" y1="2" y2="6" />
      <line x1="8" x2="8" y1="2" y2="6" />
      <line x1="3" x2="21" y1="10" y2="10" />
    </svg>
  );
}
