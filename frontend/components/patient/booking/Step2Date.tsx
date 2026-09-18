"use client";

import React, { useState, useMemo } from "react";
import { motion } from "framer-motion";
import { ChevronLeft, ChevronRight, AlertTriangle } from "lucide-react";
import { cn } from "@/lib/utils";

interface Step2DateProps {
  selectedDate: string | null;
  isEmergency: boolean;
  onSelectDate: (date: string) => void;
  onToggleEmergency: (v: boolean) => void;
}

function getMonthData(year: number, month: number) {
  const firstDay = new Date(year, month, 1);
  const daysInMonth = new Date(year, month + 1, 0).getDate();
  const startDay = firstDay.getDay(); // 0 = Sun
  const today = new Date();
  today.setHours(0, 0, 0, 0);
  return { daysInMonth, startDay, today };
}

function formatISODate(year: number, month: number, day: number): string {
  const m = String(month + 1).padStart(2, "0");
  const d = String(day).padStart(2, "0");
  return `${year}-${m}-${d}`;
}

export function Step2Date({
  selectedDate,
  isEmergency,
  onSelectDate,
  onToggleEmergency,
}: Step2DateProps): React.ReactElement {
  const now = new Date();
  const [year, setYear] = useState(now.getFullYear());
  const [month, setMonth] = useState(now.getMonth());

  const { daysInMonth, startDay, today } = useMemo(
    () => getMonthData(year, month),
    [year, month]
  );

  const monthLabel = useMemo(
    () =>
      new Date(year, month).toLocaleDateString("en-US", {
        month: "long",
        year: "numeric",
      }),
    [year, month]
  );

  const canGoBack =
    year > today.getFullYear() ||
    (year === today.getFullYear() && month > today.getMonth());

  const handlePrev = () => {
    if (!canGoBack) return;
    if (month === 0) {
      setMonth(11);
      setYear((y) => y - 1);
    } else {
      setMonth((m) => m - 1);
    }
  };

  const handleNext = () => {
    if (month === 11) {
      setMonth(0);
      setYear((y) => y + 1);
    } else {
      setMonth((m) => m + 1);
    }
  };

  const isPast = (day: number) => {
    const d = new Date(year, month, day);
    d.setHours(0, 0, 0, 0);
    return d.getTime() < today.getTime();
  };

  const isSelected = (day: number) => {
    if (!selectedDate) return false;
    return selectedDate === formatISODate(year, month, day);
  };

  return (
    <motion.div
      variants={{
        hidden: { x: 24, opacity: 0 },
        visible: { x: 0, opacity: 1, transition: { type: "spring", stiffness: 380, damping: 32 } },
        exit: { x: -24, opacity: 0, transition: { duration: 0.2, ease: "easeIn" } },
      }}
      initial="hidden"
      animate="visible"
      exit="exit"
      className="flex flex-col h-full px-4 pt-3"
    >
      <h3 className="text-section-title font-semibold text-mirageBlack mb-1">
        Select a Date
      </h3>
      <p className="text-caption text-clinicalGrey mb-4">
        Pick the day you would like to visit.
      </p>

      {/* Calendar Nav */}
      <div className="flex items-center justify-between mb-4">
        <button
          onClick={handlePrev}
          disabled={!canGoBack}
          className="w-9 h-9 rounded-full flex items-center justify-center disabled:opacity-30 active:bg-stellarWhite-200 transition-colors"
          aria-label="Previous month"
        >
          <ChevronLeft className="w-5 h-5 text-mirageBlack" />
        </button>
        <span className="text-body font-semibold text-mirageBlack">
          {monthLabel}
        </span>
        <button
          onClick={handleNext}
          className="w-9 h-9 rounded-full flex items-center justify-center active:bg-stellarWhite-200 transition-colors"
          aria-label="Next month"
        >
          <ChevronRight className="w-5 h-5 text-mirageBlack" />
        </button>
      </div>

      {/* Weekday headers */}
      <div className="grid grid-cols-7 gap-1 mb-1">
        {["S", "M", "T", "W", "T", "F", "S"].map((d) => (
          <div
            key={d}
            className="text-center text-micro font-medium text-clinicalGrey py-1"
          >
            {d}
          </div>
        ))}
      </div>

      {/* Days */}
      <div className="grid grid-cols-7 gap-1 mb-6">
        {Array.from({ length: startDay }).map((_, i) => (
          <div key={`pad-${i}`} className="aspect-square" />
        ))}
        {Array.from({ length: daysInMonth }).map((_, i) => {
          const day = i + 1;
          const past = isPast(day);
          const sel = isSelected(day);
          return (
            <button
              key={day}
              onClick={() => {
                if (!past) onSelectDate(formatISODate(year, month, day));
              }}
              disabled={past}
              className={cn(
                "aspect-square rounded-xl flex items-center justify-center text-body font-medium transition-colors",
                sel
                  ? "bg-celestialBlue text-white shadow-elevation-1"
                  : past
                  ? "text-clinicalGrey-300 cursor-not-allowed"
                  : "text-mirageBlack hover:bg-celestialBlue-50 active:bg-celestialBlue-100"
              )}
            >
              {day}
            </button>
          );
        })}
      </div>

      {/* Emergency toggle */}
      <div className="mt-auto pb-4">
        <div
          className={cn(
            "rounded-card p-4 border transition-colors",
            isEmergency
              ? "bg-alertOrange-50 border-alertOrange/30"
              : "bg-white border-border"
          )}
        >
          <label className="flex items-start gap-3 cursor-pointer min-h-[44px]">
            <input
              type="checkbox"
              checked={isEmergency}
              onChange={(e) => onToggleEmergency(e.target.checked)}
              className="mt-1 w-5 h-5 accent-alertOrange shrink-0"
            />
            <div className="flex-1">
              <div className="flex items-center gap-2">
                <AlertTriangle
                  className={cn(
                    "w-4 h-4",
                    isEmergency ? "text-alertOrange" : "text-clinicalGrey"
                  )}
                />
                <span
                  className={cn(
                    "text-body font-medium",
                    isEmergency ? "text-alertOrange" : "text-mirageBlack"
                  )}
                >
                  This is an emergency
                </span>
              </div>
              {isEmergency && (
                <motion.p
                  initial={{ opacity: 0, height: 0 }}
                  animate={{ opacity: 1, height: "auto" }}
                  className="text-caption text-alertOrange mt-1"
                >
                  If you are experiencing a life-threatening emergency, call
                  emergency services immediately.
                </motion.p>
              )}
            </div>
          </label>
        </div>
      </div>
    </motion.div>
  );
}
