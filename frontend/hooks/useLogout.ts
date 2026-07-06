"use client";

import { useCallback } from "react";
import { useAuth } from "./useAuth";

/**
 * useLogout hook
 *
 * Provides a single logout function that:
 * - Calls the auth context logout (which hits /auth/logout, clears tokens, resets state)
 * - Redirects the user to the public landing page
 */
export function useLogout(): { logout: () => void; isLoggingOut: boolean } {
  const { logout: authLogout, isLoading } = useAuth();

  const logout = useCallback(() => {
    authLogout();
  }, [authLogout]);

  return { logout, isLoggingOut: isLoading };
}
