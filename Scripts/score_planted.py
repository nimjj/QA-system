"""Check and score a planted-fault test set (Docs/GPT_TEST_SET.md): every planted item should FAIL, every other item PASS.

Usage (from the repo root):
    python Scripts/score_planted.py check "inputs/GPT-1"                     # validate the call files, no server needed
    python Scripts/score_planted.py score "inputs/GPT-1" --label v3          # after batch_test.py "inputs/GPT-1" --label v3
    python Scripts/score_planted.py score "inputs/GPT-1" --label v3 --out report.md

The key is each file's "planted_faults" list (codes as in compare_results.DEFECTS); when a file has none, the codes in its name
(gpt_25_empathy_noconfirm) are used. The results are read from "inputs/Test (results)/<folder name> (<label>)/".
The key is AI-written: these numbers are measured against synthetic calls, not human-labelled ones.
"""
import argparse
import glob
import json
import os
import re
import sys

from compare_results import DEFECTS, ITEMS, RESULTS, load_results, ratings

AUTOFAIL_WORDS = re.compile(r"\b(?:fuck\w*|shut up|idiots?|stupid)\b", re.I)


def load_calls(folder):
    """file stem -> payload, for every call JSON directly in folder."""
    calls = {}
    for fp in sorted(glob.glob(os.path.join(folder, "*.json"))):
        with open(fp, encoding="utf-8") as f:
            calls[os.path.basename(fp)[:-len(".json")]] = json.load(f)
    return calls


def planted(stem, payload):
    codes = payload.get("planted_faults")
    if codes is None:
        codes = [t for t in stem.split("_") if t in DEFECTS]
    return [c.strip().lower() for c in codes]


def expected(codes):
    fails = {DEFECTS[c] for c in codes if c in DEFECTS}
    return {name: ("FAIL" if name in fails else "PASS") for name in ITEMS}


def problems(stem, payload):
    """Format mistakes that would make the call or its key unusable."""
    out = []
    codes = payload.get("planted_faults")
    if codes is None:
        out.append("no planted_faults list (using the file name)")
        codes = planted(stem, payload)
    unknown = [c for c in codes if c not in DEFECTS]
    if unknown:
        out.append(f"unknown fault codes {unknown}")
    name_codes = sorted(t for t in stem.split("_") if t in DEFECTS)
    if name_codes and name_codes != sorted(codes):
        out.append(f"planted_faults {sorted(codes)} differ from the file name {name_codes}")
    if not payload.get("customer_name"):
        out.append("no customer_name")
    turns = payload.get("transcript")
    if not isinstance(turns, list) or len(turns) < 20:
        return out + [f"transcript missing or short ({len(turns) if isinstance(turns, list) else 0} turns)"]
    last = -1.0
    no_sent = n_cust = 0
    for i, t in enumerate(turns):
        spk = str(t.get("speaker", ""))
        if spk not in ("Agent", "Customer"):
            out.append(f"turn {i}: speaker {spk!r}")
        start, end = t.get("start_time_sec"), t.get("end_time_sec")
        if not isinstance(start, (int, float)) or not isinstance(end, (int, float)) or end < start:
            out.append(f"turn {i}: bad start/end seconds ({start}, {end})")
        elif start < last:
            out.append(f"turn {i}: starts before the previous turn ended")
        else:
            last = end
        has_sent = t.get("sentiment_score") is not None
        if spk == "Agent" and has_sent:
            out.append(f"turn {i}: agent turn has a sentiment_score")
        if spk == "Customer":
            n_cust += 1
            no_sent += not has_sent
        if spk == "Agent" and AUTOFAIL_WORDS.search(t.get("text", "")):
            out.append(f"turn {i}: agent line would trigger the profanity auto-fail")
    if no_sent:
        out.append(f"{no_sent} of {n_cust} customer turns have no sentiment_score")
    minutes = last / 60
    if not 6 <= minutes <= 25:
        out.append(f"call is {minutes:.1f} minutes long")
    return out


def cmd_check(args):
    calls = load_calls(args.folder)
    if not calls:
        sys.exit(f"No .json calls in {args.folder}")
    bad = 0
    for stem, payload in calls.items():
        issues = problems(stem, payload)
        bad += bool(issues)
        status = "OK  " if not issues else "FIX "
        print(f"{status} {stem}  faults={planted(stem, payload) or 'none'}")
        for p in issues[:8]:
            print(f"       - {p}")
        if len(issues) > 8:
            print(f"       - ... {len(issues) - 8} more")
    counts = {c: 0 for c in DEFECTS if c not in ("nopa",)}
    for stem, payload in calls.items():
        for c in planted(stem, payload):
            counts[c] = counts.get(c, 0) + 1
    print(f"\n{len(calls)} calls, {bad} need fixing. Times each fault is planted: "
          + ", ".join(f"{c} {n}" for c, n in counts.items()))


def cmd_score(args):
    calls = load_calls(args.folder)
    suite = os.path.basename(os.path.abspath(args.folder).rstrip("\\/"))
    results = load_results(suite, args.label)
    if not results:
        sys.exit(f"No results in {os.path.join(RESULTS, f'{suite} ({args.label})')}; run batch_test.py first.")

    # per item: planted calls caught / planted, clean calls passed / clean
    caught = {n: [0, 0] for n in ITEMS}
    passed = {n: [0, 0] for n in ITEMS}
    misses, false_alarms, rows = [], [], []
    for stem, payload in calls.items():
        if stem not in results:
            rows.append(f"| {stem} | - | not graded |")
            continue
        want = expected(planted(stem, payload))
        got = ratings(results[stem])
        wrong = []
        for name in ITEMS:
            if name not in got:
                continue
            if want[name] == "FAIL":
                caught[name][1] += 1
                caught[name][0] += got[name] == "FAIL"
                if got[name] != "FAIL":
                    misses.append(f"{stem}: {name} graded PASS (planted fault)")
                    wrong.append(f"missed {name}")
            else:
                passed[name][1] += 1
                passed[name][0] += got[name] == "PASS"
                if got[name] != "PASS":
                    false_alarms.append(f"{stem}: {name} graded FAIL (not planted)")
                    wrong.append(f"false alarm {name}")
        r = results[stem]["result"]
        score = f"{r['final_score']}" + (" AF" if r.get("is_auto_fail") else "")
        rows.append(f"| {stem} | {score} | {'; '.join(wrong) or 'all match'} |")

    def pct(a, b):
        return f"{a}/{b} ({100 * a / b:.0f}%)" if b else "-"

    lines = [f"# {suite} ({args.label}) vs planted faults", "",
             "Measured against AI-written synthetic calls and keys (planted faults); no human review.", "",
             "| Item | Faults caught | Clean calls passed | Overall |", "|---|---|---|---|"]
    tot = [0, 0]
    for name in ITEMS:
        ok, n = caught[name][0] + passed[name][0], caught[name][1] + passed[name][1]
        tot[0] += ok
        tot[1] += n
        lines.append(f"| {name} | {pct(*caught[name])} | {pct(*passed[name])} | {pct(ok, n)} |")
    lines += [f"| **All items** | {pct(sum(v[0] for v in caught.values()), sum(v[1] for v in caught.values()))} "
              f"| {pct(sum(v[0] for v in passed.values()), sum(v[1] for v in passed.values()))} | **{pct(*tot)}** |", "",
              f"## Missed faults ({len(misses)})", ""] + [f"- {m}" for m in misses] + [
              "", f"## False alarms ({len(false_alarms)})", ""] + [f"- {m}" for m in false_alarms] + [
              "", "## Per call", "", "| Call | Score | Mismatches |", "|---|---|---|"] + rows
    text = "\n".join(lines)
    print(text)
    if args.out:
        with open(args.out, "w", encoding="utf-8") as f:
            f.write(text + "\n")


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    sub = ap.add_subparsers(dest="cmd", required=True)
    c = sub.add_parser("check", help="validate the call files")
    c.add_argument("folder")
    s = sub.add_parser("score", help="score graded results against the planted faults")
    s.add_argument("folder")
    s.add_argument("--label", required=True, help="the --label given to batch_test.py")
    s.add_argument("--out", help="also write the report to this markdown file")
    args = ap.parse_args()
    cmd_check(args) if args.cmd == "check" else cmd_score(args)


if __name__ == "__main__":
    main()
