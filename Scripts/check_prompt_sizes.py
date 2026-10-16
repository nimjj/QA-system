"""Check what each Laya call receives, and that the evaluator still produces valid scorecards.

Runs the real evaluate_interaction over every sample call in inputs/ and tests/scoring_test/ with the
reference criteria in resources/criteria_config.json (tenant-abc). No database is needed.

Default mode replaces laya_adapter.predict_yes with a stub that records each call and returns P(yes)=0.5,
so it needs no model. --live runs the real Laya model instead and reports verdicts and timing.

Usage (from the repo root):
    .venv/Scripts/python.exe Scripts/check_prompt_sizes.py
    .venv/Scripts/python.exe Scripts/check_prompt_sizes.py --live
"""
import glob
import hashlib
import importlib.util
import json
import os
import re
import statistics
import sys
import time
from collections import Counter, defaultdict

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, ROOT)

import src.services.dynamic_evaluator as de
import src.services.laya_adapter as laya_adapter
import src.services.rule_engine as rule_engine

LIVE = "--live" in sys.argv
calls_log = []      # (label, text, question ids) for the evaluation currently running
timings = []        # seconds per real Laya call (live mode)
fallbacks = [0]     # predict_long re-runs (live mode)


def stub_predict_yes(text, questions, label=""):
    calls_log.append((label, text, list(questions)))
    return {qid: 0.5 for qid in questions}


def live_predict_yes(text, questions, label=""):
    calls_log.append((label, text, list(questions)))
    t0 = time.perf_counter()
    out = laya_adapter.predict_yes(text, questions, label=label)
    timings.append(time.perf_counter() - t0)
    return out


if LIVE:
    router = laya_adapter._get_router()
    _predict_long = router.predict_long

    def counting_predict_long(*args, **kwargs):
        fallbacks[0] += 1
        return _predict_long(*args, **kwargs)

    router.predict_long = counting_predict_long
de.predict_yes = live_predict_yes if LIVE else stub_predict_yes


def words(text):
    return len(text.split())


def between(text, start, end):
    m = re.search(re.escape(start) + r"(.*?)" + re.escape(end), text, flags=re.DOTALL)
    return m.group(1).strip() if m else ""


def load_calls():
    files = [p for p in glob.glob(os.path.join(ROOT, "inputs", "**", "*.json"), recursive=True) if "result" not in p.lower()]
    files += glob.glob(os.path.join(ROOT, "tests", "scoring_test", "*.json"))
    calls, seen = [], set()
    for fp in sorted(files):
        try:
            with open(fp, encoding="utf-8") as f:
                d = json.load(f)
        except (OSError, json.JSONDecodeError):
            continue
        tr = d.get("transcript") if isinstance(d, dict) else None
        if not tr:
            continue
        key = hashlib.md5(json.dumps(tr, sort_keys=True).encode()).hexdigest()
        if key not in seen:
            seen.add(key)
            calls.append((os.path.relpath(fp, ROOT), tr, d.get("customer_name") or d.get("customerName")))
    return calls


def unit_checks():
    ok = True

    def check(name, cond):
        nonlocal ok
        ok = ok and cond
        print(f"  [{'ok' if cond else 'FAIL'}] {name}")

    print("unit checks:")
    filler = [("Agent", "Okay."), ("Customer", "Right."), ("Agent", "Next step."), ("Customer", "Sure.")]
    turns = ([("Customer", "This is awful.")] + filler + [("Customer", "Still broken!")] + filler
             + [("Customer", "Worst service ever.")] + filler)
    scores = [-20.0] + [0.0] * 4 + [-40.0] + [0.0] * 4 + [-30.0] + [0.0] * 4
    picked = rule_engine.extract_empathy_snippet_list(turns, scores, max_snippets=2)
    check("empathy: top-2 picks the two most negative turns, most severe first",
          len(picked) == 2 and picked[0].startswith("Customer: Still broken!") and picked[1].startswith("Customer: Worst service ever."))

    turns = [("Customer", "Bad."), ("Customer", "Worse."), ("Agent", "Okay."), ("Customer", "Terrible."), ("Agent", "Hmm.")]
    scores = [-20.0, -25.0, 0.0, -18.0, 0.0]
    picked = rule_engine.extract_empathy_snippet_list(turns, scores)
    check("empathy: overlapping upset turns collapse to one snippet", len(picked) == 1 and picked[0].startswith("Customer: Worse."))
    check("empathy: legacy joined extractor still returns every snippet",
          rule_engine.extract_empathy_snippets(turns, scores).count("\n---\n") == 2)

    turns = [("Agent", "How can I help you today?"), ("Customer", "My wifi is down."),
             ("Agent", "Can I get your account number?"), ("Agent", "Is there anything else?")]
    problem, qs = rule_engine.extract_probing_inputs(turns, ["My wifi is down."], 50, 100)
    check("probing: all-boilerplate questions fall back to the unfiltered list", len(qs) == 3 and problem == "My wifi is down.")

    turns = [("Agent", "How can I help you today?"), ("Agent", "When did it start?"), ("Agent", "Which lights are on?")]
    _, qs = rule_engine.extract_probing_inputs(turns, [], 50, 100)
    check("probing: boilerplate dropped when real questions exist", qs == ["When did it start?", "Which lights are on?"])

    long_q = [("Agent", "Is " + "very " * 60 + "slow?") for _ in range(5)]
    problem, qs = rule_engine.extract_probing_inputs(long_q, ["word"] * 80, 50, 100)
    check("probing: word budgets hold", words(problem) <= 50 and sum(words(q) for q in qs) <= 100)

    near = [("Agent", "Can I get your account number?"), ("Agent", "Can I get your account number please?")]
    loose = [("Agent", "What is the make of your router?"), ("Agent", "Have you restarted the cable box today?")]
    check("active listening: difflib gate keeps near-repeats and skips loose matches",
          rule_engine.extract_active_listening_snippets(near) != "" and rule_engine.extract_active_listening_snippets(loose) == "")

    hold = [("Agent", "Can I place you on a brief hold while I run a test?"), ("Customer", "Sure."),
            ("Agent", "Thanks for holding, the test is halfway."), ("Customer", "Okay."),
            ("Agent", "Thank you for waiting, I have the results.")]
    silent = [("Agent", "Okay."), ("Customer", "Hello? Are you still there?"), ("Agent", "Yes."), ("Customer", "Hello?")]
    check("dead air: announced holds are exempt, unannounced gaps still count",
          rule_engine.evaluate_hold_and_dead_air(hold, [(0, 10), (12, 22), (70, 80), (82, 92), (140, 150)])["rating"] == "PASS"
          and rule_engine.evaluate_hold_and_dead_air(silent, [(0, 10), (50, 60), (62, 72), (110, 120)])["rating"] == "FAIL")

    turns = [("Customer", "My wifi is down."), ("Agent", "Great, let's look."), ("Customer", "It drops every evening.")]
    check("empathy: a cheerful agent turn does not make the customer's next turn a drop",
          rule_engine.extract_empathy_snippet_list(turns, [0.0, 20.0, -2.0]) == [])
    turns = [("Customer", "This is the third time I've called about it."), ("Agent", "Okay."), ("Agent", "Next.")]
    check("empathy: frustration words trigger a snippet without a big sentiment drop",
          len(rule_engine.extract_empathy_snippet_list(turns, [-3.0, 5.0, 5.0])) == 1)

    turns = [("Agent", "How long has this been happening?"), ("Customer", "Three weeks."),
             ("Agent", "Okay, the light means it lost signal. And how long has this been happening for, roughly?"),
             ("Customer", "Like I said, about three weeks."),
             ("Agent", "Is that right?"), ("Customer", "Yes."), ("Agent", "Is that right?")]
    al = rule_engine.extract_active_listening_snippets(turns)
    check("active listening: a repeat is sent as first question, the customer's answer, second question",
          "Turn 0 Agent asked: How long has this been happening?" in al and "Customer answered: Three weeks." in al
          and "Turn 2 Agent later asked: And how long has this been happening for, roughly?" in al)
    check("active listening: the customer's 'like I said' reply is not sent", "Like I said" not in al)
    check("active listening: repeated 'Is that right?' check-ins are not repeats", "Is that right" not in al)

    many = [("Agent" if i % 2 == 0 else "Customer", f"Line number {i} " + "word " * 5) for i in range(60)]
    chunks = rule_engine.extract_rapport_chunks(many)
    check("rapport: every agent line is in exactly one chunk, customer lines are not",
          sum(c.count("Agent:") for c in chunks) == 30 and not any("Customer" in c for c in chunks))
    check("rapport: chunks hold at most 8 lines and about 120 words",
          all(c.count("\n") + 1 <= rule_engine.RAPPORT_CHUNK_MAX_LINES for c in chunks)
          and all(len(c.split()) - c.count("Agent:") <= rule_engine.RAPPORT_CHUNK_MAX_WORDS for c in chunks))
    check("rapport: a rude line without any listed phrase still reaches the model",
          rule_engine.extract_rapport_chunks([("Agent", "Right, so you did nothing, as usual.")]) == ["Agent: Right, so you did nothing, as usual."])
    check("rapport: no agent lines means nothing to send", rule_engine.extract_rapport_chunks([("Customer", "Hi.")]) == [])

    turns = [("Agent", "That light means the modem lost its signal from our network. Which light is blinking?")]
    _, qs = rule_engine.extract_probing_inputs(turns, [], 50, 100)
    check("probing: only the question sentence of a turn is sent", qs == ["Which light is blinking?"])

    check("paraphrasing: greeting, verification and account-detail turns are skipped",
          rule_engine.without_setup_lines(["Thank you for calling S-Net.", "Can I get your PIN?", "So your wifi drops?"])
          == ["So your wifi drops?"]
          and rule_engine.without_detail_answers(["It's 4417-882-310.", "It's 18 Larkspur Lane.",
                                                  "I upgraded to the 500 megabit plan five weeks ago and it's slow."])
          == ["I upgraded to the 500 megabit plan five weeks ago and it's slow."])

    viol = de._batch_check({"name": "No blame", "description": "VIOLATION-BASED: FAIL if the agent blames another team."})
    pos = de._batch_check({"name": "Offered survey", "description": "Did the agent offer the survey? Output YES or NO."})
    check("batch: VIOLATION-BASED items are asked as violations, others as evidence",
          viol["yes_means"] == "FAIL" and pos["yes_means"] == "PASS")
    check("batch: 'Output YES or NO.' is stripped from generated questions",
          "output" not in json.dumps(pos["question"]).lower())
    check("batch: known names use the tested questions",
          de._batch_check({"name": "Confirmed the issue is resolved"}) is de.LAYA_CHECKS["resolved"])

    if not LIVE:
        short_call = "\n".join(f"Agent: line {i}" if i % 2 else f"Customer: line {i}" for i in range(6))
        criteria = {"categories": [{"name": "Technical Knowledge", "line_items": [
            {"name": "Confirmed the issue is resolved", "description": "Did the agent confirm?", "deduction_value": 15}]}],
            "category_weights": {"Technical Knowledge": 1.0}}
        calls_log.clear()
        de.evaluate_interaction(short_call, criteria, "unit")
        tx = next(t for lbl, t, _ in calls_log if lbl == "batch_end")
        check("resolved: a 6-line call sends all 6 lines", len(tx.splitlines()) == 6)

    check("no Ollama adapter left in src/services", importlib.util.find_spec("src.services.llm_adapter") is None)
    return ok


def main():
    with open(os.path.join(ROOT, "resources", "criteria_config.json"), encoding="utf-8") as f:
        criteria = json.load(f)["tenant-abc"]
    calls = load_calls()

    sizes = defaultdict(list)            # check -> words sent per Laya call
    empathy_calls_per_eval = []
    resolved_lines = []
    bad_scorecards = []
    verdicts = defaultdict(Counter)      # criterion -> PASS/FAIL counts, only where Laya judged it
    label_to_item = {"verify_empathy": "empathy & acknowledgment statement", "verify_al": "active listening",
                     "verify_ownership": "took ownership of the problem", "verify_rapport": "build rapport and observed professionalism",
                     "verify_probing": "probing", "verify_paraphrasing": "paraphrasing", "batch_end": "confirmed the issue is resolved"}
    t_start = time.time()

    for path, transcript, customer in calls:
        calls_log.clear()
        result = de.evaluate_interaction(transcript, criteria, "tenant-abc", caller=customer)
        card = result.get("scorecard", [])
        if not isinstance(result.get("final_score"), (int, float)) or not card or any(
                set(r) != {"category", "name", "rating", "coaching"} or r["rating"] not in ("PASS", "FAIL") or not r["coaching"]
                for r in card):
            bad_scorecards.append(path)

        n_emp = 0
        judged = set()
        for label, text, _ in calls_log:
            judged.add(label_to_item.get(label))
            if label == "verify_empathy":
                n_emp += 1
                sizes["empathy (per call)"].append(words(text))
            elif label == "verify_probing":
                problem = between(text, "CUSTOMER PROBLEM:", "The agent asked these questions")
                q_words = sum(words(ln[2:]) for ln in text.splitlines() if ln.startswith("- "))
                sizes["probing problem"].append(words(problem))
                sizes["probing questions"].append(q_words)
            elif label == "verify_paraphrasing":
                sizes["paraphrasing customer"].append(words(between(text, "CUSTOMER:", "\nAGENT:")))
                sizes["paraphrasing agent"].append(words(text.split("\nAGENT:", 1)[1]) if "\nAGENT:" in text else 0)
            elif label == "batch_end":
                sizes["resolved batch"].append(words(text))
                resolved_lines.append(len(text.splitlines()))
            elif label in ("verify_al", "verify_ownership", "verify_rapport"):
                sizes[label.replace("verify_", "")].append(words(text))
            else:
                sizes[label].append(words(text))
        if n_emp:
            empathy_calls_per_eval.append(n_emp)
        for r in card:
            if r["name"].strip().lower() in judged:
                verdicts[r["name"]][r["rating"]] += 1

    print(f"mode: {'LIVE Laya' if LIVE else 'stub (no model)'}   sample calls evaluated: {len(calls)}\n")
    print(f"{'what Laya is sent':26s} {'calls':>6s} {'median':>7s} {'90th %':>7s} {'max':>6s}   (words)")
    for label in sorted(sizes):
        v = sorted(sizes[label])
        print(f"{label:26s} {len(v):6d} {statistics.median(v):7.0f} {v[int(0.9 * (len(v) - 1))]:7d} {v[-1]:6d}")
    print(f"\nempathy Laya calls per evaluation: max {max(empathy_calls_per_eval, default=0)}")
    print(f"resolved batch lines: max {max(resolved_lines, default=0)}")
    print(f"malformed scorecards: {len(bad_scorecards)}" + (f" -> {bad_scorecards}" if bad_scorecards else ""))

    ok = not bad_scorecards
    caps = [
        ("empathy calls per evaluation <= EMPATHY_MAX_SNIPPETS", max(empathy_calls_per_eval, default=0) <= de.EMPATHY_MAX_SNIPPETS),
        ("empathy call holds a single snippet (<= 200 words)", max(sizes["empathy (per call)"], default=0) <= 200),
        ("probing problem <= PROBING_PROBLEM_MAX_WORDS", max(sizes["probing problem"], default=0) <= de.PROBING_PROBLEM_MAX_WORDS),
        ("probing questions <= PROBING_QUESTIONS_MAX_WORDS", max(sizes["probing questions"], default=0) <= de.PROBING_QUESTIONS_MAX_WORDS),
        ("paraphrasing customer <= PARAPHRASE_CUSTOMER_MAX_WORDS", max(sizes["paraphrasing customer"], default=0) <= de.PARAPHRASE_CUSTOMER_MAX_WORDS),
        ("paraphrasing agent <= PARAPHRASE_AGENT_MAX_WORDS", max(sizes["paraphrasing agent"], default=0) <= de.PARAPHRASE_AGENT_MAX_WORDS),
        ("resolved batch <= RESOLVED_TAIL_LINES lines", max(resolved_lines, default=0) <= de.RESOLVED_TAIL_LINES),
        ("rapport chunk <= 140 words (8 lines of normal length)", max(sizes["rapport"], default=0) <= 140 + 8),
        ("active listening snippet <= 3 pairs (<= 260 words)", max(sizes["al"], default=0) <= 260),
    ]
    print("\ncap checks:")
    for name, cond in caps:
        print(f"  [{'ok' if cond else 'FAIL'}] {name}")
        ok = ok and cond

    if LIVE:
        print(f"\nLaya calls: {len(timings)}, mean {statistics.mean(timings):.2f}s, max {max(timings):.2f}s, "
              f"total run {time.time() - t_start:.0f}s, windowed fallbacks: {fallbacks[0]}")
        print("verdicts where Laya judged the item:")
        for name, c in sorted(verdicts.items()):
            note = "   <- one-sided" if len(c) == 1 and sum(c.values()) >= 5 else ""
            print(f"  {name:45s} PASS {c['PASS']:3d}  FAIL {c['FAIL']:3d}{note}")

    print()
    ok = unit_checks() and ok
    print("\nRESULT:", "PASS" if ok else "FAIL")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
