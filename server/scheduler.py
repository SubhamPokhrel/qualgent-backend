import time
from collections import defaultdict

def scheduler_loop(jobs_store: dict, queue: list):
    """
    Every 5 seconds, group queued jobs by app_version_id, mark them running,
    simulate execution, then mark them completed.
    """
    while True:
        if queue:
            groups = defaultdict(list)
            # group jobs
            for job_id in list(queue):
                payload = jobs_store[job_id]["payload"]
                groups[payload.app_version_id].append(job_id)

            # process each group in turn
            for app_ver, job_ids in groups.items():
                for jid in job_ids:
                    jobs_store[jid]["status"] = "running"
                # simulate test execution time
                time.sleep(2)
                for jid in job_ids:
                    jobs_store[jid]["status"] = "completed"
                    jobs_store[jid]["result"] = f"Test {jobs_store[jid]['payload'].test_path} completed"
                    queue.remove(jid)
        time.sleep(5)
