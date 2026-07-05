'use client';

import React from 'react';
import dynamic from 'next/dynamic';

const PhoneFrame = dynamic(
  () => import('@/components/phone-frame/PhoneFrame').then((mod) => mod.PhoneFrame),
  { ssr: false }
);

/**
 * Split-Screen Demo Page
 *
 * The critical screen for Healthathons.
 * Left side: Doctor Portal (live app rendered via iframe at /doctor/dashboard).
 * Right side: PhoneFrame wrapping Patient App (live app rendered via iframe at /patient/login).
 *
 * Both applications communicate exclusively through the backend.
 */
export default function DemoPage(): React.ReactElement {
  return (
    <div className="h-screen w-screen bg-deepSpace overflow-hidden flex">
      {/* Left Panel — Doctor Portal */}
      <div className="flex-1 flex flex-col min-w-0">
        <div className="h-10 bg-deepSpace-50 flex items-center px-4 shrink-0">
          <span className="text-xs font-semibold text-clinicalGrey-300 uppercase tracking-wider">
            Doctor Portal
          </span>
        </div>
        <div className="flex-1 relative">
          <iframe
            src="/doctor/dashboard"
            title="Doctor Portal"
            className="absolute inset-0 w-full h-full border-0"
            sandbox="allow-same-origin allow-scripts allow-forms allow-popups"
          />
        </div>
      </div>

      {/* Divider */}
      <div className="w-px bg-white/10 shrink-0" />

      {/* Right Panel — Patient Phone */}
      <div className="w-[420px] lg:w-[440px] shrink-0 flex flex-col items-center justify-center bg-deepSpace relative">
        <div className="absolute top-4 left-0 right-0 text-center">
          <span className="text-xs font-semibold text-clinicalGrey-300 uppercase tracking-wider">
            Patient Application
          </span>
        </div>
        <PhoneFrame>
          <iframe
            src="/patient/login"
            title="Patient Application"
            className="w-full h-full border-0 bg-stellarWhite"
            sandbox="allow-same-origin allow-scripts allow-forms allow-popups"
          />
        </PhoneFrame>
      </div>
    </div>
  );
}
