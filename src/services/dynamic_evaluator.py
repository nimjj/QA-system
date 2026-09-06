"""Dynamic Multi-Tenant QA Evaluator Module.

Combines Python rule engines and LLM reasoning 
against dynamic company criteria schemas.
"""

import re
from typing import Dict, Any, List, Optional
from src.core.llm_client import query_llm
from src.services.qa_summary import SUMMARY_PROMPT, generate_scalable_summary
from src.services.qa_suggestions import SUGGESTIONS_PROMPT, clean_suggestions
from src.services.response_time import (
    leading_time_seconds, response_delays, response_time_score,
)

RATING_SCORES = {"PASS": 100,  "FAIL": 0, "YES": 100, "NO": 0}


def preview_evaluation_prompt(
    transcript_text: str,
    criteria_data: Dict[str, Any],
    tenant_id: str,
    channel: str = "Call"
) -> Dict[str, Any]:
    """Construct and preview the exact LLM prompt without executing evaluation."""
    # 1. Parse turns and clean timestamps
    turns = []
    clean_lines = []
    for line in transcript_text.strip().splitlines():
        line = line.strip()
        if not line:
            continue
        line = re.sub(r"^[\[\(]\s*\d{1,2}:\d{2}(?::\d{2})?\s*[\]\)]\s*", "", line)
        clean_lines.append(line)
        if ":" in line:
            spk, txt = line.split(":", 1)
            turns.append((spk.strip(), txt.strip()))

    clean_transcript = "\n".join(clean_lines)

    if not turns:
        turns = [("Agent", transcript_text)]
        clean_transcript = transcript_text

    # 2. Vector RAG Policy Search via LLM Summary
    summary = generate_scalable_summary(clean_transcript)
    matched_policies = []

    # 3. Extract Criteria Line Items and Weights
    categories = criteria_data.get("categories", [])
    category_weights = criteria_data.get("category_weights", {})
    auto_fail_rules = criteria_data.get("auto_fail_rules", [])

    if not categories:
        categories = [
            {
                "name": "General Handling",
                "weight_percentage": 100.0,
                "line_items": [
                    {"name": "Professionalism & Tone", "description": "Polite, respectful, no discourtesy."},
                    {"name": "Accuracy & Knowledge", "description": "Provided correct solution according to policy."},
                    {"name": "Ownership & Resolution", "description": "Took ownership and resolved the issue."}
                ]
            }
        ]
        category_weights = {"General Handling": 1.0}

    # 4. Build Dynamic Scorecard Prompt
    scorecard_prompt = build_dynamic_prompt(
        transcript_text=clean_transcript,
        categories=categories,
        auto_fail_rules=auto_fail_rules,
        matched_policies=matched_policies,
        channel=channel
    )

    return {
        "prompt": scorecard_prompt,
        "matched_policies": matched_policies,
        "categories_count": len(categories),
        "line_items_count": sum(len(c.get("line_items", [])) for c in categories),
        "channel": channel,
        "tenant_id": tenant_id
    }


def evaluate_interaction(
    transcript_text: str,
    criteria_data: Dict[str, Any],
    tenant_id: str,
    channel: str = "Call",
    times: Optional[List[Optional[int]]] = None,
    custom_prompt: Optional[str] = None
) -> Dict[str, Any]:
    """Execute dynamic QA evaluation for a customer interaction."""
    # 1. Parse turns and remove timestamps for LLM efficiency
    turns = []
    parsed_times = []
    clean_lines = []
    for line in transcript_text.strip().splitlines():
        line = line.strip()
        if not line:
            continue
        t = leading_time_seconds(line)
        line = re.sub(r"^[\[\(]\s*\d{1,2}:\d{2}(?::\d{2})?\s*[\]\)]\s*", "", line)
        clean_lines.append(line)
        if ":" in line:
            spk, txt = line.split(":", 1)
            turns.append((spk.strip(), txt.strip()))
            parsed_times.append(t)

    clean_transcript = "\n".join(clean_lines)

    if not turns:
        turns = [("Agent", transcript_text)]
        parsed_times = [None]
        clean_transcript = transcript_text

    # 2. Extract Topics using Lightweight LLM (LLM3:1b)
    from src.services.qa_summary import generate_scalable_summary
    topic_keywords = generate_scalable_summary(clean_transcript)

    matched_policies = []
    
    # 4. Deterministic Python Rule Engine (Branding & SLA Checks)
    from src.services.rule_engine import evaluate_branding, evaluate_hold_and_dead_air
    rule_ratings = [
        evaluate_branding(turns),
        evaluate_hold_and_dead_air(turns, parsed_times)
    ]
    harsh_lines = []

    # 5. Extract Criteria Line Items and Weights
    categories = criteria_data.get("categories", [])
    category_weights = criteria_data.get("category_weights", {})
    auto_fail_rules = criteria_data.get("auto_fail_rules", [])

    if not categories:
        categories = [
            {
                "name": "Soft Skills",
                "weight_percentage": 33.3,
                "line_items": [
                    {"name": "Personalized the call/ticket appropriately", "description": "Evaluate if the agent used the correct name in the greeting or at least once throughout the conversation."},
                    {"name": "Empathy & Acknowledgment Statement", "description": "Evaluate if the agent provided empathy statements when appropriate and acknowledged the customer's questions or statements (e.g., through paraphrasing). The agent must not be blunt."},
                    {"name": "Build rapport and observed professionalism", "description": "Evaluate if the agent was courteous, respectful, adjusted to the customer's technical pacing, did not interrupt, and avoided jargon or unprofessional sounds."}
                ]
            },
            {
                "name": "Technical Knowledge",
                "weight_percentage": 66.7,
                "line_items": [
                    {"name": "Paraphrasing", "description": "Evaluate if the agent paraphrased the issue at the onset of the call or as soon as the customer stated their request to reconfirm understanding."},
                    {"name": "Verified customer", "description": "Evaluate if the agent validated the caller's correct name, company name, email address, and contact number."},
                    {"name": "Probing", "description": "Evaluate if the agent used proper and effective probing questions to identify the concern, especially if the customer was unable to express the issue clearly."},
                    {"name": "Set proper expectations", "description": "Evaluate if the agent provided accurate expectations about the resolution, addressed possible related issues that might arise, and provided updates as soon as available."},
                    {"name": "Provided the appropriate solution", "description": "Evaluate if the agent performed logical troubleshooting steps, followed internal processes, resolved all issues, and provided initial instructions rather than just asking the customer to contact back."},
                    {"name": "Took ownership of the problem", "description": "Evaluate if the agent exhausted all resources to provide a resolution, offered meaningful troubleshooting (not just transferring without attempting to assist), and took ownership of the ticket."},
                    {"name": "Active listening", "description": "Evaluate if the agent avoided asking the customer for information that the customer had already provided earlier in the call (e.g., name, company, error message). If they ask for repeated info two or more times, rate as NO."},
                    {"name": "Confirmed the issue is resolved", "description": "Evaluate if the agent gained verbal confirmation that the issue is resolved, asked the customer to test, provided a wrap-up summary of the resolution, and offered further assistance."}
                ]
            },
            {
                "name": "Auto Fail Category",
                "weight_percentage": 0.0,
                "line_items": [
                    {"name": "Escalation", "description": "Evaluate if the agent refused to escalate to a Supervisor at the customer's request, or failed to escalate for customers threatening to cancel their service. (Rate NO if they failed to escalate when required)."},
                    {"name": "Non-First Call Resolution", "description": "Evaluate if the agent provided incomplete troubleshooting steps, gave an incorrect resolution, or failed to apply accurate changes to the account. (Rate NO if resolution was incorrect or incomplete)."}
                ]
            }
        ]
        category_weights = {"Soft Skills": 0.333, "Technical Knowledge": 0.667, "Auto Fail Category": 0.0}

    # 6. LLM Evaluation (Grouped Map-Reduce)
    if custom_prompt:
        llm_reply = query_llm(custom_prompt, label="dynamic_scorecard")
    else:
        llm_reply_parts = []
        # Chunk categories to save LLM calls but ensure accuracy.
        # We now chunk dynamically: one category per prompt for maximum focus and accuracy.
        chunks = [[c] for c in categories]
        
        for chunk in chunks:
            if not chunk: continue
            cat_prompt = build_dynamic_prompt(
                transcript_text=clean_transcript,
                categories=chunk,
                auto_fail_rules=auto_fail_rules,
                matched_policies=matched_policies,
                channel=channel,
                harsh_lines=harsh_lines
            )
            # label based on first category in chunk
            reply = query_llm(cat_prompt, label=f"scorecard_{chunk[0].get('name', 'cat')[:10]}")
            llm_reply_parts.append(reply)
            
        llm_reply = "\n\n".join(llm_reply_parts)

    ratings = parse_dynamic_ratings(llm_reply, categories)
    # Inject Python rule-based scores (Branding & Dead Air) into the scorecard
    ratings = rule_ratings + ratings
    intense_moments = []
    harsh_agent_lines = harsh_lines

    # 6. Check Auto-Fail Triggers
    is_auto_fail, auto_fail_reason = check_auto_fail(transcript_text, harsh_agent_lines, auto_fail_rules, ratings)

    # 7. Mathematical Scoring Engine
    category_scores, blended_score = calculate_category_scores(ratings, category_weights, is_auto_fail)

    # 8. Dynamic Summary (Aware of failures)
    audit_context_lines = []
    if is_auto_fail:
        audit_context_lines.append(f"CRITICAL AUTO-FAIL TRIGGERED: {auto_fail_reason}")
    for r in ratings:
        if r["rating"] in ["NO", "FAIL"]:
            audit_context_lines.append(f"FAILED CHECK - {r['name']}: {r['reason']}")
    
    evaluation_context_str = "\n".join(audit_context_lines) if audit_context_lines else "No critical failures identified. The agent passed all checks."
    
    summary = generate_scalable_summary(clean_transcript, evaluation_context=evaluation_context_str)

    # 9. Suggestions
    suggestions = clean_suggestions(query_llm(SUGGESTIONS_PROMPT.format(transcript=clean_transcript), label="suggestions"))

    return {
        "final_score": blended_score,
        "is_auto_fail": is_auto_fail,
        "auto_fail_reason": auto_fail_reason,
        "category_scores": category_scores,
        "scorecard": ratings,
        "sentiment_analysis": {
            "rows": [],
            "intense_moments": intense_moments,
            "harsh_agent_lines": harsh_agent_lines
        },
        "matched_policies": matched_policies,
        "summary": summary,
        "suggestions": suggestions
    }

def parse_llm_intensity(reply: str) -> (List[Dict[str, Any]], List[Dict[str, Any]]):
    """Parse intense moments and harsh lines from the LLM scorecard reply."""
    intense_moments = []
    harsh_lines = []
    
    current_section = None
    for line in reply.splitlines():
        clean_line = line.strip()
        upper_line = clean_line.upper()
        
        if "INTENSE MOMENTS" in upper_line:
            current_section = "intense"
            continue
        elif "HARSH AGENT LINES" in upper_line:
            current_section = "harsh"
            continue
        elif "SCORECARD" in upper_line or "PASS" in upper_line or "FAIL" in upper_line:
            if "SCORECARD" in upper_line:
                current_section = None
        
        if not clean_line or clean_line.lower() == "none" or clean_line == "- none" or clean_line == "-":
            continue
            
        if current_section == "intense" and len(clean_line) > 5:
            intense_moments.append({"turn": "?", "speaker": "?", "text": clean_line.lstrip("-* "), "sentiment": -1.0, "intense": True})
        elif current_section == "harsh" and len(clean_line) > 5:
            harsh_lines.append({"turn": "?", "speaker": "Agent", "text": clean_line.lstrip("-* "), "sentiment": -1.0, "intense": True})
            
    return intense_moments, harsh_lines

def build_dynamic_prompt(
    transcript_text: str,
    categories: List[Dict[str, Any]],
    auto_fail_rules: List[Dict[str, Any]],
    matched_policies: List[Dict[str, Any]],
    channel: str,
    harsh_lines: List[Dict[str, Any]] = None
) -> str:
    """Construct dynamic LLM prompt tailored to tenant criteria with sanitized formatting."""
    if harsh_lines is None:
        harsh_lines = []
        
    # 1. Evaluation Line Items
    items_list = []
    for cat in categories:
        cat_name = re.sub(r"<\s*br\s*/?\s*>", " ", cat.get("name", "Category"), flags=re.IGNORECASE).strip()
        for item in cat.get("line_items", []):
            name = re.sub(r"<\s*br\s*/?\s*>", " ", item.get("name", "Item"), flags=re.IGNORECASE).strip()
            name = re.sub(r"\s+", " ", name)
            desc = re.sub(r"<\s*br\s*/?\s*>", " ", item.get("description", ""), flags=re.IGNORECASE).strip()
            desc = re.sub(r"\s+", " ", desc)
            spiels = item.get("verbatim_spiels", [])
            clean_spiels = [re.sub(r"<\s*br\s*/?\s*>", " ", s, flags=re.IGNORECASE).strip() for s in spiels]
            spiel_txt = f" [Required Spiels: {', '.join(clean_spiels)}]" if clean_spiels else ""
            items_list.append(f"- [{cat_name}] {name}: {desc}{spiel_txt}")

    criteria_str = "\n".join(items_list)
    
    # 2. Auto-Fail Zero-Tolerance Rules Section
    auto_fail_list = []
    for r in auto_fail_rules:
        r_name = re.sub(r"<\s*br\s*/?\s*>", " ", r.get("name", "Auto-Fail"), flags=re.IGNORECASE).strip()
        r_desc = re.sub(r"<\s*br\s*/?\s*>", " ", r.get("description", r.get("trigger", "Immediate 0 score")), flags=re.IGNORECASE).strip()
        auto_fail_list.append(f"• {r_name}: {r_desc}")
    auto_fail_str = "\n".join(auto_fail_list) if auto_fail_list else "• Discourtesy / Rudeness: Immediate 0 score on profanity or policy abandonment."

    policies_str = "\n".join(
        f"• {re.sub(r'<\s*br\s*/?\s*>', ' ', p['title'], flags=re.IGNORECASE)}: {re.sub(r'<\s*br\s*/?\s*>', ' ', p['content'][:300], flags=re.IGNORECASE)}" 
        for p in matched_policies
    ) or "• No specific policy override found."
    
    harsh_lines_str = "\n".join(
        f"Agent: \"{h['text']}\"" for h in harsh_lines
    ) if harsh_lines else "None detected."

    import os
    _ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    prompt_path = os.getenv("PROMPT_DYNAMIC_EVALUATION_PATH", "resources/prompts/dynamic_evaluation_prompt.txt")
    full_path = os.path.join(_ROOT, prompt_path)
    with open(full_path, "r", encoding="utf-8") as f:
        template = f.read()
        
    return template.format(
        channel=channel,
        auto_fail_str=auto_fail_str,
        policies_str=policies_str,
        criteria_str=criteria_str,
        harsh_lines_str=harsh_lines_str,
        transcript_text=transcript_text
    )


def parse_dynamic_ratings(reply: str, categories: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Parse YES/NO (or PASS/FAIL) ratings from LLM output (Lenient for small models)."""
    ratings = []
    
    # 1. Pre-parse all findings from the LLM reply
    extracted_ratings = []
    for line in reply.splitlines():
        # Match YES/NO/PASS/FAIL only if it's at the start of the line, or immediately following the item name (e.g., "Item Name: YES - reason")
        match = re.search(r"^(?:[^:]*:\s*)?\**\b(PASS|FAIL|PASSED|FAILED|YES|NO)\b", line, re.IGNORECASE)
        if match:
            rating = match.group(1).upper()
            if rating == "PASSED": rating = "PASS"
            if rating == "FAILED": rating = "FAIL"
            # Extract everything after the match as the reason
            reason_parts = line.split(match.group(0), 1)
            reason = reason_parts[-1].strip(" -:*") if len(reason_parts) > 1 else ""
            if not reason:
                reason = line.strip(" -:*")
            extracted_ratings.append({"raw_line": line.lower(), "rating": rating, "reason": reason})

    for cat in categories:
        cat_name = cat.get("name", "Category")
        for item in cat.get("line_items", []):
            name = item.get("name", "Item")
            rating = "PASS"
            reason = "Standard compliant response"

            # 2. Try to find a line matching the item name
            matched = False
            for ext in extracted_ratings:
                if name.lower() in ext["raw_line"] or name.split()[0].lower() in ext["raw_line"]:
                    rating = ext["rating"]
                    reason = ext["reason"] if ext["reason"] else f"Evaluated as {rating}"
                    matched = True
                    extracted_ratings.remove(ext)
                    break
            
            # 3. Lenient fallback: If no exact name match, pop the first available rating 
            # (Works perfectly for map-reduce where there's usually 1 item per category)
            if not matched and len(extracted_ratings) > 0:
                 ext = extracted_ratings.pop(0)
                 rating = ext["rating"]
                 reason = ext["reason"] if ext["reason"] else f"Evaluated as {rating}"

            score = RATING_SCORES.get(rating, 0)
            ratings.append({
                "category": cat_name,
                "name": name,
                "rating": rating,
                "score": score,
                "reason": reason or f"Evaluated as {rating}"
            })
    return ratings


def check_auto_fail(
    transcript: str,
    harsh_lines: List[Dict[str, Any]],
    auto_fail_rules: List[Dict[str, Any]],
    ratings: List[Dict[str, Any]]
) -> (bool, Optional[str]):
    """Check for instant zero auto-fail breaches."""
    lower_tx = transcript.lower()

    # Profanity / extreme discourtesy check
    profanities = ["fuck", "shut up", "idiot", "get lost", "stupid", "hang up"]
    for word in profanities:
        if word in lower_tx:
            return True, f"Auto-Fail Triggered: Profanity/Discourtesy detected ('{word}')"

    # Extreme harsh agent lines
    if len(harsh_lines) >= 3:
        return True, "Auto-Fail Triggered: Multiple highly hostile/harsh agent statements detected"
        
    # Check LLM scorecard for Auto Fail category failures
    for r in ratings:
        if "AUTO FAIL" in r["category"].upper() and r["rating"] in ["NO", "FAIL"]:
            return True, f"Auto-Fail Triggered by Scorecard: {r['name']} - {r['reason']}"

    return False, None


def calculate_category_scores(
    ratings: List[Dict[str, Any]],
    category_weights: Dict[str, float],
    is_auto_fail: bool
) -> (Dict[str, float], float):
    """Calculate weighted category scores and blended final score."""
    if is_auto_fail:
        return {cat: 0.0 for cat in category_weights}, 0.0

    grouped = {}
    for r in ratings:
        cat = r.get("category", "General Handling")
        grouped.setdefault(cat, []).append(r["score"])

    cat_scores = {}
    for cat, scores in grouped.items():
        cat_scores[cat] = round(sum(scores) / len(scores), 1)

    total_weight = sum(category_weights.values()) or 1.0
    blended = sum(cat_scores.get(cat, 70.0) * (category_weights.get(cat, 1.0) / total_weight) for cat in category_weights)
    
    if not category_weights:
        all_scores = [r["score"] for r in ratings]
        blended = sum(all_scores) / len(all_scores) if all_scores else 80.0

    return cat_scores, round(blended, 1)
