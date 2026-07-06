import Link from 'next/link';

export default function LandingPage(): React.ReactElement {
  return (
    <div className="min-h-screen flex flex-col bg-stellarWhite">
      {/* Hero Section */}
      <section className="flex-1 flex items-center justify-center px-6 py-20">
        <div className="max-w-3xl mx-auto text-center">
          <div className="w-16 h-16 rounded-2xl bg-mirageBlack flex items-center justify-center mx-auto mb-8">
            <span className="text-white font-bold text-2xl">M</span>
          </div>
          <h1 className="text-display text-mirageBlack mb-6">
            Mirage Healthcare Platform
          </h1>
          <p className="text-body text-clinicalGrey max-w-xl mx-auto mb-10">
            Secure, real-time patient–doctor collaboration with AI-assisted
            clinical workflows. Built for modern healthcare.
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Link
              href="/demo"
              className="inline-flex items-center justify-center px-8 py-3.5 rounded-button bg-mirageBlack text-white font-medium text-sm hover:bg-mirageBlack-600 transition-colors shadow-elevation-2"
            >
              Enter Demo Mode
            </Link>
            <Link
              href="/doctor/login"
              className="inline-flex items-center justify-center px-8 py-3.5 rounded-button border border-border bg-white text-mirageBlack font-medium text-sm hover:bg-secondary transition-colors"
            >
              Doctor Login
            </Link>
          </div>
        </div>
      </section>

      {/* Feature Strip */}
      <section className="border-t border-border bg-white py-12 px-6">
        <div className="max-w-5xl mx-auto grid grid-cols-1 sm:grid-cols-3 gap-8 text-center">
          <div>
            <h3 className="text-card-title font-semibold text-mirageBlack mb-2">
              Patient App
            </h3>
            <p className="text-caption text-clinicalGrey">
              Mobile-first experience with consent, timeline, and AI symptom
              checking.
            </p>
          </div>
          <div>
            <h3 className="text-card-title font-semibold text-mirageBlack mb-2">
              Doctor Portal
            </h3>
            <p className="text-caption text-clinicalGrey">
              Desktop clinical dashboard with patient search, consultations,
              and AI assistance.
            </p>
          </div>
          <div>
            <h3 className="text-card-title font-semibold text-mirageBlack mb-2">
              Split-Screen Demo
            </h3>
            <p className="text-caption text-clinicalGrey">
              See real-time consent and record synchronization side by side.
            </p>
          </div>
        </div>
      </section>
    </div>
  );
}
