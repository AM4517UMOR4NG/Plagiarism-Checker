"use client";
import { useState } from "react";

const API_BASE = process.env.NEXT_PUBLIC_API_BASE || "http://localhost:8000";

export default function HomePage() {
  const [text, setText] = useState("");
  const [file, setFile] = useState<File | null>(null);
  const [title, setTitle] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const onSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    setLoading(true);
    try {
      const form = new FormData();
      if (file) form.append("file", file);
      if (text.trim().length > 0) form.append("text", text);
      if (title.trim().length > 0) form.append("title", title);

      const res = await fetch(`${API_BASE}/api/v1/upload`, {
        method: "POST",
        body: form,
      });
      if (!res.ok) throw new Error(`Upload failed: ${res.status}`);
      const data = await res.json();
      const jobId = data.job_id || data.jobId || data.id;
      if (!jobId) throw new Error("No job_id returned");
      window.location.href = `/results/${jobId}`;
    } catch (err: any) {
      setError(err.message || "Upload error");
    } finally {
      setLoading(false);
    }
  };

  const inputStyle = {
    width: '100%',
    padding: '14px 16px',
    fontSize: 15,
    border: '2px solid #e0e0e0',
    borderRadius: 10,
    outline: 'none',
    transition: 'all 0.3s ease',
    fontFamily: 'inherit',
    backgroundColor: '#fff'
  };

  const labelStyle = {
    display: 'block',
    marginBottom: 8,
    fontSize: 14,
    fontWeight: 600,
    color: '#444'
  };

  return (
    <div style={{
      background: 'rgba(255, 255, 255, 0.88)',
      borderRadius: 20,
      padding: '44px',
      boxShadow: '0 24px 80px rgba(16,24,40,0.18)',
      backdropFilter: 'blur(14px)',
      border: '1px solid rgba(255,255,255,0.6)'
    }}>
      <h2 style={{
        marginTop: 0,
        marginBottom: 8,
        fontSize: 28,
        fontWeight: 700,
        color: '#2d3748'
      }}>📝 Submit Document for Analysis</h2>
      <p style={{
        marginTop: 0,
        marginBottom: 32,
        color: '#475569',
        fontSize: 14
      }}>Upload a document or paste text to check for plagiarism and similarity matches</p>
      
      <form onSubmit={onSubmit} style={{ display: "grid", gap: 24 }}>
        <div>
          <label style={labelStyle}>
            📄 Document Title (Optional)
          </label>
          <input
            type="text"
            value={title}
            onChange={(e) => setTitle(e.target.value)}
            placeholder="Enter document title..."
            style={inputStyle}
            onFocus={(e) => e.target.style.borderColor = '#06b6d4'}
            onBlur={(e) => e.target.style.borderColor = '#e0e0e0'}
          />
        </div>

        <div>
          <label style={labelStyle}>
            ✍️ Paste Text Content
          </label>
          <textarea
            value={text}
            onChange={(e) => setText(e.target.value)}
            placeholder="Paste your document text here..."
            rows={10}
            style={{
              ...inputStyle,
              resize: 'vertical',
              minHeight: 200,
              background: 'linear-gradient(180deg, #ffffff 0%, #fbfbff 100%)'
            }}
            onFocus={(e) => e.target.style.borderColor = '#06b6d4'}
            onBlur={(e) => e.target.style.borderColor = '#e0e0e0'}
          />
        </div>

        <div>
          <label style={labelStyle}>
            📎 Or Upload File (PDF, DOCX, TXT)
          </label>
          <div style={{
            border: '2px dashed #cbd5e1',
            borderRadius: 14,
            padding: 32,
            textAlign: 'center',
            background: 'linear-gradient(180deg, #f8fafc 0%, #ffffff 100%)',
            transition: 'all 0.3s ease'
          }}
          onDragOver={(e) => {
            e.preventDefault();
            e.currentTarget.style.borderColor = '#06b6d4';
            e.currentTarget.style.backgroundColor = '#ecfeff';
          }}
          onDragLeave={(e) => {
            e.currentTarget.style.borderColor = '#cbd5e1';
            e.currentTarget.style.backgroundColor = '#ffffff';
          }}
          onDrop={(e) => {
            e.preventDefault();
            e.currentTarget.style.borderColor = '#cbd5e1';
            e.currentTarget.style.backgroundColor = '#ffffff';
            const files = e.dataTransfer.files;
            if (files.length > 0) setFile(files[0]);
          }}>
            <input 
              type="file" 
              onChange={(e) => setFile(e.target.files?.[0] || null)}
              accept=".pdf,.docx,.txt"
              style={{ display: 'none' }}
              id="file-upload"
            />
            <label htmlFor="file-upload" style={{ cursor: 'pointer' }}>
              {file ? (
                <div>
                  <div style={{ fontSize: 40, marginBottom: 8 }}>✅</div>
                  <div style={{ fontWeight: 600, color: '#0ea5e9' }}>{file.name}</div>
                  <div style={{ fontSize: 13, color: '#999', marginTop: 4 }}>
                    {(file.size / 1024).toFixed(1)} KB
                  </div>
                </div>
              ) : (
                <div>
                  <div style={{ fontSize: 48, marginBottom: 8 }}>📁</div>
                  <div style={{ fontWeight: 600, color: '#334155', marginBottom: 4 }}>
                    Click to upload or drag and drop
                  </div>
                  <div style={{ fontSize: 13, color: '#999' }}>
                    Supported: PDF, DOCX, TXT (Max 10MB)
                  </div>
                </div>
              )}
            </label>
          </div>
        </div>

        <button 
          type="submit" 
          disabled={loading || (!text.trim() && !file)}
          style={{
            padding: '16px 32px',
            fontSize: 16,
            fontWeight: 600,
            color: '#fff',
            background: loading || (!text.trim() && !file)
              ? '#cbd5e1'
              : 'linear-gradient(135deg, #06b6d4 0%, #8b5cf6 50%, #f43f5e 100%)',
            border: 'none',
            borderRadius: 12,
            cursor: loading || (!text.trim() && !file) ? 'not-allowed' : 'pointer',
            transition: 'all 0.3s ease',
            boxShadow: loading || (!text.trim() && !file)
              ? 'none'
              : '0 12px 30px rgba(139,92,246,0.35)',
            transform: 'scale(1)'
          }}
          onMouseEnter={(e) => {
            if (!loading && (text.trim() || file)) {
              e.currentTarget.style.transform = 'translateY(-2px)';
              e.currentTarget.style.boxShadow = '0 16px 40px rgba(139,92,246,0.45)';
            }
          }}
          onMouseLeave={(e) => {
            e.currentTarget.style.transform = 'scale(1)';
            e.currentTarget.style.boxShadow = loading || (!text.trim() && !file)
              ? 'none'
              : '0 12px 30px rgba(139,92,246,0.35)';
          }}
        >
          {loading ? "🔄 Analyzing Document..." : "🚀 Check for Plagiarism"}
        </button>
        
        {error && (
          <div style={{
            padding: 16,
            backgroundColor: '#fff1f0',
            border: '2px solid #ffccc7',
            borderRadius: 10,
            color: '#cf1322',
            fontSize: 14
          }}>
            ⚠️ {error}
          </div>
        )}
      </form>
    </div>
  );
}
