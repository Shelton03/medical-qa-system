'use client'

import React from 'react'

export default function GlobalError({ error, reset }: { error: Error; reset: () => void }): React.ReactElement {
  return (
    <div className="flex flex-col items-center justify-center min-h-screen p-4">
      <h2 className="text-page-title font-heading text-mirageBlack mb-4">Something went wrong</h2>
      <p className="text-body text-clinicalGrey mb-6">{error.message}</p>
      <button
        onClick={reset}
        className="px-6 py-3 bg-celestialBlue text-white rounded-button font-medium hover:bg-celestialBlue-600 transition-colors"
      >
        Try again
      </button>
    </div>
  )
}
