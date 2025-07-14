from pydantic import BaseModel
from typing import Optional

class JobPayload(BaseModel):
    org_id: str
    app_version_id: str
    test_path: str
    priority: int = 0
    target: str

class JobStatus(BaseModel):
    job_id: str
    status: str
    result: Optional[str] = None
