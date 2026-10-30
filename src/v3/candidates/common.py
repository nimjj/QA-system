"""Shared helpers for the window candidates: the call as "Agent: ..." / "Customer: ..." lines, in the shape the model was trained on."""
import re
from typing import List, Optional, Tuple

from src.v3.normalise import NCall, NTurn
from src.v3.text import add_question_marks


def role_lines(call: NCall) -> List[Tuple[NTurn, str]]:
    """(turn, "Agent: text") for agent and customer turns only; IVR and other speakers are left out. Bare questions get their '?'."""
    out = []
    for t in call.turns:
        if t.role == "agent":
            out.append((t, f"Agent: {add_question_marks(t.text)}"))
        elif t.role == "customer":
            out.append((t, f"Customer: {t.text}"))
    return out


def words(s: str) -> int:
    return len(s.split())


def cap_words(lines: List[str], max_words: int) -> List[str]:
    """Keep the LAST lines that fit in max_words (a window is read from its end backwards, the end matters most)."""
    kept, total = [], 0
    for ln in reversed(lines):
        w = words(ln)
        if kept and total + w > max_words:
            break
        kept.append(ln)
        total += w
    return list(reversed(kept))


# a line is a pure pleasantry when it is short, has a thanks/goodbye/good-wishes word and says nothing about the problem or the fix
_CLOSING_WORDS = re.compile(r"\b(?:bye|goodbye|good\s?bye|thanks?|thank\s+you|take\s+care|welcome|pleasure|cheers|have\s+a|you\s+too|speak\s+soon|best\s+of\s+luck|all\s+the\s+best|"
                            r"for\s+(?:calling|choosing|contacting))\b", re.I)
_INFO_WORDS = re.compile(r"\b(?:fixed|resolved|working|works|sorted|restored|back\s+(?:on|up|online)|anything\s+else|still|issue|problem|error|"
                         r"refund|credit|ticket|appointment|engineer|reference|confirm|everything|all\s+set|complete[d]?)\b", re.I)


def is_closing_line(text: str) -> bool:
    """True for pure pleasantries ("Thanks Craig, take care.", "Goodbye."). Anything that mentions the problem or the fix is kept."""
    t = text.strip()
    if not t or len(t.split()) > 14:
        return False
    if _INFO_WORDS.search(t):
        return False
    return bool(_CLOSING_WORDS.search(t))


def last_index_where(items: List[str], pred) -> Optional[int]:
    for i in range(len(items) - 1, -1, -1):
        if pred(items[i]):
            return i
    return None
