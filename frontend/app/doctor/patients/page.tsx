import React from 'react';

export default function DoctorPatientsPage(): React.ReactElement {
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-page-title font-bold text-mirageBlack">Patients</h1>
        <p className="text-body text-clinicalGrey mt-1">
          Search and manage your patient registry.
        </p>
      </div>

      {/* Search Input Placeholder */}
      <div className="bg-white border border-border rounded-card px-4 py-3 flex items-center gap-3">
        <div className="w-5 h-5 rounded-full bg-secondary" />
        <span className="text-caption text-clinicalGrey-400">
          Search by name, national ID, or phone number…
        </span>
      </div>

      {/* Patient List Placeholder */}
      <div className="bg-white border border-border rounded-card overflow-hidden">
        <div className="divide-y divide-border">
          {[1, 2, 3, 4, 5].map((i) => (
            <div
              key={i}
              className="px-6 py-4 flex items-center gap-4 animate-pulse"
            >
              <div className="w-10 h-10 rounded-full bg-secondary" />
              <div className="flex-1 space-y-2">
                <div className="w-1/3 h-4 bg-secondary rounded" />
                <div className="w-1/4 h-3 bg-secondary rounded" />
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
