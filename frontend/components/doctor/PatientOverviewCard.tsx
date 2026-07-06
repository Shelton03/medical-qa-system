"use client";

import React from "react";
import { motion } from "framer-motion";
import { User, Droplets } from "lucide-react";
import type { PatientFullProfileResponse, PatientResponse } from "@/lib/types";

interface PatientOverviewCardProps {
  patient: PatientResponse | PatientFullProfileResponse;
  compact?: boolean;
}

export function PatientOverviewCard({ patient, compact = false }: PatientOverviewCardProps): React.ReactElement {
  const dob = patient.date_of_birth ? new Date(patient.date_of_birth) : null;
  const age = dob ? Math.floor((Date.now() - dob.getTime()) / (365.25 * 24 * 60 * 60 * 1000)) : null;

  if (compact) {
    return (
      <motion.div
        initial={{ opacity: 0, y: 8 }}
        animate={{ opacity: 1, y: 0 }}
        className="flex items-center gap-3 p-3 bg-white rounded-card border border-border"
      >
        <div className="w-9 h-9 rounded-full bg-mirageBlack-100 flex items-center justify-center shrink-0">
          <User className="w-4 h-4 text-mirageBlack" />
        </div>
        <div className="min-w-0">
          <p className="text-sm font-medium text-mirageBlack truncate">
            {patient.first_name} {patient.last_name}
          </p>
          <p className="text-[11px] text-clinicalGrey">
            {patient.medical_record_number} · {age ?? "—"}y · {patient.gender}
          </p>
        </div>
        {patient.blood_type && (
          <div className="ml-auto flex items-center gap-1 text-[11px] text-clinicalGrey">
            <Droplets className="w-3 h-3" />
            <span>{patient.blood_type}</span>
          </div>
        )}
      </motion.div>
    );
  }

  return (
    <motion.div
      initial={{ opacity: 0, y: 12 }}
      animate={{ opacity: 1, y: 0 }}
      className="bg-white rounded-card border border-border p-5"
    >
      <div className="flex items-center gap-4">
        <div className="w-14 h-14 rounded-full bg-mirageBlack-100 flex items-center justify-center shrink-0">
          <User className="w-7 h-7 text-mirageBlack" />
        </div>
        <div className="flex-1 min-w-0">
          <h2 className="text-card-title font-semibold text-mirageBlack">
            {patient.first_name} {patient.last_name}
          </h2>
          <p className="text-caption text-clinicalGrey mt-0.5">
            MRN: {patient.medical_record_number} · ID: {patient.national_identifier}
          </p>
        </div>
        {patient.blood_type && (
          <div className="flex items-center gap-1.5 px-3 py-1.5 rounded-full bg-healthGreen-50 text-healthGreen text-xs font-medium">
            <Droplets className="w-3.5 h-3.5" />
            {patient.blood_type}
          </div>
        )}
      </div>
      <div className="grid grid-cols-3 gap-4 mt-4 pt-4 border-t border-border">
        <div>
          <p className="text-micro text-clinicalGrey uppercase tracking-wider">DOB</p>
          <p className="text-sm text-mirageBlack mt-0.5">
            {dob?.toLocaleDateString() ?? "—"}
          </p>
        </div>
        <div>
          <p className="text-micro text-clinicalGrey uppercase tracking-wider">Age</p>
          <p className="text-sm text-mirageBlack mt-0.5">{age ?? "—"}</p>
        </div>
        <div>
          <p className="text-micro text-clinicalGrey uppercase tracking-wider">Gender</p>
          <p className="text-sm text-mirageBlack mt-0.5 capitalize">{patient.gender}</p>
        </div>
      </div>
      {(patient.phone || patient.email) && (
        <div className="grid grid-cols-2 gap-4 mt-3">
          {patient.phone && (
            <div>
              <p className="text-micro text-clinicalGrey uppercase tracking-wider">Phone</p>
              <p className="text-sm text-mirageBlack mt-0.5">{patient.phone}</p>
            </div>
          )}
          {patient.email && (
            <div>
              <p className="text-micro text-clinicalGrey uppercase tracking-wider">Email</p>
              <p className="text-sm text-mirageBlack mt-0.5">{patient.email}</p>
            </div>
          )}
        </div>
      )}
    </motion.div>
  );
}
