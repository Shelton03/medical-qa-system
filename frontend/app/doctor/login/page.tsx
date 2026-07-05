"use client";

import React, { useState } from "react";
import { useAuth } from "@/hooks/useAuth";
import { useToast } from "@/hooks/useToast";
import { motion } from "framer-motion";
import { Stethoscope, Eye, EyeOff } from "lucide-react";

export default function DoctorLoginPage(): React.ReactElement {
  const { loginDoctor, isLoading } = useAuth();
  const { showToast } = useToast();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [showPassword, setShowPassword] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!email.trim() || !password.trim()) {
      showToast({
        title: "Validation Error",
        message: "Please enter both email and password.",
        type: "warning",
      });
      return;
    }

    try {
      await loginDoctor(email.trim(), password.trim());
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
    <div className="min-h-screen flex items-center justify-center bg-stellarWhite px-6">
      <motion.div
        initial={{ opacity: 0, y: 16 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ type: "spring", stiffness: 380, damping: 32 }}
        className="w-full max-w-sm"
      >
        <div className="text-center mb-8">
          <div className="w-14 h-14 rounded-2xl bg-mirageBlack flex items-center justify-center mx-auto mb-4 shadow-elevation-2">
            <Stethoscope className="w-7 h-7 text-white" />
          </div>
          <h1 className="text-page-title font-bold text-mirageBlack">
            Doctor Portal
          </h1>
          <p className="text-caption text-clinicalGrey mt-2">
            Sign in to manage consultations and patient records
          </p>
        </div>

        <form className="space-y-4" onSubmit={handleSubmit} noValidate>
          <div>
            <label
              htmlFor="doctor-email"
              className="block text-micro uppercase tracking-wide text-clinicalGrey mb-1.5"
            >
              Email
            </label>
            <input
              id="doctor-email"
              type="email"
              autoComplete="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              placeholder="sarah.mirage@hararehospital.zw"
              className="w-full px-4 py-3 rounded-input border border-input bg-white text-sm placeholder:text-clinicalGrey-400 focus:outline-none focus:ring-2 focus:ring-celestialBlue transition-shadow"
              disabled={isLoading}
            />
          </div>

          <div>
            <label
              htmlFor="doctor-password"
              className="block text-micro uppercase tracking-wide text-clinicalGrey mb-1.5"
            >
              Password
            </label>
            <div className="relative">
              <input
                id="doctor-password"
                type={showPassword ? "text" : "password"}
                autoComplete="current-password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder="••••••••"
                className="w-full px-4 py-3 rounded-input border border-input bg-white text-sm placeholder:text-clinicalGrey-400 focus:outline-none focus:ring-2 focus:ring-celestialBlue transition-shadow pr-11"
                disabled={isLoading}
              />
              <button
                type="button"
                onClick={() => setShowPassword((s) => !s)}
                className="absolute right-3 top-1/2 -translate-y-1/2 p-1 text-clinicalGrey hover:text-mirageBlack transition-colors"
                aria-label={showPassword ? "Hide password" : "Show password"}
                tabIndex={-1}
              >
                {showPassword ? (
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
            className="w-full py-3 rounded-button bg-mirageBlack text-white font-medium text-sm hover:bg-mirageBlack-600 transition-colors disabled:opacity-60 disabled:cursor-not-allowed flex items-center justify-center gap-2"
          >
            {isLoading ? (
              <>
                <span className="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin" />
                Signing in...
              </>
            ) : (
              "Sign In"
            )}
          </button>
        </form>

        <div className="mt-6 p-4 rounded-card bg-secondary/60 border border-border">
          <p className="text-micro uppercase tracking-wide text-clinicalGrey mb-2 font-medium">
            Demo Credentials
          </p>
          <div className="flex items-center gap-3 mb-2">
            <div className="w-8 h-8 rounded-full bg-mirageBlack-100 flex items-center justify-center shrink-0">
              <span className="text-xs font-bold text-mirageBlack">SM</span>
            </div>
            <div className="text-sm">
              <p className="font-medium text-mirageBlack">Dr. Sarah Mirage</p>
              <p className="text-caption text-clinicalGrey">
                sarah.mirage@hararehospital.zw / password123
              </p>
            </div>
          </div>
        </div>
      </motion.div>
    </div>
  );
}
