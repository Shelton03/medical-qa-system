"use client";

import React from "react";
import Link from "next/link";
import { Bell } from "lucide-react";
import { useQuery } from "@tanstack/react-query";
import { notificationsApi, getStoredAccessToken } from "@/lib/api";

interface NotificationBellProps {
  href: string;
  variant?: "dark" | "light";
}

export function NotificationBell({ href, variant = "dark" }: NotificationBellProps): React.ReactElement {
  const token = typeof window !== "undefined" ? getStoredAccessToken() : null;
  const { data } = useQuery({
    queryKey: ["notifications", "unread-count"],
    queryFn: () => notificationsApi.getUnreadCount(),
    refetchInterval: 30_000,
    enabled: !!token,
  });

  const unreadCount = data?.count ?? 0;
  const iconColor = variant === "dark" ? "text-white" : "text-clinicalGrey";
  const hoverBg = variant === "dark" ? "hover:bg-white/10" : "hover:bg-secondary";

  return (
    <Link
      href={href}
      aria-label="Notifications"
      className={`relative p-2 rounded-full ${hoverBg} transition-colors touch-target`}
    >
      <Bell className={`w-5 h-5 ${iconColor}`} />
      {unreadCount > 0 && (
        <span className="absolute top-1 right-1 min-w-[18px] h-[18px] px-1 flex items-center justify-center bg-alertOrange text-white text-[10px] font-bold rounded-full border-2 border-mirageBlack">
          {unreadCount > 9 ? "9+" : unreadCount}
        </span>
      )}
    </Link>
  );
}
