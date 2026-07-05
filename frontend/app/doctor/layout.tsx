import React from 'react';
import Link from 'next/link';
import { cn } from '@/lib/utils';
import {
  LayoutDashboard,
  Users,
  FileCheck,
  Stethoscope,
  Bell,
  Settings,
} from 'lucide-react';

const navItems = [
  { label: 'Dashboard', href: '/doctor/dashboard', icon: LayoutDashboard },
  { label: 'Patients', href: '/doctor/patients', icon: Users },
  { label: 'Consents', href: '/doctor/consents', icon: FileCheck },
  { label: 'Consultations', href: '/doctor/consultations', icon: Stethoscope },
];

interface DoctorLayoutProps {
  children: React.ReactNode;
}

/**
 * Doctor Portal Layout
 *
 * Desktop-first clinical dashboard with a persistent sidebar.
 * Navigation links: Dashboard, Patients, Consents, Consultations.
 */
export default function DoctorLayout({ children }: DoctorLayoutProps): React.ReactElement {
  return (
    <div className="flex h-screen bg-stellarWhite overflow-hidden">
      {/* Sidebar */}
      <aside className="w-64 shrink-0 border-r border-border bg-white flex flex-col">
        {/* Brand */}
        <div className="h-16 flex items-center px-6 border-b border-border">
          <div className="w-8 h-8 rounded-md bg-mirageBlack flex items-center justify-center mr-3">
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
          <button className="w-full flex items-center gap-3 px-3 py-2.5 rounded-card text-sm font-medium text-clinicalGrey hover:bg-secondary transition-colors">
            <Bell className="w-5 h-5" />
            Notifications
          </button>
          <button className="w-full flex items-center gap-3 px-3 py-2.5 rounded-card text-sm font-medium text-clinicalGrey hover:bg-secondary transition-colors">
            <Settings className="w-5 h-5" />
            Settings
          </button>
        </div>
      </aside>

      {/* Main content */}
      <div className="flex-1 flex flex-col min-w-0">
        {/* Top bar */}
        <header className="h-16 bg-white border-b border-border flex items-center justify-between px-8 shrink-0">
          <h1 className="font-semibold text-mirageBlack">Doctor Portal</h1>
          <div className="flex items-center gap-4">
            <button
              aria-label="Notifications"
              className="relative p-2 rounded-full hover:bg-secondary transition-colors touch-target"
            >
              <Bell className="w-5 h-5 text-clinicalGrey" />
              <span className="absolute top-1.5 right-1.5 w-2 h-2 bg-alertOrange rounded-full" />
            </button>
            <div className="w-9 h-9 rounded-full bg-mirageBlack-100 flex items-center justify-center">
              <span className="text-xs font-bold text-mirageBlack">DR</span>
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
  return (
    <Link
      href={href}
      className={cn(
        'flex items-center gap-3 px-3 py-2.5 rounded-card text-sm font-medium transition-colors',
        'text-clinicalGrey hover:bg-secondary hover:text-mirageBlack'
      )}
    >
      <Icon className="w-5 h-5" />
      {label}
    </Link>
  );
}
