"use client";

import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { appointmentsApi } from "@/lib/api";
import type { AppointmentCreateRequest, AppointmentStatus, AppointmentResponse } from "@/lib/types";

const LIST_KEY = ["appointments", "list"] as const;

export function useAppointments(params?: {
  status?: AppointmentStatus;
  upcoming?: boolean;
  limit?: number;
  offset?: number;
}) {
  return useQuery({
    queryKey: [...LIST_KEY, params],
    queryFn: () => appointmentsApi.listMy(params),
  });
}

export function useAppointment(id: string | null) {
  return useQuery<AppointmentResponse>({
    queryKey: ["appointments", "detail", id],
    queryFn: () => {
      if (!id) throw new Error("No appointment id");
      return appointmentsApi.getById(id);
    },
    enabled: !!id,
  });
}

export function useCreateAppointment() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: appointmentsApi.create,
    onSuccess: () => {
      void queryClient.invalidateQueries({ queryKey: LIST_KEY });
    },
  });
}

export function useCancelAppointment() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: ({ id, reason }: { id: string; reason?: string }) =>
      appointmentsApi.cancel(id, reason),
    onSuccess: () => {
      void queryClient.invalidateQueries({ queryKey: LIST_KEY });
    },
  });
}

export function useStartConsultation() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: appointmentsApi.startConsultation,
    onSuccess: () => {
      void queryClient.invalidateQueries({ queryKey: LIST_KEY });
    },
  });
}
