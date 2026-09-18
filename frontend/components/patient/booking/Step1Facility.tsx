"use client";

import React, { useState, useMemo } from "react";
import { motion } from "framer-motion";
import { Search, MapPin, Clock, ChevronRight } from "lucide-react";
import { useFacilitiesSearch } from "@/hooks/useFacilities";
import { LoadingSkeleton } from "@/components/ui/LoadingSkeleton";
import { EmptyState } from "@/components/ui/EmptyState";
import type { Facility } from "@/lib/types";

interface Step1FacilityProps {
  selectedFacilityId: string | null;
  onSelect: (facility: Facility) => void;
}

export function Step1Facility({
  selectedFacilityId,
  onSelect,
}: Step1FacilityProps): React.ReactElement {
  const [query, setQuery] = useState("");
  const debouncedQuery = useMemo(() => query.trim() || undefined, [query]);
  const { data, isLoading, error } = useFacilitiesSearch(debouncedQuery);

  const facilities = data?.items ?? [];

  return (
    <motion.div
      variants={{
        hidden: { x: 24, opacity: 0 },
        visible: { x: 0, opacity: 1, transition: { type: "spring", stiffness: 380, damping: 32 } },
        exit: { x: -24, opacity: 0, transition: { duration: 0.2, ease: "easeIn" } },
      }}
      initial="hidden"
      animate="visible"
      exit="exit"
      className="flex flex-col h-full px-4 pt-3"
    >
      <h3 className="text-section-title font-semibold text-mirageBlack mb-1">
        Select a Facility
      </h3>
      <p className="text-caption text-clinicalGrey mb-4">
        Choose the healthcare facility for your appointment.
      </p>

      <div className="relative mb-4">
        <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-clinicalGrey" />
        <input
          type="text"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="Search facilities..."
          className="w-full bg-stellarWhite-100 border border-border rounded-input pl-10 pr-4 py-2.5 text-body text-mirageBlack placeholder:text-clinicalGrey focus:outline-none focus:ring-2 focus:ring-celestialBlue/30"
        />
      </div>

      {isLoading && <LoadingSkeleton type="list" count={4} />}

      {!isLoading && error && (
        <EmptyState
          icon={<MapPin className="w-8 h-8 text-clinicalGrey" />}
          title="Could not load facilities"
          description="Something went wrong. Please try again later."
        />
      )}

      {!isLoading && !error && facilities.length === 0 && (
        <EmptyState
          icon={<MapPin className="w-8 h-8 text-clinicalGrey" />}
          title="No facilities found"
          description={query ? "Try a different search term." : "No facilities available at this time."}
        />
      )}

      {!isLoading && !error && facilities.length > 0 && (
        <div className="space-y-2 flex-1 overflow-y-auto pb-4">
          {facilities.map((facility) => {
            const isSelected = selectedFacilityId === facility.id;
            return (
              <button
                key={facility.id}
                onClick={() => onSelect(facility)}
                className={`w-full text-left bg-white border rounded-card p-3.5 flex items-center gap-3 transition-all min-h-[56px] ${
                  isSelected
                    ? "border-celestialBlue shadow-elevation-1"
                    : "border-border hover:shadow-elevation-1"
                }`}
              >
                <div
                  className={`w-10 h-10 rounded-lg flex items-center justify-center shrink-0 ${
                    isSelected
                      ? "bg-celestialBlue/10 text-celestialBlue"
                      : "bg-mirageBlack-50 text-mirageBlack"
                  }`}
                >
                  <MapPin className="w-5 h-5" />
                </div>
                <div className="flex-1 min-w-0">
                  <p className="text-body font-medium text-mirageBlack truncate">
                    {facility.name}
                  </p>
                  <p className="text-caption text-clinicalGrey truncate">
                    {facility.address}
                  </p>
                  <p className="text-micro text-clinicalGrey mt-0.5 flex items-center gap-1">
                    <Clock className="w-3 h-3" />
                    {facility.city}
                  </p>
                </div>
                <ChevronRight
                  className={`w-4 h-4 shrink-0 ${
                    isSelected ? "text-celestialBlue" : "text-clinicalGrey"
                  }`}
                />
              </button>
            );
          })}
        </div>
      )}
    </motion.div>
  );
}
