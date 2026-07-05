'use client';

import React from 'react';
import { cn } from '@/lib/utils';

interface PhoneFrameProps {
  children: React.ReactNode;
  className?: string;
}

/**
 * PhoneFrame
 *
 * Visually simulates a modern smartphone to wrap Patient App pages during demos.
 * Fixed dimensions per the Mirage Design System:
 * - Large screens: 370px × 800px
 * - Smaller laptops: 350px × 760px (fallback via CSS responsive scale)
 *
 * Includes rounded bezel, speaker notch, camera cut-out, status bar,
 * home indicator, and safe area insets.
 */
export function PhoneFrame({ children, className }: PhoneFrameProps): React.ReactElement {
  return (
    <div
      className={cn(
        'relative flex items-center justify-center',
        className
      )}
      aria-label="Simulated mobile device"
    >
      {/* Outer Device Bezel */}
      <div
        className={cn(
          'relative rounded-phone-frame bg-deepSpace-50',
          'shadow-phone ring-1 ring-white/10',
          'p-[10px]',
          'w-[350px] h-[760px]',
          'lg:w-[370px] lg:h-[800px]',
          'select-none'
        )}
      >
        {/* Camera / Notch Bar */}
        <div className="absolute top-0 left-1/2 -translate-x-1/2 z-20 pt-2">
          <div className="w-[90px] h-[28px] bg-deepSpace rounded-b-[14px] flex items-center justify-center gap-2">
            <div className="w-[8px] h-[8px] rounded-full bg-deepSpace-100 ring-1 ring-white/20" />
            <div className="w-[40px] h-[4px] rounded-full bg-deepSpace-100/60" />
          </div>
        </div>

        {/* Side Buttons (decorative) */}
        <div className="absolute -right-[3px] top-[120px] w-[3px] h-[30px] bg-clinicalGrey-400 rounded-r-sm" />
        <div className="absolute -right-[3px] top-[170px] w-[3px] h-[50px] bg-clinicalGrey-400 rounded-r-sm" />
        <div className="absolute -left-[3px] top-[140px] w-[3px] h-[40px] bg-clinicalGrey-400 rounded-l-sm" />

        {/* Screen Container */}
        <div
          className={cn(
            'relative w-full h-full rounded-[32px] overflow-hidden',
            'bg-stellarWhite',
            'flex flex-col'
          )}
        >
          {/* Simulated Status Bar */}
          <div className="relative z-10 h-12 bg-mirageBlack shrink-0 flex items-center justify-between px-6 pt-1">
            <span className="text-[13px] font-semibold text-white tracking-wide">9:41</span>
            <div className="flex items-center gap-1.5">
              {/* Signal bars */}
              <div className="flex items-end gap-[2px] h-3">
                <div className="w-[3px] h-[6px] bg-white rounded-sm" />
                <div className="w-[3px] h-[9px] bg-white rounded-sm" />
                <div className="w-[3px] h-[12px] bg-white rounded-sm" />
              </div>
              <span className="text-[10px] font-bold text-white ml-0.5">5G</span>
              {/* Battery */}
              <div className="w-[22px] h-[11px] border border-white/80 rounded-[3px] relative ml-1">
                <div className="absolute inset-[1px] w-[70%] bg-white rounded-[1px]" />
                <div className="absolute -right-[2px] top-1/2 -translate-y-1/2 w-[1px] h-[5px] bg-white/80 rounded-r-sm" />
              </div>
            </div>
          </div>

          {/* Scrollable Application Area */}
          <div className="flex-1 overflow-y-auto scrollbar-hide relative">
            {children}
          </div>

          {/* Home Indicator */}
          <div className="shrink-0 h-[34px] bg-white/95 backdrop-blur flex items-start justify-center pt-2">
            <div className="w-[134px] h-[5px] bg-deepSpace/20 rounded-full" />
          </div>
        </div>
      </div>
    </div>
  );
}
