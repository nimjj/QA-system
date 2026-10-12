"""Post a folder of sample calls to a running QA service and save each scorecard.

Usage (from the repo root):
    python Scripts/batch_test.py                      # inputs/Main tests
    python Scripts/batch_test.py bulk                 # inputs/Bulk tests
    python Scripts/batch_test.py "inputs/Tough checks" --label ollama
    python Scripts/batch_test.py main --dry-run       # list what would be sent

Every payload gets the tenant's criteria from resources/criteria_config.json as `criteria_data`
(unless it already has one), so no database is needed. --use-db sends payloads unchanged instead.
Results go to "inputs/Test (results)/<suite> (<label>)/".
"""
import argparse
import glob
import json
import os
import time
import urllib.error
import urllib.request
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SERVER_PORT = os.getenv("SERVER_PORT", "8006")
API_EVALUATE_URL = os.getenv("API_EVALUATE_URL", f"http://localhost:{SERVER_PORT}/api/evaluate")
SUITES = {
    "main": os.path.join(ROOT, "inputs", "Main tests"),
    "bulk": os.path.join(ROOT, "inputs", "Bulk tests"),
}
RESULTS_DIR = os.path.join(ROOT, "inputs", "Test (results)")
CRITERIA_FILE = os.path.join(ROOT, "resources", "criteria_config.json")


def find_calls(folder):
    """Every JSON under folder that is a call payload (has a transcript); expected/ and result files are skipped."""
    calls = []
    for fp in sorted(glob.glob(os.path.join(folder, "**", "*.json"), recursive=True)):
        rel = os.path.relpath(fp, folder)
        parts = rel.lower().replace("\\", "/").split("/")
        if "expected" in parts[:-1] or parts[-1].startswith(("result_", "expected_")):
            continue
        try:
            with open(fp, "r", encoding="utf-8") as f:
                payload = json.load(f)
        except (OSError, json.JSONDecodeError):
            continue
        if isinstance(payload, dict) and payload.get("transcript"):
            calls.append((rel, payload))
    return calls


def main():
    parser = argparse.ArgumentParser(description="Post sample calls to /api/evaluate and save the scorecards.")
    parser.add_argument("suite", nargs="?", default="main", help="main, bulk, or a folder path (default: main)")
    parser.add_argument("--label", default="", help="engine label for the results folder, e.g. ollama or laya")
    parser.add_argument("--url", default=API_EVALUATE_URL, help=f"evaluate endpoint (default: {API_EVALUATE_URL})")
    parser.add_argument("--use-db", action="store_true", help="don't add criteria_data; let the service read PostgreSQL")
    parser.add_argument("--dry-run", action="store_true", help="list the calls that would be sent, send nothing")
    parser.add_argument("--timeout", type=int, default=1800, help="seconds to wait for each call (default: 1800)")
    args = parser.parse_args()

    folder = SUITES.get(args.suite.lower(), os.path.abspath(args.suite))
    if not os.path.isdir(folder):
        print(f"Folder not found: {folder}")
        return
    calls = find_calls(folder)
    if not calls:
        print(f"No call payloads found in '{folder}'.")
        return

    criteria = {}
    if not args.use_db:
        with open(CRITERIA_FILE, "r", encoding="utf-8") as f:
            criteria = json.load(f)

    suite_name = os.path.basename(folder.rstrip("\\/"))
    out_dir = os.path.join(RESULTS_DIR, f"{suite_name} ({args.label})" if args.label else suite_name)

    print(f"Found {len(calls)} calls in '{os.path.relpath(folder, ROOT)}'. "
          f"Criteria: {'database' if args.use_db else 'resources/criteria_config.json'}.")
    if args.dry_run:
        for rel, payload in calls:
            source = "payload" if payload.get("criteria_data") else ("database" if args.use_db else "injected")
            print(f"  {rel}  ({len(payload['transcript'])} turns, criteria: {source})")
        print(f"Results would go to: {os.path.relpath(out_dir, ROOT)}")
        return

    os.makedirs(out_dir, exist_ok=True)
    print(f"Endpoint: {args.url}\nResults:  {os.path.relpath(out_dir, ROOT)}\n")

    timings, failures = [], 0
    for idx, (rel, payload) in enumerate(calls, 1):
        print(f"[{idx}/{len(calls)}] Processing: {rel}")
        if not args.use_db and not payload.get("criteria_data"):
            tenant = payload.get("tenant_id") or payload.get("tenantId") or "tenant-abc"
            payload["criteria_data"] = criteria.get(tenant) or criteria["tenant-abc"]

        start = time.perf_counter()
        try:
            req = urllib.request.Request(
                args.url,
                data=json.dumps(payload).encode("utf-8"),
                headers={"Content-Type": "application/json"}
            )
            with urllib.request.urlopen(req, timeout=args.timeout) as resp:
                result_data = json.loads(resp.read().decode("utf-8"))
        except Exception as e:
            failures += 1
            print(f"  -> EXCEPTION after {time.perf_counter() - start:.1f}s: {e}\n")
            continue

        elapsed = round(time.perf_counter() - start, 1)
        timings.append(elapsed)
        result_data["engine_label"] = args.label or None
        result_data["elapsed_sec"] = elapsed

        status = result_data.get("status", "completed")
        final_score = result_data.get("result", {}).get("final_score")
        print(f"  -> [{status.upper()}] Final Score: {final_score}  ({elapsed}s)")

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = os.path.join(out_dir, f"result_{timestamp}_{rel.replace(os.sep, '__').replace('/', '__')}")
        with open(output_path, "w", encoding="utf-8") as out_f:
            json.dump(result_data, out_f, indent=2)
        print(f"  -> Saved result to: {os.path.relpath(output_path, ROOT)}\n")

    mean = f"{sum(timings) / len(timings):.1f}s" if timings else "n/a"
    print(f"Done: {len(timings)} succeeded, {failures} failed, mean time per call {mean}.")


if __name__ == "__main__":
    main()
