"use client";

import React, { useState, useEffect, useRef } from "react";
import { motion } from "framer-motion";
import { useAuth } from "@/hooks/useAuth";
import { useToast } from "@/hooks/useToast";

const DEMO_NATIONAL_ID = "ZIM-89-4567234";
const DEMO_PIN = "2024";

export default function PatientLoginPage(): React.ReactElement {
  const { loginPatient, isLoading } = useAuth();
  const { showToast } = useToast();
  const [nationalId, setNationalId] = useState("");
  const [pin, setPin] = useState("");
  const [showPin, setShowPin] = useState(false);
  const formRef = useRef<HTMLFormElement>(null);
  const demoSubmitScheduled = useRef(false);

  useEffect(() => {
    const params = new URLSearchParams(window.location.search);
    if (params.get("demo") === "1" && !demoSubmitScheduled.current) {
      demoSubmitScheduled.current = true;
      setNationalId(DEMO_NATIONAL_ID);
      setPin(DEMO_PIN);
      const timer = setTimeout(() => {
        formRef.current?.requestSubmit();
      }, 1500);
      return () => clearTimeout(timer);
    }
  }, []);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await loginPatient(nationalId, pin);
    } catch (err: unknown) {
      const msg = err instanceof Error ? err.message : "Login failed";
      showToast({ title: "Error", message: msg, type: "error" });
    }
  };

  const fillDemo = () => {
    setNationalId(DEMO_NATIONAL_ID);
    setPin(DEMO_PIN);
  };

  return (
    <div className="min-h-screen bg-stellarWhite flex items-center justify-center p-4">
      <motion.div
        initial={{ opacity: 0, y: 24 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5, ease: [0.22, 1, 0.36, 1] }}
        className="w-full max-w-sm"
      >
        <div className="text-center mb-8">
          <img
            src="/logo-icon.svg"
            alt="Mirage"
            className="h-14 w-auto mx-auto mb-4"
          />
          <h1 className="text-2xl font-bold text-mirageBlack">Patient Access</h1>
          <p className="text-clinicalGrey mt-1">Sign in with your National ID</p>
        </div>

        <form ref={formRef} onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-mirageBlack mb-1">National ID</label>
            <input
              type="text"
              value={nationalId}
              onChange={(e) => setNationalId(e.target.value)}
              required
              className="w-full px-4 py-2.5 rounded-lg border border-border bg-white text-mirageBlack focus:outline-none focus:ring-2 focus:ring-celestialBlue/30 focus:border-celestialBlue transition-all"
              placeholder="ZIM-89-4567234"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-mirageBlack mb-1">PIN</label>
            <div className="relative">
              <input
                type={showPin ? "text" : "password"}
                value={pin}
                onChange={(e) => setPin(e.target.value)}
                required
                className="w-full px-4 py-2.5 rounded-lg border border-border bg-white text-mirageBlack focus:outline-none focus:ring-2 focus:ring-celestialBlue/30 focus:border-celestialBlue transition-all pr-10"
                placeholder="••••"
              />
              <button
                type="button"
                onClick={() => setShowPin(!showPin)}
                className="absolute right-3 top-1/2 -translate-y-1/2 text-clinicalGrey hover:text-mirageBlack text-sm"
              >
                {showPin ? "Hide" : "Show"}
              </button>
            </div>
          </div>

          <button
            type="submit"
            disabled={isLoading}
            className="w-full py-2.5 bg-mirageBlack text-white rounded-lg font-medium hover:bg-mirageBlack/90 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {isLoading ? "Signing in..." : "Continue"}
          </button>
        </form>

        <div className="mt-6 p-4 bg-celestialBlue/5 border border-celestialBlue/20 rounded-lg">
          <p className="text-xs font-medium text-celestialBlue mb-1">Demo Credentials</p>
          <p className="text-sm text-mirageBlack">
            <strong>Tendai Mutasa</strong>
          </p>
          <p className="text-xs text-clinicalGrey">National ID: {DEMO_NATIONAL_ID}</p>
          <p className="text-xs text-clinicalGrey">PIN: {DEMO_PIN}</p>
          <button
            onClick={fillDemo}
            className="mt-2 text-xs text-celestialBlue hover:underline font-medium"
          >
            Fill demo credentials
          </button>
        </div>
      </motion.div>
    </div>
  );
}
