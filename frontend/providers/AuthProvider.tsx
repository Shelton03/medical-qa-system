"use client";

import React, { useCallback, useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { authApi, clearStoredTokens, setStoredTokens } from "@/lib/api";
import type { UserProfile, UserRole } from "@/lib/types";
import { AuthContext } from "@/hooks/useAuth";

interface AuthState {
  user: UserProfile | null;
  isLoading: boolean;
  isAuthenticated: boolean;
  role: UserRole | null;
}

function readStoredTokens(role: UserRole): { access: string | null; refresh: string | null } {
  if (typeof window === "undefined") return { access: null, refresh: null };
  const accessKey = `mirage_${role}_access_token`;
  const refreshKey = `mirage_${role}_refresh_token`;
  return {
    access: localStorage.getItem(accessKey),
    refresh: localStorage.getItem(refreshKey),
  };
}

function getActiveRole(): UserRole | null {
  if (typeof window === "undefined") return null;
  const path = window.location.pathname;
  if (path.startsWith("/doctor")) return "doctor";
  if (path.startsWith("/patient")) return "patient";
  if (path.startsWith("/admin")) return "admin";
  // Try to infer from any stored token
  for (const role of ["doctor", "patient", "admin"] as UserRole[]) {
    if (localStorage.getItem(`mirage_${role}_access_token`)) return role;
  }
  return null;
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
    const activeRole = getActiveRole();
    if (!activeRole) {
      setState((prev) => ({ ...prev, isLoading: false }));
      return;
    }
    const { access, refresh } = readStoredTokens(activeRole);
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
          setStoredTokens(activeRole, refreshed.access_token, refresh);
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
  }, [hydrateUser]);

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

  useEffect(() => {
    const handleWsAuthRequired = () => {
      const activeRole = getActiveRole();
      if (!activeRole) return;
      const { refresh } = readStoredTokens(activeRole);
      if (refresh) {
        authApi
          .refreshToken(refresh)
          .then((refreshed) => {
            setStoredTokens(activeRole, refreshed.access_token, refresh);
            // WebSocketProvider will reconnect on storage event
          })
          .catch(() => {
            clearStoredTokens();
            setState({
              user: null,
              isLoading: false,
              isAuthenticated: false,
              role: null,
            });
            router.push("/doctor/login");
          });
      } else {
        clearStoredTokens();
        setState({
          user: null,
          isLoading: false,
          isAuthenticated: false,
          role: null,
        });
        router.push("/doctor/login");
      }
    };

    window.addEventListener("mirage:ws_auth_required", handleWsAuthRequired);
    return () => window.removeEventListener("mirage:ws_auth_required", handleWsAuthRequired);
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
