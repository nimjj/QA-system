import os
import re
from typing import Dict, Any, List, Optional, Union
from src.services.laya_adapter import predict_yes

RATING_SCORES = {"PASS": 100, "FAIL": 0, "YES": 100, "NO": 0}

from src.services.laya_inputs import (  # noqa: F401  (re-exported: other scripts read them from here)
    EMPATHY_MAX_SNIPPETS, PROBING_PROBLEM_MAX_WORDS, PROBING_QUESTIONS_MAX_WORDS, RESOLVED_TAIL_LINES,
    PARAPHRASE_CUSTOMER_MAX_WORDS, PARAPHRASE_AGENT_MAX_WORDS, al_source2_enabled, build_laya_inputs,
)

RULE_BASED_PASS_DESCRIPTIONS = {
    "branding and survey check": "Agent successfully used required opening and closing branding scripts.",
    "hold time and dead air": "Agent maintained active communication without excessive dead air (>30s).",
    "personalized the call/ticket appropriately": "Agent addressed customer by their verified name during the interaction.",
    "empathy & acknowledgment statement": "Agent demonstrated appropriate empathy and acknowledgment of the customer's situation.",
    "build rapport and observed professionalism": "Agent maintained a professional, courteous, and respectful demeanor throughout.",
    "paraphrasing": "Agent accurately acknowledged and mirrored the customer's reported issue.",
    "verified customer": "Agent verified customer identity within the required time window.",
    "probing": "Agent asked effective diagnostic questions to investigate the root cause.",
    "took ownership of the problem": "Agent demonstrated clear ownership without deflecting or blaming other departments.",
    "active listening": "Agent practiced active listening without repetitive or redundant questions.",
    "confirmed the issue is resolved": "Agent explicitly confirmed that the issue was resolved before closing.",
    "escalation": "Agent handled call escalation paths in compliance with standard procedure.",
    "hostility": "No hostile, abusive, or unprofessional language detected from the agent."
}

# Static coaching for failed items that have no rule-specific message (Laya cannot generate text)
RULE_BASED_FAIL_COACHING = {
    "confirmed the issue is resolved": "Before closing, ask the customer to confirm the issue is fixed and state clearly that it is resolved.",
    "escalation": "When a customer asks for a supervisor or escalation, transfer or schedule it promptly instead of refusing or discouraging it.",
    "hostility": "Stay calm and respectful at all times; never insult, mock, threaten or hang up on a customer."
}

def _noul(instructions: str, true_text: str, false_text: str, neutral_labels: bool = False) -> Dict[str, Any]:
    question = {"type": "noul", "instructions": instructions, "criteria": {"true": true_text, "false": false_text}}
    if neutral_labels:
        # on the English checkpoint the default "true"/"false" option labels can outweigh the text itself
        question["labels"] = {"true": "A", "false": "B"}
    return question

# One Laya question per check. pass_threshold applies to P(pass): P(yes) when yes means PASS, else 1 - P(yes).
# Wording and thresholds come from the out-of-the-box test in laya_eval/ (synthetic data, so they are
# starting values to re-tune on human-reviewed calls).
LAYA_CHECKS = {
    "empathy": {"yes_means": "PASS", "pass_threshold": 0.78, "question": _noul(
        "Does the agent acknowledge the customer's frustration with empathy?",
        "the agent acknowledges the customer's frustration or feelings and responds with care",
        "the agent ignores, brushes off or is rude about the customer's frustration", neutral_labels=True)},
    "active_listening": {"yes_means": "FAIL", "pass_threshold": 0.19, "question": _noul(
        "Does the second agent question ask again for information the customer already gave in their answer?",
        "the second question asks again for information the customer already gave in their answer",
        "the second question asks for something new, or re-checks something that may have changed")},
    "ownership": {"yes_means": "FAIL", "pass_threshold": 0.52, "question": _noul(
        "Does the agent deflect responsibility, blame another team, or refuse to help?",
        "the agent deflects, blames another team or department, refuses to help, or tells the customer to contact someone else",
        "the agent takes ownership and keeps working on the customer's problem", neutral_labels=True)},
    # judged on every agent line in chunks (rule_engine.extract_rapport_chunks); one rude chunk fails the item.
    # INTERIM cutoff 0.50: the untrained model gives every chunk of every probed call (polite or rude) P(rude) of only
    # 0.19-0.22, so no cutoff separates them. 0.81 (P(rude) > 0.19) sat on that floor and failed 29 of 33 polite
    # bulk calls. At 0.50 the check never fails until the model is fine-tuned, then re-tune at call level.
    "rapport": {"yes_means": "FAIL", "pass_threshold": 0.50, "question": _noul(
        "Is any agent line rude, condescending, dismissive, sarcastic or unprofessional toward the customer?",
        "at least one agent line is rude, condescending, dismissive, sarcastic or unprofessional toward the customer, "
        "for example blaming the customer, talking down to them or brushing them off",
        "every agent line is polite, respectful and professional")},
    "probing": {"yes_means": "PASS", "pass_threshold": 0.70, "question": _noul(
        "Did the agent ask at least one genuine diagnostic question about the customer's problem?",
        "the agent asked at least one question that investigates the cause or specifics of the problem, such as when it started, which device, what error or lights, or what was already tried",
        "the agent only asked greetings, identity verification, confirmations, upsell, scheduling or closing questions", neutral_labels=True)},
    # 0.73: best balanced accuracy (0.68) on the b_* bulk calls, whose filenames name the missing confirmation.
    # The scores barely separate (no-confirmation endings 0.66-0.75, confirmed 0.47-0.79), so this needs training.
    "resolved": {"yes_means": "PASS", "pass_threshold": 0.73, "question": _noul(
        "Did the agent explicitly confirm that the customer's issue was resolved?",
        "the agent explicitly confirms the issue is resolved or fixed, usually after checking with the customer",
        "the agent never confirms resolution: the call just ends, the agent assumes it is fixed, the customer says it still fails, or it is handed off", neutral_labels=True)},
    "escalation": {"yes_means": "FAIL", "pass_threshold": 0.47, "question": _noul(
        "Did the customer ask for a supervisor, manager or escalation that the agent refused, ignored or discouraged?",
        "the customer asked for a supervisor, manager or escalation and the agent refused, ignored, discouraged or faked it",
        "the customer did not ask to escalate, or the agent handled the request properly")},
    "hostility": {"yes_means": "FAIL", "pass_threshold": 0.79, "question": _noul(
        "Is the agent hostile, abusive, insulting, threatening, mocking, or hangs up on the customer?",
        "the agent insults, mocks, threatens, is abusive toward the customer, or abruptly hangs up",
        "the agent stays professional and respectful, even if the customer is angry")},
    # not covered by the test yet: threshold is a neutral default
    "paraphrasing": {"yes_means": "PASS", "pass_threshold": 0.50, "question": _noul(
        "Does the agent restate or paraphrase the customer's problem back to them?",
        "the agent restates the customer's problem in their own words to confirm they understood it",
        "the agent never restates the customer's problem")},
}

# Cutoffs for the FINE-TUNED checkpoint (applied only when LAYA_CHECKPOINT is set; the stock model keeps the values above).
# Tuned on Claude-written dev data (empathy, paraphrasing, active_listening, resolved: laya-training run ft2-20261017-0354,
# softce). Rapport is a call-level cutoff: the call fails if any chunk's P(pass) is below it. The tuned model is very
# confident (P near 0.05 or 0.95), 0.20 sits between the 5 rude Main/bulk calls (max 0.09) and the polite natural call
# gold_02 (0.37). It was chosen ON those calls, so they are no longer an independent check. probing, ownership,
# escalation and hostility keep their values (regression checks, no change needed).
FINETUNED_CUTOFFS = {"empathy": 0.49, "paraphrasing": 0.47, "active_listening": 0.50, "resolved": 0.42, "rapport": 0.20}
if os.getenv("LAYA_CHECKPOINT"):
    for _name, _cut in FINETUNED_CUTOFFS.items():
        LAYA_CHECKS[_name]["pass_threshold"] = _cut

def _p_pass(check: Dict[str, Any], p_yes: float) -> float:
    return p_yes if check["yes_means"] == "PASS" else 1.0 - p_yes

def _laya_verdict(check_key: str, text: str, label: str) -> str:
    check = LAYA_CHECKS[check_key]
    p_yes = predict_yes(text, {"q": check["question"]}, label=label)["q"]
    return "PASS" if _p_pass(check, p_yes) >= check["pass_threshold"] else "FAIL"

def _batch_check(item: Dict[str, Any]) -> Dict[str, Any]:
    """Laya check for a batch-rated line item: a tested question for known names, otherwise one built from the item text."""
    lname = item.get("name", "").lower()
    if "resolved" in lname or "resolution" in lname:
        return LAYA_CHECKS["resolved"]
    if "escalation" in lname:
        return LAYA_CHECKS["escalation"]
    if "hostility" in lname:
        return LAYA_CHECKS["hostility"]

    name = re.sub(r"\s+", " ", re.sub(r"<\s*br\s*/?\s*>", " ", item.get("name", "Item"), flags=re.IGNORECASE)).strip()
    desc = re.sub(r"<\s*br\s*/?\s*>", " ", item.get("description", ""), flags=re.IGNORECASE)
    desc = re.sub(r"\boutput\s+(yes\s+or\s+no|pass\s+or\s+fail)\b\.?", "", desc, flags=re.IGNORECASE)
    desc = re.sub(r"\s+", " ", desc).strip()
    if desc.upper().startswith("VIOLATION-BASED"):
        rule = re.sub(r"^VIOLATION-BASED:?\s*", "", desc, flags=re.IGNORECASE)
        return {"yes_means": "FAIL", "pass_threshold": 0.50, "question": _noul(
            f"Does the agent violate this rule: {name}?",
            f"an agent line clearly violates it: {rule}",
            "no agent line violates it")}
    return {"yes_means": "PASS", "pass_threshold": 0.50, "question": _noul(
        f"Did the agent do this: {name}?",
        f"the agent clearly did it: {desc or name}",
        "the agent did not do it")}

def evaluate_interaction(
    transcript_data: Union[str, List[Dict[str, Any]]],
    criteria_data: Dict[str, Any],
    tenant_id: str,
    channel: str = "Call",
    times: Optional[List[Optional[int]]] = None,
    caller: Optional[str] = None
) -> Dict[str, Any]:
    from src.services.rule_engine import (
        evaluate_branding, evaluate_hold_and_dead_air,
        evaluate_verified_customer, evaluate_personalized_call,
    )

    inp = build_laya_inputs(transcript_data, caller)
    turns, parsed_times, customer_name = inp.turns, inp.times, inp.customer_name

    categories = criteria_data.get("categories", [])
    category_weights = criteria_data.get("category_weights", {})
    auto_fail_rules = criteria_data.get("auto_fail_rules", [])

    selected_criteria = {
        item.get("name", "").strip().lower()
        for cat in categories
        for item in cat.get("line_items", [])
    }
    selected_categories = {cat.get("name", "").strip() for cat in categories}

    rule_ratings = []

    if "branding and survey check" in selected_criteria:
        rule_ratings.append(evaluate_branding(turns))

    if "hold time and dead air" in selected_criteria:
        rule_ratings.append(evaluate_hold_and_dead_air(turns, parsed_times))

    if "verified customer" in selected_criteria:
        rule_ratings.append(evaluate_verified_customer(turns, parsed_times))

    if "personalized the call/ticket appropriately" in selected_criteria:
        rule_ratings.append(evaluate_personalized_call(turns, customer_name))

    if "empathy & acknowledgment statement" in selected_criteria:
        empathy_snippets = inp.empathy
        emp_rating = {
            "category": "Soft Skills",
            "name": "Empathy & Acknowledgment Statement",
            "rating": "PASS",
            "score": 100,
            "deduction_value": 35,
            "coaching": ""
        }
        # each snippet is judged on its own; one FAIL fails the item
        for empathy_snippet in empathy_snippets:
            if _laya_verdict("empathy", empathy_snippet, "verify_empathy") == "FAIL":
                emp_rating["rating"] = "FAIL"
                emp_rating["coaching"] = "Failed to show empathy to customer's frustration."
                break
        rule_ratings.append(emp_rating)

    if "paraphrasing" in selected_criteria:
        # flow v2: no restatement cue in the first minutes -> FAIL without asking the model (inp.paraphrasing is None)
        para_rating = "FAIL" if inp.paraphrasing is None else _laya_verdict("paraphrasing", inp.paraphrasing, "verify_paraphrasing")
        rule_ratings.append({
            "category": "Technical Knowledge",
            "name": "Paraphrasing",
            "rating": para_rating,
            "score": 100 if para_rating == "PASS" else 0,
            "deduction_value": 15,
            "coaching": "Failed to paraphrase core issue." if para_rating == "FAIL" else ""
        })

    if "active listening" in selected_criteria:
        al_snippet = inp.active_listening
        al_rating = "PASS"
        if al_snippet:
            # LAYA_AL_SOURCE2 on: one model call per pair, so a real repeat is not diluted by harmless ones
            al_blocks = al_snippet.split("\n\n") if al_source2_enabled() else [al_snippet]
            if any(_laya_verdict("active_listening", b, "verify_al") == "FAIL" for b in al_blocks):
                al_rating = "FAIL"
        rule_ratings.append({
            "category": "Technical Knowledge",
            "name": "Active listening",
            "rating": al_rating,
            "score": 100 if al_rating == "PASS" else 0,
            "deduction_value": 10,
            "coaching": "Repeated questions unnecessarily." if al_rating == "FAIL" else ""
        })

    if "took ownership of the problem" in selected_criteria:
        own_snip = inp.ownership
        own_rating = {
            "category": "Technical Knowledge",
            "name": "Took ownership of the problem",
            "rating": "PASS",
            "score": 100,
            "deduction_value": 25,
            "coaching": ""
        }
        if own_snip:
            if _laya_verdict("ownership", own_snip, "verify_ownership") == "FAIL":
                own_rating["rating"] = "FAIL"
                own_rating["coaching"] = "Agent deflected responsibility or blamed another team instead of owning the issue."
        rule_ratings.append(own_rating)

    if "build rapport and observed professionalism" in selected_criteria:
        rap_rating = {
            "category": "Soft Skills",
            "name": "Build rapport and observed professionalism",
            "rating": "PASS",
            "score": 100,
            "deduction_value": 20,
            "coaching": ""
        }
        # each snippet is judged on its own; one FAIL fails the item
        for rap_snip in inp.rapport:
            if _laya_verdict("rapport", rap_snip, "verify_rapport") == "FAIL":
                rap_rating["rating"] = "FAIL"
                rap_rating["coaching"] = "Agent used rude or condescending language."
                break
        rule_ratings.append(rap_rating)

    if "probing" in selected_criteria:
        prob_rating = {
            "category": "Technical Knowledge",
            "name": "Probing",
            "rating": "FAIL",
            "score": 0,
            "deduction_value": 25,
            "coaching": "Agent did not ask diagnostic questions to investigate the problem."
        }
        if inp.probing is not None:
            if _laya_verdict("probing", inp.probing, "verify_probing") == "PASS":
                prob_rating["rating"] = "PASS"
                prob_rating["score"] = 100
                prob_rating["coaching"] = ""
        rule_ratings.append(prob_rating)

    handled = [r["name"].lower() for r in rule_ratings]
    all_items = []
    for cat in categories:
        for item in cat.get("line_items", []):
            lname = item["name"].lower()
            if lname not in handled and "expectations" not in lname and "solution" not in lname and "non-first" not in lname:
                all_items.append((cat["name"], item))
                
    b1_agent, b2_end, b3_full = [], [], []
    for cat, item in all_items:
        lname = item["name"].lower()
        if "resolved" in lname or "resolution" in lname:
            b2_end.append((cat, item))
        elif "escalation" in lname or "hostility" in lname:
            b3_full.append((cat, item))
        else:
            b1_agent.append((cat, item))
        
    def run_batch(items, tx, label):
        """All items of one batch become noul questions answered in a single Laya call over the same text."""
        if not items:
            return []
        checks = [(cat, item, _batch_check(item)) for cat, item in items]
        questions = {f"item_{n}": check["question"] for n, (_, _, check) in enumerate(checks)}
        p_yes = predict_yes(tx, questions, label=label)
        batch = []
        for n, (cat, item, check) in enumerate(checks):
            rating = "PASS" if _p_pass(check, p_yes[f"item_{n}"]) >= check["pass_threshold"] else "FAIL"
            batch.append({
                "category": cat,
                "name": item.get("name", "Item"),
                "description": item.get("description", ""),
                "rating": rating,
                "score": RATING_SCORES[rating],
                "deduction_value": item.get("deduction_value", 10),
                "coaching": ""
            })
        return batch

    batch_ratings = []
    batch_ratings.extend(run_batch(b1_agent, inp.batch_agent_only, "batch_agent_only"))
    batch_ratings.extend(run_batch(b2_end, inp.resolved, "batch_end"))
    batch_ratings.extend(run_batch(b3_full, inp.batch_full, "batch_full"))

    ratings = rule_ratings + batch_ratings

    ded_map = {}
    for cat in categories:
        for it in cat.get("line_items", []):
            ded_map[it.get("name", "").strip().lower()] = it.get("deduction_value", 10)
    for r in ratings:
        dv = ded_map.get(r.get("name", "").strip().lower())
        if dv is not None:
            r["deduction_value"] = dv
        if r.get("rating") == "NOT_RATED":
            r["rating"] = "FAIL"
            if not r.get("coaching"):
                r["coaching"] = "Could not be verified from the transcript."

    # profanity is checked on agent lines only; the customer's language never fails the agent
    is_auto_fail, reason = check_auto_fail(inp.agent_text, [], auto_fail_rules, ratings)

    cat_scores, b_score = calculate_category_scores(
        ratings,
        category_weights,
        is_auto_fail,
        selected_categories
    )
    
    _norm = {"YES": "PASS", "NO": "FAIL"}
    clean_scorecard = []
    for r in ratings:
        norm_rating = _norm.get(r.get("rating"), r.get("rating", "FAIL"))
        item_name = r.get("name", "")
        name_key = item_name.strip().lower()
        
        if norm_rating == "PASS":
            coaching_text = RULE_BASED_PASS_DESCRIPTIONS.get(
                name_key,
                f"Standard compliant performance observed for '{item_name}'."
            )
        else:
            coaching_text = (
                r.get("coaching")
                or RULE_BASED_FAIL_COACHING.get(name_key)
                or f"Criteria standard for '{item_name}' was not met."
            )

        clean_scorecard.append({
            "category": r.get("category", "General Handling"),
            "name": item_name,
            "rating": norm_rating,
            "coaching": coaching_text
        })

    cat_summary_map: Dict[str, Dict[str, int]] = {}
    for entry in clean_scorecard:
        c = entry["category"]
        if c not in cat_summary_map:
            cat_summary_map[c] = {"passed": 0, "total": 0}
        cat_summary_map[c]["total"] += 1
        if entry.get("rating") == "PASS":
            cat_summary_map[c]["passed"] += 1

    category_summary = [
        {
            "category": cat_name,
            "passed": stats["passed"],
            "total": stats["total"],
            "ratio": f"{stats['passed']:02d}/{stats['total']:02d}"
        }
        for cat_name, stats in cat_summary_map.items()
    ]

    return {
        "final_score": b_score,
        "auto_failed_count": 1 if is_auto_fail else 0,
        "category_summary": category_summary,
        "scorecard": clean_scorecard,
        "is_auto_fail": is_auto_fail,
        "auto_fail_reason": reason
    }

def check_auto_fail(
    transcript: str,
    harsh_lines: List[Dict[str, Any]],
    auto_fail_rules: List[Dict[str, Any]],
    ratings: List[Dict[str, Any]]
) -> (bool, Optional[str]):
    lower_tx = transcript.lower()
    profanities = ["fuck", "shut up", "idiot", "get lost", "stupid", "hang up"]
    for word in profanities:
        if word in lower_tx:
            return True, f"Auto-Fail Triggered: Profanity/Discourtesy detected ('{word}')"

    if len(harsh_lines) >= 3:
        return True, "Auto-Fail Triggered: Multiple highly hostile/harsh agent statements detected"
        
    for r in ratings:
        if "AUTO FAIL" in r["category"].upper() and r["rating"] in ["NO", "FAIL"]:
            return True, f"Auto-Fail Triggered by Scorecard: {r['name']}"

    return False, None

def calculate_category_scores(
    ratings: List[Dict[str, Any]],
    category_weights: Dict[str, float],
    is_auto_fail: bool,
    selected_categories: Optional[set] = None
) -> (Dict[str, float], float):
    if is_auto_fail:
        return {cat: 0.0 for cat in category_weights}, 0.0

    grouped = {}
    for r in ratings:
        cat = r.get("category", "General Handling")
        grouped.setdefault(cat, []).append(r)

    cat_scores = {}
    for cat, items in grouped.items():
        score = 100.0
        for item in items:
            if item.get("rating") in ["FAIL", "NO"]:
                deduction = item.get("deduction_value", 10)
                score -= deduction
        cat_scores[cat] = max(0.0, float(score))

    active_weights = {}
    if selected_categories:
        for cat in selected_categories:
            if cat in category_weights:
                active_weights[cat] = float(category_weights[cat])
            elif cat in cat_scores:
                active_weights[cat] = 1.0
    else:
        for cat, weight in category_weights.items():
            active_weights[cat] = float(weight)

    if not active_weights:
        active_weights = {cat: 1.0 for cat in cat_scores} if cat_scores else {"General Handling": 1.0}

    total_weight = sum(active_weights.values())
    if total_weight > 0:
        normalized_weights = {cat: w / total_weight for cat, w in active_weights.items()}
    else:
        n = len(active_weights) or 1
        normalized_weights = {cat: 1.0 / n for cat in active_weights}

    blended = sum(
        cat_scores.get(cat, 100.0) * normalized_weights[cat]
        for cat in active_weights
    )

    return cat_scores, round(blended, 1)
