import type { ReactNode } from 'react';

export const metadata = {
  title: 'Professional Plagiarism Checker',
  description: 'Advanced plagiarism detection system',
};

export default function RootLayout({ children }: { children: ReactNode }) {
  return (
    <html lang="en">
      <body style={{
        margin: 0,
        padding: 0,
        fontFamily: '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif',
        background: 'radial-gradient(1000px 600px at 20% 10%, rgba(45, 212, 191, 0.25), transparent 60%), radial-gradient(1000px 600px at 80% 0%, rgba(167, 139, 250, 0.25), transparent 60%), linear-gradient(135deg, #0ea5e9 0%, #9333ea 100%)',
        minHeight: '100vh',
        color: '#1f2937'
      }}>
        <div style={{
          maxWidth: 1200,
          margin: '0 auto',
          padding: '24px'
        }}>
          <header style={{
            background: 'rgba(255, 255, 255, 0.9)',
            borderRadius: 16,
            padding: '28px 36px',
            marginBottom: 32,
            boxShadow: '0 20px 60px rgba(16,24,40,0.15)',
            backdropFilter: 'blur(10px)'
          }}>
            <h1 style={{
              margin: 0,
              fontSize: 36,
              fontWeight: 700,
              background: 'linear-gradient(135deg, #06b6d4 0%, #8b5cf6 50%, #f43f5e 100%)',
              WebkitBackgroundClip: 'text',
              WebkitTextFillColor: 'transparent',
              backgroundClip: 'text'
            }}>🔍 Professional Plagiarism Checker</h1>
            <p style={{
              margin: '8px 0 0 0',
              color: '#475569',
              fontSize: 14
            }}>Advanced AI-powered document similarity detection</p>
          </header>
          <main>{children}</main>
        </div>
      </body>
    </html>
  );
}
