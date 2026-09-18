import React from "react";
import { Bell } from "lucide-react";
import { PatientBottomNav } from "@/components/patient/BottomNav";

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
        <button
          aria-label="Notifications"
          className="relative p-2 rounded-full hover:bg-white/10 transition-colors touch-target"
        >
          <Bell className="w-5 h-5 text-white" />
          <span className="absolute top-1.5 right-1.5 w-2 h-2 bg-alertOrange rounded-full" />
        </button>
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
