"""Stage 3: rows from COMPLETE natural-sounding calls. The extractors (build_laya_inputs) cut the snippets, so the model
sees exactly the context, length and mix of speech it sees in production, instead of short hand-built excerpts.

Fragment format (data/fragments/claude/calls_*.txt), speakers and (sentiment) as in build_rows.py:

    @@call id=nc_tr_01 industry=telecom persona=warm name=Dana labels=rapport:PASS,paraphrasing:PASS,resolved:FAIL
    C(-12): ...
    A: ...
    A*: ...        <- for rapport:FAIL, the rude line(s); for resolved/others no marker needed
    C*(-30): ...   <- empathy: the upset customer turn the snippet must start at (only needed when there are several)

`labels` lists only the checks whose label the author is sure of; anything not listed is skipped. How each check becomes rows:
  rapport    every chunk is a row: FAIL if the call is rapport:FAIL and the chunk contains a marked line, else PASS (at most 2 PASS chunks)
  paraphrasing / resolved / probing / ownership / hostility / escalation   one row from the call's snippet
  active_listening   one row when the extractor finds exactly one question pair
  empathy    one row when there is exactly one snippet (or the one that starts at the marked turn)
Rows whose snippet does not fit the model window are dropped and logged.

    python tools/build_calls.py --fragments "data/fragments/claude/calls_train*.txt" --out data/rows/calls_train.jsonl
"""
import argparse
import collections
import glob
import hashlib
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import re  # noqa: E402
from build_rows import Builder, parse_turns, to_transcript  # noqa: E402


def parse_attrs(header, src):
    attrs = {k: v.strip('"') for k, v in re.findall(r"(\w+)=((?:\"[^\"]*\")|\S+)", header)}
    if "id" not in attrs:
        raise ValueError(f"{src}: call header lacks id=")
    return attrs


def parse_calls(path):
    calls, cur = [], None
    for n, raw in enumerate(open(path, encoding="utf-8"), 1):
        line = raw.rstrip("\n")
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if line.startswith("@@call"):
            cur = {"header": line, "n": n, "lines": []}
            calls.append(cur)
        elif cur is None:
            raise ValueError(f"{path}:{n}: line before any @@call header")
        else:
            cur["lines"].append((n, line))
    out = []
    for c in calls:
        src = f"{os.path.basename(path)}:{c['n']}"
        a = parse_attrs(c["header"][6:], src)
        labels = {}
        for kv in a.get("labels", "").split(","):
            if kv:
                k, v = kv.split(":")
                labels[k] = v.upper()
        out.append({**a, "labels": labels, "src": src, "turns": parse_turns(c["lines"], src), "pair": a["id"]})
    return out


def snippets(b, call):
    """[(check, label, snippet, key)] or a list of (check, None, reason, None) for problems."""
    transcript, focus_idx, rough = to_transcript(call)
    inp = b.build_laya_inputs(transcript, call.get("name"))
    L = call["labels"]
    focus_texts = [transcript[i]["text"] for i in focus_idx]
    out = []
    if "rapport" in L:
        chunks = inp.rapport
        marked = [c for c in chunks if any(f"Agent: {t}" in c for t in focus_texts)]
        if L["rapport"] == "FAIL" and not marked:
            out.append(("rapport", None, "rapport:FAIL but no marked line is in any chunk", None))
        pool = [c for c in chunks if c not in marked]
        step = max(1, -(-len(pool) // 2))
        for k, c in enumerate(marked if L["rapport"] == "FAIL" else []):
            out.append(("rapport", "FAIL", c, f"f{k}"))
        for k, c in enumerate(pool[::step][:2]):
            out.append(("rapport", "PASS", c, f"p{k}"))
    for chk, text in (("paraphrasing", inp.paraphrasing), ("resolved", inp.resolved), ("ownership", inp.ownership),
                      ("hostility", inp.batch_full), ("escalation", inp.batch_full)):
        if chk in L:
            if not text:
                out.append((chk, None, "gate not reached / empty snippet", None))
            else:
                out.append((chk, L[chk], text, ""))
    if "probing" in L:
        if inp.probing is None:
            out.append(("probing", None, "agent asked no questions", None))
        else:
            out.append(("probing", L["probing"], inp.probing, ""))
    if "active_listening" in L:
        blocks = inp.active_listening.split("\n\n") if inp.active_listening else []
        if len(blocks) != 1:
            out.append(("active_listening", None, f"{len(blocks)} question pairs found, need exactly 1", None))
        else:
            out.append(("active_listening", L["active_listening"], blocks[0], ""))
    if "empathy" in L:
        sn = inp.empathy
        if focus_texts:
            sn = [s for s in sn if s.startswith("Customer: " + focus_texts[0])]
        if len(sn) != 1:
            out.append(("empathy", None, f"{len(sn)} empathy snippets", None))
        else:
            out.append(("empathy", L["empathy"], sn[0], ""))
    return out, rough


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--fragments", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--max-pass-ratio", type=float, default=0, help="train only: keep at most this many PASS rows per FAIL row for each check, so natural style cannot predict PASS")
    args = ap.parse_args()
    b = Builder(source="claude-call")
    calls = [c for p in sorted(glob.glob(os.path.join(REPO, args.fragments))) for c in parse_calls(p)]
    dup = [i for i, n in collections.Counter(c["id"] for c in calls).items() if n > 1]
    if dup:
        sys.exit(f"duplicate call ids: {dup}")
    rows, dropped = [], []
    for call in calls:
        items, rough = snippets(b, call)
        for chk, label, snip, key in items:
            if label is None:
                dropped.append({"id": call["id"], "check": chk, "reason": snip, "src": call["src"]})
                continue
            q = b.checks[chk]["question"]
            room = b.lc.state_room(b.tok, b.lt.to_internal(chk, q), b.max_len, b.head_max_len)
            n_tok = len(b.lt.encode_state(b.tok, snip, 10 ** 6))
            if n_tok > room:
                dropped.append({"id": call["id"], "check": chk, "reason": f"{n_tok} tokens > room {room}", "src": call["src"]})
                continue
            rid = f"{call['id']}_{chk}" + (f"_{key}" if key else "")
            rows.append({"state": snip, "questions": {chk: q}, "expected": {chk: label == b.checks[chk]["yes_means"]},
                         "meta": {"id": rid, "call_id": call["id"], "pair_id": call["id"], "check": chk, "label": label,
                                  "industry": call.get("industry"), "persona": call.get("persona"), "hard": "natural_call",
                                  "rough": rough, "source": "claude-call", "tokens": n_tok, "room": room,
                                  "inputs_sha256": b.frozen["inputs_sha256"]}})
    if args.max_pass_ratio:
        keep = []
        for chk in sorted({r["meta"]["check"] for r in rows}):
            fails = [r for r in rows if r["meta"]["check"] == chk and r["meta"]["label"] == "FAIL"]
            passes = sorted((r for r in rows if r["meta"]["check"] == chk and r["meta"]["label"] == "PASS"),
                            key=lambda r: hashlib.md5(r["meta"]["id"].encode()).hexdigest())
            keep += fails + passes[:int(args.max_pass_ratio * len(fails) + 0.5)]
        order = {id(r): i for i, r in enumerate(rows)}
        rows = sorted(keep, key=lambda r: order[id(r)])
    with open(os.path.join(REPO, args.out), "w", encoding="utf-8", newline="\n") as fh:
        for r in rows:
            fh.write(json.dumps(r, ensure_ascii=False) + "\n")
    cnt = collections.Counter((r["meta"]["check"], r["meta"]["label"]) for r in rows)
    words = collections.defaultdict(list)
    for r in rows:
        words[r["meta"]["check"]].append(len(r["state"].split()))
    print(f"{len(calls)} calls -> {len(rows)} rows, {len(dropped)} dropped")
    for k in sorted(cnt):
        print(f"  {k[0]:<17}{k[1]:<6}{cnt[k]:>4}")
    print("mean words per snippet:", {k: round(sum(v) / len(v)) for k, v in sorted(words.items())})
    for d in dropped:
        print("  DROPPED", d["id"], d["check"], "-", d["reason"])


if __name__ == "__main__":
    main()
