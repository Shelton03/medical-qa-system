'use client';

import React from 'react';
import { QueryProvider } from './QueryProvider';
import { AuthProvider } from './AuthProvider';
import { ToastProvider } from './ToastProvider';
import { WebSocketProvider } from './WebSocketProvider';

export function Providers({ children }: { children: React.ReactNode }): React.ReactElement {
  return (
    <QueryProvider>
      <ToastProvider>
        <AuthProvider>
          <WebSocketProvider>
            {children}
          </WebSocketProvider>
        </AuthProvider>
      </ToastProvider>
    </QueryProvider>
  );
}
