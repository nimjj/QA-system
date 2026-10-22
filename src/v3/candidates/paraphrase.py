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


VARIANTS: Dict[str, Callable[[NCall], List[str]]] = {"v2cue": v2cue, "cue_any": cue_any, "cue_aff": cue_aff}
