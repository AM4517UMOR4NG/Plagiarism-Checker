"use client";
import { useEffect, useState } from "react";

const API_BASE = process.env.NEXT_PUBLIC_API_BASE || "http://localhost:8000";

type ResultPayload = {
  doc_id: string;
  title?: string | null;
  summary?: { similarity: number; sources: any[]; processing_time_ms: number };
  fragments?: any[];
  explain?: Record<string, number>;
};

export default function ResultsPage({ params }: { params: { jobId: string } }) {
  const { jobId } = params;
  const [status, setStatus] = useState<string>("PENDING");
  const [result, setResult] = useState<ResultPayload | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    let timer: any;
    const poll = async () => {
      try {
        const res = await fetch(`${API_BASE}/api/v1/jobs/${jobId}`);
        if (!res.ok) throw new Error(`Status fetch failed ${res.status}`);
        const data = await res.json();
        setStatus(data.status || data.state || "UNKNOWN");

        if (data.ready) {
          const res2 = await fetch(`${API_BASE}/api/v1/results/${jobId}`);
          if (!res2.ok) throw new Error(`Result fetch failed ${res2.status}`);
          const data2 = await res2.json();
          setResult(data2.result || null);
          return;
        }
      } catch (e: any) {
        setError(e.message || "Polling error");
      }
      timer = setTimeout(poll, 1000);
    };
    poll();
    return () => clearTimeout(timer);
  }, [jobId]);

  const getSimilarityColor = (similarity: number) => {
    if (similarity < 0.15) return { bg: '#d4edda', border: '#28a745', text: '#155724' };
    if (similarity < 0.30) return { bg: '#fff3cd', border: '#ffc107', text: '#856404' };
    return { bg: '#f8d7da', border: '#dc3545', text: '#721c24' };
  };

  const getSimilarityLabel = (similarity: number) => {
    if (similarity < 0.15) return 'Low Risk';
    if (similarity < 0.30) return 'Medium Risk';
    return 'High Risk';
  };

  const renderProgressBar = (value: number, label: string, color: string) => (
    <div style={{ marginBottom: 16 }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: 6 }}>
        <span style={{ fontSize: 13, fontWeight: 600, color: '#444' }}>{label}</span>
        <span style={{ fontSize: 13, fontWeight: 700, color }}>{(value * 100).toFixed(1)}%</span>
      </div>
      <div style={{
        width: '100%',
        height: 10,
        backgroundColor: '#e9ecef',
        borderRadius: 10,
        overflow: 'hidden'
      }}>
        <div style={{
          width: `${value * 100}%`,
          height: '100%',
          background: `linear-gradient(90deg, ${color}, ${color}dd)`,
          transition: 'width 1s ease-out',
          borderRadius: 10
        }} />
      </div>
    </div>
  );

  if (error) {
    return (
      <div style={{
        background: 'rgba(255, 255, 255, 0.95)',
        borderRadius: 16,
        padding: 40,
        boxShadow: '0 10px 40px rgba(0,0,0,0.1)',
        textAlign: 'center'
      }}>
        <div style={{ fontSize: 64, marginBottom: 16 }}>⚠️</div>
        <h2 style={{ color: '#dc3545', marginBottom: 8 }}>Analysis Failed</h2>
        <p style={{ color: '#666' }}>{error}</p>
        <button
          onClick={() => window.location.href = '/'}
          style={{
            marginTop: 24,
            padding: '12px 24px',
            background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
            color: '#fff',
            border: 'none',
            borderRadius: 10,
            fontSize: 14,
            fontWeight: 600,
            cursor: 'pointer'
          }}
        >
          ← Back to Home
        </button>
      </div>
    );
  }

  if (!result) {
    return (
      <div style={{
        background: 'rgba(255, 255, 255, 0.95)',
        borderRadius: 16,
        padding: 60,
        boxShadow: '0 10px 40px rgba(0,0,0,0.1)',
        textAlign: 'center'
      }}>
        <div style={{
          width: 80,
          height: 80,
          margin: '0 auto 24px',
          border: '6px solid #f3f3f3',
          borderTop: '6px solid #667eea',
          borderRadius: '50%',
          animation: 'spin 1s linear infinite'
        }} />
        <style jsx>{`
          @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
          }
        `}</style>
        <h2 style={{ color: '#2d3748', marginBottom: 8 }}>Analyzing Document...</h2>
        <p style={{ color: '#666', fontSize: 14 }}>Status: {status}</p>
        <p style={{ color: '#999', fontSize: 13, marginTop: 16 }}>
          Job ID: {jobId}
        </p>
      </div>
    );
  }

  const similarity = result.summary?.similarity || 0;
  const colors = getSimilarityColor(similarity);
  const riskLabel = getSimilarityLabel(similarity);

  return (
    <div style={{ display: 'grid', gap: 24 }}>
      {/* Header Card */}
      <div style={{
        background: 'rgba(255, 255, 255, 0.95)',
        borderRadius: 16,
        padding: 32,
        boxShadow: '0 10px 40px rgba(0,0,0,0.1)'
      }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'start', marginBottom: 24 }}>
          <div>
            <h2 style={{ margin: 0, fontSize: 28, fontWeight: 700, color: '#2d3748' }}>
              📊 Analysis Results
            </h2>
            <p style={{ margin: '8px 0 0 0', color: '#666', fontSize: 14 }}>
              {result.title || 'Untitled Document'}
            </p>
          </div>
          <button
            onClick={() => window.location.href = '/'}
            style={{
              padding: '10px 20px',
              background: '#fff',
              border: '2px solid #667eea',
              color: '#667eea',
              borderRadius: 8,
              fontSize: 14,
              fontWeight: 600,
              cursor: 'pointer',
              transition: 'all 0.3s'
            }}
            onMouseEnter={(e) => {
              e.currentTarget.style.background = '#667eea';
              e.currentTarget.style.color = '#fff';
            }}
            onMouseLeave={(e) => {
              e.currentTarget.style.background = '#fff';
              e.currentTarget.style.color = '#667eea';
            }}
          >
            ← New Analysis
          </button>
        </div>

        {/* Similarity Score */}
        <div style={{
          background: colors.bg,
          border: `3px solid ${colors.border}`,
          borderRadius: 16,
          padding: 32,
          textAlign: 'center'
        }}>
          <div style={{ fontSize: 72, fontWeight: 800, color: colors.text, marginBottom: 8 }}>
            {(similarity * 100).toFixed(1)}%
          </div>
          <div style={{ fontSize: 18, fontWeight: 600, color: colors.text, marginBottom: 4 }}>
            Similarity Score
          </div>
          <div style={{
            display: 'inline-block',
            padding: '6px 16px',
            background: colors.text,
            color: '#fff',
            borderRadius: 20,
            fontSize: 13,
            fontWeight: 700,
            marginTop: 8
          }}>
            {riskLabel}
          </div>
        </div>
      </div>

      {/* Detailed Metrics */}
      <div style={{
        background: 'rgba(255, 255, 255, 0.95)',
        borderRadius: 16,
        padding: 32,
        boxShadow: '0 10px 40px rgba(0,0,0,0.1)'
      }}>
        <h3 style={{ margin: '0 0 24px 0', fontSize: 20, fontWeight: 700, color: '#2d3748' }}>
          📈 Detailed Analysis
        </h3>
        
        {result.explain && Object.entries(result.explain).map(([key, value]) => {
          const colors = ['#667eea', '#764ba2', '#f093fb', '#4facfe'];
          const colorIndex = Object.keys(result.explain!).indexOf(key);
          return renderProgressBar(
            value as number,
            key.charAt(0).toUpperCase() + key.slice(1) + ' Match',
            colors[colorIndex % colors.length]
          );
        })}

        <div style={{
          display: 'grid',
          gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))',
          gap: 16,
          marginTop: 24,
          padding: 20,
          background: '#f8f9fa',
          borderRadius: 12
        }}>
          <div>
            <div style={{ fontSize: 12, color: '#666', marginBottom: 4 }}>Processing Time</div>
            <div style={{ fontSize: 20, fontWeight: 700, color: '#2d3748' }}>
              {result.summary?.processing_time_ms || 0}ms
            </div>
          </div>
          <div>
            <div style={{ fontSize: 12, color: '#666', marginBottom: 4 }}>Sources Found</div>
            <div style={{ fontSize: 20, fontWeight: 700, color: '#2d3748' }}>
              {result.summary?.sources?.length || 0}
            </div>
          </div>
          <div>
            <div style={{ fontSize: 12, color: '#666', marginBottom: 4 }}>Matched Fragments</div>
            <div style={{ fontSize: 20, fontWeight: 700, color: '#2d3748' }}>
              {result.fragments?.length || 0}
            </div>
          </div>
        </div>
      </div>

      {/* Matched Fragments */}
      {result.fragments && result.fragments.length > 0 && (
        <div style={{
          background: 'rgba(255, 255, 255, 0.95)',
          borderRadius: 16,
          padding: 32,
          boxShadow: '0 10px 40px rgba(0,0,0,0.1)'
        }}>
          <h3 style={{ margin: '0 0 20px 0', fontSize: 20, fontWeight: 700, color: '#2d3748' }}>
            🔍 Matched Content Fragments
          </h3>
          {result.fragments.map((frag: any, idx: number) => (
            <div key={idx} style={{
              background: '#f8f9fa',
              border: '2px solid #e9ecef',
              borderRadius: 12,
              padding: 20,
              marginBottom: 16
            }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: 12 }}>
                <span style={{ fontSize: 13, fontWeight: 600, color: '#667eea' }}>
                  Fragment #{idx + 1}
                </span>
                <span style={{ fontSize: 13, fontWeight: 700, color: '#dc3545' }}>
                  {((frag.score || 0) * 100).toFixed(1)}% Match
                </span>
              </div>
              <div style={{
                background: '#fff',
                padding: 16,
                borderRadius: 8,
                fontSize: 14,
                color: '#2d3748',
                lineHeight: 1.6,
                fontFamily: 'monospace',
                marginBottom: 12
              }}>
                "{frag.text}"
              </div>
              {frag.source && (
                <div style={{ fontSize: 12, color: '#666' }}>
                  <strong>Source:</strong> {frag.source}
                </div>
              )}
            </div>
          ))}
        </div>
      )}

      {/* Footer Info */}
      <div style={{
        background: 'rgba(255, 255, 255, 0.95)',
        borderRadius: 16,
        padding: 24,
        boxShadow: '0 10px 40px rgba(0,0,0,0.1)',
        fontSize: 13,
        color: '#666',
        textAlign: 'center'
      }}>
        <div style={{ marginBottom: 8 }}>
          <strong>Document ID:</strong> {result.doc_id}
        </div>
        <div>
          <strong>Job ID:</strong> {jobId}
        </div>
        <div style={{ marginTop: 16, fontSize: 12, color: '#999' }}>
          ✅ Analysis completed successfully • {new Date().toLocaleString()}
        </div>
      </div>
    </div>
  );
}
