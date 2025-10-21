from fastapi import FastAPI, Response
from fastapi.middleware.cors import CORSMiddleware

from app.routes import upload, jobs, results, auth

app = FastAPI(title="Plagiarism Checker API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/api/v1", tags=["auth"])
app.include_router(upload.router, prefix="/api/v1", tags=["upload"])
app.include_router(jobs.router, prefix="/api/v1", tags=["jobs"])
app.include_router(results.router, prefix="/api/v1", tags=["results"])


@app.get("/", tags=["info"])
async def root():
    return {
        "name": "Plagiarism Checker API",
        "version": "0.1.0",
        "endpoints": {
            "health": "/health",
            "upload": "POST /api/v1/upload",
            "jobs": "GET /api/v1/jobs/{job_id}",
            "results": "GET /api/v1/results/{job_id}",
            "auth": "/api/v1/auth/login, /api/v1/auth/register"
        },
        "frontend": "http://localhost:3000"
    }


@app.get("/health", tags=["health"])
async def health():
    return {"status": "ok"}


@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return Response(status_code=204)
