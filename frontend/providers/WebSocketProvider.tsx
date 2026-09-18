"use client";

import React, {
  useCallback,
  useEffect,
  useMemo,
  useRef,
  useState,
} from "react";
import { WebSocketContext } from "@/hooks/useWebSocket";
import { getStoredAccessToken, notificationsApi } from "@/lib/api";
import type { ConsentStatus, NotificationResponse, WsEvent } from "@/lib/types";

const WS_URL =
  typeof process !== "undefined" && process.env.NEXT_PUBLIC_WS_URL
    ? process.env.NEXT_PUBLIC_WS_URL
    : "ws://localhost:8002/ws/notifications";

// Absolute minimum time between reconnection attempts — prevents tight loops.
const MIN_RECONNECT_INTERVAL_MS = 5000;
const HEARTBEAT_INTERVAL_MS = 30000;

// Stable wrapper so internal WebSocket state churn doesn't re-render the rest of the app.
const StableChildren = React.memo(function StableChildren({
  children,
}: {
  children: React.ReactNode;
}) {
  return <>{children}</>;
});

function localGetStoredAccessToken(): string | null {
  if (typeof window === "undefined") return null;
  const roleKeys = [
    "mirage_doctor_access_token",
    "mirage_patient_access_token",
    "mirage_admin_access_token",
  ];
  for (const key of roleKeys) {
    const token = localStorage.getItem(key);
    if (token) return token;
  }
  return getStoredAccessToken();
}

export function WebSocketProvider({
  children,
}: {
  children: React.ReactNode;
}): React.ReactElement {
  // Expose a versioned snapshot to context consumers. Internals use refs to avoid re-rendering
  // the provider (and therefore the whole app) on every transient socket event.
  const [version, setVersion] = useState(0);

  const isConnectedRef = useRef(false);
  const notificationsRef = useRef<NotificationResponse[]>([]);
  const unreadCountRef = useRef(0);

  const socketRef = useRef<WebSocket | null>(null);
  const heartbeatRef = useRef<ReturnType<typeof setInterval> | null>(null);
  const reconnectTimeoutRef = useRef<ReturnType<typeof setTimeout> | null>(null);
  const lastReconnectRef = useRef<number>(0);
  const isMountedRef = useRef(true);

  const bump = useCallback(() => {
    if (isMountedRef.current) setVersion((v) => v + 1);
  }, []);

  // Fetch initial notifications only once per mount when a token exists.
  useEffect(() => {
    const token = localGetStoredAccessToken();
    if (!token) return;
    notificationsApi
      .listNotifications({ unread_only: false, limit: 50 })
      .then((data) => {
        if (!isMountedRef.current) return;
        notificationsRef.current = data.items;
        unreadCountRef.current = data.items.filter((n) => !n.is_read).length;
        bump();
      })
      .catch(() => {
        // Silently fail — we'll retry when socket connects
      });
  }, [bump]);

  const playNotificationSound = useCallback(() => {
    try {
      const AudioCtx = (window.AudioContext ||
        (window as unknown as Record<string, unknown>)
          .webkitAudioContext) as typeof AudioContext;
      if (!AudioCtx) return;
      const ctx = new AudioCtx();
      const osc = ctx.createOscillator();
      const gain = ctx.createGain();
      osc.connect(gain);
      gain.connect(ctx.destination);
      osc.frequency.value = 600;
      osc.type = "sine";
      gain.gain.setValueAtTime(0.05, ctx.currentTime);
      gain.gain.exponentialRampToValueAtTime(0.001, ctx.currentTime + 0.3);
      osc.start();
      osc.stop(ctx.currentTime + 0.3);
    } catch {
      /* ignore audio errors */
    }
  }, []);

  const handleWsMessage = useCallback(
    (event: MessageEvent) => {
      try {
        const msg = JSON.parse(event.data) as WsEvent;
        switch (msg.type) {
          case "CONSENT_REQUESTED": {
            const payload = msg.payload as {
              consentId: string;
              doctorId: string;
              patientId: string;
            };
            const existing = notificationsRef.current.find(
              (n) => n.id === payload.consentId
            );
            if (existing) break;
            const incoming: NotificationResponse = {
              id: payload.consentId,
              type: "CONSENT",
              title: "New Consent Request",
              body: "A doctor has requested access to your medical record.",
              is_read: false,
              created_at: new Date().toISOString(),
            };
            notificationsRef.current = [incoming, ...notificationsRef.current];
            unreadCountRef.current += 1;
            bump();
            playNotificationSound();
            break;
          }

          case "CONSENT_APPROVED":
          case "CONSENT_DECLINED":
          case "CONSENT_REVOKED": {
            const payloadConsent = msg.payload as { consentId: string };
            notificationsRef.current = notificationsRef.current.map((n) =>
              n.id === payloadConsent.consentId ? { ...n, is_read: true } : n
            );
            bump();
            break;
          }

          case "NOTIFICATION":
          case "NOTIFICATION_CREATED": {
            const payloadNote = msg.payload as unknown as NotificationResponse;
            const existing = notificationsRef.current.find(
              (n) => n.id === payloadNote.id
            );
            if (existing) break;
            notificationsRef.current = [payloadNote, ...notificationsRef.current];
            unreadCountRef.current += 1;
            bump();
            playNotificationSound();
            break;
          }

          default:
            break;
        }
      } catch {
        // Ignore malformed messages
      }
    },
    [bump, playNotificationSound]
  );

  const cleanupSocket = useCallback(() => {
    if (heartbeatRef.current) {
      clearInterval(heartbeatRef.current);
      heartbeatRef.current = null;
    }
    if (socketRef.current) {
      // Only close if still open/connecting to avoid errors on already-closed sockets.
      if (
        socketRef.current.readyState === WebSocket.OPEN ||
        socketRef.current.readyState === WebSocket.CONNECTING
      ) {
        socketRef.current.close();
      }
      socketRef.current = null;
    }
  }, []);

  const connect = useCallback(() => {
    if (!isMountedRef.current) return;
    const token = localGetStoredAccessToken();
    if (!token) return;

    // Enforce minimum reconnect interval to stop flashing loops.
    const now = Date.now();
    const timeSinceLast = now - lastReconnectRef.current;
    if (timeSinceLast < MIN_RECONNECT_INTERVAL_MS) {
      const wait = MIN_RECONNECT_INTERVAL_MS - timeSinceLast;
      reconnectTimeoutRef.current = setTimeout(() => connect(), wait);
      return;
    }
    lastReconnectRef.current = now;

    cleanupSocket();

    try {
      const ws = new WebSocket(`${WS_URL}?token=${encodeURIComponent(token)}`);
      socketRef.current = ws;

      ws.onopen = () => {
        if (!isMountedRef.current) return;
        isConnectedRef.current = true;
        bump();
      };

      ws.onmessage = handleWsMessage;

      ws.onclose = () => {
        if (!isMountedRef.current) return;
        if (isConnectedRef.current) {
          isConnectedRef.current = false;
          bump();
        }
        cleanupSocket();
        reconnectTimeoutRef.current = setTimeout(() => connect(), MIN_RECONNECT_INTERVAL_MS);
      };

      ws.onerror = () => {
        ws.close();
      };

      heartbeatRef.current = setInterval(() => {
        if (ws.readyState === WebSocket.OPEN) {
          ws.send(JSON.stringify({ type: "heartbeat" }));
        }
      }, HEARTBEAT_INTERVAL_MS);
    } catch {
      reconnectTimeoutRef.current = setTimeout(() => connect(), MIN_RECONNECT_INTERVAL_MS);
    }
  }, [bump, cleanupSocket, handleWsMessage]);

  useEffect(() => {
    connect();
    return () => {
      isMountedRef.current = false;
      if (reconnectTimeoutRef.current) clearTimeout(reconnectTimeoutRef.current);
      cleanupSocket();
    };
  }, [connect, cleanupSocket]);

  // Re-establish socket when token changes (e.g. after login)
  useEffect(() => {
    const handleStorage = (e: StorageEvent) => {
      const trackedKeys = [
        "mirage_doctor_access_token",
        "mirage_patient_access_token",
        "mirage_admin_access_token",
        "mirage_access_token",
      ];
      if (e.key && trackedKeys.includes(e.key)) {
        cleanupSocket();
        setTimeout(() => connect(), 100);
      }
    };
    window.addEventListener("storage", handleStorage);
    return () => window.removeEventListener("storage", handleStorage);
  }, [connect, cleanupSocket]);

  const markRead = useCallback(
    async (notificationId: string) => {
      const next = notificationsRef.current.map((n) =>
        n.id === notificationId ? { ...n, is_read: true } : n
      );
      notificationsRef.current = next;
      unreadCountRef.current = Math.max(
        0,
        next.filter((n) => !n.is_read).length
      );
      bump();
      try {
        await notificationsApi.markRead(notificationId);
      } catch {
        // Revert not necessary — badge sync via WebSocket handles it
      }
    },
    [bump]
  );

  const markAllRead = useCallback(async () => {
    notificationsRef.current = notificationsRef.current.map((n) => ({
      ...n,
      is_read: true,
    }));
    unreadCountRef.current = 0;
    bump();
    try {
      await notificationsApi.markAllRead();
    } catch {
      // Ignore
    }
  }, [bump]);

  const value = useMemo(
    () => ({
      isConnected: isConnectedRef.current,
      notifications: notificationsRef.current,
      unreadCount: unreadCountRef.current,
      markRead,
      markAllRead,
    }),
    // eslint-disable-next-line react-hooks/exhaustive-deps
    [version, markRead, markAllRead]
  );

  return (
    <WebSocketContext.Provider value={value}>
      <StableChildren>{children}</StableChildren>
    </WebSocketContext.Provider>
  );
}
