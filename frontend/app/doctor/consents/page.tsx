import React from 'react';

export default function DoctorConsentsPage(): React.ReactElement {
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-page-title font-bold text-mirageBlack">
          Consent Management
        </h1>
        <p className="text-body text-clinicalGrey mt-1">
          Track and manage patient consent requests.
        </p>
      </div>

      <div className="bg-white border border-border rounded-card overflow-hidden">
        <div className="px-6 py-4 border-b border-border bg-secondary">
          <div className="flex items-center gap-4 text-micro uppercase tracking-wide text-clinicalGrey">
            <span className="w-1/4">Patient</span>
            <span className="w-1/4">Status</span>
            <span className="w-1/4">Requested</span>
            <span className="w-1/4">Expires</span>
          </div>
        </div>
        <div className="divide-y divide-border">
          {[1, 2, 3].map((i) => (
            <div
              key={i}
              className="px-6 py-4 flex items-center gap-4 animate-pulse"
            >
              <div className="w-1/4 h-4 bg-secondary rounded" />
              <div className="w-1/4 h-4 bg-secondary rounded" />
              <div className="w-1/4 h-4 bg-secondary rounded" />
              <div className="w-1/4 h-4 bg-secondary rounded" />
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
