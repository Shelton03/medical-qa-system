"use client";

import React, { useState } from "react";
import { motion } from "framer-motion";
import { ChevronDown, ChevronUp, User, Droplets, AlertTriangle, Pill, Stethoscope } from "lucide-react";

const recordSections = [
  {
    id: "personal",
    title: "Personal Information",
    icon: User,
    content: [
      { label: "Full Name", value: "Tendai Mutasa" },
      { label: "Date of Birth", value: "14 May 1989" },
      { label: "National ID", value: "ZIM-89-4567234" },
      { label: "Gender", value: "Male" },
      { label: "Blood Type", value: "O+" },
    ],
  },
  {
    id: "allergies",
    title: "Allergies",
    icon: AlertTriangle,
    badge: "2 active",
    content: [
      { label: "Penicillin", value: "Severe — Anaphylaxis" },
      { label: "Shellfish", value: "Moderate — Skin rash" },
    ],
  },
  {
    id: "conditions",
    title: "Chronic Conditions",
    icon: Stethoscope,
    badge: "1 active",
    content: [
      { label: "Hypertension (Type 2)", value: "Diagnosed 2018 · Managed with medication" },
    ],
  },
  {
    id: "medications",
    title: "Current Medications",
    icon: Pill,
    badge: "3 active",
    content: [
      { label: "Lisinopril 10mg", value: "Once daily · For hypertension" },
      { label: "Metformin 500mg", value: "Twice daily · For blood sugar" },
      { label: "Aspirin 75mg", value: "Once daily · Cardioprotective" },
    ],
  },
];

export default function PatientRecordsPage(): React.ReactElement {
  const [openSections, setOpenSections] = useState<string[]>(["personal"]);

  const toggle = (id: string) => {
    setOpenSections((prev) =>
      prev.includes(id) ? prev.filter((s) => s !== id) : [...prev, id]
    );
  };

  return (
    <div className="p-4 space-y-4">
      <motion.div initial={{ opacity: 0, y: 8 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.3 }}>
        <h1 className="text-xl font-bold text-mirageBlack">My Health Records</h1>
        <p className="text-xs text-clinicalGrey">Your complete medical history</p>
      </motion.div>

      <div className="space-y-2">
        {recordSections.map((section, i) => {
          const Icon = section.icon;
          const isOpen = openSections.includes(section.id);
          return (
            <motion.div
              key={section.id}
              initial={{ opacity: 0, y: 8 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: i * 0.05, duration: 0.3 }}
              className="bg-white border border-border rounded-xl overflow-hidden"
            >
              <button
                onClick={() => toggle(section.id)}
                className="w-full flex items-center gap-3 p-3 text-left"
              >
                <div className="w-8 h-8 rounded-lg bg-celestialBlue/10 flex items-center justify-center shrink-0">
                  <Icon className="w-4 h-4 text-celestialBlue" />
                </div>
                <div className="flex-1">
                  <p className="text-sm font-medium text-mirageBlack">{section.title}</p>
                </div>
                {section.badge && (
                  <span className="text-[10px] px-2 py-0.5 bg-healthGreen/10 text-healthGreen rounded-full font-medium">
                    {section.badge}
                  </span>
                )}
                {isOpen ? (
                  <ChevronUp className="w-4 h-4 text-clinicalGrey" />
                ) : (
                  <ChevronDown className="w-4 h-4 text-clinicalGrey" />
                )}
              </button>
              {isOpen && (
                <motion.div
                  initial={{ height: 0, opacity: 0 }}
                  animate={{ height: "auto", opacity: 1 }}
                  className="px-3 pb-3 space-y-2"
                >
                  {section.content.map((item) => (
                    <div key={item.label} className="flex justify-between items-start py-1.5 border-b border-border/50 last:border-0">
                      <span className="text-xs text-clinicalGrey">{item.label}</span>
                      <span className="text-xs font-medium text-mirageBlack text-right max-w-[60%]">{item.value}</span>
                    </div>
                  ))}
                </motion.div>
              )}
            </motion.div>
          );
        })}
      </div>
    </div>
  );
}
