"use client";

import React, { useCallback, useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { authApi } from "@/lib/api";
import type { UserProfile, UserRole } from "@/lib/types";
import { AuthContext } from "@/hooks/useAuth";

interface AuthState {
  user: UserProfile | null;
  isLoading: boolean;
  isAuthenticated: boolean;
  role: UserRole | null;
}

const STORAGE_KEYS = {
  accessToken: "mirage_access_token",
  refreshToken: "mirage_refresh_token",
} as const;

function readStoredTokens(): { access: string | null; refresh: string | null } {
  if (typeof window === "undefined") return { access: null, refresh: null };
  return {
    access: localStorage.getItem(STORAGE_KEYS.accessToken),
    refresh: localStorage.getItem(STORAGE_KEYS.refreshToken),
  };
}

function storeTokens(access: string, refresh: string): void {
  if (typeof window === "undefined") return;
  localStorage.setItem(STORAGE_KEYS.accessToken, access);
  localStorage.setItem(STORAGE_KEYS.refreshToken, refresh);
}

function clearTokens(): void {
  if (typeof window === "undefined") return;
  localStorage.removeItem(STORAGE_KEYS.accessToken);
  localStorage.removeItem(STORAGE_KEYS.refreshToken);
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
      clearTokens();
      setState({
        user: null,
        isLoading: false,
        isAuthenticated: false,
        role: null,
      });
    }
  }, []);

  const checkAuth = useCallback(async () => {
    const { access, refresh } = readStoredTokens();
    if (!access) {
      setState((prev) => ({ ...prev, isLoading: false }));
      return;
    }

    // Optimistically assume valid; getMe will clear if not
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
          storeTokens(refreshed.accessToken, refreshed.refreshToken);
          await hydrateUser();
          return;
        } catch {
          // Refresh failed — fallthrough to clear
        }
      }
      clearTokens();
      setState({
        user: null,
        isLoading: false,
        isAuthenticated: false,
        role: null,
      });
    }
  }, [hydrateUser]);

  useEffect(() => {
    checkAuth();
  }, [checkAuth]);

  const loginDoctor = useCallback(
    async (email: string, password: string) => {
      setState((prev) => ({ ...prev, isLoading: true }));
      try {
        const response = await authApi.loginDoctor(email, password);
        storeTokens(response.accessToken, response.refreshToken);
        setState({
          user: response.user,
          isLoading: false,
          isAuthenticated: true,
          role: response.user.role,
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
    async (nationalId: string, pin: string) => {
      setState((prev) => ({ ...prev, isLoading: true }));
      try {
        const response = await authApi.loginPatient(nationalId, pin);
        storeTokens(response.accessToken, response.refreshToken);
        setState({
          user: response.user,
          isLoading: false,
          isAuthenticated: true,
          role: response.user.role,
        });
        router.push("/patient/consent");
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
      // Ignore logout errors — always clear locally
    } finally {
      clearTokens();
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
    loginPatient,
    logout,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}
