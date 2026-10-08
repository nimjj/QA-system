import difflib
import re
from typing import List, Tuple, Dict, Any

def evaluate_branding(turns: List[Tuple[str, str]]) -> Dict[str, Any]:
    agent_lines = [txt for spk, txt in turns if spk.lower() == "agent"]
    if not agent_lines:
        return {
            "category": "Soft Skills",
            "name": "Branding and Survey Check",
            "rating": "FAIL",
            "score": 0,
            "coaching": "No agent lines found in the transcript."
        }
        
    first_4 = " ".join(agent_lines[:4]).lower()
    last_4 = " ".join(agent_lines[-4:]).lower()
    
    greeting_match = "thank you for calling s-net" in first_4
    closing_match = "thank you for choosing s-net" in last_4

    if greeting_match and closing_match:
        return {
            "category": "Soft Skills",
            "name": "Branding and Survey Check",
            "rating": "PASS",
            "score": 100,
            "coaching": ""
        }
    else:
        missed = []
        if not greeting_match: missed.append("Greeting")
        if not closing_match: missed.append("Closing")
        return {
            "category": "Soft Skills",
            "name": "Branding and Survey Check",
            "rating": "FAIL",
            "score": 0,
            "deduction_value": 10,
            "coaching": f"Agent missed verbatim scripts for: {', '.join(missed)}"
        }

def evaluate_hold_and_dead_air(turns: List[Tuple[str, str]], parsed_times: List[Tuple[int, int]]) -> Dict[str, Any]:
    if not parsed_times or len(parsed_times) != len(turns) or all(not isinstance(t, tuple) for t in parsed_times):
        return {
            "category": "Soft Skills",
            "name": "Hold time and Dead Air",
            "rating": "PASS",
            "score": 100,
            "coaching": ""
        }
        
    dead_air_count = 0
    max_gap = 0
    
    for i in range(1, len(parsed_times)):
        prev_end = parsed_times[i-1][1]
        curr_start = parsed_times[i][0]
        
        if prev_end is not None and curr_start is not None:
            gap = curr_start - prev_end
            if gap > max_gap:
                max_gap = gap
            if gap > 30:
                dead_air_count += 1
                
    if dead_air_count >= 2:
        return {
            "category": "Soft Skills",
            "name": "Hold time and Dead Air",
            "rating": "FAIL",
            "score": 0,
            "deduction_value": 15,
            "coaching": f"Dead Air Breach: Agent had {dead_air_count} occurrences of >30s dead air (max gap {max_gap}s)."
        }
        
    return {
        "category": "Soft Skills",
        "name": "Hold time and Dead Air",
        "rating": "PASS",
        "score": 100,
        "coaching": ""
    }

def evaluate_verified_customer(turns: List[Tuple[str, str]], parsed_times: List[Tuple[int, int]]) -> Dict[str, Any]:
    agent_verified = False
    for i, (speaker, text) in enumerate(turns):
        if speaker.lower() == "agent":
            start_time = parsed_times[i][0] if i < len(parsed_times) and parsed_times[i] and parsed_times[i][0] is not None else 0
            if start_time <= 240:
                if re.search(r'\b(pin|address|security question)\b', text, re.IGNORECASE):
                    agent_verified = True
                    break
                    
    if agent_verified:
        return {
            "category": "Technical Knowledge",
            "name": "Verified customer",
            "rating": "PASS",
            "score": 100,
            "coaching": ""
        }
    else:
        return {
            "category": "Technical Knowledge",
            "name": "Verified customer",
            "rating": "FAIL",
            "score": 0,
            "deduction_value": 20,
            "coaching": "Agent failed to ask for a PIN, address, or security question within the first 4 minutes of the call."
        }

def evaluate_personalized_call(turns: List[Tuple[str, str]], customer_name: str) -> Dict[str, Any]:
    if not customer_name or customer_name.strip() == "":
        return {"category": "Soft Skills", "name": "Personalized the call/ticket appropriately", "rating": "PASS", "score": 100, "coaching": ""}
    
    name_lower = customer_name.lower().strip()
    for spk, txt in turns:
        if spk.lower() == "agent" and name_lower in txt.lower():
            return {"category": "Soft Skills", "name": "Personalized the call/ticket appropriately", "rating": "PASS", "score": 100, "coaching": ""}
            
    return {
        "category": "Soft Skills",
        "name": "Personalized the call/ticket appropriately",
        "rating": "FAIL",
        "score": 0,
        "deduction_value": 15,
        "coaching": f"Agent failed to use the customer's verified name '{customer_name}' during the call."
    }

# Two agent questions at least this similar (difflib ratio) are sent to the model as a possible repeat
AL_SIMILARITY_THRESHOLD = 0.70

def extract_active_listening_snippets(turns: List[Tuple[str, str]]) -> str:
    agent_questions = [(i, txt) for i, (spk, txt) in enumerate(turns) if spk.lower() == 'agent' and '?' in txt]
    snippets = []
    for idx1, (i1, q1) in enumerate(agent_questions):
        for idx2 in range(idx1 + 1, len(agent_questions)):
            i2, q2 = agent_questions[idx2]
            if difflib.SequenceMatcher(None, q1.lower(), q2.lower()).ratio() > AL_SIMILARITY_THRESHOLD:
                snippets.append(f"Turn {i1}: {q1}\n... Turn {i2}: {q2}")
    return "\n".join(snippets)

def _empathy_candidates(turns: List[Tuple[str, str]], sentiment_scores: List[float]) -> List[Tuple[int, float, float, str]]:
    """(turn index, sentiment score, biggest drop, snippet) for every unanswered negative customer turn, in call order."""
    candidates = []
    apology_keywords = ["sorry", "apologize", "understand", "frustrating", "apologies", "let me help"]

    for i, (speaker, text) in enumerate(turns):
        if speaker.lower() != 'customer' or not sentiment_scores or i >= len(sentiment_scores):
            continue
        score = sentiment_scores[i]
        drop = max((sentiment_scores[i-k] - score for k in (1, 2, 3) if i >= k), default=0.0)
        if score > -15.0 and drop < 8.0:
            continue

        agent_apologized = any(
            spk.lower() == 'agent' and any(kw in txt.lower() for kw in apology_keywords)
            for spk, txt in turns[i+1:i+4]
        )
        if not agent_apologized:
            snippet = f"Customer: {text}\n"
            for spk, txt in turns[i+1:i+5]:
                snippet += f"{spk}: {txt}\n"
            candidates.append((i, score, drop, snippet))
    return candidates

def extract_empathy_snippets(turns: List[Tuple[str, str]], sentiment_scores: List[float]) -> str:
    """All empathy snippets joined into one string (legacy form; the evaluator uses extract_empathy_snippet_list)."""
    return "\n---\n".join(c[3] for c in _empathy_candidates(turns, sentiment_scores))

def extract_empathy_snippet_list(turns: List[Tuple[str, str]], sentiment_scores: List[float], max_snippets: int = None) -> List[str]:
    """Empathy snippets most severe first (lowest sentiment, then biggest drop), without overlapping windows."""
    ranked = sorted(_empathy_candidates(turns, sentiment_scores), key=lambda c: (c[1], -c[2], c[0]))
    picked = []
    for idx, _, _, snippet in ranked:
        # a snippet covers its customer turn plus the next 4 turns, so starts within 4 turns overlap
        if all(abs(idx - p_idx) > 4 for p_idx, _ in picked):
            picked.append((idx, snippet))
        if max_snippets is not None and len(picked) >= max_snippets:
            break
    return [snippet for _, snippet in picked]

_PROBING_BOILERPLATE = [
    "how can i help", "how may i help", "how can i assist", "how are you",
    "account number", "pin", "name on the account", "verify", "date of birth", "security question",
    "is that right", "is that correct", "did i get that right",
    "anything else", "did that fix", "did that work", "did that help", "is it working now", "is that working",
    "have a good", "can i put you on hold", "may i place you on hold",
]
_PROBING_BOILERPLATE_RE = re.compile(r"\b(" + "|".join(re.escape(p) for p in _PROBING_BOILERPLATE) + r")\b", re.IGNORECASE)

def extract_probing_inputs(turns: List[Tuple[str, str]], customer_lines: List[str],
                           problem_max_words: int, questions_max_words: int) -> Tuple[str, List[str]]:
    """Customer problem text and agent questions for the probing check, each held to a word budget.

    Greeting, identity-check, confirmation and wrap-up questions are dropped first (the probing check
    ignores them anyway); if that leaves nothing, the unfiltered questions are used so the model still decides.
    """
    problem_text = " ".join(" ".join(customer_lines).split()[:problem_max_words])

    questions = [txt for spk, txt in turns if spk.lower() == "agent" and "?" in txt]
    candidates = [q for q in questions if not _PROBING_BOILERPLATE_RE.search(q)] or questions

    selected, used = [], 0
    for q in candidates:
        n = len(q.split())
        if used + n > questions_max_words:
            if not selected:
                selected.append(" ".join(q.split()[:questions_max_words]))
            break
        selected.append(q)
        used += n
    return problem_text, selected

def _agent_lines_with_ctx(turns):
    return [(i, txt) for i, (spk, txt) in enumerate(turns) if spk.lower() == "agent"]

def extract_ownership_snippets(turns: List[Tuple[str, str]]) -> str:
    patterns = [
        "not my department", "not my job", "not something i deal", "not something i handle",
        "that's not my", "thats not my", "i don't handle", "i dont handle",
        "call back", "another department", "another team", "different department",
        "wrong department", "other department", "nothing i can do", "can't do anything",
        "cant do anything", "you'd have to", "youd have to", "you would have to",
        "hope you get", "network team", "billing team", "provisioning team", "that's their",
        "not our problem", "not my problem", "contact them", "you'll have to ask",
    ]
    hits = []
    for i, txt in _agent_lines_with_ctx(turns):
        low = txt.lower()
        if any(p in low for p in patterns):
            hits.append(f"Agent: {txt}")
    return "\n".join(hits)

def extract_rapport_snippets(turns: List[Tuple[str, str]]) -> str:
    patterns = [
        "read the manual", "basic stuff", "obviously", "wasting my time", "waste of time",
        "calm down", "i already told you", "as i said", "like i said", "i just said",
        "don't be", "dont be", "how many times", "you should have", "if you'd", "if youd",
        "not that hard", "figure it out", "not rocket science", "that's a stupid",
        "thats a stupid", "are you serious", "seriously?", "what did you expect",
        "should have known", "it's not difficult", "its not difficult",
    ]
    hits = []
    for i, txt in _agent_lines_with_ctx(turns):
        low = txt.lower()
        if any(p in low for p in patterns):
            hits.append(f"Agent: {txt}")
    return "\n".join(hits)
