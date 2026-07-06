"use client";

export const dynamic = "force-dynamic";

import React, { Suspense } from "react";
import { Loader2 } from "lucide-react";
import SummaryContent from "./SummaryContent";

function LoadingFallback(): React.ReactElement {
  return (
    <div className="flex items-center justify-center h-screen">
      <div className="text-center">
        <Loader2 className="w-8 h-8 text-celestialBlue mx-auto mb-2 animate-spin" />
        <p className="text-sm text-clinicalGrey">Loading clinical summary...</p>
      </div>
    </div>
  );
}

export default function SummaryPage(): React.ReactElement {
  return (
    <Suspense fallback={<LoadingFallback />}>
      <SummaryContent />
    </Suspense>
  );
}
