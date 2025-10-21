from fastapi import APIRouter, HTTPException
from app.core.celery_app import celery_app

router = APIRouter()


@router.get("/results/{job_id}")
async def get_result(job_id: str):
    # Development fallback: return a mocked result for dev_ jobs
    if job_id.startswith("dev_"):
        import random
        similarity_score = round(random.uniform(0.08, 0.35), 3)
        return {
            "job_id": job_id,
            "status": "SUCCESS",
            "result": {
                "doc_id": job_id.replace("dev_", ""),
                "title": "Professional Document Analysis",
                "summary": {
                    "similarity": similarity_score,
                    "sources": [
                        {"title": "Academic Paper Database", "url": "https://example.com/paper1"},
                        {"title": "Web Content Archive", "url": "https://example.com/web1"}
                    ],
                    "processing_time_ms": random.randint(1200, 2800)
                },
                "fragments": [
                    {
                        "text": "This is a sample text fragment that demonstrates content matching capabilities of the plagiarism detection system.",
                        "score": round(similarity_score * 0.9, 3),
                        "source": "Academic Research Database"
                    },
                    {
                        "text": "Another example of matched content showing similarity analysis across multiple documents and sources.",
                        "score": round(similarity_score * 0.7, 3),
                        "source": "Online Publication Archive"
                    },
                    {
                        "text": "Advanced detection algorithms identify semantic similarity patterns beyond simple text matching.",
                        "score": round(similarity_score * 0.5, 3),
                        "source": "Scientific Journal Repository"
                    }
                ],
                "explain": {
                    "cosine": round(similarity_score * 0.8, 3),
                    "ngram": round(similarity_score * 0.6, 3),
                    "lexical": round(similarity_score * 0.9, 3),
                    "semantic": round(similarity_score * 0.7, 3)
                }
            },
        }
    res = celery_app.AsyncResult(job_id)
    if not res.ready():
        return {"job_id": job_id, "status": res.status, "result": None}
    result = res.get()  # In dev, ok. In prod, prefer storing in DB and return URL.
    if result is None:
        raise HTTPException(status_code=404, detail="Result not found")
    return {"job_id": job_id, "status": res.status, "result": result}
