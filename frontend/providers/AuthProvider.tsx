"use client";

import React, { useCallback, useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import {
  authApi,
  clearStoredTokens,
  getStoredAccessToken,
  getStoredRefreshToken,
  setStoredTokens,
} from "@/lib/api";
import type { UserProfile, UserRole } from "@/lib/types";
import { AuthContext } from "@/hooks/useAuth";

interface AuthState {
  user: UserProfile | null;
  isLoading: boolean;
  isAuthenticated: boolean;
  role: UserRole | null;
}

export function AuthProvider({ children }: { children: React.ReactNode }): React.ReactElement {
  const router = useRouter();
  const [state, setState] = useState<AuthState>({
    user: null,
    isLoading: true,
    isAuthenticated: false,
    role: null,
  });

  const hydrateUser = useCallback(async () => {
    try {
      const profile = await authApi.getMe();
      setState({
        user: profile,
        isLoading: false,
        isAuthenticated: true,
        role: profile.role,
      });
    } catch {
      clearStoredTokens();
      setState({
        user: null,
        isLoading: false,
        isAuthenticated: false,
        role: null,
      });
    }
  }, []);

  const checkAuth = useCallback(async () => {
    const access = getStoredAccessToken();
    const refresh = getStoredRefreshToken();
    if (!access) {
      setState((prev) => ({ ...prev, isLoading: false }));
      return;
    }
    try {
      const profile = await authApi.getMe();
      setState({
        user: profile,
        isLoading: false,
        isAuthenticated: true,
        role: profile.role,
      });
    } catch {
      if (refresh) {
        try {
          const refreshed = await authApi.refreshToken(refresh);
          const role = state.role ?? "doctor";
          setStoredTokens(role, refreshed.access_token, refresh);
          await hydrateUser();
          return;
        } catch {
          // fallthrough
        }
      }
      clearStoredTokens();
      setState({
        user: null,
        isLoading: false,
        isAuthenticated: false,
        role: null,
      });
    }
  }, [hydrateUser, state.role]);

  useEffect(() => {
    checkAuth();
  }, [checkAuth]);

  const loginDoctor = useCallback(
    async (email: string, password: string) => {
      setState((prev) => ({ ...prev, isLoading: true }));
      try {
        const response = await authApi.loginDoctor(email, password);
        setStoredTokens("doctor", response.access_token, response.refresh_token);
        const profile = await authApi.getMe();
        setState({
          user: profile,
          isLoading: false,
          isAuthenticated: true,
          role: profile.role,
        });
        router.push("/doctor/dashboard");
      } catch (error) {
        setState((prev) => ({ ...prev, isLoading: false }));
        throw error;
      }
    },
    [router]
  );

  const loginPatient = useCallback(
    async (national_id: string, pin: string) => {
      setState((prev) => ({ ...prev, isLoading: true }));
      try {
        const response = await authApi.loginPatient(national_id, pin);
        setStoredTokens("patient", response.access_token, response.refresh_token);
        const profile = await authApi.getMe();
        setState({
          user: profile,
          isLoading: false,
          isAuthenticated: true,
          role: profile.role,
        });
        router.push("/patient/consent");
      } catch (error) {
        setState((prev) => ({ ...prev, isLoading: false }));
        throw error;
      }
    },
    [router]
  );

  const loginAdmin = useCallback(
    async (email: string, password: string) => {
      setState((prev) => ({ ...prev, isLoading: true }));
      try {
        const response = await authApi.loginAdmin(email, password);
        setStoredTokens("admin", response.access_token, response.refresh_token);
        const profile = await authApi.getMe();
        setState({
          user: profile,
          isLoading: false,
          isAuthenticated: true,
          role: profile.role,
        });
        router.push("/admin/dashboard");
      } catch (error) {
        setState((prev) => ({ ...prev, isLoading: false }));
        throw error;
      }
    },
    [router]
  );

  const logout = useCallback(async () => {
    setState((prev) => ({ ...prev, isLoading: true }));
    try {
      await authApi.logout();
    } catch {
      // Ignore logout errors
    } finally {
      clearStoredTokens();
      setState({
        user: null,
        isLoading: false,
        isAuthenticated: false,
        role: null,
      });
      router.push("/");
    }
  }, [router]);

  const value = {
    user: state.user,
    isLoading: state.isLoading,
    isAuthenticated: state.isAuthenticated,
    role: state.role,
    loginDoctor,
    loginAdmin,
    loginPatient,
    logout,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}
