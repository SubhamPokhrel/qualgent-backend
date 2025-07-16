# server/main.py
from fastapi import FastAPI, HTTPException
from celery import Celery
from pydantic import BaseModel
from executors.emulator import run_emulator_test
import redis
import json
import time
import os

app = FastAPI()
celery_app = Celery('appwright_tests', broker='redis://localhost:6379')
redis_client = redis.Redis(host='localhost', port=6379, db=0)

class JobRequest(BaseModel):
    org_id: str
    app_version_id: str
    test_path: str
    priority: int = 0
    target: str  # "emulator", "device", "browserstack"
    platform: str = "android"  # "android" or "ios"
    app_path: str = None  # Path to app file

@app.post("/jobs")
async def submit_job(job_request: JobRequest):
    job_id = f"job_{int(time.time())}"
    job_data = job_request.dict()
    job_data['job_id'] = job_id
    
    # Queue the job
    task = run_test_job.delay(job_data)
    
    # Store job info in Redis
    redis_client.hset(f"job:{job_id}", mapping={
        'status': 'queued',
        'task_id': task.id,
        'created_at': str(time.time())
    })
    
    return {"job_id": job_id, "status": "queued"}

@app.get("/jobs/{job_id}")
async def get_job_status(job_id: str):
    job_info = redis_client.hgetall(f"job:{job_id}")
    if not job_info:
        raise HTTPException(status_code=404, detail="Job not found")
    
    result = None
    if job_info.get('result'):
        try:
            result = json.loads(job_info['result'].decode())
        except:
            result = job_info['result'].decode()
    
    return {
        "job_id": job_id,
        "status": job_info.get('status', b'unknown').decode(),
        "result": result
    }

@celery_app.task
def run_test_job(job_data):
    job_id = job_data['job_id']
    target = job_data['target']
    
    try:
        redis_client.hset(f"job:{job_id}", 'status', 'running')
        if target == 'emulator':
            result = run_emulator_test(job_data)
        else:
            raise ValueError(f"Unknown target: {target}")
        
        redis_client.hset(f"job:{job_id}", mapping={
            'status': 'completed',
            'result': json.dumps(result)
        })
        
        return result
        
    except Exception as e:
        redis_client.hset(f"job:{job_id}", mapping={
            'status': 'failed',
            'result': str(e)
        })
        raise