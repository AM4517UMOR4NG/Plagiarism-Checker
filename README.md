# Plagiarism Checker

Professional-grade plagiarism detection platform that combines FastAPI services, Celery-powered background processing, and a polished Next.js 14 interface. The system emulates commercial plagiarism suites with rich analytics, fragment-level insights, and extensible infrastructure for production deployments.

---

## Table of Contents
1. [Architecture at a Glance](#architecture-at-a-glance)
2. [Feature Overview](#feature-overview)
3. [Directory Structure](#directory-structure)
4. [Environment Matrix](#environment-matrix)
5. [Quick Start (Windows)](#quick-start-windows)
6. [End-to-End Workflow](#end-to-end-workflow)
7. [API Surface](#api-surface)
8. [Frontend Experience](#frontend-experience)
9. [Worker & Processing Pipeline](#worker--processing-pipeline)
10. [Configuration Reference](#configuration-reference)
11. [Troubleshooting & Tips](#troubleshooting--tips)
12. [Roadmap](#roadmap)
13. [License](#license)

---

## Architecture at a Glance

```
┌───────────┐      REST / WebSocket (planned)      ┌────────────┐
│ Frontend  │  <------------------------------->   │ FastAPI API│
│ Next.js   │                                      │ (backend)  │
└────┬──────┘                                      └─────┬──────┘
     │  Uploads / Job status requests                     │ Celery tasks
     ▼                                                     ▼
┌─────────────┐    ┌──────────┐    ┌──────────┐    ┌────────────┐
│ Object Store│    │PostgreSQL│    │Redis     │    │Celery Worker│
│   (MinIO)   │    │ Metadata │    │ Broker   │    │  (Python)   │
└─────────────┘    └──────────┘    └──────────┘    └────────────┘
```

- **Frontend (Next.js 14)** renders a professional upload & results dashboard and calls the API for every action.
- **Backend (FastAPI)** exposes document ingestion, job tracking, and results retrieval endpoints.
- **Worker (Celery)** executes heavy similarity checks, NLP embedding generation (Sentence Transformers), FAISS vector search, and aggregation logic.
- **Redis** brokers tasks; **PostgreSQL**/MinIO store metadata and documents; Elasticsearch is planned for shingled text search.

---

## Feature Overview

| Category            | Highlights |
|---------------------|------------|
| **Document Intake** | Drag-and-drop upload, clipboard paste, optional metadata, instant validation |
| **Analysis Engines**| Cosine similarity, N-gram overlap, lexical heuristics, semantic embedding comparison, source attribution |
| **Results UI**      | Large score card, dynamic risk badge, algorithm-by-algorithm progress bars, matched fragment explorer, source links |
| **Operations**      | Health endpoint, structured logging, togglable mock mode, modular workers for horizontal scaling |
| **Extensibility**   | Config-driven pipelines, placeholder hooks for authentication, roadmap for batch processing & premium tiers |

---

## Directory Structure

```
CheckTurnitin/
├── backend/          # FastAPI app, database models, Celery config
├── frontend/         # Next.js 14 UI, components, API client utilities
├── worker/           # Celery tasks, embeddings, scoring orchestration
├── infrastructure/   # Docker, deployment manifests, IaC stubs
└── README.md         # You are here
```

---

## Environment Matrix

| Mode           | Description | Requirements |
|----------------|-------------|--------------|
| **Development**| Mocked job queue; instant deterministic responses; ideal for UI work | Node.js + Python only |
| **Hybrid**     | FastAPI + worker with Redis; useful for realistic local tests | Redis; optional PostgreSQL/MinIO |
| **Production** | Full pipeline with persistence, object storage, observability hooks | Redis, PostgreSQL, MinIO, SSL termination |

---

## Quick Start (Windows)

### Prerequisites
- Python ≥ 3.10 (recommended 3.11)
- Node.js ≥ 18
- Redis (only required for worker/production flow)
- PowerShell 7 for the commands below

### 1. Backend API
```powershell
cd backend
python -m venv .venv
\.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
copy .env.example .env
\.\.venv\Scripts\python.exe -m uvicorn app.main:app --reload --port 8000
```
- Runs at `http://localhost:8000`
- Auto-reloads on file changes thanks to `--reload`

### 2. Frontend UI
```powershell
cd frontend
npm install
echo "NEXT_PUBLIC_API_BASE=http://localhost:8000" > .env
npm run dev
```
- Accessible at `http://localhost:3000`
- Proxies API calls using `NEXT_PUBLIC_API_BASE`

### 3. Celery Worker (optional, enables real processing)
```powershell
cd worker
python -m venv .venv
\.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
set REDIS_URL=redis://localhost:6379/0
\.\.venv\Scripts\python.exe -m celery -A worker.app worker --loglevel=INFO
```
- Requires Redis running locally
- Streams structured logs describing each analysis step

---

## End-to-End Workflow

1. **User uploads** a document or pastes text via the Next.js form.
2. **Frontend sends** `POST /api/v1/upload` with metadata + file payload.
3. **Backend validates** size, format (PDF/DOCX/TXT), stores reference, and enqueues a Celery job (or simulates result in mock mode).
4. **Worker processes** the text: normalization → chunking → embeddings → similarity scores → fragment alignment.
5. **Progress updates** are pulled by polling `GET /api/v1/jobs/{job_id}`. (WebSocket streaming is on the roadmap.)
6. **Result aggregation** persists final metrics, including per-algorithm contributions, matched sources, fragment excerpts, and audit trail.
7. **Frontend renders** the results dashboard with risk badges, progress bars, top sources, and actionable recommendations.

---

## API Surface

| Endpoint | Method | Purpose | Notes |
|----------|--------|---------|-------|
| `/` | GET | API metadata splash | Build info, version, uptime |
| `/health` | GET | Liveness & readiness probe | Checks Redis connectivity when available |
| `/api/v1/upload` | POST | Submit document or raw text | Returns `job_id` immediately |
| `/api/v1/jobs/{job_id}` | GET | Poll processing status | Includes percentage, current stage, ETA |
| `/api/v1/results/{job_id}` | GET | Retrieve final analysis | Contains similarity breakdown + fragments |
| `/api/v1/auth/login` | POST | (stub) user authentication | Wireframe endpoint for future auth | 
| `/api/v1/auth/register` | POST | (stub) registration | Placeholder for roadmap feature |

All endpoints return structured JSON with error codes aligned to FastAPI exception handlers. CORS is enabled for `http://localhost:3000` by default.

---

## Frontend Experience

### Upload Screen
- Gradient background with radial highlights for premium feel.
- Drag-and-drop zone, file picker, clipboard paste support.
- Live file metadata (type, size) and validation feedback.
- CTA button "🚀 Check for Plagiarism" triggers upload + status poller.

### Results Dashboard
- Prominent overall similarity percentage with color-coded risk badge (Low/Medium/High).
- Per-algorithm bars show contribution of cosine, N-gram, lexical, semantic, etc.
- Fragment viewer highlights suspicious excerpts with source reference and overlap score.
- Secondary stats: processing time, number of sources, token count, detection heuristics triggered.

Responsive layouts ensure that both screens remain usable on tablets and large desktops.

---

## Worker & Processing Pipeline

1. **Ingestion** – document is normalized (PDF/DOCX → text) and split into logical sections.
2. **Embedding generation** – Sentence Transformers produce vector representations; lexical shingles are created for FAISS/Elasticsearch.
3. **Similarity matching** – multiple algorithms (cosine, N-gram, lexical heuristics, semantic) run in parallel to mitigate false negatives.
4. **Aggregation** – per-algorithm scores are weighted, risk levels assigned, matched fragments curated with source context.
5. **Persistence** – results stored for retrieval; optional MinIO/PostgreSQL integration ensures durability.

Mock mode bypasses steps 2–5 with deterministic sample data for rapid UI iteration.

---

## Configuration Reference

### Backend (`backend/.env`)
```env
REDIS_URL=redis://localhost:6379/0
DATABASE_URL=postgresql+psycopg2://user:pass@localhost:5432/plagiarism
JWT_SECRET=your-secret-key
```

### Frontend (`frontend/.env`)
```env
NEXT_PUBLIC_API_BASE=http://localhost:8000
```

### Worker (`worker/.env` or shell)
```env
REDIS_URL=redis://localhost:6379/0
MODEL_NAME=sentence-transformers/all-MiniLM-L6-v2   # example
FAISS_INDEX_PATH=./data/faiss.index
```

### Optional Infrastructure Values
- `MINIO_ENDPOINT`, `MINIO_ACCESS_KEY`, `MINIO_SECRET_KEY`
- `ELASTICSEARCH_URL`
- `LOG_LEVEL`, `SENTRY_DSN`

---

## Troubleshooting & Tips

| Symptom | Likely Cause | Resolution |
|---------|--------------|------------|
| Job stuck in `queued` | Redis not running / worker offline | Start Redis, re-run Celery worker, watch logs |
| Frontend shows CORS error | Missing `NEXT_PUBLIC_API_BASE` or mismatched origin | Verify `.env` and FastAPI CORS origins |
| Uvicorn crashes on start | Virtual env not activated / deps missing | Re-run `pip install -r requirements.txt` inside venv |
| Worker cannot import modules | Started outside repo root | `cd worker` before launching Celery |
| Large PDFs fail | File exceeds configured limit | Adjust backend upload size or compress document |

Use `--reload` for rapid backend iteration and rely on Next.js Hot Reload for UI changes.

---

## Roadmap

- [ ] Full authentication & RBAC
- [ ] Document history dashboard with saved reports
- [ ] PDF/DOCX export of analysis summaries
- [ ] Batch processing & scheduling
- [ ] Rate limiting + usage analytics
- [ ] Advanced multilingual models (LaBSE, XLM-R)
- [ ] WebSocket live progress streaming
- [ ] Premium tier (custom thresholds, branded reports)

---

## License

Educational and professional use permitted. Contact the maintainers for commercial licensing inquiries.
