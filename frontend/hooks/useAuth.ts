"use client";

import React from "react";
import type { UserProfile, UserRole } from "@/lib/types";

export interface AuthContextValue {
  user: UserProfile | null;
  isLoading: boolean;
  isAuthenticated: boolean;
  role: UserRole | null;
  loginDoctor: (email: string, password: string) => Promise<void>;
  loginPatient: (nationalId: string, pin: string) => Promise<void>;
  logout: () => void;
}

export const AuthContext = React.createContext<AuthContextValue>({
  user: null,
  isLoading: false,
  isAuthenticated: false,
  role: null,
  loginDoctor: async () => {},
  loginPatient: async () => {},
  logout: () => {},
});

export function useAuth(): AuthContextValue {
  return React.useContext(AuthContext);
}
