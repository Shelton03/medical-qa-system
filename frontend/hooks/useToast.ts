"use client";

import React from "react";
import type { ToastType } from "@/providers/ToastProvider";

export interface ToastContextValue {
  showToast: (payload: {
    title: string;
    message: string;
    type: ToastType;
    duration?: number;
  }) => void;
}

export const ToastContext = React.createContext<ToastContextValue>({
  showToast: () => {},
});

export function useToast(): ToastContextValue {
  return React.useContext(ToastContext);
}
