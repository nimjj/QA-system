"""Import Gemini's replies, validate them, and build the blind labelling sheets.

Reads data/fragments/gemini/raw/batch_NN.json (Gemini's reply, saved unedited), checks each excerpt against its card in
data/review/gemini_cards.json, runs it through the SAME production gates and token-window check as the Claude data
(tools/build_rows.py), and writes:

  data/rows/gemini_candidates.jsonl           rows carrying the INTENDED label (for agreement checks only)
  data/review/gemini_label_sheet_dev.xlsx     BLIND sheets for the human: text + question, no intended label
  data/review/gemini_label_sheet_test.xlsx
  data/fragments/gemini/polite_calls.jsonl    full polite calls (Rapport call-level false-positive test)
  prompts/gemini/reask_NN.md                  a prompt for every card that was missing, invalid or failed a gate
  data/review/gemini_import_status.json       what arrived, what is missing, what was dropped and why

Usage (qa-analysis venv):
    python tools/import_gemini.py                       # import everything in the raw folder
    python tools/import_gemini.py --raw some/other/dir  # e.g. for a test
"""
import argparse
import collections
import glob
import json
import os
import random
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import build_rows  # noqa: E402
import make_gemini_batches as mgb  # noqa: E402

LEAK_WORDS = ["scorecard", "grading", "quality assurance", "paraphras", "active listening", "empathy statement", "behaviour:", "test set"]
STANDARD = {
    "rapport": "FAIL if any agent line is rude, condescending, dismissive, sarcastic or unprofessional (no insult needed). PASS if all lines are polite or merely curt.",
    "paraphrasing": "PASS if the agent restates the customer's problem in their own words. FAIL if they only ask questions (even ones that echo the customer's words), read back a plan name, or never restate it.",
    "active_listening": "FAIL if the second question asks again for information the customer already gave. PASS if it asks for something new or re-checks something that may have changed.",
    "resolved": "PASS if, before closing, the agent explicitly confirms the issue is fixed/resolved and the customer confirms. FAIL if the call just ends, it is assumed fixed, only 'anything else?', a hand-off, or the customer says it still fails.",
    "empathy": "PASS if the agent acknowledges the upset customer's feeling or situation, even briefly. FAIL if they ignore it, brush it off or answer coldly.",
    "ownership": "FAIL if an agent line deflects, blames another team, sends the customer elsewhere or refuses to help. PASS if the agent keeps ownership (hands off with action) or uses the phrase harmlessly.",
    "probing": "PASS if the agent asks at least one real diagnostic question about the problem. FAIL if only greetings, identity checks, confirmations, upsell, scheduling or wrap-up questions.",
    "hostility": "FAIL if the agent insults, mocks, threatens or abruptly hangs up on the customer. PASS if the agent stays professional, even if the customer is angry.",
    "escalation": "FAIL if the customer asked for a supervisor/manager and the agent refused, ignored, discouraged or faked it. PASS if there was no request or it was handled properly.",
}


def parse_reply(path):
    text = open(path, encoding="utf-8").read()
    text = re.sub(r"^```(?:json)?\s*|\s*```\s*$", "", text.strip())
    a, b = text.find("["), text.rfind("]")
    if a < 0 or b < 0:
        raise ValueError("no JSON array found")
    return json.loads(text[a:b + 1])


def validate(item, card):
    """List of problems (empty = fine)."""
    errs = []
    turns = item.get("turns")
    if not isinstance(turns, list) or len(turns) < 3:
        return ["fewer than 3 turns"]
    for i, t in enumerate(turns):
        if not isinstance(t, dict) or str(t.get("speaker", "")).strip().lower() not in ("agent", "customer"):
            errs.append(f"turn {i + 1}: speaker must be Agent or Customer")
        elif not isinstance(t.get("text"), str) or not t["text"].strip():
            errs.append(f"turn {i + 1}: empty text")
    blob = " ".join(str(t.get("text", "")) for t in turns if isinstance(t, dict)).lower()
    errs += [f"mentions '{w}'" for w in LEAK_WORDS if w in blob]
    if card["check"] == "polite_call" and len(turns) < 30:
        errs.append("a full call needs at least 30 turns")
    return errs


def to_fragment(item, card):
    turns = []
    for t in item["turns"]:
        spk = "Agent" if t["speaker"].strip().lower() == "agent" else "Customer"
        try:
            sent = float(t.get("sentiment"))
        except (TypeError, ValueError):
            sent = 6.0 if spk == "Agent" else -4.0
        turns.append({"speaker": spk, "text": t["text"].strip(), "focus": False, "sentiment": max(-40.0, min(30.0, sent)), "gap": 0})
    return {"id": card["id"], "check": card["check"], "label": card["intended"], "industry": card["industry"],
            "persona": card["agent_persona"], "hard": card["type"], "rough": "0", "turns": turns, "src": f"gemini {card['id']}"}


def polite_payload(item, card):
    t_sec, out = 0, []
    for t in item["turns"]:
        spk = "Agent" if t["speaker"].strip().lower() == "agent" else "Customer"
        try:
            sent = float(t.get("sentiment"))
        except (TypeError, ValueError):
            sent = 6.0 if spk == "Agent" else -4.0
        out.append({"speaker": spk, "text": t["text"].strip(), "start_time_sec": t_sec, "sentiment_score": sent})
        t_sec += max(6, int(len(t["text"].split()) * 0.45)) + 2
    return {"id": card["id"], "industry": card["industry"], "persona": card["agent_persona"], "transcript": out}


def write_label_sheet(rows, path, split, seed):
    from openpyxl import Workbook
    from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
    from openpyxl.worksheet.datavalidation import DataValidation
    wb = Workbook()
    rd = wb.active
    rd.title = "Read me first"
    arial = Font(name="Arial", size=10)
    side = Side(style="thin", color="BFBFBF")
    lines = [
        ("What this is", f"The independent {split} set. Each row is a short piece of a support call, shown exactly as the grading model sees it."),
        ("What you do", "For each row decide PASS or FAIL for the check named in the Check column, using the one-line standard next to it and docs/LABELLING_GUIDE.md. Pick PASS, FAIL or UNSURE in the yellow column."),
        ("Your own judgement", "Please label these yourself. They are the independent test of the model, so they only count if the labels are your judgement and not an assistant's, and not Claude's."),
        ("UNSURE", "Use it when a reasonable person could go either way, and write one line why. UNSURE rows are left out."),
        ("Order", "Rows are grouped by check and shuffled inside each check. There is no hint in the Item id."),
        ("Done", "Save the file and tell Claude."),
    ]
    rd.column_dimensions["A"].width = 22
    rd.column_dimensions["B"].width = 110
    rd["A1"] = "Labelling sheet"
    rd["A1"].font = Font(name="Arial", size=14, bold=True)
    for i, (k, v) in enumerate(lines, 3):
        for col, val, bold in (("A", k, True), ("B", v, False)):
            c = rd[f"{col}{i}"]
            c.value, c.font, c.alignment = val, Font(name="Arial", size=10, bold=bold), Alignment(wrap_text=True, vertical="top")
            c.border = Border(left=side, right=side, top=side, bottom=side)
    ws = wb.create_sheet("Label")
    heads = ["Item", "Check", "The standard", "What the model sees", "YOUR LABEL", "Note (required if UNSURE)"]
    for j, h in enumerate(heads, 1):
        c = ws.cell(1, j, h)
        c.font, c.fill, c.alignment = Font(name="Arial", size=10, bold=True, color="FFFFFF"), PatternFill("solid", fgColor="1F3864"), Alignment(wrap_text=True, vertical="center")
    rng = random.Random(seed)
    order = [c for c in mgb.SPEC]
    ordered = []
    for check in order:
        grp = [r for r in rows if r["meta"]["check"] == check]
        rng.shuffle(grp)
        ordered += grp
    for i, r in enumerate(ordered, 2):
        vals = [r["meta"]["id"], r["meta"]["check"], STANDARD[r["meta"]["check"]], r["state"], None, None]
        for j, v in enumerate(vals, 1):
            c = ws.cell(i, j, v)
            c.font, c.alignment = Font(name="Arial", size=10, bold=(j == 1)), Alignment(wrap_text=True, vertical="top")
            c.border = Border(left=side, right=side, top=side, bottom=side)
            if j in (5, 6):
                c.fill = PatternFill("solid", fgColor="FFFF99")
    for col, w in zip("ABCDEF", (9, 16, 44, 100, 13, 36)):
        ws.column_dimensions[col].width = w
    ws.freeze_panes = "D2"
    ws.auto_filter.ref = f"A1:F{len(ordered) + 1}"
    dv = DataValidation(type="list", formula1='"PASS,FAIL,UNSURE"', allow_blank=True, showErrorMessage=True)
    ws.add_data_validation(dv)
    dv.add(f"E2:E{len(ordered) + 1}")
    wb.save(path)
    return len(ordered)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--raw", default=os.path.join(REPO, "data", "fragments", "gemini", "raw"))
    ap.add_argument("--cards", default=os.path.join(REPO, "data", "review", "gemini_cards.json"))
    ap.add_argument("--out-dir", default=REPO)
    args = ap.parse_args()

    cards = json.load(open(args.cards, encoding="utf-8"))["cards"]
    files = sorted(glob.glob(os.path.join(args.raw, "batch_*.json")))
    if not files:
        sys.exit(f"no batch_NN.json files in {args.raw}")

    seen, problems, items = {}, collections.defaultdict(list), {}
    for path in files:
        name = os.path.basename(path)
        try:
            reply = parse_reply(path)
        except Exception as e:
            problems[name].append(f"cannot read as JSON: {e}")
            continue
        for item in reply if isinstance(reply, list) else []:
            cid = item.get("id") if isinstance(item, dict) else None
            if cid not in cards:
                problems[name].append(f"unknown id {cid!r}")
                continue
            if cid in seen:
                problems[name].append(f"{cid} appears again (first in {seen[cid]})")
                continue
            seen[cid] = name
            errs = validate(item, cards[cid])
            if errs:
                problems[name].append(f"{cid}: " + "; ".join(errs))
            else:
                items[cid] = item

    builder = build_rows.Builder("gemini")
    rows, dropped, polite = [], [], []
    for cid, item in sorted(items.items()):
        card = cards[cid]
        if card["check"] == "polite_call":
            payload = polite_payload(item, card)
            n_agent = sum(t["speaker"] == "Agent" for t in payload["transcript"])
            if n_agent < 15:
                dropped.append({"id": cid, "check": "polite_call", "reason": f"only {n_agent} agent lines"})
            else:
                polite.append(payload)
            continue
        row, drop = builder.row(to_fragment(item, card))
        if row:
            row["meta"]["split"] = card["split"]
            row["meta"]["card_id"] = cid
            rows.append(row)
        else:
            dropped.append(drop)

    failed_ids = {d["id"] for d in dropped}

    out = args.out_dir
    for sub in (("data", "rows"), ("data", "review"), ("data", "fragments", "gemini")):
        os.makedirs(os.path.join(out, *sub), exist_ok=True)
    with open(os.path.join(out, "data", "rows", "gemini_candidates.jsonl"), "w", encoding="utf-8", newline="\n") as fh:
        for r in rows:
            fh.write(json.dumps(r, ensure_ascii=False) + "\n")
    with open(os.path.join(out, "data", "fragments", "gemini", "polite_calls.jsonl"), "w", encoding="utf-8", newline="\n") as fh:
        for p in polite:
            fh.write(json.dumps(p, ensure_ascii=False) + "\n")
    for split in ("dev", "test"):
        srows = [r for r in rows if r["meta"]["split"] == split]
        if srows:
            n = write_label_sheet(srows, os.path.join(out, "data", "review", f"gemini_label_sheet_{split}.xlsx"), split, mgb.SEED)
            print(f"wrote blind label sheet ({split}): {n} items")

    # re-ask prompts for everything not yet usable AND already attempted (missing batches are simply not run yet)
    attempted = {cid for cid in cards if cid in seen} | failed_ids
    kept_ids = {r["meta"]["card_id"] for r in rows} | {p["id"] for p in polite}
    redo = sorted(cid for cid in attempted if cid not in kept_ids)
    prompts_dir = os.path.join(out, "prompts", "gemini")
    os.makedirs(prompts_dir, exist_ok=True)
    for old in glob.glob(os.path.join(prompts_dir, "reask_*.md")):
        os.remove(old)
    for n, i in enumerate(range(0, len(redo), 25), 1):
        chunk = [cards[c] for c in redo[i:i + 25]]
        body = mgb.HEADER + f"\nThis batch has {len(chunk)} card(s). Write one excerpt for each.\n\nCARDS\n" + json.dumps(
            [{"id": c["id"], "industry": c["industry"], "problem": c["problem"], "agent_style": c["agent_persona"], "customer_mood": c["customer_mood"],
              "style": c["style"], "STRUCTURE": mgb.SPEC[c["check"]][0] if c["check"] in mgb.SPEC else "Write a COMPLETE call of 40 to 60 turns.",
              "BEHAVIOUR": c["behaviour"]} for c in chunk], indent=1, ensure_ascii=False) + "\n"
        with open(os.path.join(prompts_dir, f"reask_{n:02d}.md"), "w", encoding="utf-8", newline="\n") as fh:
            fh.write(body)

    # report
    print(f"\nfiles read: {len(files)}   cards answered: {len(items)} of {len(cards)}   rows kept: {len(rows)}   polite calls kept: {len(polite)}")
    kept = collections.Counter((r["meta"]["check"], r["meta"]["split"]) for r in rows)
    print(f"{'check':18s} {'dev kept/want':>14s} {'test kept/want':>15s}")
    for check, (dev, test) in mgb.TARGETS.items():
        print(f"{check:18s} {kept[(check, 'dev')]:6d} /{dev:4d} {kept[(check, 'test')]:8d} /{test:4d}")
    print(f"polite calls: {len(polite)} / {mgb.POLITE_CALLS}")
    for name, errs in problems.items():
        print(f"\n{name}: {len(errs)} problem(s)")
        for e in errs[:8]:
            print("   -", e)
    why = collections.Counter(re.sub(r"\d+", "N", d["reason"]) for d in dropped)
    if dropped:
        print("\ndropped by the production gates:")
        for r, n in why.most_common():
            print(f"   {n:3d} x {r}")
    print(f"\nre-ask prompts written: {len(range(0, len(redo), 25))} (cards to redo: {len(redo)})")
    json.dump({"files": [os.path.basename(f) for f in files], "answered": len(items), "kept": len(rows), "polite": len(polite),
               "problems": problems, "dropped": dropped, "redo": redo, "never_answered": [c for c in cards if c not in seen]},
              open(os.path.join(out, "data", "review", "gemini_import_status.json"), "w", encoding="utf-8"), indent=1)


if __name__ == "__main__":
    main()
