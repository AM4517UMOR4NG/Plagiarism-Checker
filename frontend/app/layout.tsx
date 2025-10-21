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
        background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
        minHeight: '100vh',
        color: '#333'
      }}>
        <div style={{
          maxWidth: 1200,
          margin: '0 auto',
          padding: '24px'
        }}>
          <header style={{
            background: 'rgba(255, 255, 255, 0.95)',
            borderRadius: 16,
            padding: '32px 40px',
            marginBottom: 32,
            boxShadow: '0 10px 40px rgba(0,0,0,0.1)',
            backdropFilter: 'blur(10px)'
          }}>
            <h1 style={{
              margin: 0,
              fontSize: 36,
              fontWeight: 700,
              background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
              WebkitBackgroundClip: 'text',
              WebkitTextFillColor: 'transparent',
              backgroundClip: 'text'
            }}>🔍 Professional Plagiarism Checker</h1>
            <p style={{
              margin: '8px 0 0 0',
              color: '#666',
              fontSize: 14
            }}>Advanced AI-powered document similarity detection</p>
          </header>
          <main>{children}</main>
        </div>
      </body>
    </html>
  );
}
