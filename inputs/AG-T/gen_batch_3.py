import json
import os
import sys

sys.path.insert(0, os.path.abspath("."))
from src.services.rule_engine import evaluate_branding, evaluate_hold_and_dead_air, evaluate_verified_customer, evaluate_personalized_call
from Scripts.validate_calls import SPEC, final_score

def mmss(sec):
    return f"[{sec//60:02d}:{sec%60:02d}]"

def build_call(cid, cname, target_dur, scenario, tier, raw_turns, ratings, coaching_map, evidence_map, markers, hard_cases, notes, auto_fail_word=None):
    word_counts = [len(t[1].split()) for t in raw_turns]
    durs = [max(4, min(24, int(w / 2.3))) for w in word_counts]
    durs[-1] = 6

    # Identify hold gaps
    # We look for agent turns announcing hold
    hold_indices = []
    for i in range(len(raw_turns) - 1):
        if raw_turns[i][0] == "Agent" and any(h in raw_turns[i][1].lower() for h in ["bear with me", "one moment while", "give me a moment", "place you on", "put you on hold"]):
            if raw_turns[i+1][0] == "Agent" and any(th in raw_turns[i+1][1].lower() for th in ["thank you for waiting", "thank you for holding", "sorry for the wait"]):
                hold_indices.append(i)

    # Initial pass with 3s pauses and 85s holds
    curr = 0
    raw_starts = []
    for i in range(len(raw_turns)):
        dur = durs[i]
        st = curr
        raw_starts.append(st)
        if i < len(raw_turns) - 1:
            if i in hold_indices:
                curr = st + dur + 85
            else:
                curr = st + dur + 3
    
    current_end = raw_starts[-1] + durs[-1]
    diff = target_dur - current_end
    
    normal_indices = [i for i in range(len(raw_turns) - 1) if i not in hold_indices]
    extra_per = diff // len(normal_indices) if normal_indices else 0
    extra_rem = diff % len(normal_indices) if normal_indices else 0

    curr = 0
    transcript = []
    for i, (spk, txt, score) in enumerate(raw_turns):
        dur = durs[i]
        st = curr
        et = st + dur
        turn_dict = {
            "speaker": spk,
            "start_time": mmss(st),
            "end_time": mmss(et),
            "start_time_sec": st,
            "text": txt
        }
        if spk == "Customer":
            turn_dict["sentiment_score"] = round(float(score), 1)
        transcript.append(turn_dict)

        if i < len(raw_turns) - 1:
            if i in hold_indices:
                curr = max(et + 1, st + 95)
            else:
                add = extra_per + (1 if normal_indices.index(i) < extra_rem else 0)
                curr = et + max(1, 3 + add)

    transcript[-1]["end_time"] = mmss(target_dur)

    # Validate rule items with code
    tl = [(t["speaker"], t["text"]) for t in transcript]
    tm = [(t["start_time_sec"], t["start_time_sec"] + 10) for t in transcript]

    b_res = evaluate_branding(tl)["rating"]
    d_res = evaluate_hold_and_dead_air(tl, tm)["rating"]
    v_res = evaluate_verified_customer(tl, tm)["rating"]
    p_res = evaluate_personalized_call(tl, cname)["rating"]

    assert b_res == ratings["Branding and Survey Check"], f"{cid} Branding mismatch: got {b_res}, expected {ratings['Branding and Survey Check']}"
    assert d_res == ratings["Hold time and Dead Air"], f"{cid} Dead Air mismatch: got {d_res}, expected {ratings['Hold time and Dead Air']}"
    assert v_res == ratings["Verified customer"], f"{cid} Verified mismatch: got {v_res}, expected {ratings['Verified customer']}"
    assert p_res == ratings["Personalized the call/ticket appropriately"], f"{cid} Personalized mismatch: got {p_res}, expected {ratings['Personalized the call/ticket appropriately']}"

    payload = {
        "tenant_id": "tenant-abc",
        "customer_name": cname,
        "transcript": transcript
    }

    with open(f"inputs/AG-T/{cid}.json", "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2, ensure_ascii=False)
        f.write("\n")

    # Build scorecard
    scorecard = []
    is_af = auto_fail_word is not None
    af_reason = f"Agent used prohibited word '{auto_fail_word}'" if is_af else None

    for cat, nm, ded in SPEC:
        r = ratings[nm]
        c = coaching_map.get(nm, "") if r == "FAIL" else ""
        scorecard.append({
            "category": cat,
            "name": nm,
            "rating": r,
            "coaching": c
        })

    sc = final_score(scorecard, is_af)

    grader_items = []
    for cat, nm, ded in SPEC:
        r = ratings[nm]
        ev = evidence_map.get(nm, "")
        grader_items.append({
            "name": nm,
            "rating": r,
            "confidence": "clear",
            "evidence": ev
        })

    expected = {
        "call_id": cid,
        "tenant_id": "tenant-abc",
        "status": "completed",
        "result": {
            "final_score": sc,
            "is_auto_fail": is_af,
            "auto_fail_reason": af_reason,
            "scorecard": scorecard
        },
        "grader": {
            "graded_by": "Antigravity (gemini-3.8-flash)",
            "graded_on": "2026-10-21",
            "scenario": scenario,
            "tier": tier,
            "duration_sec": target_dur,
            "notes": notes,
            "hard_cases": hard_cases,
            "items": grader_items,
            "markers": markers
        }
    }

    with open(f"inputs/AG-T/expected/expected_{cid}.json", "w", encoding="utf-8") as f:
        json.dump(expected, f, indent=2, ensure_ascii=False)
        f.write("\n")

    print(f"Generated {cid} ({tier}, score {sc}, duration {target_dur}s)")
    return sc

print("Helper defined.")
