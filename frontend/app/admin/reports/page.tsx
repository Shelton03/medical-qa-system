"use client";

import React from "react";
import { motion } from "framer-motion";
import Link from "next/link";
import { useQuery } from "@tanstack/react-query";
import { adminApi } from "@/lib/api";
import { BarChart3 } from "lucide-react";

const spring = { type: "spring", stiffness: 380, damping: 32 };

export default function AdminReportsPage(): React.ReactElement {
  return (
    <div className="space-y-6">
      <motion.div initial={{ opacity: 0, y: 12 }} animate={{ opacity: 1, y: 0 }} transition={spring}>
        <h1 className="text-2xl font-bold text-mirageBlack">Reports</h1>
        <p className="text-clinicalGrey">Analytics and insights</p>
      </motion.div>

      <motion.div
        initial={{ opacity: 0, y: 12 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ ...spring, delay: 0.1 }}
        className="bg-white rounded-xl border border-border p-12 text-center"
      >
        <div className="w-16 h-16 rounded-full bg-celestialBlue/10 flex items-center justify-center mx-auto mb-4">
          <BarChart3 className="w-8 h-8 text-celestialBlue" />
        </div>
        <h2 className="text-xl font-semibold text-mirageBlack mb-2">Coming Soon</h2>
        <p className="text-clinicalGrey max-w-md mx-auto">
          Advanced reporting and analytics features are under development. 
          Check back later for facility occupancy trends, doctor utilization reports, 
          and patient appointment analytics.
        </p>
      </motion.div>
    </div>
  );
}
