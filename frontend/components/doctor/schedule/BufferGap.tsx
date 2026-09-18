"use client";

import React from "react";
import { cn } from "@/lib/utils";

interface BufferGapProps {
  top: number;
  height: number;
  className?: string;
}

export function BufferGap({ top, height, className }: BufferGapProps): React.ReactElement {
  return (
    <div
      className={cn("absolute left-2 right-2 pointer-events-none", className)}
      style={{ top, height }}
      aria-hidden="true"
      title="Buffer gap"
    >
      <div className="w-full h-full border-t border-dashed border-alertOrange/40 bg-alertOrange/5 rounded-sm" />
    </div>
  );
}
