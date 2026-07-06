"use client";

import React, { useCallback, useState } from "react";
import { AnimatePresence, motion } from "framer-motion";
import { X, CheckCircle, AlertCircle, Info, AlertTriangle } from "lucide-react";
import { ToastContext } from "@/hooks/useToast";

export type ToastType = "success" | "error" | "info" | "warning";

export interface ToastItem {
  id: string;
  title: string;
  message: string;
  type: ToastType;
  duration: number;
}

interface ToastProviderProps {
  children: React.ReactNode;
}

const TOAST_ICONS: Record<ToastType, React.ReactNode> = {
  success: <CheckCircle className="w-5 h-5 text-healthGreen" />,
  error: <AlertCircle className="w-5 h-5 text-alertOrange" />,
  info: <Info className="w-5 h-5 text-celestialBlue" />,
  warning: <AlertTriangle className="w-5 h-5 text-alertOrange" />,
};

const TOAST_STYLES: Record<ToastType, string> = {
  success: "border-l-4 border-healthGreen",
  error: "border-l-4 border-alertOrange",
  info: "border-l-4 border-celestialBlue",
  warning: "border-l-4 border-alertOrange",
};

export function ToastProvider({ children }: ToastProviderProps): React.ReactElement {
  const [toasts, setToasts] = useState<ToastItem[]>([]);

  const removeToast = useCallback((id: string) => {
    setToasts((prev) => prev.filter((t) => t.id !== id));
  }, []);

  const showToast = useCallback(
    (payload: {
      title: string;
      message: string;
      type: ToastType;
      duration?: number;
    }) => {
      const id = `${Date.now()}-${Math.random().toString(36).slice(2, 9)}`;
      const duration = payload.duration ?? 4000;

      const item: ToastItem = {
        id,
        title: payload.title,
        message: payload.message,
        type: payload.type,
        duration,
      };

      setToasts((prev) => [...prev, item]);

      setTimeout(() => {
        removeToast(id);
      }, duration);
    },
    [removeToast]
  );

  return (
    <ToastContext.Provider value={{ showToast }}>
      {children}

      {/* Toast overlay — doctor portal top-right; patient handled separately */}
      <div className="fixed top-4 right-4 z-[9999] flex flex-col gap-3 w-80 pointer-events-none">
        <AnimatePresence mode="popLayout">
          {toasts.map((toast) => (
            <motion.div
              key={toast.id}
              layout
              initial={{ opacity: 0, y: -24, scale: 0.98 }}
              animate={{ opacity: 1, y: 0, scale: 1 }}
              exit={{ opacity: 0, y: -16, scale: 0.98 }}
              transition={{ type: "spring", stiffness: 380, damping: 32 }}
              className={`pointer-events-auto glass-card rounded-card p-4 shadow-elevation-5 ${TOAST_STYLES[toast.type]}`}
            >
              <div className="flex items-start gap-3">
                {TOAST_ICONS[toast.type]}
                <div className="flex-1 min-w-0">
                  <h4 className="text-sm font-semibold text-mirageBlack">
                    {toast.title}
                  </h4>
                  <p className="text-caption text-clinicalGrey mt-0.5 leading-relaxed">
                    {toast.message}
                  </p>
                </div>
                <button
                  onClick={() => removeToast(toast.id)}
                  className="touch-target flex items-center justify-center -mr-1 -mt-1 text-clinicalGrey hover:text-mirageBlack transition-colors"
                  aria-label="Dismiss notification"
                >
                  <X className="w-4 h-4" />
                </button>
              </div>
            </motion.div>
          ))}
        </AnimatePresence>
      </div>
    </ToastContext.Provider>
  );
}
