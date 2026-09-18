"use client";

import { useQuery } from "@tanstack/react-query";
import { facilitiesApi } from "@/lib/api";

export function useFacilitiesSearch(query?: string, enabled = true) {
  return useQuery({
    queryKey: ["facilities", "search", query],
    queryFn: () => facilitiesApi.search(query),
    enabled,
  });
}

export function useFacility(id: string | null) {
  return useQuery({
    queryKey: ["facilities", "detail", id],
    queryFn: () => {
      if (!id) throw new Error("No facility id");
      return facilitiesApi.getById(id);
    },
    enabled: !!id,
  });
}

export function useFacilityDoctors(id: string | null) {
  return useQuery({
    queryKey: ["facilities", "doctors", id],
    queryFn: () => {
      if (!id) throw new Error("No facility id");
      return facilitiesApi.getDoctors(id);
    },
    enabled: !!id,
  });
}
