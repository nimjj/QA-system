"""Windows for "Paraphrasing" (did the agent restate the customer's problem back to them?).

v2 only looks for a restatement cue phrase ("so you're saying...", "just to confirm...") in agent lines during the first 300 seconds, and
FAILS the item without asking the model when it finds none. Real agents restate in many wordings and at any point. The variants widen WHERE and
HOW a candidate is found; the model still decides whether the candidate really is a restatement, so the window format is v2's.
"""
import re
from typing import Callable, Dict, List, Optional

from src.services import laya_windows as W
from src.v3.candidates.common import role_lines
from src.v3.normalise import NCall, NTurn

_AFFIRM = re.compile(r"^\W*(?:yes|yeah|yep|yup|right|exactly|correct|precisely|absolutely|that'?s (?:right|correct|it|exactly)|spot on|that is (?:right|correct|it))\b", re.I)
MAX_AGENT_LINES = 2


def _trim(text: str, n: int) -> str:
    w = text.split()
    return text if len(w) <= n else " ".join(w[:n]) + " ..."


def _problem_statement(call: NCall) -> Optional[NTurn]:
    cust = [t for t in call.turns if t.role == "customer"]
    return next((t for t in cust if len(t.text.split()) >= 12), cust[0] if cust else None)


def _window(problem: NTurn, agent_turns: List[NTurn]) -> List[str]:
    if not agent_turns:
        return []
    return [f"CUSTOMER: {_trim(problem.text, 80)}\nAGENT: {' '.join(_trim(t.text, 60) for t in agent_turns[:MAX_AGENT_LINES])}"]


def v2cue(call: NCall) -> List[str]:
    """v2 behaviour: a cue phrase in an agent line within the first 300 s."""
    problem = _problem_statement(call)
    if problem is None:
        return []
    cands = [t for t in call.turns if t.role == "agent" and t.start <= 300 and W._PARAPHRASE_CUE.search(t.text)]
    return _window(problem, cands)


def cue_any(call: NCall) -> List[str]:
    """The same cue phrases, but anywhere after the customer has stated the problem."""
    problem = _problem_statement(call)
    if problem is None:
        return []
    cands = [t for t in call.turns if t.role == "agent" and t.index > problem.index and W._PARAPHRASE_CUE.search(t.text)]
    return _window(problem, cands)


def _overlaps_problem(agent_text: str, problem_text: str, need: int = 2) -> bool:
    return len(W._content_words(agent_text) & W._content_words(problem_text)) >= need


def cue_aff(call: NCall) -> List[str]:
    """cue_any, plus an agent line that the customer answers with a plain agreement ("yes", "exactly") and that reuses the customer's own
    words. Customers agree after a restatement far more often than after other agent lines."""
    problem = _problem_statement(call)
    if problem is None:
        return []
    turns = call.turns
    cands = []
    for k, t in enumerate(turns):
        if t.role != "agent" or t.index <= problem.index:
            continue
        cue = bool(W._PARAPHRASE_CUE.search(t.text))
        nxt = next((u for u in turns[k + 1:k + 3] if u.role == "customer"), None)
        affirmed = (nxt is not None and bool(_AFFIRM.match(nxt.text)) and len(t.text.split()) >= 8
                    and _overlaps_problem(t.text, problem.text))
        if cue or affirmed:
            cands.append(t)
    return _window(problem, cands)


# ------------------------------------------------------------------ context windows
# v2 (and the variants above) pair every candidate with the customer's FIRST long line. A restatement usually sums up what the customer said
# just before it ("So the phone prompted you yesterday and rejected the password, have I got that right?"), which the opening line may not
# mention at all, so the model rightly answers "no". The _ctx variants pair each candidate with the customer lines just before it instead.
CTX_CUSTOMER_TURNS = 3
CTX_CUSTOMER_WORDS = 80
MAX_CTX_WINDOWS = 3


def _context_window(call: NCall, cand: NTurn) -> Optional[str]:
    """'CUSTOMER: <the customer lines just before cand>\\nAGENT: <cand>'. Backchannels ("okay", "yes thanks") are skipped. None when no
    customer has spoken yet."""
    before = [t for t in call.turns if t.role == "customer" and t.index < cand.index and len(t.text.split()) > W.BACKCHANNEL_MAX_WORDS]
    kept, total = [], 0
    for t in reversed(before[-CTX_CUSTOMER_TURNS:]):
        n = len(t.text.split())
        if kept and total + n > CTX_CUSTOMER_WORDS:
            break
        kept.append(t.text)
        total += n
    if not kept:
        return None
    return f"CUSTOMER: {_trim(' '.join(reversed(kept)), CTX_CUSTOMER_WORDS)}\nAGENT: {_trim(cand.text, 60)}"


def _ctx_windows(call: NCall, cands: List[NTurn]) -> List[str]:
    out = []
    for t in cands:
        w = _context_window(call, t)
        if w:
            out.append(w)
        if len(out) >= MAX_CTX_WINDOWS:
            break
    return out


def v2cue_ctx(call: NCall) -> List[str]:
    """v2's candidates (a cue phrase within the first 300 s), each in its own window with the customer lines just before it."""
    return _ctx_windows(call, [t for t in call.turns if t.role == "agent" and t.start <= 300 and W._PARAPHRASE_CUE.search(t.text)])


def cue_any_ctx(call: NCall) -> List[str]:
    """cue_any's candidates (a cue phrase anywhere after the customer has spoken), each with the customer lines just before it."""
    return _ctx_windows(call, [t for t in call.turns if t.role == "agent" and W._PARAPHRASE_CUE.search(t.text)])


VARIANTS: Dict[str, Callable[[NCall], List[str]]] = {"v2cue": v2cue, "cue_any": cue_any, "cue_aff": cue_aff,
                                                     "v2cue_ctx": v2cue_ctx, "cue_any_ctx": cue_any_ctx}
