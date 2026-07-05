"use client";

import React, { useState } from "react";
import { useAuth } from "@/hooks/useAuth";
import { useToast } from "@/hooks/useToast";
import { motion } from "framer-motion";
import { ShieldCheck, Eye, EyeOff } from "lucide-react";

export default function PatientLoginPage(): React.ReactElement {
  const { loginPatient, isLoading } = useAuth();
  const { showToast } = useToast();
  const [nationalId, setNationalId] = useState("");
  const [pin, setPin] = useState("");
  const [showPin, setShowPin] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!nationalId.trim() || !pin.trim()) {
      showToast({
        title: "Validation Error",
        message: "Please enter both National ID and PIN.",
        type: "warning",
      });
      return;
    }

    try {
      await loginPatient(nationalId.trim(), pin.trim());
    } catch (err) {
      const message =
        err instanceof Error
          ? err.message
          : "Login failed. Please check your credentials and try again.";
      showToast({
        title: "Login Failed",
        message,
        type: "error",
      });
    }
  };

  return (
    <div className="flex flex-col h-full px-5 py-6 bg-stellarWhite">
      <motion.div
        initial={{ opacity: 0, y: 16 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ type: "spring", stiffness: 380, damping: 32 }}
        className="flex-1 flex flex-col justify-center"
      >
        <div className="text-center mb-8">
          <div className="w-14 h-14 rounded-2xl bg-mirageBlack flex items-center justify-center mx-auto mb-5 shadow-elevation-2">
            <ShieldCheck className="w-7 h-7 text-white" />
          </div>
          <h1 className="text-page-title font-bold text-mirageBlack">
            Welcome to Mirage
          </h1>
          <p className="text-caption text-clinicalGrey mt-2">
            Your health record, securely in your hands.
          </p>
        </div>

        <form className="space-y-4" onSubmit={handleSubmit} noValidate>
          <div>
            <label
              htmlFor="patient-national-id"
              className="block text-micro uppercase tracking-wide text-clinicalGrey mb-1.5"
            >
              National ID
            </label>
            <input
              id="patient-national-id"
              type="text"
              autoComplete="username"
              value={nationalId}
              onChange={(e) => setNationalId(e.target.value)}
              placeholder="63-1234567X89"
              className="w-full px-4 py-3.5 rounded-input border border-input bg-white text-sm placeholder:text-clinicalGrey-400 focus:outline-none focus:ring-2 focus:ring-celestialBlue transition-shadow"
              disabled={isLoading}
            />
          </div>

          <div>
            <label
              htmlFor="patient-pin"
              className="block text-micro uppercase tracking-wide text-clinicalGrey mb-1.5"
            >
              PIN
            </label>
            <div className="relative">
              <input
                id="patient-pin"
                type={showPin ? "text" : "password"}
                autoComplete="current-password"
                value={pin}
                onChange={(e) => setPin(e.target.value)}
                placeholder="••••••"
                className="w-full px-4 py-3.5 rounded-input border border-input bg-white text-sm placeholder:text-clinicalGrey-400 focus:outline-none focus:ring-2 focus:ring-celestialBlue transition-shadow pr-11"
                disabled={isLoading}
              />
              <button
                type="button"
                onClick={() => setShowPin((s) => !s)}
                className="absolute right-3 top-1/2 -translate-y-1/2 p-1 text-clinicalGrey hover:text-mirageBlack transition-colors"
                aria-label={showPin ? "Hide PIN" : "Show PIN"}
                tabIndex={-1}
              >
                {showPin ? (
                  <EyeOff className="w-4 h-4" />
                ) : (
                  <Eye className="w-4 h-4" />
                )}
              </button>
            </div>
          </div>

          <button
            type="submit"
            disabled={isLoading}
            className="w-full py-3.5 rounded-button bg-mirageBlack text-white font-medium text-sm hover:bg-mirageBlack-600 transition-colors mt-2 disabled:opacity-60 disabled:cursor-not-allowed flex items-center justify-center gap-2"
          >
            {isLoading ? (
              <>
                <span className="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin" />
                Signing in...
              </>
            ) : (
              "Continue"
            )}
          </button>
        </form>

        <div className="mt-6 p-4 rounded-card bg-secondary/60 border border-border">
          <p className="text-micro uppercase tracking-wide text-clinicalGrey mb-2 font-medium">
            Demo Credentials
          </p>
          <div className="flex items-center gap-3">
            <div className="w-8 h-8 rounded-full bg-mirageBlack-100 flex items-center justify-center shrink-0">
              <span className="text-xs font-bold text-mirageBlack">TM</span>
            </div>
            <div className="text-sm">
              <p className="font-medium text-mirageBlack">Tendai Mutasa</p>
              <p className="text-caption text-clinicalGrey">
                63-1234567X89 / 123456
              </p>
            </div>
          </div>
        </div>
      </motion.div>

      <p className="text-center text-micro text-clinicalGrey mt-4">
        Protected by end-to-end encryption
      </p>
    </div>
  );
}
