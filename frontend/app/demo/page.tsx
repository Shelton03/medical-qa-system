"use client";

import React, { useState, useEffect, useCallback } from "react";
import { motion, AnimatePresence } from "framer-motion";
import dynamic from "next/dynamic";
import {
  Play,
  Pause,
  SkipForward,
  SkipBack,
  RotateCcw,
  ChevronUp,
  ChevronDown,
  Mic,
} from "lucide-react";

const PhoneFrame = dynamic(
  () => import("@/components/phone-frame/PhoneFrame").then((mod) => mod.PhoneFrame),
  { ssr: false }
);

// ------------------------------------------------------------------
// Demo Script — 10-step Healthathon flow
// ------------------------------------------------------------------

interface DemoStep {
  id: number;
  title: string;
  description: string;
  narration: string;
  doctorAction: string;
  patientAction: string;
  autoAdvanceDelay: number; // ms
}

const DEMO_STEPS: DemoStep[] = [
  {
    id: 1,
    title: "Introduction",
    description: "Welcome to the Mirage healthcare platform demonstration.",
    narration: "Welcome to Mirage — a unified healthcare platform connecting doctors and patients with AI-powered clinical insights and patient-controlled consent.",
    doctorAction: "Dr. Sarah Mirage is about to start her day.",
    patientAction: "Tendai Mutasa is waiting at home.",
    autoAdvanceDelay: 4000,
  },
  {
    id: 2,
    title: "Doctor Login",
    description: "Dr. Mirage logs into the Doctor Portal.",
    narration: "Dr. Mirage securely logs into the portal. Every session uses JWT authentication with role-based access control.",
    doctorAction: "Auto-login with demo credentials",
    patientAction: "—",
    autoAdvanceDelay: 3000,
  },
  {
    id: 3,
    title: "Patient Login",
    description: "Tendai Mutasa logs into the Patient App.",
    narration: "Meanwhile, Tendai opens the Mirage Patient App on his phone — a mobile-first interface for managing his health.",
    doctorAction: "—",
    patientAction: "Auto-login with demo credentials",
    autoAdvanceDelay: 3000,
  },
  {
    id: 4,
    title: "Search Patient",
    description: "Dr. Mirage searches for Tendai Mutasa.",
    narration: "Dr. Mirage searches for her patient. The system supports fuzzy search across name, national ID, and phone number.",
    doctorAction: "Search for 'Tendai Mutasa' — patient found",
    patientAction: "—",
    autoAdvanceDelay: 3500,
  },
  {
    id: 5,
    title: "Request Consent",
    description: "Dr. Mirage requests access to Tendai's medical records.",
    narration: "Before accessing any patient data, the doctor must request explicit consent. This is patient-controlled privacy by design.",
    doctorAction: "Create consent request for allergies, medications, and diagnoses",
    patientAction: "—",
    autoAdvanceDelay: 4000,
  },
  {
    id: 6,
    title: "Patient Receives Request",
    description: "Tendai receives a real-time consent notification.",
    narration: "Tendai instantly receives the consent request via real-time WebSocket notification. No polling, no delays.",
    doctorAction: "—",
    patientAction: "Notification appears in the Patient App",
    autoAdvanceDelay: 3000,
  },
  {
    id: 7,
    title: "Patient Approves",
    description: "Tendai reviews and approves the consent request.",
    narration: "Tendai reviews exactly what data the doctor wants to access, and approves. He can revoke this at any time.",
    doctorAction: "—",
    patientAction: "Tap 'Approve' — consent granted",
    autoAdvanceDelay: 4000,
  },
  {
    id: 8,
    title: "Doctor Sees Approval",
    description: "Dr. Mirage sees the consent status update in real-time.",
    narration: "The doctor's dashboard updates instantly. The consent status changes from Pending to Approved — with full audit logging.",
    doctorAction: "Consent list refreshes — status: Approved",
    patientAction: "—",
    autoAdvanceDelay: 3500,
  },
  {
    id: 9,
    title: "AI-Assisted Consultation",
    description: "Dr. Mirage starts a consultation with AI assistance.",
    narration: "With consent approved, Dr. Mirage starts a consultation. The AI clinical assistant analyzes Tendai's approved records and suggests differential diagnoses.",
    doctorAction: "Start consultation — AI generates differential diagnosis",
    patientAction: "—",
    autoAdvanceDelay: 4500,
  },
  {
    id: 10,
    title: "Patient Sees Updated Record",
    description: "Tendai views the updated health record with new diagnosis.",
    narration: "After the consultation, Tendai can view his updated health record — including the new diagnosis and prescribed treatment. Full transparency.",
    doctorAction: "—",
    patientAction: "View updated health records",
    autoAdvanceDelay: 4000,
  },
];

export default function DemoPage(): React.ReactElement {
  const [currentStep, setCurrentStep] = useState(0);
  const [isAutoRunning, setIsAutoRunning] = useState(false);
  const [panelCollapsed, setPanelCollapsed] = useState(false);
  const [showNarration, setShowNarration] = useState(true);

  const step = DEMO_STEPS[currentStep] ?? DEMO_STEPS[0];

  // Keyboard shortcuts
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.key === "ArrowRight") advanceStep();
      if (e.key === "ArrowLeft") previousStep();
      if (e.key === " ") {
        e.preventDefault();
        toggleAutoRun();
      }
      if (e.key === "r" || e.key === "R") resetDemo();
      if (e.key === "n" || e.key === "N") setShowNarration((s) => !s);
    };
    window.addEventListener("keydown", handleKeyDown);
    return () => window.removeEventListener("keydown", handleKeyDown);
  }, [currentStep, isAutoRunning]);

  // Auto-advance logic
  useEffect(() => {
    if (!isAutoRunning) return;
    if (currentStep >= DEMO_STEPS.length - 1) {
      setIsAutoRunning(false);
      return;
    }
    const timer = setTimeout(() => {
      advanceStep();
    }, step.autoAdvanceDelay);
    return () => clearTimeout(timer);
  }, [currentStep, isAutoRunning, step.autoAdvanceDelay]);

  const advanceStep = useCallback(() => {
    setCurrentStep((s) => Math.min(s + 1, DEMO_STEPS.length - 1));
  }, []);

  const previousStep = useCallback(() => {
    setCurrentStep((s) => Math.max(s - 1, 0));
  }, []);

  const toggleAutoRun = useCallback(() => {
    setIsAutoRunning((prev) => !prev);
  }, []);

  const resetDemo = useCallback(() => {
    setIsAutoRunning(false);
    setCurrentStep(0);
    // Reload both iframes to reset state
    const doctorFrame = document.getElementById("doctor-frame") as HTMLIFrameElement;
    const patientFrame = document.getElementById("patient-frame") as HTMLIFrameElement;
    if (doctorFrame) doctorFrame.src = "/doctor/login";
    if (patientFrame) patientFrame.src = "/patient/login";
  }, []);

  // Build iframe URLs based on current step
  const getDoctorUrl = () => {
    if (currentStep >= 1) return "/doctor/dashboard?demo=1"; // Auto-login from step 2
    return "/doctor/login";
  };

  const getPatientUrl = () => {
    if (currentStep >= 2) return "/patient/consent?demo=1"; // Auto-login from step 3
    return "/patient/login";
  };

  const progressPercent = ((currentStep + 1) / DEMO_STEPS.length) * 100;

  return (
    <div className="h-screen w-screen bg-deepSpace overflow-hidden flex flex-col">
      {/* Top Header */}
      <div className="h-12 bg-mirageBlack flex items-center justify-between px-4 shrink-0 z-20">
        <div className="flex items-center gap-3">
          <img
            src="/logo-icon.svg"
            alt="Mirage"
            className="h-7 w-auto"
          />
          <h1 className="text-sm font-semibold text-white">Mirage Healthathon Demo</h1>
          <span className="text-[10px] text-white/50 hidden sm:inline">Press Space to play/pause · → next · ← prev · N narration · R reset</span>
        </div>
        <div className="flex items-center gap-2">
          <span className="text-[10px] text-white/60">
            Step {currentStep + 1} of {DEMO_STEPS.length}
          </span>
          <div className="w-24 h-1.5 bg-white/10 rounded-full overflow-hidden">
            <motion.div
              className="h-full bg-celestialBlue rounded-full"
              animate={{ width: `${progressPercent}%` }}
              transition={{ duration: 0.3 }}
            />
          </div>
        </div>
      </div>

      {/* Main Split Panels */}
      <div className="flex-1 flex overflow-hidden">
        {/* Left — Doctor Portal */}
        <div className="flex-1 flex flex-col min-w-0">
          <div className="h-8 bg-deepSpace-50 flex items-center px-4 shrink-0 border-b border-white/5">
            <span className="text-[10px] font-semibold text-clinicalGrey-300 uppercase tracking-wider">
              Doctor Portal
            </span>
            {step.doctorAction !== "—" && (
              <span className="ml-auto text-[10px] text-celestialBlue">{step.doctorAction}</span>
            )}
          </div>
          <div className="flex-1 relative">
            <iframe
              id="doctor-frame"
              key={`doctor-${currentStep}`}
              src={getDoctorUrl()}
              title="Doctor Portal"
              className="absolute inset-0 w-full h-full border-0 bg-white"
              sandbox="allow-same-origin allow-scripts allow-forms allow-popups"
            />
          </div>
        </div>

        {/* Vertical Divider */}
        <div className="w-px bg-white/5 shrink-0" />

        {/* Right — Patient App in PhoneFrame */}
        <div className="w-[420px] lg:w-[440px] shrink-0 flex flex-col items-center justify-center bg-deepSpace relative">
          <div className="absolute top-2 left-0 right-0 text-center z-10">
            <span className="text-[10px] font-semibold text-clinicalGrey-300 uppercase tracking-wider">
              Patient Application
            </span>
            {step.patientAction !== "—" && (
              <span className="block text-[10px] text-celestialBlue mt-0.5">{step.patientAction}</span>
            )}
          </div>
          <PhoneFrame>
            <iframe
              id="patient-frame"
              key={`patient-${currentStep}`}
              src={getPatientUrl()}
              title="Patient Application"
              className="w-full h-full border-0 bg-stellarWhite"
              sandbox="allow-same-origin allow-scripts allow-forms allow-popups"
            />
          </PhoneFrame>
        </div>
      </div>

      {/* Demo Script Panel */}
      <AnimatePresence>
        {!panelCollapsed && (
          <motion.div
            initial={{ height: 0, opacity: 0 }}
            animate={{ height: "auto", opacity: 1 }}
            exit={{ height: 0, opacity: 0 }}
            className="bg-mirageBlack border-t border-white/10 shrink-0 overflow-hidden"
          >
            <div className="px-4 py-3">
              {/* Narration */}
              {showNarration && (
                <motion.div
                  key={step.id}
                  initial={{ opacity: 0, y: 4 }}
                  animate={{ opacity: 1, y: 0 }}
                  className="flex items-start gap-3 mb-3"
                >
                  <div className="w-6 h-6 rounded-full bg-celestialBlue/20 flex items-center justify-center shrink-0 mt-0.5">
                    <Mic className="w-3 h-3 text-celestialBlue" />
                  </div>
                  <div>
                    <p className="text-xs text-white font-medium">{step.title}</p>
                    <p className="text-[11px] text-white/70 leading-relaxed">{step.narration}</p>
                  </div>
                </motion.div>
              )}

              {/* Controls */}
              <div className="flex items-center gap-2">
                <button
                  onClick={previousStep}
                  disabled={currentStep === 0}
                  className="p-1.5 rounded-lg bg-white/5 hover:bg-white/10 transition-colors disabled:opacity-30"
                  title="Previous step (←)"
                >
                  <SkipBack className="w-4 h-4 text-white" />
                </button>

                <button
                  onClick={toggleAutoRun}
                  className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-celestialBlue hover:bg-celestialBlue/90 transition-colors"
                  title="Auto-play (Space)"
                >
                  {isAutoRunning ? (
                    <Pause className="w-3.5 h-3.5 text-white" />
                  ) : (
                    <Play className="w-3.5 h-3.5 text-white" />
                  )}
                  <span className="text-xs font-medium text-white">
                    {isAutoRunning ? "Pause" : "Auto-Play"}
                  </span>
                </button>

                <button
                  onClick={advanceStep}
                  disabled={currentStep === DEMO_STEPS.length - 1}
                  className="p-1.5 rounded-lg bg-white/5 hover:bg-white/10 transition-colors disabled:opacity-30"
                  title="Next step (→)"
                >
                  <SkipForward className="w-4 h-4 text-white" />
                </button>

                <div className="w-px h-5 bg-white/10 mx-1" />

                <button
                  onClick={resetDemo}
                  className="flex items-center gap-1.5 px-2 py-1.5 rounded-lg bg-white/5 hover:bg-white/10 transition-colors"
                  title="Reset demo (R)"
                >
                  <RotateCcw className="w-3.5 h-3.5 text-white/70" />
                  <span className="text-[11px] text-white/70">Reset</span>
                </button>

                <button
                  onClick={() => setShowNarration((s) => !s)}
                  className={`ml-auto text-[11px] px-2 py-1 rounded transition-colors ${
                    showNarration ? "text-celestialBlue bg-celestialBlue/10" : "text-white/40"
                  }`}
                >
                  Narration
                </button>
              </div>

              {/* Step dots */}
              <div className="flex gap-1 mt-2 justify-center">
                {DEMO_STEPS.map((s, i) => (
                  <button
                    key={s.id}
                    onClick={() => setCurrentStep(i)}
                    className={`w-1.5 h-1.5 rounded-full transition-colors ${
                      i === currentStep ? "bg-celestialBlue" : i < currentStep ? "bg-white/30" : "bg-white/10"
                    }`}
                    title={s.title}
                  />
                ))}
              </div>
            </div>
          </motion.div>
        )}
      </AnimatePresence>

      {/* Collapse toggle */}
      <button
        onClick={() => setPanelCollapsed((c) => !c)}
        className="h-6 bg-mirageBlack border-t border-white/5 flex items-center justify-center shrink-0 hover:bg-white/5 transition-colors"
      >
        {panelCollapsed ? (
          <ChevronUp className="w-3 h-3 text-white/40" />
        ) : (
          <ChevronDown className="w-3 h-3 text-white/40" />
        )}
      </button>
    </div>
  );
}
