#!/usr/bin/env python3
import argparse
import requests
import sys

API_URL = "http://localhost:8000"

def submit(args):
    payload = {
        "org_id": args.org_id,
        "app_version_id": args.app_version_id,
        "test_path": args.test,
        "priority": args.priority,
        "target": args.target,
    }
    resp = requests.post(f"{API_URL}/jobs", json=payload)
    if resp.status_code == 200:
        data = resp.json()
        print(f"Job submitted: {data['job_id']} (status: {data['status']})")
    else:
        print(f"Error submitting job: {resp.text}", file=sys.stderr)
        sys.exit(1)

def status(args):
    resp = requests.get(f"{API_URL}/jobs/{args.job_id}")
    if resp.status_code == 200:
        data = resp.json()
        print(f"Job {data['job_id']} status: {data['status']}")
        if data.get("result"):
            print(f"Result: {data['result']}")
        sys.exit(0 if data["status"] == "completed" else 2)
    else:
        print(f"Error fetching status: {resp.text}", file=sys.stderr)
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(prog="qgjob")
    subparsers = parser.add_subparsers(dest="command")

    ps = subparsers.add_parser("submit", help="Submit a test job")
    ps.add_argument("--org-id", required=True, help="Organization ID")
    ps.add_argument("--app-version-id", required=True, help="App version to test")
    ps.add_argument("--test", required=True, help="Path to test script")
    ps.add_argument("--priority", type=int, default=0, help="Job priority")
    ps.add_argument(
        "--target",
        choices=["emulator", "device", "browserstack"],
        default="emulator",
        help="Execution target",
    )
    ps.set_defaults(func=submit)

    ps2 = subparsers.add_parser("status", help="Check status of a job")
    ps2.add_argument("--job-id", required=True, help="ID of the job")
    ps2.set_defaults(func=status)

    args = parser.parse_args()
    if not hasattr(args, "func"):
        parser.print_help()
        sys.exit(1)
    args.func(args)

if __name__ == "__main__":
    main()
