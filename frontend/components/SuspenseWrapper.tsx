import React, { Suspense } from 'react';

export function SuspenseWrapper({ children }: { children: React.ReactNode }): React.ReactElement {
  return (
    <Suspense fallback={
      <div className="flex items-center justify-center h-64">
        <div className="animate-pulse text-clinicalGrey">Loading...</div>
      </div>
    }>
      {children}
    </Suspense>
  );
}
