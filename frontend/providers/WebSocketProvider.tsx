"use client";

import React, { useCallback, useEffect, useRef, useState } from "react";
import { WebSocketContext } from "@/hooks/useWebSocket";
import { notificationsApi } from "@/lib/api";
import type { ConsentStatus, Notification, WsEvent } from "@/lib/types";

const WS_URL = "ws://localhost:8000/ws/notifications";
const RECONNECT_DELAYS = [1000, 2000, 5000, 10000, 30000];
const HEARTBEAT_INTERVAL = 30000;

function getStoredAccessToken(): string | null {
  if (typeof window === "undefined") return null;
  return localStorage.getItem("mirage_access_token");
}

export function WebSocketProvider({ children }: { children: React.ReactNode }): React.ReactElement {
  const [isConnected, setIsConnected] = useState(false);
  const [notifications, setNotifications] = useState<Notification[]>([]);
  const [unreadCount, setUnreadCount] = useState(0);
  const socketRef = useRef<WebSocket | null>(null);
  const reconnectAttemptRef = useRef(0);
  const heartbeatRef = useRef<ReturnType<typeof setInterval> | null>(null);
  const reconnectTimeoutRef = useRef<ReturnType<typeof setTimeout> | null>(null);
  const isMountedRef = useRef(true);

  // Fetch initial notifications
  useEffect(() => {
    notificationsApi.listNotifications({ unread: false, pageSize: 50 }).then((data) => {
      if (isMountedRef.current) {
        setNotifications(data);
        setUnreadCount(data.filter((n) => !n.read).length);
      }
    }).catch(() => {
      // Silently fail — we'll retry when socket connects
    });
  }, []);

  const playNotificationSound = useCallback(() => {
    try {
      const AudioCtx = (window.AudioContext || (window as unknown as Record<string, unknown>).webkitAudioContext) as typeof AudioContext;
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
          case "CONSENT_REQUESTED":
            setNotifications((prev) => {
              const payload = msg.payload as { consentId: string; doctorId: string; patientId: string };
              const existing = prev.find((n) => n.id === payload.consentId);
              if (existing) return prev;
              const incoming: Notification = {
                id: payload.consentId,
                type: "CONSENT",
                title: "New Consent Request",
                body: "A doctor has requested access to your medical record.",
                read: false,
                createdAt: new Date().toISOString(),
              };
              return [incoming, ...prev];
            });
            setUnreadCount((c) => c + 1);
            playNotificationSound();
            break;

          case "CONSENT_APPROVED":
          case "CONSENT_DENIED":
          case "CONSENT_REVOKED": {
            const payloadConsent = msg.payload as { consentId: string };
            const normalizedStatus: ConsentStatus =
              msg.type === "CONSENT_APPROVED"
                ? "APPROVED"
                : msg.type === "CONSENT_DENIED"
                ? "DENIED"
                : "REVOKED";
            // Update local consent-related notifications if applicable
            setNotifications((prev) =>
              prev.map((n) =>
                n.id === payloadConsent.consentId
                  ? { ...n, read: true }
                  : n
              )
            );
            // Trigger a toast via console or custom event could go here
            break;
          }

          case "NOTIFICATION":
          case "NOTIFICATION_CREATED": {
            const payloadNote = msg.payload as unknown as Notification;
            setNotifications((prev) => {
              const existing = prev.find((n) => n.id === payloadNote.id);
              if (existing) return prev;
              return [payloadNote, ...prev];
            });
            setUnreadCount((c) => c + 1);
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
    [playNotificationSound]
  );

  const connect = useCallback(() => {
    if (!isMountedRef.current) return;
    const token = getStoredAccessToken();
    if (!token) return;

    const ws = new WebSocket(`${WS_URL}?token=${encodeURIComponent(token)}`);
    socketRef.current = ws;

    ws.onopen = () => {
      if (!isMountedRef.current) return;
      setIsConnected(true);
      reconnectAttemptRef.current = 0;
    };

    ws.onmessage = handleWsMessage;

    ws.onclose = () => {
      if (!isMountedRef.current) return;
      setIsConnected(false);

      const delay = RECONNECT_DELAYS[Math.min(reconnectAttemptRef.current, RECONNECT_DELAYS.length - 1)];
      reconnectAttemptRef.current += 1;

      reconnectTimeoutRef.current = setTimeout(() => {
        if (isMountedRef.current) connect();
      }, delay);
    };

    ws.onerror = () => {
      // Let onclose handle reconnection
      ws.close();
    };

    // Heartbeat
    heartbeatRef.current = setInterval(() => {
      if (ws.readyState === WebSocket.OPEN) {
        ws.send(JSON.stringify({ type: "heartbeat" }));
      }
    }, HEARTBEAT_INTERVAL);
  }, [handleWsMessage]);

  useEffect(() => {
    connect();
    return () => {
      isMountedRef.current = false;
      if (heartbeatRef.current) clearInterval(heartbeatRef.current);
      if (reconnectTimeoutRef.current) clearTimeout(reconnectTimeoutRef.current);
      if (socketRef.current) {
        socketRef.current.close();
      }
    };
  }, [connect]);

  // Re-establish socket when token changes (e.g. after login)
  useEffect(() => {
    const handleStorage = (e: StorageEvent) => {
      if (e.key === "mirage_access_token") {
        if (socketRef.current) socketRef.current.close();
        reconnectAttemptRef.current = 0;
        setTimeout(() => connect(), 100);
      }
    };
    window.addEventListener("storage", handleStorage);
    return () => window.removeEventListener("storage", handleStorage);
  }, [connect]);

  const markRead = useCallback(async (notificationId: string) => {
    setNotifications((prev) =>
      prev.map((n) => (n.id === notificationId ? { ...n, read: true } : n))
    );
    setUnreadCount((c) => Math.max(0, c - 1));
    try {
      await notificationsApi.markRead(notificationId);
    } catch {
      // Revert not necessary — badge sync via WebSocket handles it
    }
  }, []);

  const markAllRead = useCallback(async () => {
    setNotifications((prev) => prev.map((n) => ({ ...n, read: true })));
    setUnreadCount(0);
    try {
      await notificationsApi.markAllRead();
    } catch {
      // Ignore
    }
  }, []);

  return (
    <WebSocketContext.Provider
      value={{
        isConnected,
        notifications,
        unreadCount,
        markRead,
        markAllRead,
      }}
    >
      {children}
    </WebSocketContext.Provider>
  );
}
