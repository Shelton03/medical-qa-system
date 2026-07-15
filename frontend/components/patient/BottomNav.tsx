"use client";

import React from "react";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { Home, FileText, Stethoscope, Bell, User } from "lucide-react";

const navItems = [
  { href: "/patient", label: "Home", icon: Home },
  { href: "/patient/timeline", label: "Timeline", icon: FileText },
  { href: "/patient/services", label: "Services", icon: Stethoscope },
  { href: "/patient/notifications", label: "Alerts", icon: Bell },
  { href: "/patient/profile", label: "Profile", icon: User },
];

export function PatientBottomNav(): React.ReactElement {
  const pathname = usePathname();

  return (
    <nav className="shrink-0 h-14 bg-white border-t border-border flex items-center justify-around fixed bottom-0 left-0 right-0 z-10">
      {navItems.map((item) => {
        const isActive = pathname === item.href || pathname?.startsWith(`${item.href}/`);
        return (
          <Link
            key={item.href}
            href={item.href}
            className={`flex flex-col items-center gap-0.5 py-1 px-3 transition-colors ${
              isActive ? "text-celestialBlue" : "text-clinicalGrey"
            }`}
          >
            <item.icon className="w-5 h-5" />
            <span className="text-[10px] font-medium">{item.label}</span>
          </Link>
        );
      })}
    </nav>
  );
}
