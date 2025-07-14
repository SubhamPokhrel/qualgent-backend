from fastapi import FastAPI, HTTPException
from server.models import JobPayload, JobStatus
import uuid
from typing import Dict, List

app = FastAPI()
jobs_store: Dict[str, dict] = {}
queue: List[str] = []

@app.post("/jobs", response_model=JobStatus)
def submit_job(payload: JobPayload):
    job_id = str(uuid.uuid4())
    jobs_store[job_id] = {
        "payload": payload,
        "status": "queued",
        "result": None
    }
    queue.append(job_id)
    return JobStatus(job_id=job_id, status="queued")

@app.get("/jobs/{job_id}", response_model=JobStatus)
def get_status(job_id: str):
    if job_id not in jobs_store:
        raise HTTPException(status_code=404, detail="Job not found")
    job = jobs_store[job_id]
    return JobStatus(job_id=job_id, status=job["status"], result=job["result"])

@app.on_event("startup")
def start_scheduler():
    import threading
    from server.scheduler import scheduler_loop
    thread = threading.Thread(
        target=scheduler_loop, args=(jobs_store, queue), daemon=True
    )
    thread.start()
