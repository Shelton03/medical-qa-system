import Link from 'next/link';

export default function NotFound(): React.ReactElement {
  return (
    <div className="min-h-screen flex items-center justify-center px-6 bg-stellarWhite">
      <div className="text-center">
        <h1 className="text-6xl font-bold text-mirageBlack mb-4">404</h1>
        <h2 className="text-2xl font-semibold text-mirageBlack mb-4">
          Page Not Found
        </h2>
        <p className="text-body text-clinicalGrey mb-8">
          The page you&apos;re looking for doesn&apos;t exist or has been moved.
        </p>
        <Link
          href="/"
          className="inline-block px-6 py-3 rounded-button bg-mirageBlack text-white font-medium text-sm hover:bg-mirageBlack-600 transition-colors"
        >
          Go Home
        </Link>
      </div>
    </div>
  );
}
