"use client";

import React, { useEffect } from "react";
import Link from "next/link";
import { usePathname, useRouter } from "next/navigation";
import { cn } from "@/lib/utils";
import { useAuth } from "@/hooks/useAuth";
import {
  LayoutDashboard,
  Building2,
  Users,
  CalendarDays,
  CalendarCheck,
  BarChart3,
  Settings,
  LogOut,
  Search,
} from "lucide-react";

const navItems = [
  { label: "Dashboard", href: "/admin/dashboard", icon: LayoutDashboard },
  { label: "Facilities", href: "/admin/facilities", icon: Building2 },
  { label: "Doctors", href: "/admin/doctors", icon: Users },
  { label: "Schedules", href: "/admin/schedules", icon: CalendarDays },
  { label: "Appointments", href: "/admin/appointments", icon: CalendarCheck },
  { label: "Reports", href: "/admin/reports", icon: BarChart3 },
  { label: "Settings", href: "/admin/settings", icon: Settings },
];

export default function AdminLayout({
  children,
}: {
  children: React.ReactNode;
}): React.ReactElement {
  const { user, isLoading, isAuthenticated, logout } = useAuth();
  const router = useRouter();

  useEffect(() => {
    if (!isLoading && (!isAuthenticated || user?.role !== "admin")) {
      router.replace("/admin/login");
    }
  }, [isLoading, isAuthenticated, user, router]);

  if (isLoading) {
    return (
      <div className="min-h-screen bg-stellarWhite flex items-center justify-center">
        <div className="w-8 h-8 border-2 border-celestialBlue border-t-transparent rounded-full animate-spin" />
      </div>
    );
  }

  if (!isAuthenticated || user?.role !== "admin") {
    return (
      <div className="min-h-screen bg-stellarWhite flex items-center justify-center">
        <p className="text-clinicalGrey text-sm">Redirecting...</p>
      </div>
    );
  }

  return (
    <div className="flex h-screen bg-stellarWhite overflow-hidden">
      {/* Sidebar */}
      <aside className="w-64 shrink-0 border-r border-border bg-white flex flex-col">
        {/* Brand */}
        <div className="h-16 flex items-center px-6 border-b border-border">
          <div className="w-8 h-8 rounded-md bg-deepSpace flex items-center justify-center mr-3">
            <span className="text-white font-bold text-sm">M</span>
          </div>
          <span className="font-heading font-bold text-mirageBlack text-page-title">
            Mirage
          </span>
        </div>

        {/* Navigation */}
        <nav className="flex-1 px-3 py-4 space-y-1 overflow-y-auto">
          {navItems.map((item) => (
            <NavLink key={item.href} href={item.href} icon={item.icon} label={item.label} />
          ))}
        </nav>

        {/* Bottom actions */}
        <div className="px-3 py-4 border-t border-border space-y-1">
          <button
            onClick={() => logout()}
            className={cn(
              "flex items-center gap-3 px-3 py-2.5 rounded-card text-sm font-medium transition-colors w-full",
              "text-clinicalGrey hover:bg-secondary hover:text-mirageBlack"
            )}
          >
            <LogOut className="w-5 h-5" />
            Logout
          </button>
        </div>
      </aside>

      {/* Main content */}
      <div className="flex-1 flex flex-col min-w-0">
        {/* Top bar */}
        <header className="h-16 bg-white border-b border-border flex items-center justify-between px-8 shrink-0">
          <div className="flex items-center gap-4 flex-1">
            <div className="relative max-w-md w-full">
              <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-clinicalGrey" />
              <input
                type="text"
                placeholder="Search..."
                className="w-full pl-9 pr-4 py-2 rounded-lg border border-border bg-stellarWhite text-sm text-mirageBlack focus:outline-none focus:ring-2 focus:ring-celestialBlue/30 focus:border-celestialBlue transition-all"
              />
            </div>
          </div>
          <div className="flex items-center gap-4 ml-6">
            <div className="flex items-center gap-3">
              <div className="w-9 h-9 rounded-full bg-deepSpace flex items-center justify-center">
                <span className="text-xs font-bold text-white">
                  {user?.first_name?.[0] ?? "A"}
                  {user?.last_name?.[0] ?? "D"}
                </span>
              </div>
              <div className="text-sm">
                <p className="font-medium text-mirageBlack">
                  {user?.first_name} {user?.last_name}
                </p>
                <p className="text-xs text-clinicalGrey">Administrator</p>
              </div>
            </div>
          </div>
        </header>

        {/* Page content */}
        <main className="flex-1 overflow-auto p-8">
          {children}
        </main>
      </div>
    </div>
  );
}

function NavLink({
  href,
  icon: Icon,
  label,
}: {
  href: string;
  icon: React.ElementType;
  label: string;
}): React.ReactElement {
  const pathname = usePathname();
  const isActive = pathname === href || pathname.startsWith(`${href}/`);
  return (
    <Link
      href={href}
      className={cn(
        "flex items-center gap-3 px-3 py-2.5 rounded-card text-sm font-medium transition-colors",
        isActive
          ? "bg-celestialBlue/10 text-celestialBlue"
          : "text-clinicalGrey hover:bg-secondary hover:text-mirageBlack"
      )}
    >
      <Icon className="w-5 h-5" />
      {label}
    </Link>
  );
}
