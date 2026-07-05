import React from 'react';
import { LayoutDashboard, Users, FileCheck, Stethoscope } from 'lucide-react';

export default function DoctorDashboardPage(): React.ReactElement {
  return (
    <div className="space-y-8">
      <div>
        <h1 className="text-page-title font-bold text-mirageBlack">Dashboard</h1>
        <p className="text-body text-clinicalGrey mt-1">
          Overview of your clinical activity today.
        </p>
      </div>

      {/* Stat Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <StatCard
          label="Today's Consultations"
          value="4"
          icon={Stethoscope}
        />
        <StatCard label="Pending Consents" value="2" icon={FileCheck} />
        <StatCard label="Recent Patients" value="12" icon={Users} />
        <StatCard label="Notifications" value="3" icon={LayoutDashboard} />
      </div>

      {/* Placeholder Widgets */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="bg-white border border-border rounded-card p-6">
          <h2 className="text-card-title font-semibold text-mirageBlack mb-4">
            Today's Schedule
          </h2>
          <div className="space-y-3">
            {[1, 2, 3].map((i) => (
              <div
                key={i}
                className="h-12 bg-secondary rounded-lg animate-pulse"
              />
            ))}
          </div>
        </div>

        <div className="bg-white border border-border rounded-card p-6">
          <h2 className="text-card-title font-semibold text-mirageBlack mb-4">
            Pending Consent Requests
          </h2>
          <div className="space-y-3">
            {[1, 2].map((i) => (
              <div
                key={i}
                className="h-12 bg-secondary rounded-lg animate-pulse"
              />
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}

function StatCard({
  label,
  value,
  icon: Icon,
}: {
  label: string;
  value: string;
  icon: React.ElementType;
}): React.ReactElement {
  return (
    <div className="bg-white border border-border rounded-card p-5 flex items-center gap-4">
      <div className="w-10 h-10 rounded-lg bg-mirageBlack-50 flex items-center justify-center">
        <Icon className="w-5 h-5 text-mirageBlack" />
      </div>
      <div>
        <p className="text-micro text-clinicalGrey uppercase tracking-wide">
          {label}
        </p>
        <p className="text-page-title font-bold text-mirageBlack">{value}</p>
      </div>
    </div>
  );
}
