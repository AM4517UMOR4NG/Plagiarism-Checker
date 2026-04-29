# Plagiarism Checker

Professional-grade plagiarism detection platform that combines FastAPI services, Celery-powered background processing, and a polished Next.js 14 interface. The system emulates commercial plagiarism suites with rich analytics, fragment-level insights, and extensible infrastructure for production deployments.

<p align="center">
  <img alt="Status" src="https://img.shields.io/badge/status-active-success?style=for-the-badge&color=10b981" />
  <img alt="Backend" src="https://img.shields.io/badge/FastAPI-Backend-0EA5E9?style=for-the-badge&logo=fastapi" />
  <img alt="Frontend" src="https://img.shields.io/badge/Next.js-14-000000?style=for-the-badge&logo=next.js" />
  <img alt="License" src="https://img.shields.io/badge/License-Professional-blueviolet?style=for-the-badge" />
</p>

<div align="center">
  <table>
    <tr>
      <td><strong>⚙️ Pipelines</strong><br/>Hybrid Celery workers orchestrate multi-stage NLP similarity checks.</td>
      <td><strong>📊 Analytics</strong><br/>Risk gradients, fragment explorer, per-algorithm telemetry.</td>
      <td><strong>☁️ Infra Ready</strong><br/>Docker-first layouts + IaC scaffolding for cloud rollout.</td>
    </tr>
  </table>
</div>

---

## Table of Contents
1. [Visual Overview](#visual-overview)
2. [Architecture at a Glance](#architecture-at-a-glance)
3. [Feature Overview](#feature-overview)
4. [Directory Structure](#directory-structure)
5. [Environment Matrix](#environment-matrix)
6. [System Components](#system-components)
7. [Quick Start (Windows)](#quick-start-windows)
8. [Deployment Options](#deployment-options)
9. [End-to-End Workflow](#end-to-end-workflow)
10. [Data Lifecycle & Storage](#data-lifecycle--storage)
11. [API Surface](#api-surface)
12. [Frontend Experience](#frontend-experience)
13. [Worker & Processing Pipeline](#worker--processing-pipeline)
14. [Testing & Quality](#testing--quality)
15. [Observability & Operations](#observability--operations)
16. [Security & Compliance](#security--compliance)
17. [Performance & Scalability](#performance--scalability)
18. [Configuration Reference](#configuration-reference)
19. [Troubleshooting & Tips](#troubleshooting--tips)
20. [Roadmap](#roadmap)
21. [Supporting Docs](#supporting-docs)
22. [Contribution Guidelines](#contribution-guidelines)
23. [License](#license)

---

## Visual Overview

> **Experience Flow** – From dropzone to insight cards, every touchpoint is illustrated below for a quick mental model.

```mermaid
graph LR
    A[User Uploads] --> B(Next.js Form)
    B --> C{FastAPI Gateway}
    C -->|Validate| D[(PostgreSQL)]
    C -->|Enqueue| E[[Redis Queue]]
    E --> F[[Celery Workers]]
    F --> G[Similarity Engines]
    G --> H>Results Store]
    H --> I{Results API}
    I --> J[Interactive Dashboard]
```

```mermaid
sequenceDiagram
    participant User
    participant UI as Frontend UI
    participant API as FastAPI
    participant Worker as Celery Worker
    participant Store as Results Store

    User->>UI: Drag & drop document
    UI->>API: POST /api/v1/upload
    API->>Worker: Dispatch job (Redis)
    Worker-->>API: Status updates
    API-->>UI: job_id + progress
    Worker->>Store: Persist scores/fragments
    UI->>API: GET /api/v1/results/{job_id}
    API->>UI: Detailed report JSON
    UI->>User: Visual insights + fragments
```

### UI Layout Blueprint

```
┌───────────────────────────────────────────┐
│ Header (logo + action buttons)           │
├───────────────┬──────────────────────────┤
│ Upload Panel  │ Hero Metrics Card        │
│ - Drag area   │ - Similarity gauge       │
│ - File stats  │ - Risk badge             │
├───────────────┴──────────────────────────┤
│ Algorithm Breakdown (progress stacks)    │
├──────────────────────────────────────────┤
│ Fragment Explorer + Source Timeline      │
└───────────────────────────────────────────┘
```

Pair these visuals with live screenshots (drop `docs/ui-preview.png`) to complete the narrative.

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

## System Components

| Component | Location | Responsibilities | Notes |
|-----------|----------|------------------|-------|
| **Frontend Web App** | `frontend/` | Next.js 14 pages, upload form, results dashboard, REST client hooks | Uses React Server Components + Tailwind/inline styles |
| **Backend API** | `backend/` | FastAPI routers, job persistence, validation, REST contract, CORS config | Houses Pydantic models, SQLAlchemy ORM, Celery config |
| **Worker Engine** | `worker/` | Celery tasks for preprocessing, embedding, similarity scoring, aggregation | Imports shared utilities from backend via package path |
| **Messaging Layer** | Redis | Task queue, rate limiting primitives, caching (optional) | Required when running Celery |
| **Relational DB** | PostgreSQL (planned) | Persist jobs, documents, audit trail | SQLite fallback possible for dev |
| **Object Storage** | MinIO / S3 (planned) | Binary document storage, derived artifacts | Optional in dev; local filesystem fallback |
| **Search Index** | FAISS + Elasticsearch (planned) | Vector similarity & full-text search over corpus | Activated in production profile |
| **Infrastructure** | `infrastructure/` | Dockerfiles, Compose templates, IaC stubs | Extend to Helm/Terraform as needed |

All components are decoupled through Celery tasks and REST APIs, allowing independent scaling.

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

## Deployment Options

| Scenario | Strategy | Commands / Notes |
|----------|----------|------------------|
| **Local Development** | Run backend, frontend, and (optionally) worker directly as described above | Ideal for rapid iteration; uses mock data when worker offline |
| **Docker Compose (hybrid)** | Use manifests in `infrastructure/` (extend `docker-compose.yml`) to spin up API, worker, Redis | Great for parity with staging; mount source dirs for live reload |
| **Production** | Containerize services, deploy behind reverse proxy (NGINX/Caddy), attach managed Redis/PostgreSQL, configure TLS | Ensure environment secrets injected via CI/CD or orchestration (Kubernetes/Nomad) |

General guidance:
1. Use `.env` files per service and never commit secrets.
2. Frontend can be statically exported or hosted via Next.js server. Configure `NEXT_PUBLIC_API_BASE` to public gateway.
3. Add autoscaling for Celery workers when queue depth increases; keep API stateless for horizontal scaling.

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

## Data Lifecycle & Storage

| Stage | Description | Storage Layer |
|-------|-------------|---------------|
| **Acquisition** | User uploads file / text; metadata captured | FastAPI request body, temporary disk buffer |
| **Normalization** | Files converted to plain text, sanitized, chunked | In-memory during job; optional MinIO snapshot |
| **Processing Artifacts** | Embeddings, shingles, algorithm metrics | Redis (short-term) + FAISS index + PostgreSQL JSON fields |
| **Result Persistence** | Final similarity scores, fragments, risk levels | PostgreSQL tables (`jobs`, `results`, `fragments`) |
| **Archival / Cleanup** | Old jobs pruned or archived based on retention policy | MinIO bucket lifecycle rules or manual scripts |

Personally identifiable information (PII) should be anonymized before long-term storage. Update retention jobs to purge raw uploads if policy requires.

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


## Testing & Quality

| Scope | Command | Notes |
|-------|---------|-------|
| **Backend unit tests** | `cd backend && pytest` | Covers FastAPI routes, services, Celery tasks (mocked) |
| **Backend linting** | `cd backend && ruff check .` | Enforces PEP8/ruff rules |
| **Frontend tests** | `cd frontend && npm run test` | Jest / React Testing Library snapshots |
| **Frontend linting** | `cd frontend && npm run lint` | Next.js ESLint config |
| **Type checking** | `cd frontend && npm run type-check` | Ensures TypeScript safety |

CI (recommended):
1. Install dependencies for every service.
2. Run lint + tests in parallel to keep pipelines fast.
3. Upload coverage artifacts (Codecov/Sonar) for regression awareness.

---

## Observability & Operations

- **Logging**: Backend and worker emit structured logs (JSON-friendly). Configure log level via `LOG_LEVEL` env.
- **Metrics**: Expose Prometheus-compatible metrics (planned) using FastAPI instrumentation; Celery provides task runtime stats.
- **Tracing**: Hooks in place for OpenTelemetry exporters. Configure `OTEL_EXPORTER_OTLP_ENDPOINT` when available.
- **Health Checks**: `/health` verifies app + Redis; add DB ping when configured.
- **Alerting**: Wire logs/metrics into preferred stack (ELK, Grafana, Sentry) for error budgets.

Operational checklist:
1. Monitor queue length to scale workers.
2. Enforce log retention; mask document snippets before shipping logs externally.
3. Enable structured exception handling to avoid leaking stack traces to end users.

---

## Security & Compliance

- **Secrets Management**: Never commit `.env`; load via secret manager (Azure Key Vault, AWS Secrets Manager) in production.
- **Transport Security**: Terminate TLS at ingress; enforce HTTPS-only cookies when auth launches.
- **Input Validation**: FastAPI validators enforce file size/type; extend with antivirus scanning (ClamAV) for uploaded files.
- **Access Control**: Auth endpoints stubbed—connect to JWT or OAuth provider before exposing externally.
- **Audit Logging**: Persist job ownership, timestamps, IP metadata for compliance.
- **Data Privacy**: Provide data deletion endpoints to meet GDPR/PDPA requirements; document retention schedules.

---

## Performance & Scalability

- **Asynchronous Processing**: Celery decouples CPU-heavy work; scale worker replicas horizontally.
- **Batching**: Group embedding requests when using GPU-backed models to improve throughput.
- **Caching**: Cache frequent corpus comparisons in Redis/FAISS to reduce duplicate work.
- **Chunk Strategy**: Tune chunk size + overlap for long documents to balance accuracy vs speed.
- **Resource Limits**: Set `--concurrency` on Celery workers based on CPU cores; enable autoscaling rules in orchestrator.
- **Frontend Optimization**: Prefetch API calls, leverage Next.js image optimization, lazy load heavy components.

Benchmark before production pushes and document realistic SLAs (e.g., <10s for 10-page document).

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

## Supporting Docs

- `CARA_MENJALANKAN.md` – Bahasa Indonesia quick-start guide with screenshots.
- `infrastructure/` – templates for containerization, compose stacks, and future IaC scripts.
- API schemas & mock responses (planned) – publish via Swagger UI (`/docs`) and Postman collection.

Ensure any new operational playbooks or design decisions are mirrored in this README and supporting docs.

---

## Contribution Guidelines

1. Fork the repository and create a topic branch (`feat/<name>` or `fix/<name>`).
2. Install dependencies for relevant services and ensure `pre-commit` (if configured) passes.
3. Add/adjust tests for every code change; keep README/diagram updates in the same PR when relevant.
4. Run the full lint/test matrix before opening a PR.
5. Use descriptive commit messages and link issue tracker IDs if available.
6. Submit PR with context, screenshots (for UI), and verification checklist.

Code reviews focus on correctness, readability, and adherence to the architecture described above.

---

---

## License

Educational and professional use permitted.
