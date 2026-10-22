"""v3 evaluation pipeline (stage 1): fixed rules + the existing model windows + tenant-aware scoring.

    evaluate_v3(transcript, criteria_data, tenant_id, channel, caller) -> {final_score, scorecard, is_auto_fail, auto_fail_reason, meta}

The response keeps the v2 shape; `meta` and the per-item `evidence` are additive. Model checks still use the v2 windows (laya_inputs) and the
frozen question wording and cutoffs in dynamic_evaluator, so a verdict differs from v2 only where a rule or the input layer was fixed. Later
stages replace the windows one check at a time (src/v3/candidates). Nothing here edits the frozen modules.
"""
import os
import re
import time
from typing import Any, Dict, List, Optional

from src.services import dynamic_evaluator as de
from src.services.laya_inputs import al_source2_enabled, build_laya_inputs
from src.v3 import load_config, rules, scoring
from src.v3.normalise import NCall, normalise
from src.v3.text import add_question_marks

RULE_ITEMS = {
    "branding and survey check": rules.evaluate_branding,
    "hold time and dead air": rules.evaluate_dead_air,
    "verified customer": rules.evaluate_verified,
    "personalized the call/ticket appropriately": rules.evaluate_personalized,
}
MODEL_ITEMS = {"empathy & acknowledgment statement", "paraphrasing", "active listening", "took ownership of the problem",
               "build rapport and observed professionalism", "probing", "confirmed the issue is resolved"}
LEGACY_ITEMS = {"escalation": "escalation", "hostility": "hostility"}          # exact names only (v2 matched any name containing them)


def _v2_transcript(call: NCall) -> List[Dict[str, Any]]:
    """The normalised call in the shape the v2 window builders read: agent and customer turns only, question marks restored."""
    out = []
    for t in call.turns:
        if t.role == "other":
            continue
        out.append({"speaker": "Agent" if t.role == "agent" else "Customer",
                    "text": add_question_marks(t.text) if t.role == "agent" else t.text,
                    "start_time_sec": int(t.start),
                    "sentiment_score": t.sentiment if t.sentiment is not None else 0.0})
    return out


def _custom_check(item: Dict[str, Any]) -> Dict[str, Any]:
    """A tenant-defined criterion: one yes/no question built from its own name and description (no name-substring routing)."""
    name = re.sub(r"\s+", " ", re.sub(r"<\s*br\s*/?\s*>", " ", item.get("name") or "Item", flags=re.I)).strip()
    desc = re.sub(r"<\s*br\s*/?\s*>", " ", item.get("description") or "", flags=re.I)
    desc = re.sub(r"\boutput\s+(yes\s+or\s+no|pass\s+or\s+fail)\b\.?", "", desc, flags=re.I)
    desc = re.sub(r"\s+", " ", desc).strip()
    if desc.upper().startswith("VIOLATION-BASED"):
        rule = re.sub(r"^VIOLATION-BASED:?\s*", "", desc, flags=re.I)
        return {"yes_means": "FAIL", "pass_threshold": 0.50, "question": de._noul(
            f"Does the agent violate this rule: {name}?", f"an agent line clearly violates it: {rule}", "no agent line violates it")}
    return {"yes_means": "PASS", "pass_threshold": 0.50, "question": de._noul(
        f"Did the agent do this: {name}?", f"the agent clearly did it: {desc or name}", "the agent did not do it")}


class _Budget:
    """Counts what the model is asked, so cost is visible per call (a hard cap and shedding come with the candidate stage)."""
    def __init__(self):
        self.rows = 0
        self.words = 0
        self.by_check: Dict[str, int] = {}

    def ask(self, check_key: str, text: str, label: str) -> str:
        self.rows += 1
        self.words += len(text.split())
        self.by_check[check_key] = self.by_check.get(check_key, 0) + 1
        return de._laya_verdict(check_key, text, label)


def _model_ratings(inp, budget: _Budget, wanted: set) -> Dict[str, Dict[str, Any]]:
    out: Dict[str, Dict[str, Any]] = {}

    def put(name, ok, coaching):
        out[name] = {"name": name, "rating": "PASS" if ok else "FAIL", "coaching": "" if ok else coaching, "evidence": []}

    if "empathy & acknowledgment statement" in wanted:
        ok = all(budget.ask("empathy", s, "verify_empathy") != "FAIL" for s in inp.empathy)
        put("empathy & acknowledgment statement", ok, "Failed to show empathy to customer's frustration.")
    if "paraphrasing" in wanted:
        ok = inp.paraphrasing is not None and budget.ask("paraphrasing", inp.paraphrasing, "verify_paraphrasing") == "PASS"
        put("paraphrasing", ok, "Failed to paraphrase core issue.")
    if "active listening" in wanted:
        blocks = (inp.active_listening.split("\n\n") if al_source2_enabled() else [inp.active_listening]) if inp.active_listening else []
        ok = all(budget.ask("active_listening", b, "verify_al") != "FAIL" for b in blocks)
        put("active listening", ok, "Repeated questions unnecessarily.")
    if "took ownership of the problem" in wanted:
        ok = not inp.ownership or budget.ask("ownership", inp.ownership, "verify_ownership") != "FAIL"
        put("took ownership of the problem", ok, "Agent deflected responsibility or blamed another team instead of owning the issue.")
    if "build rapport and observed professionalism" in wanted:
        ok = all(budget.ask("rapport", s, "verify_rapport") != "FAIL" for s in inp.rapport)
        put("build rapport and observed professionalism", ok, "Agent used rude or condescending language.")
    if "probing" in wanted:
        ok = inp.probing is not None and budget.ask("probing", inp.probing, "verify_probing") == "PASS"
        put("probing", ok, "Agent did not ask diagnostic questions to investigate the problem.")
    if "confirmed the issue is resolved" in wanted:
        ok = budget.ask("resolved", inp.resolved, "batch_end") == "PASS"
        put("confirmed the issue is resolved", ok, "")
    return out


def evaluate_v3(transcript_data, criteria_data: Dict[str, Any], tenant_id: str = "", channel: str = "Call", caller: Optional[str] = None) -> Dict[str, Any]:
    t0 = time.perf_counter()
    cfg = load_config()
    call = normalise(transcript_data, caller, cfg)
    items = scoring.tenant_items(criteria_data)                       # NoCriteria when the tenant has none
    cat_of = {scoring.name_key(i.get("name")): cat for cat, i in items}
    item_of = {scoring.name_key(i.get("name")): i for _, i in items}
    wanted = set(item_of)
    ratings: Dict[str, Dict[str, Any]] = {}

    for key, fn in RULE_ITEMS.items():
        if key in wanted:
            ratings[key] = fn(call)

    budget = _Budget()
    want_model = wanted & MODEL_ITEMS
    custom = [k for k in wanted if k not in RULE_ITEMS and k not in MODEL_ITEMS]
    inp = build_laya_inputs(_v2_transcript(call), call.customer_name) if (want_model or custom) else None
    if want_model:
        ratings.update(_model_ratings(inp, budget, want_model))

    contexts = {"agent": (inp.batch_agent_only if inp else ""), "end": (inp.resolved if inp else ""), "full": (inp.batch_full if inp else "")}
    for k in custom:
        item = item_of[k]
        check = de.LAYA_CHECKS[LEGACY_ITEMS[k]] if k in LEGACY_ITEMS else _custom_check(item)
        scope = "full" if k in LEGACY_ITEMS else item.get("scope", "agent")
        text = contexts.get(scope, contexts["agent"])
        budget.rows += 1
        budget.words += len(text.split())
        p_yes = de.predict_yes(text, {"q": check["question"]}, label=f"custom_{scope}")["q"]
        ok = de._p_pass(check, p_yes) >= check["pass_threshold"]
        ratings[k] = {"name": item.get("name"), "rating": "PASS" if ok else "FAIL", "score": 100 if ok else 0, "coaching": "", "evidence": []}

    is_af, af_reason, af_turn = rules.check_auto_fail(call)
    for k, item in item_of.items():                                   # tenant-defined auto-fail items (category named "AUTO FAIL ...")
        if "auto fail" in cat_of[k].lower() and ratings.get(k, {}).get("rating") == "FAIL" and not is_af:
            is_af, af_reason = True, f"Auto-Fail Triggered by Scorecard: {item.get('name')}"

    _, final = scoring.score(list(ratings.values()), criteria_data, is_auto_fail=is_af)
    scorecard = []
    for cat, item in items:
        k = scoring.name_key(item.get("name"))
        r = ratings.get(k) or {"rating": "FAIL", "coaching": "Could not be verified from the transcript.", "evidence": []}
        ok = r["rating"] == "PASS"
        coaching = (de.RULE_BASED_PASS_DESCRIPTIONS.get(k, f"Standard compliant performance observed for '{item.get('name')}'.") if ok
                    else (r.get("coaching") or de.RULE_BASED_FAIL_COACHING.get(k) or f"Criteria standard for '{item.get('name')}' was not met."))
        entry = {"category": cat, "name": item.get("name"), "rating": r["rating"], "coaching": coaching}
        ev = [call.turns[i].source_index for i in r.get("evidence", []) if 0 <= i < len(call.turns)]
        if ev:
            entry["evidence_turns"] = ev
        if r.get("note"):
            entry["note"] = r["note"]
        scorecard.append(entry)

    checkpoint = os.getenv("LAYA_CHECKPOINT")
    return {
        "final_score": final,
        "scorecard": scorecard,
        "is_auto_fail": is_af,
        "auto_fail_reason": af_reason,
        "meta": {"flow": "v3", "config_version": cfg["version"], "model": os.path.basename(checkpoint.rstrip("/\\")) if checkpoint else "stock",
                 "al_second_source": al_source2_enabled(), "sentiment_available": call.sentiment_available, "warnings": call.warnings,
                 "model_rows": budget.rows, "model_words": budget.words, "rows_by_check": budget.by_check,
                 "seconds": round(time.perf_counter() - t0, 2)},
    }
