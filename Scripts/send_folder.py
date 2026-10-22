"""Send every call in a folder to the running QA service (REST) and save each response as a JSON file in an outputs folder.

    python Scripts/send_folder.py                              # everything under inputs/  ->  outputs/
    python Scripts/send_folder.py "inputs/AG-T" --limit 5      # one set, first 5 calls
    python Scripts/send_folder.py inputs --only agt_01         # only files whose path contains this text
    python Scripts/send_folder.py inputs --redo                # grade again even if a response file already exists

Input: .json files that hold a "transcript" (the whole request, or see Scripts/try_call.py for the formats) and .txt transcripts
(one "Agent: ..." / "Customer: ..." line per turn). Folders named expected, Test (results) and __pycache__ are skipped.
Output: outputs/<same sub-folder>/<same file name>.json holds the service's reply exactly as received (call_id, tenant_id, status,
result{final_score, scorecard[], is_auto_fail, auto_fail_reason, meta}); a failed call is saved as <name>.error.json. After every run
outputs/_summary.csv is rebuilt with one line per response (score, failed checks, seconds).
Calls already answered are skipped, so an interrupted run can simply be started again. The service must be running
(python main.py, LAYA_FLOW=v3). Default address http://127.0.0.1:8006.
"""
import argparse
import csv
import json
import os
import sys
import time
import urllib.error
import urllib.request

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SKIP_DIRS = {"expected", "test (results)", "__pycache__", ".git"}


def find_calls(folder):
    out = []
    for dirpath, dirnames, filenames in os.walk(folder):
        dirnames[:] = sorted(d for d in dirnames if d.lower() not in SKIP_DIRS)
        for fn in sorted(filenames):
            low = fn.lower()
            if low.startswith("result") or low.endswith(".error.json"):
                continue
            path = os.path.join(dirpath, fn)
            if low.endswith(".txt"):
                out.append(path)
            elif low.endswith(".json"):
                try:
                    data = json.load(open(path, encoding="utf-8"))
                except Exception:
                    continue
                if (isinstance(data, dict) and data.get("transcript")) or isinstance(data, list):
                    out.append(path)
    return out


def load_body(path):
    if path.lower().endswith(".txt"):
        body = {"transcript": open(path, encoding="utf-8").read()}
    else:
        data = json.load(open(path, encoding="utf-8"))
        body = data if isinstance(data, dict) else {"transcript": data}
    body.setdefault("call_id", os.path.splitext(os.path.basename(path))[0])
    return body


def post(url, body, timeout=600):
    req = urllib.request.Request(url, data=json.dumps(body).encode(), method="POST", headers={"content-type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return r.status, json.loads(r.read())
    except urllib.error.HTTPError as e:
        raw = e.read()
        try:
            return e.code, json.loads(raw)
        except Exception:
            return e.code, {"detail": raw[:300].decode("utf-8", "replace")}


def get(url, timeout=60):
    with urllib.request.urlopen(url, timeout=timeout) as r:
        return json.loads(r.read())


def grade(base, body):
    """POST /api/evaluate; if the service says it is still working (503 with a job id), poll that job until it finishes."""
    code, reply = post(base + "/api/evaluate", body)
    detail = reply.get("detail") if isinstance(reply, dict) else None
    if code == 503 and isinstance(detail, dict) and detail.get("job_id"):
        for _ in range(180):
            time.sleep(5)
            job = get(f"{base}/api/jobs/{detail['job_id']}")
            if job.get("status") == "done":
                return 200, {"call_id": job.get("call_id"), "tenant_id": job.get("tenant_id"), "status": "completed", "result": job["result"]}
            if job.get("status") == "failed":
                return (job.get("error") or {}).get("status", 500), {"detail": (job.get("error") or {}).get("detail")}
    return code, reply


def write_summary(out_dir):
    rows = []
    for dirpath, _, filenames in os.walk(out_dir):
        for fn in sorted(filenames):
            if not fn.endswith(".json") or fn.endswith(".error.json"):
                continue
            path = os.path.join(dirpath, fn)
            try:
                data = json.load(open(path, encoding="utf-8"))
                res = data["result"]
            except Exception:
                continue
            failed = [i["name"] for i in res["scorecard"] if i["rating"] == "FAIL"]
            rows.append({"set": os.path.relpath(dirpath, out_dir).replace("\\", "/"), "call": os.path.splitext(fn)[0], "final_score": res["final_score"],
                         "auto_fail": res["is_auto_fail"], "failed_count": len(failed), "failed_checks": "; ".join(failed),
                         "seconds": res.get("meta", {}).get("seconds", "")})
    with open(os.path.join(out_dir, "_summary.csv"), "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["set", "call", "final_score", "auto_fail", "failed_count", "failed_checks", "seconds"])
        w.writeheader()
        w.writerows(rows)
    return len(rows)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("folder", nargs="?", default="inputs")
    ap.add_argument("--out", default="outputs")
    ap.add_argument("--url", default="http://127.0.0.1:8006")
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--only", default="")
    ap.add_argument("--redo", action="store_true")
    args = ap.parse_args()
    base = args.url.rstrip("/")
    in_root = os.path.abspath(args.folder if os.path.isabs(args.folder) else os.path.join(ROOT, args.folder))
    out_root = os.path.abspath(args.out if os.path.isabs(args.out) else os.path.join(ROOT, args.out))
    top = os.path.join(ROOT, "inputs")                       # response paths mirror the layout under inputs/
    rel_base = top if in_root.startswith(top) else in_root

    try:
        get(base + "/ready")
    except Exception as e:
        print(f"The service is not answering at {base} ({e}). Start it first: LAYA_FLOW=v3 python main.py")
        return 1
    calls = [p for p in find_calls(in_root) if args.only.lower() in p.lower()]
    if args.limit:
        calls = calls[:args.limit]
    print(f"{len(calls)} call file(s) in {in_root}  ->  {out_root}")
    done = skipped = failed = 0
    t_start = time.time()
    for n, path in enumerate(calls, 1):
        rel = os.path.relpath(path, rel_base)
        target = os.path.join(out_root, os.path.splitext(rel)[0] + ".json")
        if os.path.exists(target) and not args.redo:
            skipped += 1
            continue
        os.makedirs(os.path.dirname(target), exist_ok=True)
        t0 = time.time()
        try:
            code, reply = grade(base, load_body(path))
        except Exception as e:
            code, reply = 0, {"detail": f"{type(e).__name__}: {e}"}
        if code == 200 and "result" in reply:
            json.dump(reply, open(target, "w", encoding="utf-8"), indent=2)
            res = reply["result"]
            bad = [i["name"].split(" ")[0] for i in res["scorecard"] if i["rating"] == "FAIL"]
            done += 1
            print(f"[{n}/{len(calls)}] {rel}  ->  {res['final_score']}" + ("  AUTO-FAIL" if res["is_auto_fail"] else "") + f"  fails: {', '.join(bad) or 'none'}  ({time.time() - t0:.1f}s)", flush=True)
        else:
            json.dump({"http_status": code, "reply": reply}, open(target[:-5] + ".error.json", "w", encoding="utf-8"), indent=2)
            failed += 1
            print(f"[{n}/{len(calls)}] {rel}  ->  ERROR {code}: {str(reply)[:150]}", flush=True)
    total = write_summary(out_root) if os.path.isdir(out_root) else 0
    print(f"\nsent {done}, already answered {skipped}, errors {failed}, in {time.time() - t_start:.0f}s. outputs/_summary.csv has {total} line(s).")
    return 0 if not failed else 2


if __name__ == "__main__":
    sys.exit(main())
