"use client";

import React, { useState, useEffect, useRef } from "react";
import { motion } from "framer-motion";
import { useAuth } from "@/hooks/useAuth";
import { useToast } from "@/hooks/useToast";

const DEMO_DOCTOR_EMAIL = "dr.sarah.mirage@mirage.health";
const DEMO_DOCTOR_PASSWORD = "Healthathon2024!";

export default function DoctorLoginPage(): React.ReactElement {
  const { loginDoctor, isLoading } = useAuth();
  const { showToast } = useToast();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [showPassword, setShowPassword] = useState(false);
  const formRef = useRef<HTMLFormElement>(null);
  const demoSubmitScheduled = useRef(false);

  useEffect(() => {
    const params = new URLSearchParams(window.location.search);
    if (params.get("demo") === "1" && !demoSubmitScheduled.current) {
      demoSubmitScheduled.current = true;
      setEmail(DEMO_DOCTOR_EMAIL);
      setPassword(DEMO_DOCTOR_PASSWORD);
      // Auto-submit after a short delay for animation
      const timer = setTimeout(() => {
        formRef.current?.requestSubmit();
      }, 1500);
      return () => clearTimeout(timer);
    }
  }, []);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await loginDoctor(email, password);
    } catch (err: unknown) {
      const msg = err instanceof Error ? err.message : "Login failed";
      showToast({ title: "Error", message: msg, type: "error" });
    }
  };

  const fillDemo = () => {
    setEmail(DEMO_DOCTOR_EMAIL);
    setPassword(DEMO_DOCTOR_PASSWORD);
  };

  return (
    <div className="min-h-screen bg-stellarWhite flex items-center justify-center p-4">
      <motion.div
        initial={{ opacity: 0, y: 24 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5, ease: [0.22, 1, 0.36, 1] }}
        className="w-full max-w-md"
      >
        <div className="text-center mb-8">
          <div className="w-14 h-14 rounded-xl bg-mirageBlack flex items-center justify-center mx-auto mb-4">
            <span className="text-white font-bold text-xl">M</span>
          </div>
          <h1 className="text-2xl font-bold text-mirageBlack">Doctor Portal</h1>
          <p className="text-clinicalGrey mt-1">Sign in to access Mirage</p>
        </div>

        <form ref={formRef} onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-mirageBlack mb-1">Email</label>
            <input
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
              className="w-full px-4 py-2.5 rounded-lg border border-border bg-white text-mirageBlack focus:outline-none focus:ring-2 focus:ring-celestialBlue/30 focus:border-celestialBlue transition-all"
              placeholder="doctor@hospital.zw"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-mirageBlack mb-1">Password</label>
            <div className="relative">
              <input
                type={showPassword ? "text" : "password"}
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
                className="w-full px-4 py-2.5 rounded-lg border border-border bg-white text-mirageBlack focus:outline-none focus:ring-2 focus:ring-celestialBlue/30 focus:border-celestialBlue transition-all pr-10"
                placeholder="••••••••"
              />
              <button
                type="button"
                onClick={() => setShowPassword(!showPassword)}
                className="absolute right-3 top-1/2 -translate-y-1/2 text-clinicalGrey hover:text-mirageBlack text-sm"
              >
                {showPassword ? "Hide" : "Show"}
              </button>
            </div>
          </div>

          <button
            type="submit"
            disabled={isLoading}
            className="w-full py-2.5 bg-mirageBlack text-white rounded-lg font-medium hover:bg-mirageBlack/90 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {isLoading ? "Signing in..." : "Sign In"}
          </button>
        </form>

        <div className="mt-6 p-4 bg-celestialBlue/5 border border-celestialBlue/20 rounded-lg">
          <p className="text-xs font-medium text-celestialBlue mb-1">Demo Credentials</p>
          <p className="text-sm text-mirageBlack">
            <strong>Dr. Sarah Mirage</strong>
          </p>
          <p className="text-xs text-clinicalGrey">{DEMO_DOCTOR_EMAIL}</p>
          <p className="text-xs text-clinicalGrey">Password: {DEMO_DOCTOR_PASSWORD}</p>
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
