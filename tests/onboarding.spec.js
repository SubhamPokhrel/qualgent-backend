// tests/job-api.spec.js
const { test, expect, request } = require('@playwright/test');

test('submit and fetch job status from FastAPI', async ({ request }) => {
  const API_BASE = 'http://localhost:8000';

  // Submit job
  const jobData = {
    org_id: 'qualgent',
    app_version_id: 'xyz123',
    test_path: 'tests/onboarding.spec.js',
    priority: 0,
    target: 'emulator',
    platform: 'android',
    app_path: 'path',
  };

  const submitRes = await request.post(`${API_BASE}/jobs`, {
    data: jobData,
  });

  if (!submitRes.ok()) {
    const text = await submitRes.text();
    console.error('Submission failed:', submitRes.status(), text);
  }
  expect(submitRes.ok()).toBeTruthy();
  const submitBody = await submitRes.json();
  const jobId = submitBody.job_id;
  console.log('Submitted Job ID:', jobId);

  // Poll until job completes
  let status = 'queued';
  let jobResult;

  for (let i = 0; i < 20; i++) {
    const res = await request.get(`${API_BASE}/jobs/${jobId}`);
    const body = await res.json();
    status = body.status;
    console.log(`Attempt ${i + 1}: Status - ${status}`);
    if (status === 'completed' || status === 'failed') {
      jobResult = body.result;
      break;
    }
    await new Promise((r) => setTimeout(r, 2000));
  }

  expect(status).toBe('completed');
  expect(jobResult).toBeDefined();
  console.log('Result:', jobResult);
});
