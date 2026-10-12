"""Compare batch_test.py result folders with the expected grades.

Usage (from the repo root):
    python Scripts/compare_results.py                         # labels: ollama laya
    python Scripts/compare_results.py laya laya-v2            # any result-folder labels
    python Scripts/compare_results.py laya laya-v2 --out report.md

Main tests: each label's scorecard vs inputs/Main tests/expected/expected_<call>.json.
Bulk tests: b_* calls vs the defects planted in their filenames (b_09_gaps -> Hold time and Dead Air FAIL,
every other item PASS); the auto-fail calls are skipped, and b_31/b_34 (filenames cut short) only count their FAILs.
The other bulk calls (real_*, v8_*) have no item labels, so only their final scores are listed.
"""
import argparse
import glob
import json
import os
import re

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
INPUTS = os.path.join(ROOT, "inputs")
RESULTS = os.path.join(INPUTS, "Test (results)")

ITEMS = [
    "Branding and Survey Check", "Hold time and Dead Air", "Verified customer",
    "Personalized the call/ticket appropriately", "Empathy & Acknowledgment Statement", "Paraphrasing",
    "Active listening", "Took ownership of the problem", "Build rapport and observed professionalism",
    "Probing", "Confirmed the issue is resolved",
]
# filename token -> item that should FAIL
DEFECTS = {
    "nogreet": "Branding and Survey Check", "noclose": "Branding and Survey Check",
    "noverify": "Verified customer", "noname": "Personalized the call/ticket appropriately",
    "gaps": "Hold time and Dead Air", "empathy": "Empathy & Acknowledgment Statement",
    "nopara": "Paraphrasing", "nopa": "Paraphrasing", "noprobe": "Probing",
    "ownership": "Took ownership of the problem", "al": "Active listening",
    "noconfirm": "Confirmed the issue is resolved", "rapport": "Build rapport and observed professionalism",
}
TRUNCATED = {"b_31", "b_34"}


def load_results(suite, label):
    """call name (input file stem) -> latest result payload for that suite and label."""
    out = {}
    for fp in sorted(glob.glob(os.path.join(RESULTS, f"{suite} ({label})", "result_*.json"))):
        stem = re.sub(r"^result_\d{8}_\d{6}_", "", os.path.basename(fp))[:-len(".json")]
        with open(fp, encoding="utf-8") as f:
            out[stem] = json.load(f)
    return out


def ratings(doc):
    return {i["name"]: i["rating"] for i in doc["result"]["scorecard"]}


def bulk_labels(stem):
    """Expected rating per item for a b_* call, or None when the call is not item-labelled."""
    m = re.match(r"^(b_\d+)_(.*)$", stem)
    if not m or "autofail" in stem:
        return None
    fails = {DEFECTS[t] for t in m.group(2).split("_") if t in DEFECTS}
    if m.group(1) in TRUNCATED:
        return {name: "FAIL" for name in fails}
    return {name: ("FAIL" if name in fails else "PASS") for name in ITEMS}


def agreement_table(per_item, labels):
    lines = ["| Item | " + " | ".join(labels) + " |", "|---|" + "---|" * len(labels)]
    for name in ITEMS:
        lines.append(f"| {name} | " + " | ".join(
            f"{per_item[lb][name][0]}/{per_item[lb][name][1]}" for lb in labels) + " |")
    lines.append("| **All items** | " + " | ".join(
        f"**{sum(v[0] for v in per_item[lb].values())}/{sum(v[1] for v in per_item[lb].values())}**"
        for lb in labels) + " |")
    return lines


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("labels", nargs="*", default=["ollama", "laya"])
    ap.add_argument("--out", help="also write the report to this markdown file")
    args = ap.parse_args()
    labels = args.labels
    lines = []

    # Main tests vs expected scorecards
    main_res = {lb: load_results("Main tests", lb) for lb in labels}
    per_item = {lb: {n: [0, 0] for n in ITEMS} for lb in labels}
    lines += ["## Main tests vs expected", ""]
    for exp_fp in sorted(glob.glob(os.path.join(INPUTS, "Main tests", "expected", "expected_*.json"))):
        call = os.path.basename(exp_fp)[len("expected_"):-len(".json")]
        with open(exp_fp, encoding="utf-8") as f:
            exp = json.load(f)
        scores = ", ".join(
            f"{lb} {main_res[lb][call]['result']['final_score']}" if call in main_res[lb] else f"{lb} n/a"
            for lb in labels)
        lines += [f"### {call}: expected {exp['result']['final_score']}, {scores}", "",
                  "| Item | Expected | " + " | ".join(labels) + " |", "|---|---|" + "---|" * len(labels)]
        want = ratings(exp)
        for name in ITEMS:
            cells = []
            for lb in labels:
                got = ratings(main_res[lb][call]).get(name) if call in main_res[lb] else None
                if got is None:
                    cells.append("-")
                    continue
                per_item[lb][name][1] += 1
                per_item[lb][name][0] += got == want.get(name)
                cells.append(got if got == want.get(name) else f"**{got}** ✗")
            lines.append(f"| {name} | {want.get(name, '-')} | " + " | ".join(cells) + " |")
        lines.append("")
    lines += ["### Main tests: items matching expected", ""] + agreement_table(per_item, labels) + [""]

    # Bulk tests: b_* vs filename labels, the rest by final score
    bulk_res = {lb: load_results("Bulk tests", lb) for lb in labels}
    stems = sorted(set().union(*[set(r) for r in bulk_res.values()]))
    if stems:
        per_item = {lb: {n: [0, 0] for n in ITEMS} for lb in labels}
        misses = {lb: [] for lb in labels}
        for stem in stems:
            want = bulk_labels(stem)
            if want is None:
                continue
            for lb in labels:
                if stem not in bulk_res[lb]:
                    continue
                got = ratings(bulk_res[lb][stem])
                for name, w in want.items():
                    if name in got:
                        per_item[lb][name][1] += 1
                        per_item[lb][name][0] += got[name] == w
                        if got[name] != w:
                            misses[lb].append(f"{stem}: {name} {got[name]} (want {w})")
        lines += ["## Bulk b_* calls vs the defects in their filenames", ""] + agreement_table(per_item, labels) + [""]
        for lb in labels:
            lines += [f"<details><summary>{lb}: {len(misses[lb])} mismatches</summary>", ""]
            lines += [f"- {m}" for m in misses[lb]] + ["", "</details>", ""]

        lines += ["## Other bulk calls: final scores", "", "| Call | " + " | ".join(labels) + " |",
                  "|---|" + "---|" * len(labels)]
        for stem in stems:
            if bulk_labels(stem) is not None:
                continue
            row = []
            for lb in labels:
                r = bulk_res[lb].get(stem)
                row.append("-" if r is None else
                           f"{r['result']['final_score']}" + (" AF" if r["result"].get("is_auto_fail") else ""))
            lines.append(f"| {stem} | " + " | ".join(row) + " |")

    text = "\n".join(lines)
    print(text)
    if args.out:
        with open(args.out, "w", encoding="utf-8") as f:
            f.write(text + "\n")


if __name__ == "__main__":
    main()
