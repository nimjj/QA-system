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

# A gap after an announced hold, or one the agent closes by thanking the customer for holding, is a managed
# hold rather than dead air, up to HOLD_MAX_EXEMPT_SEC. A bare "hold on" is not an announcement.
HOLD_MAX_EXEMPT_SEC = 120
_HOLD_ANNOUNCE_RE = re.compile(
    r"\b(place|put) you on (a )?(brief |short |quick )?hold\b|\bbear with me\b"
    r"|\b(one|a) moment while\b|\bgive me (a|one) (moment|minute|second|sec) while\b",
    re.IGNORECASE)
_HOLD_RETURN_RE = re.compile(
    r"\bthank(s| you)( so much)? for (holding|waiting|your patience|bearing with me)\b|\bsorry for the wait\b",
    re.IGNORECASE)
_CUSTOMER_CHASING_RE = re.compile(r"\bhello\?|\b(are )?you still there\b|\banyone there\b", re.IGNORECASE)

def _is_managed_hold(turns: List[Tuple[str, str]], i: int, gap: int) -> bool:
    """True when the gap before turn i is an announced or acknowledged hold (turn i-1 -> turn i)."""
    if gap > HOLD_MAX_EXEMPT_SEC:
        return False
    prev_spk, prev_txt = turns[i - 1]
    spk, txt = turns[i]
    if spk.lower() == "customer" and _CUSTOMER_CHASING_RE.search(txt):
        return False
    return ((spk.lower() == "agent" and bool(_HOLD_RETURN_RE.search(txt)))
            or (prev_spk.lower() == "agent" and bool(_HOLD_ANNOUNCE_RE.search(prev_txt))))

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
            if gap > 30 and _is_managed_hold(turns, i, gap):
                continue
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

def question_sentences(text: str) -> List[str]:
    """The sentences of a turn that ask something, without the statements around them."""
    return [s.strip() for s in re.split(r"(?<=[.!?])\s+", text) if "?" in s]

# Two agent questions at least this similar (difflib ratio) are sent to the model as a possible repeat
AL_SIMILARITY_THRESHOLD = 0.55
AL_MAX_PAIRS = 3             # strongest pairs per call, so the snippet stays well inside the model window
AL_ANSWER_MAX_WORDS = 40
# Short check-ins and confirmations are asked many times in a normal call and are not repeats
_AL_IGNORE_RE = re.compile(
    r"\b(is that right|is that correct|did i get that right|does that make sense|anything else|still there"
    r"|still with me|can you hear me|are you there|how can i help|how are you)\b", re.IGNORECASE)
# The customer pointing out they already answered
_ALREADY_ANSWERED_RE = re.compile(
    r"\b(like i said|as i said|i already (said|told you|mentioned|answered)|i told you|i mentioned|i just said"
    r"|you already asked)\b", re.IGNORECASE)

def _similarity(a: str, b: str) -> float:
    return difflib.SequenceMatcher(None, a.lower(), b.lower()).ratio()

def _customer_answer(turns: List[Tuple[str, str]], after: int, before: int) -> str:
    """The first customer turn between turn `after` and turn `before`, cut to AL_ANSWER_MAX_WORDS words."""
    for spk, txt in turns[after + 1:before]:
        if spk.lower() == 'customer':
            return " ".join(txt.split()[:AL_ANSWER_MAX_WORDS])
    return ""

def extract_active_listening_snippets(turns: List[Tuple[str, str]]) -> str:
    """Possible repeated agent questions for the model to judge, as: first question, the customer's answer, second question.

    Two sources: question sentences more similar than AL_SIMILARITY_THRESHOLD, and agent questions the customer
    answers with "like I said" / "I mentioned", paired with the most similar earlier question. The customer's
    "like I said" reply itself is NOT sent: it made the model read the pair as a status re-check. Pairs where the
    customer complained come first, then the most similar; at most AL_MAX_PAIRS are sent.
    """
    agent_questions = [(i, q) for i, (spk, txt) in enumerate(turns) if spk.lower() == 'agent'
                       for q in question_sentences(txt) if len(q.split()) >= 4 and not _AL_IGNORE_RE.search(q)]
    pairs = {}  # (earlier turn, later turn) -> (complained, similarity, q1, q2)
    for idx1, (i1, q1) in enumerate(agent_questions):
        for i2, q2 in agent_questions[idx1 + 1:]:
            if i2 == i1:
                continue
            sim = _similarity(q1, q2)
            if sim > AL_SIMILARITY_THRESHOLD and sim > pairs.get((i1, i2), (0, 0))[1]:
                pairs[(i1, i2)] = (0, sim, q1, q2)

    for j, (spk, txt) in enumerate(turns):
        if spk.lower() != 'customer' or not _ALREADY_ANSWERED_RE.search(txt):
            continue
        asked = next((i for i in range(j - 1, -1, -1) if turns[i][0].lower() == 'agent'), None)
        asked_qs = question_sentences(turns[asked][1]) if asked is not None else []
        if not asked_qs:
            continue
        q2 = asked_qs[-1]
        earlier = [(i, q) for i, q in agent_questions if i < asked]
        if not earlier:
            continue
        i1, q1 = max(earlier, key=lambda iq: _similarity(iq[1], q2))
        pairs[(i1, asked)] = (1, _similarity(q1, q2), q1, q2)

    ranked = sorted(pairs.items(), key=lambda kv: (-kv[1][0], -kv[1][1], kv[0]))[:AL_MAX_PAIRS]
    blocks = []
    for (i1, i2), (_, _, q1, q2) in ranked:
        answer = _customer_answer(turns, i1, i2)
        blocks.append(f"Turn {i1} Agent asked: {q1}\n"
                      + (f"Customer answered: {answer}\n" if answer else "")
                      + f"Turn {i2} Agent later asked: {q2}")
    return "\n\n".join(blocks)

# Customer words that signal frustration even when the sentiment score barely moves
_FRUSTRATION_RE = re.compile(
    r"\b(frustrat\w*|annoy\w*|ridiculous|nightmare|unbelievable|fed up|sick of|embarrass\w*|stress\w*|worried"
    r"|third time|again and again)\b", re.IGNORECASE)

def _empathy_candidates(turns: List[Tuple[str, str]], sentiment_scores: List[float]) -> List[Tuple[int, float, float, str]]:
    """(turn index, sentiment score, biggest drop, snippet) for every unanswered negative customer turn, in call order.

    A drop is measured against the customer's own previous 3 turns; agent turns usually score higher and would
    make nearly every customer turn look like a drop.
    """
    candidates = []
    apology_keywords = ["sorry", "apologize", "understand", "frustrating", "apologies", "let me help"]
    customer_scores = []

    for i, (speaker, text) in enumerate(turns):
        if speaker.lower() != 'customer' or not sentiment_scores or i >= len(sentiment_scores):
            continue
        score = sentiment_scores[i]
        drop = max((prev - score for prev in customer_scores[-3:]), default=0.0)
        customer_scores.append(score)
        upset_words = score < 0 and bool(_FRUSTRATION_RE.search(text))
        if score > -15.0 and drop < 8.0 and not upset_words:
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
    "pleasure of speaking", "who am i speaking", "who do i have", "service address", "confirm the address",
    "what's going on with the service", "what's going on with your service", "what's going on today",
    "what can i do for you", "what's the issue", "what seems to be",
    "do you mind if i ask", "can i ask you a few", "still there", "still with me", "can you hear me",
]
_PROBING_BOILERPLATE_RE = re.compile(r"\b(" + "|".join(re.escape(p) for p in _PROBING_BOILERPLATE) + r")\b", re.IGNORECASE)

def extract_probing_inputs(turns: List[Tuple[str, str]], customer_lines: List[str],
                           problem_max_words: int, questions_max_words: int) -> Tuple[str, List[str]]:
    """Customer problem text and agent questions for the probing check, each held to a word budget.

    Only the question sentences of each agent turn are used. Greeting, identity-check, confirmation and wrap-up
    questions are dropped first (the probing check ignores them anyway); if that leaves nothing, the unfiltered
    questions are used so the model still decides.
    """
    problem_text = " ".join(" ".join(customer_lines).split()[:problem_max_words])

    questions = [q for spk, txt in turns if spk.lower() == "agent" for q in question_sentences(txt)]
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

_AGENT_SETUP_RE = re.compile(
    r"\b(thank you for calling|account number|pin|verify|verified|verification|name on the account|address"
    r"|date of birth|security question)\b", re.IGNORECASE)
_CUSTOMER_DETAILS_RE = re.compile(r"\b(pin|account number)\b|\d{4,}|\d+-\d+", re.IGNORECASE)

def without_setup_lines(agent_lines: List[str]) -> List[str]:
    """Agent lines minus the greeting and identity-verification turns."""
    return [txt for txt in agent_lines if not _AGENT_SETUP_RE.search(txt)]

def without_detail_answers(customer_lines: List[str]) -> List[str]:
    """Customer lines minus the turns that only give account details (account number, PIN, a short address)."""
    return [txt for txt in customer_lines
            if not _CUSTOMER_DETAILS_RE.search(txt) and not (len(txt.split()) < 9 and re.search(r"\d", txt))]

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
    """Legacy phrase-gated rapport input. No longer used by the evaluator (see extract_rapport_chunks); kept for the
    old benchmark in laya-test/qa_eval, which builds its gold set from it."""
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

# Every agent line is checked for rudeness, in consecutive chunks. A phrase gate let any rude line without a listed
# phrase skip the model entirely, which training cannot fix. One rude chunk fails the item.
RAPPORT_CHUNK_MAX_LINES = 8
RAPPORT_CHUNK_MAX_WORDS = 120

def extract_rapport_chunks(turns: List[Tuple[str, str]], max_lines: int = RAPPORT_CHUNK_MAX_LINES,
                           max_words: int = RAPPORT_CHUNK_MAX_WORDS) -> List[str]:
    """All agent lines in order, grouped into chunks of at most max_lines lines and max_words words (a single
    longer line forms its own chunk). Each chunk is "Agent: ..." lines, one per line."""
    chunks, current, words = [], [], 0
    for spk, txt in turns:
        if spk.lower() != "agent" or not txt.strip():
            continue
        n = len(txt.split())
        if current and (len(current) >= max_lines or words + n > max_words):
            chunks.append("\n".join(current))
            current, words = [], 0
        current.append(f"Agent: {txt}")
        words += n
    if current:
        chunks.append("\n".join(current))
    return chunks
