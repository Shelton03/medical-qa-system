"use client";

import React from "react";
import { motion } from "framer-motion";
import { User, LogOut } from "lucide-react";
import { useAuth } from "@/hooks/useAuth";

export default function PatientProfilePage(): React.ReactElement {
  const { logout } = useAuth();

  return (
    <div className="p-4 space-y-6">
      <motion.div initial={{ opacity: 0, y: 8 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.3 }}>
        <div className="flex flex-col items-center py-6">
          <div className="w-16 h-16 rounded-full bg-mirageBlack/10 flex items-center justify-center mb-3">
            <User className="w-8 h-8 text-mirageBlack" />
          </div>
          <h1 className="text-lg font-bold text-mirageBlack">Tendai Mutasa</h1>
          <p className="text-xs text-clinicalGrey">Patient ID: ZIM-89-4567234</p>
        </div>
      </motion.div>

      <motion.div
        initial={{ opacity: 0, y: 8 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.1, duration: 0.3 }}
        className="bg-white border border-border rounded-xl overflow-hidden"
      >
        <div className="p-3 border-b border-border">
          <p className="text-xs text-clinicalGrey">Emergency Contact</p>
          <p className="text-sm font-medium text-mirageBlack">Sekai Mutasa</p>
          <p className="text-xs text-clinicalGrey">+263 77 123 4567</p>
        </div>
        <div className="p-3">
          <p className="text-xs text-clinicalGrey">Insurance</p>
          <p className="text-sm font-medium text-mirageBlack">CIMAS Medical Aid</p>
          <p className="text-xs text-clinicalGrey">Policy: CMP-784321</p>
        </div>
      </motion.div>

      <motion.div initial={{ opacity: 0, y: 8 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.2, duration: 0.3 }}>
        <button
          onClick={() => logout()}
          className="w-full flex items-center justify-center gap-2 py-3 border border-red-200 text-red-600 rounded-xl text-sm font-medium hover:bg-red-50 transition-colors"
        >
          <LogOut className="w-4 h-4" />
          Sign Out
        </button>
      </motion.div>

      <div className="text-center pt-4">
        <p className="text-[10px] text-clinicalGrey">Mirage Health v1.0</p>
      </div>
    </div>
  );
}
