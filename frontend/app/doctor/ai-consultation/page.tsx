"use client";

export const dynamic = "force-dynamic";

import React, { Suspense } from "react";
import { Loader2 } from "lucide-react";
import AIConsultationContent from "./AIConsultationContent";

function LoadingFallback(): React.ReactElement {
  return (
    <div className="h-[calc(100vh-64px)] flex items-center justify-center">
      <div className="text-center">
        <Loader2 className="w-8 h-8 text-celestialBlue mx-auto mb-2 animate-spin" />
        <p className="text-sm text-clinicalGrey">Loading AI consultation...</p>
      </div>
    </div>
  );
}

export default function AIConsultationPage(): React.ReactElement {
  return (
    <Suspense fallback={<LoadingFallback />}>
      <AIConsultationContent />
    </Suspense>
  );
}
