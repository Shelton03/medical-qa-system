import React from 'react';

export default function PatientConsentPage(): React.ReactElement {
  return (
    <div className="flex flex-col h-full px-5 py-6 bg-stellarWhite">
      {/* Doctor Card */}
      <div className="bg-white border border-border rounded-card p-4 mb-4">
        <p className="text-micro uppercase tracking-wide text-clinicalGrey mb-2">
          Requesting Access
        </p>
        <h2 className="text-card-title font-bold text-mirageBlack">
          Dr. Chiedza Ncube
        </h2>
        <p className="text-caption text-clinicalGrey mt-1">
          Reg. MDPCZ-2018-0442 · Verified
        </p>
        <div className="mt-3 inline-flex items-center px-2.5 py-1 rounded bg-clinicalGrey-50 text-micro text-clinicalGrey font-medium">
          Harare Central Hospital
        </div>
      </div>

      {/* Consent Purpose */}
      <div className="bg-white border border-border rounded-card p-4 mb-4">
        <p className="text-micro uppercase tracking-wide text-clinicalGrey mb-2">
          Purpose
        </p>
        <p className="text-body text-mirageBlack">
          Routine consultation and review of medical history for ongoing
          treatment.
        </p>
      </div>

      {/* Scope */}
      <div className="bg-white border border-border rounded-card p-4 mb-4">
        <p className="text-micro uppercase tracking-wide text-clinicalGrey mb-2">
          Shared Data
        </p>
        <ul className="space-y-2">
          {['Medical timeline', 'Allergies & conditions', 'Current medications'].map(
            (item) => (
              <li
                key={item}
                className="flex items-center gap-2 text-caption text-mirageBlack"
              >
                <span className="w-1.5 h-1.5 rounded-full bg-celestialBlue" />
                {item}
              </li>
            )
          )}
        </ul>
      </div>

      {/* Expiry */}
      <div className="bg-alertOrange-50 border border-alertOrange/20 rounded-card p-4 mb-6">
        <p className="text-caption text-alertOrange font-medium">
          Expires in 24 hours
        </p>
      </div>

      {/* Actions */}
      <div className="mt-auto space-y-3">
        <button
          type="button"
          className="w-full py-3.5 rounded-button bg-healthGreen text-white font-medium text-sm hover:bg-healthGreen-600 transition-colors"
        >
          Approve Access
        </button>
        <button
          type="button"
          className="w-full py-3.5 rounded-button border border-border bg-white text-mirageBlack font-medium text-sm hover:bg-secondary transition-colors"
        >
          Decline
        </button>
      </div>
    </div>
  );
}
