import type { Metadata } from 'next';
import { Inter } from 'next/font/google';
import { Providers } from '@/providers';
import './globals.css';

const inter = Inter({
  subsets: ['latin'],
  variable: '--font-inter',
  display: 'swap',
});

export const metadata: Metadata = {
  title: 'Mirage — Healthcare Platform',
  description:
    'Secure, real-time patient–doctor collaboration with AI-assisted clinical workflows.',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}): React.ReactElement {
  return (
    <html lang="en" className={inter.variable}>
      <body className="min-h-screen bg-stellarWhite text-foreground antialiased">
        <Providers>{children}</Providers>
      </body>
    </html>
  );
}
