"use client";

import React from "react";
import type { NotificationResponse, WsEvent } from "@/lib/types";

export interface WebSocketContextValue {
  isConnected: boolean;
  notifications: NotificationResponse[];
  unreadCount: number;
  markRead: (notificationId: string) => void;
  markAllRead: () => void;
}

export const WebSocketContext = React.createContext<WebSocketContextValue>({
  isConnected: false,
  notifications: [],
  unreadCount: 0,
  markRead: () => {},
  markAllRead: () => {},
});

export function useWebSocket(): WebSocketContextValue {
  return React.useContext(WebSocketContext);
}
