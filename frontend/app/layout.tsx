import type { Metadata } from 'next';
import { Providers } from '@/providers';
import './globals.css';

export const metadata: Metadata = {
  title: 'Mirage — Healthcare Platform',
  description:
    'Secure, real-time patient–doctor collaboration with AI-assisted clinical workflows.',
  icons: {
    icon: '/icon.svg',
    apple: '/icon.svg',
  },
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}): React.ReactElement {
  return (
    <html lang="en">
      <body className="min-h-screen bg-stellarWhite text-foreground antialiased">
        <Providers>{children}</Providers>
      </body>
    </html>
  );
}
