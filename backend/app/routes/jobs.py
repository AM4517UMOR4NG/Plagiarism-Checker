from fastapi import APIRouter, HTTPException
from app.core.celery_app import celery_app

router = APIRouter()


@router.get("/jobs/{job_id}")
async def get_job(job_id: str):
    # Development fallback: instantly mark dev_ jobs as ready
    if job_id.startswith("dev_"):
        return {"job_id": job_id, "status": "SUCCESS", "ready": True}
    res = celery_app.AsyncResult(job_id)
    if res is None:
        raise HTTPException(status_code=404, detail="Job not found")
    return {"job_id": job_id, "status": res.status, "ready": res.ready()}
