"""Record exactly what Laya is sent for every sample call, without loading any model.

Runs the real evaluate_interaction over every sample call (inputs/ and tests/scoring_test/) with a stub
predict_yes that logs (label, text, question ids) and answers P(yes)=0.5. The output JSON maps each call to its
list of Laya inputs, so two versions of the code can be compared byte for byte (see --compare).

Usage (repo root):
    .venv/Scripts/python.exe Scripts/dump_laya_inputs.py out.json
    .venv/Scripts/python.exe Scripts/dump_laya_inputs.py out.json --code-root ../other-checkout   # dump another version's src/
    .venv/Scripts/python.exe Scripts/dump_laya_inputs.py --compare old.json new.json              # which labels differ
"""
import argparse
import glob
import hashlib
import json
import os
import sys
from collections import Counter

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))


def load_calls():
    files = [p for p in glob.glob(os.path.join(ROOT, "inputs", "**", "*.json"), recursive=True) if "result" not in p.lower()]
    files += glob.glob(os.path.join(ROOT, "tests", "scoring_test", "*.json"))
    calls, seen = [], set()
    for fp in sorted(files):
        try:
            d = json.load(open(fp, encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue
        tr = d.get("transcript") if isinstance(d, dict) else None
        if not tr:
            continue
        key = hashlib.md5(json.dumps(tr, sort_keys=True).encode()).hexdigest()
        if key not in seen:
            seen.add(key)
            calls.append((os.path.relpath(fp, ROOT).replace("\\", "/"), tr, d.get("customer_name") or d.get("customerName")))
    return calls


def dump(out_path, code_root):
    sys.path[:0] = [code_root, os.path.join(code_root, "src")]
    import src.services.dynamic_evaluator as de
    log = []

    def stub(text, questions, label=""):
        log.append([label, text, list(questions)])
        return {qid: 0.5 for qid in questions}

    de.predict_yes = stub
    criteria = json.load(open(os.path.join(ROOT, "resources", "criteria_config.json"), encoding="utf-8"))["tenant-abc"]
    result = {}
    for path, transcript, customer in load_calls():
        log.clear()
        de.evaluate_interaction(transcript, criteria, "tenant-abc", caller=customer)
        result[path] = [list(x) for x in log]
    json.dump(result, open(out_path, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    print(f"{len(result)} calls, {sum(len(v) for v in result.values())} Laya inputs -> {out_path}")


def compare(a_path, b_path):
    a, b = json.load(open(a_path, encoding="utf-8")), json.load(open(b_path, encoding="utf-8"))
    differs, same, only = Counter(), Counter(), 0
    for call in sorted(set(a) | set(b)):
        la, lb = a.get(call), b.get(call)
        if la is None or lb is None:
            only += 1
            continue
        def by_label(lst):
            return {lbl: [x for x in lst if x[0] == lbl] for lbl in {x[0] for x in lst}}
        ga, gb = by_label(la), by_label(lb)
        for lbl in sorted(set(ga) | set(gb)):
            (same if ga.get(lbl) == gb.get(lbl) else differs)[lbl] += 1
    print(f"calls only in one file: {only}")
    print(f"{'label':22s} {'identical':>9s} {'different':>9s}   (calls)")
    for lbl in sorted(set(same) | set(differs)):
        print(f"{lbl:22s} {same[lbl]:9d} {differs[lbl]:9d}")
    sys.exit(0 if not differs and not only else 1)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("out", nargs="?")
    ap.add_argument("--code-root", default=ROOT)
    ap.add_argument("--compare", nargs=2, metavar=("OLD", "NEW"))
    args = ap.parse_args()
    if args.compare:
        compare(*args.compare)
    else:
        dump(args.out, os.path.abspath(args.code_root))
