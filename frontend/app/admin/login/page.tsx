"use client";

import React, { useState, useEffect } from "react";
import { motion } from "framer-motion";
import { useAuth } from "@/hooks/useAuth";
import { useToast } from "@/hooks/useToast";

const DEMO_ADMIN_EMAIL = "admin@mirage.health";
const DEMO_ADMIN_PASSWORD = "Admin2024!";

export default function AdminLoginPage(): React.ReactElement {
  const { loginAdmin, isLoading } = useAuth();
  const { showToast } = useToast();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [showPassword, setShowPassword] = useState(false);

  useEffect(() => {
    const params = new URLSearchParams(window.location.search);
    if (params.get("demo") === "1") {
      setEmail(DEMO_ADMIN_EMAIL);
      setPassword(DEMO_ADMIN_PASSWORD);
      const timer = setTimeout(() => {
        const form = document.querySelector("form");
        if (form) form.requestSubmit();
      }, 1500);
      return () => clearTimeout(timer);
    }
  }, []);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await loginAdmin(email, password);
    } catch (err: unknown) {
      const msg = err instanceof Error ? err.message : "Login failed";
      showToast({ title: "Error", message: msg, type: "error" });
    }
  };

  const fillDemo = () => {
    setEmail(DEMO_ADMIN_EMAIL);
    setPassword(DEMO_ADMIN_PASSWORD);
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
          <div className="w-14 h-14 rounded-xl bg-deepSpace flex items-center justify-center mx-auto mb-4">
            <span className="text-white font-bold text-xl">M</span>
          </div>
          <h1 className="text-2xl font-bold text-mirageBlack">Admin Portal</h1>
          <p className="text-clinicalGrey mt-1">Sign in to manage Mirage</p>
        </div>

        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-mirageBlack mb-1">Email</label>
            <input
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
              className="w-full px-4 py-2.5 rounded-lg border border-border bg-white text-mirageBlack focus:outline-none focus:ring-2 focus:ring-celestialBlue/30 focus:border-celestialBlue transition-all"
              placeholder="admin@mirage.health"
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
            className="w-full py-2.5 bg-deepSpace text-white rounded-lg font-medium hover:bg-deepSpace-50 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {isLoading ? "Signing in..." : "Sign In"}
          </button>
        </form>

        <div className="mt-6 p-4 bg-celestialBlue/5 border border-celestialBlue/20 rounded-lg">
          <p className="text-xs font-medium text-celestialBlue mb-1">Demo Credentials</p>
          <p className="text-sm text-mirageBlack">
            <strong>Admin Demo</strong>
          </p>
          <p className="text-xs text-clinicalGrey">{DEMO_ADMIN_EMAIL}</p>
          <p className="text-xs text-clinicalGrey">Password: {DEMO_ADMIN_PASSWORD}</p>
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
