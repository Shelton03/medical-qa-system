"use client";

import React from "react";
import { motion } from "framer-motion";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { Bell, MailOpen, CheckCheck } from "lucide-react";
import { notificationsApi } from "@/lib/api";
import { NotificationCard } from "@/components/patient/NotificationCard";
import { LoadingSkeleton } from "@/components/ui/LoadingSkeleton";
import { EmptyState } from "@/components/ui/EmptyState";
import { useToast } from "@/hooks/useToast";

export default function PatientNotificationsPage(): React.ReactElement {
  const { showToast } = useToast();
  const queryClient = useQueryClient();

  const {
    data: notificationData,
    isLoading,
    error,
  } = useQuery({
    queryKey: ["patient-notifications"],
    queryFn: () => notificationsApi.listNotifications({ limit: 50 }),
  });

  const markReadMutation = useMutation({
    mutationFn: (id: string) => notificationsApi.markRead(id),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["patient-notifications"] });
      queryClient.invalidateQueries({ queryKey: ["notifications-unread"] });
    },
    onError: (err: unknown) => {
      const msg = err instanceof Error ? err.message : "Failed to mark as read";
      showToast({ title: "Error", message: msg, type: "error" });
    },
  });

  const markAllReadMutation = useMutation({
    mutationFn: () => notificationsApi.markAllRead(),
    onSuccess: (result) => {
      showToast({
        title: "Marked as read",
        message: `${result.count} notification(s) marked as read.`,
        type: "success",
      });
      queryClient.invalidateQueries({ queryKey: ["patient-notifications"] });
      queryClient.invalidateQueries({ queryKey: ["notifications-unread"] });
    },
    onError: (err: unknown) => {
      const msg = err instanceof Error ? err.message : "Failed to mark all as read";
      showToast({ title: "Error", message: msg, type: "error" });
    },
  });

  const notifications = notificationData?.items ?? [];
  const unreadCount = notifications.filter((n) => !n.is_read).length;

  return (
    <div className="p-4 space-y-4 pb-20">
      <motion.div
        initial={{ opacity: 0, y: 8 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.3 }}
        className="flex items-center justify-between"
      >
        <div>
          <h1 className="text-page-title font-heading text-mirageBlack">Notifications</h1>
          <p className="text-caption text-clinicalGrey">
            {unreadCount > 0 ? `${unreadCount} unread` : "You're all caught up"}
          </p>
        </div>
        {unreadCount > 0 && (
          <button
            onClick={() => markAllReadMutation.mutate()}
            disabled={markAllReadMutation.isPending}
            className="flex items-center gap-1.5 px-3 py-2 bg-mirageBlack text-white rounded-button text-micro font-medium hover:bg-mirageBlack-700 transition-colors disabled:opacity-50"
          >
            <CheckCheck className="w-3.5 h-3.5" />
            Mark all read
          </button>
        )}
      </motion.div>

      {isLoading && <LoadingSkeleton type="list" count={4} />}

      {error && (
        <EmptyState
          icon={<Bell className="w-8 h-8 text-errorRed" />}
          title="Could not load notifications"
          description="Something went wrong while fetching notifications. Please try again later."
        />
      )}

      {!isLoading && !error && notifications.length === 0 && (
        <EmptyState
          icon={<MailOpen className="w-8 h-8 text-clinicalGrey" />}
          title="No notifications yet"
          description="We'll notify you when there's something new."
        />
      )}

      {!isLoading && !error && notifications.length > 0 && (
        <div className="space-y-2">
          {notifications.map((notification, index) => (
            <motion.div
              key={notification.id}
              initial={{ opacity: 0, y: 8 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: index * 0.03, duration: 0.3 }}
            >
              <NotificationCard
                notification={notification}
                onClick={() => {
                  if (!notification.is_read) {
                    markReadMutation.mutate(notification.id);
                  }
                }}
              />
            </motion.div>
          ))}
        </div>
      )}
    </div>
  );
}
