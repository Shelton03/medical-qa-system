/** @type {import('next').NextConfig} */
const nextConfig = {
  output: 'standalone',
  reactStrictMode: true,
  async rewrites() {
    // Use build-time env for Docker; fallback to localhost for non-Docker dev
    const apiBase = process.env.API_INTERNAL_URL || 'http://localhost:8000';
    return [
      {
        source: '/api/v1/:path*',
        destination: `${apiBase}/api/v1/:path*`,
      },
      {
        source: '/ws/:path*',
        destination: `${apiBase}/ws/:path*`,
      },
    ];
  },
};

module.exports = nextConfig;
