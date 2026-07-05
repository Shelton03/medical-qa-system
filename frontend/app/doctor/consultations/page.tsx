import React from 'react';

export default function DoctorConsultationsPage(): React.ReactElement {
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-page-title font-bold text-mirageBlack">
          Consultations
        </h1>
        <p className="text-body text-clinicalGrey mt-1">
          Active and historical consultations.
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="bg-white border border-border rounded-card p-6">
          <h2 className="text-card-title font-semibold text-mirageBlack mb-4">
            Active Consultation
          </h2>
          <div className="h-40 bg-secondary rounded-lg animate-pulse" />
        </div>

        <div className="bg-white border border-border rounded-card p-6">
          <h2 className="text-card-title font-semibold text-mirageBlack mb-4">
            Upcoming
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
