"""Combine the row files into the three files the notebook uses and prove the splits are clean.

    data/rows/train_all.jsonl = train.jsonl + replay_train.jsonl
    data/rows/dev_all.jsonl   = dev.jsonl   + replay_dev.jsonl
    data/rows/test.jsonl      (as built; replay rows are never in test)

Checks (any failure exits 1): no pair_id / call_id appears in two splits; no identical state text for the same check in two
splits; near-duplicates across splits (word-5-gram Jaccard >= 0.6) are listed; every row carries the frozen inputs hash.
Writes data/rows/manifest.json with row counts per split/check and sha256 of each file.
"""
import hashlib
import json
import os
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ROWS = os.path.join(REPO, "data", "rows")


def load(name):
    return [json.loads(l) for l in open(os.path.join(ROWS, name), encoding="utf-8") if l.strip()]


def write(name, rows):
    with open(os.path.join(ROWS, name), "w", encoding="utf-8", newline="\n") as fh:
        for r in rows:
            fh.write(json.dumps(r, ensure_ascii=False) + "\n")


def sha(name):
    return hashlib.sha256(open(os.path.join(ROWS, name), "rb").read()).hexdigest()


def shingles(text, n=5):
    w = text.lower().split()
    return {" ".join(w[i:i + n]) for i in range(max(1, len(w) - n + 1))}


def main():
    pilot = load("pilot.jsonl")
    train = [r for r in load("train.jsonl")]       # train.jsonl already includes the pilot rows
    splits = {"train": train + load("replay_train.jsonl"), "dev": load("dev.jsonl") + load("replay_dev.jsonl"),
              "test": load("test.jsonl")}
    # near-duplicate removal: a dev/test pair is dropped (both members) if any of its rows is a near-copy of a row in an
    # earlier split. Short snippets (ownership) repeat often, so this matters.
    sh = {s: [(r, shingles(r["state"])) for r in rows if r["meta"]["check"] != "replay"] for s, rows in splits.items()}
    removed = []
    for later, earlier in (("dev", ["train"]), ("test", ["train", "dev"])):
        bad_pairs = set()
        for r, sa in sh[later]:
            for e in earlier:
                for r2, sb in sh[e]:
                    if r["meta"]["check"] == r2["meta"]["check"] and sa and sb and len(sa & sb) / len(sa | sb) >= 0.6:
                        bad_pairs.add(r["meta"]["pair_id"])
        removed += [(later, p) for p in sorted(bad_pairs)]
        splits[later] = [r for r in splits[later] if r["meta"]["pair_id"] not in bad_pairs]
        sh[later] = [(r, s) for r, s in sh[later] if r["meta"]["pair_id"] not in bad_pairs]
    print(f"removed near-duplicate pairs: {len(removed)}", removed)
    write("train_all.jsonl", splits["train"])
    write("dev_all.jsonl", splits["dev"])
    write("test.jsonl", splits["test"])

    problems = []
    frozen = {r["meta"]["inputs_sha256"] for s in splits.values() for r in s}
    if len(frozen) != 1:
        problems.append(f"rows carry {len(frozen)} different inputs hashes")
    for key in ("pair_id", "call_id"):
        owner = {}
        for sname, rows in splits.items():
            for r in rows:
                owner.setdefault(r["meta"][key], set()).add(sname)
        bad = [k for k, v in owner.items() if len(v) > 1]
        if bad:
            problems.append(f"{key} in more than one split: {bad[:5]} ({len(bad)})")
    for a, b in (("train", "dev"), ("train", "test"), ("dev", "test")):
        sa = {(r["meta"]["check"], r["state"]) for r in splits[a] if r["meta"]["check"] != "replay"}
        sb = {(r["meta"]["check"], r["state"]) for r in splits[b] if r["meta"]["check"] != "replay"}
        same = sa & sb
        if same:
            problems.append(f"{len(same)} identical states in both {a} and {b}")
    near = []
    sup = {s: [(r, shingles(r["state"])) for r in rows if r["meta"]["check"] != "replay"] for s, rows in splits.items()}
    for a, b in (("train", "test"), ("train", "dev"), ("dev", "test")):
        for ra, sa in sup[a]:
            for rb, sb in sup[b]:
                if ra["meta"]["check"] != rb["meta"]["check"] or not sa or not sb:
                    continue
                j = len(sa & sb) / len(sa | sb)
                if j >= 0.6:
                    near.append((a, b, ra["meta"]["id"], rb["meta"]["id"], round(j, 2)))

    counts = {s: {} for s in splits}
    for s, rows in splits.items():
        for r in rows:
            c = r["meta"]["check"]
            lab = r["meta"].get("label", "gold")
            counts[s].setdefault(c, {}).setdefault(lab, 0)
            counts[s][c][lab] += 1
    manifest = {"inputs_sha256": next(iter(frozen)), "rows": {s: len(r) for s, r in splits.items()}, "counts": counts,
                "pairs": {s: len({r["meta"]["pair_id"] for r in rows if r["meta"]["check"] != "replay"}) for s, rows in splits.items()},
                "sha256": {n: sha(n) for n in ("train_all.jsonl", "dev_all.jsonl", "test.jsonl")},
                "near_duplicates_ge_0.6": near, "removed_pairs": removed, "problems": problems,
                "authorship": "All train, dev and test rows were written and labelled by Claude; none is human-labelled."}
    json.dump(manifest, open(os.path.join(ROWS, "manifest.json"), "w", encoding="utf-8"), indent=2)
    print(json.dumps({k: manifest[k] for k in ("rows", "pairs")}, indent=1))
    for s in counts:
        print(s, {c: dict(v) for c, v in counts[s].items()})
    print(f"near-duplicates across splits (>=0.6): {len(near)}", near[:8])
    if problems:
        print("PROBLEMS:", *problems, sep="\n  ")
        sys.exit(1)
    print("splits clean")


if __name__ == "__main__":
    main()
