"use client";

import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { scheduleApi } from "@/lib/api";
import type { TimeOffRequest, AppointmentStatus } from "@/lib/types";

export function useMySchedule() {
  return useQuery({
    queryKey: ["doctor", "schedule"],
    queryFn: () => scheduleApi.getMySchedule(),
  });
}

export function useMyAppointmentsToday() {
  return useQuery({
    queryKey: ["doctor", "appointments", "today"],
    queryFn: () => scheduleApi.getMyAppointmentsToday(),
  });
}

export function useMyAppointments() {
  return useQuery({
    queryKey: ["doctor", "appointments", "all"],
    queryFn: () => scheduleApi.getMyAppointments(),
  });
}

export function useUpdateAppointmentStatus() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: ({ id, status }: { id: string; status: AppointmentStatus }) =>
      scheduleApi.updateAppointmentStatus(id, status),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["doctor", "schedule"] });
      queryClient.invalidateQueries({ queryKey: ["doctor", "appointments", "today"] });
      queryClient.invalidateQueries({ queryKey: ["doctor", "appointments", "all"] });
    },
  });
}

export function useRequestLeave() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (data: TimeOffRequest) => scheduleApi.requestLeave(data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["doctor", "schedule"] });
    },
  });
}
