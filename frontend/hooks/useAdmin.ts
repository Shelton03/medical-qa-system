"use client";

import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { adminApi } from "@/lib/api";
import type {
  AppointmentAdminFilters,
  ScheduleUpdateRequest,
  TimeOffAdminRequest,
} from "@/lib/types";

export function useAdminDashboard() {
  return useQuery({
    queryKey: ["admin", "dashboard"],
    queryFn: () => adminApi.getDashboard(),
  });
}

export function useAdminDoctors(params?: { limit?: number; offset?: number }) {
  return useQuery({
    queryKey: ["admin", "doctors", params],
    queryFn: () => adminApi.listDoctors(params),
  });
}

export function useAdminDoctorSchedule(doctorId: string) {
  return useQuery({
    queryKey: ["admin", "schedule", doctorId],
    queryFn: () => adminApi.getDoctorSchedule(doctorId),
    enabled: !!doctorId,
  });
}

export function useUpdateDoctorSchedule() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: ({
      doctorId,
      data,
    }: {
      doctorId: string;
      data: ScheduleUpdateRequest;
    }) => adminApi.updateDoctorSchedule(doctorId, data),
    onSuccess: (_, variables) => {
      queryClient.invalidateQueries({
        queryKey: ["admin", "schedule", variables.doctorId],
      });
      queryClient.invalidateQueries({ queryKey: ["admin", "doctors"] });
    },
  });
}

export function useAdminAppointments(filters?: AppointmentAdminFilters) {
  return useQuery({
    queryKey: ["admin", "appointments", filters],
    queryFn: () => adminApi.listAppointments(filters),
  });
}

export function useAdminTimeOff(doctorId: string) {
  return useQuery({
    queryKey: ["admin", "time-off", doctorId],
    queryFn: () => adminApi.listDoctorTimeOff(doctorId),
    enabled: !!doctorId,
  });
}

export function useAddTimeOff() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: ({
      doctorId,
      data,
    }: {
      doctorId: string;
      data: TimeOffAdminRequest;
    }) => adminApi.addTimeOff(doctorId, data),
    onSuccess: (_, variables) => {
      queryClient.invalidateQueries({
        queryKey: ["admin", "time-off", variables.doctorId],
      });
    },
  });
}

export function useApproveTimeOff() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (timeOffId: string) => adminApi.approveTimeOff(timeOffId),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["admin", "time-off"] });
    },
  });
}

export function useRejectTimeOff() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (timeOffId: string) => adminApi.rejectTimeOff(timeOffId),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["admin", "time-off"] });
    },
  });
}

export function useCancelAppointment() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (appointmentId: string) => adminApi.cancelAppointment(appointmentId),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["admin", "appointments"] });
      queryClient.invalidateQueries({ queryKey: ["appointments", "list"] });
    },
  });
}

export function useReassignDoctor() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: ({
      appointmentId,
      doctorId,
    }: {
      appointmentId: string;
      doctorId: string;
    }) => adminApi.reassignDoctor(appointmentId, doctorId),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["admin", "appointments"] });
      queryClient.invalidateQueries({ queryKey: ["appointments", "list"] });
    },
  });
}
