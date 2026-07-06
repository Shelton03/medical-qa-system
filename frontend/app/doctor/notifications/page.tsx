"use client";

import React from "react";
import { motion } from "framer-motion";
import { useQuery, useMutation } from "@tanstack/react-query";
import { Bell, CheckCheck, AlertTriangle, FileText, ShieldCheck, Brain } from "lucide-react";
import { notificationsApi } from "@/lib/api";
import { useToast } from "@/hooks/useToast";
import type { NotificationResponse } from "@/lib/types";

const ICONS: Record<string, React.ReactNode> = {
  CONSENT: <ShieldCheck className="w-4 h-4 text-celestialBlue" />,
  MEDICAL_RECORD: <FileText className="w-4 h-4 text-healthGreen" />,
  AI: <Brain className="w-4 h-4 text-mirageBlack" />,
  SYSTEM: <AlertTriangle className="w-4 h-4 text-alertOrange" />,
};

const COLORS: Record<string, string> = {
  CONSENT: "bg-celestialBlue/5 border-celestialBlue/10",
  MEDICAL_RECORD: "bg-healthGreen/5 border-healthGreen/10",
  AI: "bg-mirageBlack/5 border-mirageBlack/10",
  SYSTEM: "bg-alertOrange/5 border-alertOrange/10",
};

export default function DoctorNotificationsPage(): React.ReactElement {
  const { showToast } = useToast();

  const { data, isLoading, refetch } = useQuery({
    queryKey: ["notifications"],
    queryFn: () => notificationsApi.listNotifications({ unread_only: false, limit: 50 }),
  });

  const markRead = useMutation({
    mutationFn: (id: string) => notificationsApi.markRead(id),
    onSuccess: () => refetch(),
  });

  const markAllRead = useMutation({
    mutationFn: () => notificationsApi.markAllRead(),
    onSuccess: () => {
      showToast({ title: "All Read", message: "All notifications marked as read.", type: "success" });
      refetch();
    },
  });

  const notifications = data?.items ?? [];
  const unreadCount = notifications.filter((n) => !n.is_read).length;

  return (
    <div className="space-y-6">
      <motion.div
        initial={{ opacity: 0, y: 12 }}
        animate={{ opacity: 1, y: 0 }}
        className="flex items-center justify-between"
      >
        <div>
          <h1 className="text-2xl font-bold text-mirageBlack">Notifications</h1>
          <p className="text-clinicalGrey">{unreadCount > 0 ? `${unreadCount} unread` : "You're all caught up"}</p>
        </div>
        {unreadCount > 0 && (
          <button
            onClick={() => markAllRead.mutate()}
            disabled={markAllRead.isPending}
            className="inline-flex items-center gap-2 px-4 py-2 bg-secondary text-mirageBlack rounded-lg text-sm font-medium hover:bg-secondary/80 transition-colors disabled:opacity-50"
          >
            <CheckCheck className="w-4 h-4" />
            Mark All Read
          </button>
        )}
      </motion.div>

      {isLoading ? (
        <div className="space-y-3">
          {[1, 2, 3].map((i) => (
            <div key={i} className="skeleton h-20 w-full rounded-card" />
          ))}
        </div>
      ) : notifications.length > 0 ? (
        <div className="space-y-3">
          {notifications.map((notification: NotificationResponse, i: number) => {
            const Icon = ICONS[notification.type] || <Bell className="w-4 h-4 text-clinicalGrey" />;
            const colorClass = COLORS[notification.type] || "bg-secondary border-border";
            return (
              <motion.div
                key={notification.id}
                initial={{ opacity: 0, y: 8 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: i * 0.03 }}
                className={`relative flex items-start gap-3 p-4 rounded-card border ${colorClass} ${
                  !notification.is_read ? "ring-1 ring-inset ring-celestialBlue/10" : ""
                }`}
              >
                {!notification.is_read && (
                  <span className="absolute top-4 right-4 w-2 h-2 bg-celestialBlue rounded-full" />
                )}
                <div className="w-8 h-8 rounded-full bg-white flex items-center justify-center shrink-0 mt-0.5 shadow-sm">
                  {Icon}
                </div>
                <div className="flex-1 min-w-0">
                  <p className="text-sm font-medium text-mirageBlack">{notification.title}</p>
                  {notification.body && (
                    <p className="text-caption text-clinicalGrey mt-0.5 leading-relaxed">{notification.body}</p>
                  )}
                  <p className="text-micro text-clinicalGrey mt-1.5">
                    {new Date(notification.created_at).toLocaleString()}
                  </p>
                </div>
                {!notification.is_read && (
                  <button
                    onClick={() => markRead.mutate(notification.id)}
                    disabled={markRead.isPending}
                    className="shrink-0 px-2.5 py-1 rounded-lg text-[10px] font-medium bg-white text-clinicalGrey hover:text-mirageBlack hover:bg-secondary transition-colors border border-border"
                  >
                    Mark Read
                  </button>
                )}
              </motion.div>
            );
          })}
        </div>
      ) : (
        <div className="text-center py-16 bg-white rounded-card border border-border">
          <Bell className="w-10 h-10 text-clinicalGrey mx-auto mb-3" />
          <p className="text-sm text-mirageBlack font-medium">No notifications</p>
          <p className="text-xs text-clinicalGrey mt-1">Consent updates and AI completions appear here.</p>
        </div>
      )}
    </div>
  );
}
