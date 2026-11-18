"""Accuracy report: run the gold set against a running service and compare each verdict to its reference label.

This measures the scorer against the hand-authored reference labels in tests/gold/ (ground truth a reviewer
agreed on), NOT against the model's own AI-written keys and NOT against a statistically representative sample
of production calls. It is a regression and sanity tool: it tells you when a change moves a known case the
wrong way, and gives a per-check precision/recall so a gate change can be judged on evidence.

Usage (service must be up, e.g. `docker compose up -d --build`, model loaded):
    python Scripts/accuracy_report.py
    python Scripts/accuracy_report.py --url http://localhost:8006/api/evaluate --gold tests/gold
"""
import argparse
import json
import os
import sys
import urllib.error
import urllib.request

_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))


def _norm(name):
    return " ".join((name or "").split()).strip().lower()


def load_gold(gold_dir):
    cases = []
    for fname in sorted(os.listdir(gold_dir)):
        if not fname.endswith(".json"):
            continue
        with open(os.path.join(gold_dir, fname), "r", encoding="utf-8") as f:
            case = json.load(f)
        case["_file"] = fname
        cases.append(case)
    return cases


def evaluate(url, payload):
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=600) as resp:
        body = json.loads(resp.read().decode("utf-8"))
    return body.get("result", body)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--url", default=os.getenv("API_EVALUATE_URL", "http://localhost:8006/api/evaluate"))
    ap.add_argument("--gold", default=os.path.join(_ROOT, "tests", "gold"))
    args = ap.parse_args()

    cases = load_gold(args.gold)
    if not cases:
        print(f"No gold cases found in {args.gold}")
        return 1

    # Per check, treating FAIL as the positive class (the problem the scorer should catch).
    stat = {}                                                   # check -> {tp, fp, fn, tn}
    case_rows = []
    total_match = total_checks = 0

    for case in cases:
        expected = {_norm(k): v.upper() for k, v in case.get("expected", {}).items()}
        try:
            result = evaluate(args.url, case["payload"])
        except (urllib.error.URLError, urllib.error.HTTPError, OSError) as e:
            print(f"  [{case['name']}] request failed: {e}")
            return 1
        got = {_norm(e["name"]): e["rating"].upper() for e in result.get("scorecard", [])}

        mism = []
        for check, want in expected.items():
            have = got.get(check)
            if have is None:
                continue
            s = stat.setdefault(check, {"tp": 0, "fp": 0, "fn": 0, "tn": 0})
            if want == "FAIL" and have == "FAIL":
                s["tp"] += 1
            elif want == "PASS" and have == "FAIL":
                s["fp"] += 1
            elif want == "FAIL" and have == "PASS":
                s["fn"] += 1
            else:
                s["tn"] += 1
            total_checks += 1
            if want == have:
                total_match += 1
            else:
                mism.append(f"{check}: expected {want}, got {have}")

        af_want = bool(case.get("expected_auto_fail", False))
        af_have = bool(result.get("is_auto_fail"))
        af_note = "" if af_want == af_have else f" | AUTO-FAIL expected {af_want}, got {af_have}"
        case_rows.append((case["name"], result.get("final_score"), len(mism), mism, af_note))

    print("=" * 72)
    print("PER-CASE")
    print("=" * 72)
    for name, score, nmis, mism, af_note in case_rows:
        flag = "OK " if nmis == 0 and not af_note else "XX "
        print(f"{flag}{name:22} score={score}{af_note}")
        for m in mism:
            print(f"      - {m}")

    print("\n" + "=" * 72)
    print("PER-CHECK (FAIL = positive class)")
    print("=" * 72)
    print(f"{'check':34} {'acc':>6} {'prec':>6} {'rec':>6}   (tp/fp/fn/tn)")
    for check in sorted(stat):
        s = stat[check]
        n = s["tp"] + s["fp"] + s["fn"] + s["tn"]
        acc = (s["tp"] + s["tn"]) / n if n else 0.0
        prec = s["tp"] / (s["tp"] + s["fp"]) if (s["tp"] + s["fp"]) else float("nan")
        rec = s["tp"] / (s["tp"] + s["fn"]) if (s["tp"] + s["fn"]) else float("nan")
        print(f"{check:34} {acc:6.2f} {prec:6.2f} {rec:6.2f}   ({s['tp']}/{s['fp']}/{s['fn']}/{s['tn']})")

    overall = total_match / total_checks if total_checks else 0.0
    print("\n" + "=" * 72)
    print(f"OVERALL: {total_match}/{total_checks} verdicts match reference labels ({overall:.1%})")
    print("=" * 72)
    return 0


if __name__ == "__main__":
    sys.exit(main())
