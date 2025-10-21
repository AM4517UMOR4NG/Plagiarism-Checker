import uuid
from pathlib import Path
from typing import Optional

from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from pydantic import BaseModel

from app.core.celery_app import celery_app

router = APIRouter()

UPLOAD_DIR = Path(__file__).resolve().parents[2] / "storage" / "uploads"
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


class UploadResponse(BaseModel):
    job_id: str


@router.post("/upload", response_model=UploadResponse)
async def upload(
    file: Optional[UploadFile] = File(default=None),
    text: Optional[str] = Form(default=None),
    title: Optional[str] = Form(default=None),
    user_id: Optional[str] = Form(default=None),
):
    if not file and not text:
        raise HTTPException(status_code=400, detail="Provide either file or text")

    doc_id = str(uuid.uuid4())
    payload = {"doc_id": doc_id, "title": title, "user_id": user_id}

    if file:
        dest = UPLOAD_DIR / f"{doc_id}_{file.filename}"
        content = await file.read()
        dest.write_bytes(content)
        payload.update({"file_path": str(dest)})
    else:
        payload.update({"text": text})

    # Enqueue processing task. If broker is unavailable (dev without Redis),
    # fall back to returning a dev job id so the UI can continue.
    try:
        async_result = celery_app.send_task("worker.process_upload", args=[payload])
        return UploadResponse(job_id=async_result.id)
    except Exception:
        # Development fallback: return a deterministic dev job id
        dev_job_id = f"dev_{doc_id}"
        return UploadResponse(job_id=dev_job_id)
