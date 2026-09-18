import React from "react";
import { PatientBottomNav } from "@/components/patient/BottomNav";
import { NotificationBell } from "@/components/notifications/NotificationBell";

interface PatientLayoutProps {
  children: React.ReactNode;
}

export default function PatientLayout({ children }: PatientLayoutProps): React.ReactElement {
  return (
    <div className="flex flex-col h-full bg-stellarWhite">
      {/* Header */}
      <header className="shrink-0 h-14 bg-mirageBlack flex items-center justify-between px-4">
        <div className="flex items-center gap-2">
          <img
            src="/logo-icon.svg"
            alt="Mirage"
            className="h-7 w-auto"
          />
          <span className="text-white font-semibold text-sm">Mirage</span>
        </div>
        <NotificationBell href="/patient/notifications" variant="dark" />
      </header>

      {/* Content */}
      <main className="flex-1 overflow-y-auto scrollbar-hide pb-16">
        {children}
      </main>

      {/* Bottom Navigation */}
      <PatientBottomNav />
    </div>
  );
}
