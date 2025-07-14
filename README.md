# QualGent Backend Coding Challenge

## Setup Instructions

1. **Clone** this repo:
   ```bash
   git clone <repo-url> && cd qualgent-backend```


2. **install dependencies** 

```pip install -r requirements.txt

pip install .```


3. **start server** 

```uvicorn server.main:app --reload```


4. **submit job** 

```qgjob submit \
  --org-id=qualgent \
  --app-version-id=xyz123 \
  --test=tests/onboarding.spec.js```


5. **check status** 

```qgjob status --job-id=<JOB_ID>```


6. **Architecture Design**  in mermaid code

```graph LR
  CLI[qgjob CLI] -->|HTTP POST /jobs| Server[Job Server (FastAPI)]
  Server -->|enqueue| Queue[In-Memory Queue]
  Scheduler[Background Scheduler] -->|group by app_version_id| Queue
  Scheduler -->|dispatch| Worker[Agent Simulator]
  Worker -->|run tests| Targets[Device/Emulator/BrowserStack]
  Worker -->|update| Server```
