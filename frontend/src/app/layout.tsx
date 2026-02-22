import type { ReactNode } from 'react';

export const metadata = {
  title: 'Nunuterapi Video',
  description: '1:1 video görüşme MVP',
};

export default function RootLayout({ children }: { children: ReactNode }) {
  return (
    <html lang="tr">
      <body>{children}</body>
    </html>
  );
}
