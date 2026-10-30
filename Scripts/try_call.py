"""Send one call to a running QA service and print the result in plain language.

    python Scripts/try_call.py path/to/call.json
    python Scripts/try_call.py path/to/call.txt --name "Sam Smith"     # a text transcript: one "Agent: ..." / "Customer: ..." line per turn

A .json file is either the whole request ({"transcript": [...], "customer_name": "..."}) or just the list of turns
[{"speaker": "Agent", "text": "...", "start_time_sec": 0}, {"speaker": "Customer", "text": "...", "start_time_sec": 8, "sentiment_score": -20}].
Customer turns may carry a sentiment_score (negative = upset); without scores the mood-based part of "Confirmed the issue is resolved"
falls back to the model alone. A text file may start each line with a time like [01:05] or 1:05.

The service must be running (python main.py, with LAYA_FLOW=v3 and LAYA_CHECKPOINT set). Default address http://127.0.0.1:8006.
"""
import argparse
import json
import os
import sys
import urllib.error
import urllib.request


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("file")
    ap.add_argument("--url", default="http://127.0.0.1:8006")
    ap.add_argument("--name", default=None, help="the customer's name (the Personalized check looks for it)")
    ap.add_argument("--raw", action="store_true", help="also print the full JSON reply")
    args = ap.parse_args()

    with open(args.file, encoding="utf-8") as f:
        text = f.read()
    if args.file.lower().endswith(".json"):
        data = json.loads(text)
        body = data if isinstance(data, dict) else {"transcript": data}
    else:
        body = {"transcript": text}
    if args.name:
        body["customer_name"] = args.name
    body.setdefault("call_id", os.path.splitext(os.path.basename(args.file))[0])

    req = urllib.request.Request(args.url.rstrip("/") + "/api/evaluate", data=json.dumps(body).encode(), method="POST", headers={"content-type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=600) as r:
            reply = json.loads(r.read())
    except urllib.error.HTTPError as e:
        print(f"The service refused the call (HTTP {e.code}): {e.read().decode('utf-8', 'replace')[:400]}")
        return 1
    except urllib.error.URLError as e:
        print(f"Could not reach the service at {args.url}: {e.reason}. Is it running?")
        return 1

    res = reply["result"]
    meta = res.get("meta", {})
    print(f"\nCall {reply.get('call_id')}:  FINAL SCORE {res['final_score']} / 100" + ("   (AUTO-FAIL: " + str(res.get("auto_fail_reason")) + ")" if res.get("is_auto_fail") else ""))
    cat = None
    for item in res["scorecard"]:
        if item["category"] != cat:
            cat = item["category"]
            print(f"\n  {cat}")
        mark = "PASS" if item["rating"] == "PASS" else "FAIL"
        print(f"    {mark}  {item['name']}")
        if mark == "FAIL":
            print(f"          why: {item['coaching']}")
        if item.get("note"):
            print(f"          note: {item['note']}")
        if item.get("evidence_turns"):
            print(f"          see turn(s): {item['evidence_turns']}")
    if meta:
        print(f"\n  graded in {meta.get('seconds')} s with {meta.get('model_rows')} model questions; pipeline {meta.get('flow')}, model {meta.get('model')}")
        for w in meta.get("warnings", []):
            print(f"  warning: {w}")
    if args.raw:
        print(json.dumps(reply, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
