import subprocess

def run_emulator_test(job_data):
    test_path = job_data["test_path"]
    try:
        result = subprocess.run(
            ["npx", "playwright", "test", test_path, "--project=Pixel 9a"],
            capture_output=True,
            text=True,
            check=True
        )
        return {
            "status": "passed",
            "output": result.stdout
        }
    except subprocess.CalledProcessError as e:
        return {
            "status": "failed",
            "error": e.stderr
        }
