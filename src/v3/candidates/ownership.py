"""Windows for "Took ownership of the problem" (FAIL when the agent deflects, blames someone else or refuses to help).

v2 opens a window only when an agent line contains one of a fixed list of phrases; on calls written by other authors it opened none for most
of the real deflections ("...is Telstra's responsibility, not ours", "...so that's essentially Netflix's problem, not S-Net's"), and a call
with no window is PASSED without asking the model. The wide gate adds the wording families below. It only decides WHICH agent lines the
model reads (same agent-only format, same question): the model still decides whether a line is a deflection.
"""
import re
from typing import Callable, Dict, List

from src.services import laya_windows as W
from src.v3.candidates.common import role_lines
from src.v3.normalise import NCall

MAX_LINES = 6
MAX_LINE_WORDS = 70

_WIDE = re.compile(
    # disowning: "not ours", "not S-Net's responsibility", "X's problem / fault / policy", "responsibility of / for"
    r"\bnot\s+(?:ours|mine|on\s+us|s-?\s?net'?s|our\s+(?:side|end|remit|area))\b"
    r"|\b(?:isn'?t|is\s+not|aren'?t|are\s+not|wasn'?t|not)\s+(?:s-?\s?net'?s|our|my)\s+\w*\s?(?:responsibility|problem|fault|job|issue|doing)\b"
    r"|\b\w+'s\s+(?:problem|fault|responsibility|policy|issue|job|call)\b"
    r"|\bresponsib(?:le|ility)\s+(?:of|for|lies)\b|\bhandled\s+by\s+(?:them|another|a\s+third)\b"
    r"|\b(?:third[\s-]party|another\s+company|the\s+provider|the\s+landlord|the\s+manufacturer|the\s+regulator)\b.{0,60}\b(?:problem|fault|responsib|control|handle)"
    # can't / won't / refuse
    r"|\b(?:can(?:'?t|not)|unable\s+to|not\s+able\s+to|not\s+allowed\s+to|not\s+permitted\s+to|won'?t\s+be\s+able\s+to|no\s+way\s+(?:for\s+me\s+)?to)\s+"
    r"(?:fix|help|do\s+anything|override|change|waive|refund|expedite|escalate|speed|intervene|look\s+into|resolve|assist|touch)\b"
    r"|\b(?:out\s+of\s+(?:my|our)\s+hands|outside\s+(?:of\s+)?(?:my|our)\s+(?:control|remit|scope)|beyond\s+(?:my|our)\s+(?:control|remit|scope)|"
    r"not\s+within\s+(?:my|our)|above\s+my\s+pay|nothing\s+(?:more\s+)?(?:i|we)\s+can\s+do|there'?s\s+nothing\s+(?:i|we|s-?net)\s+can)\b"
    r"|\b(?:i\s+(?:refuse|decline)|we\s+(?:refuse|decline)|policy\s+(?:doesn'?t|does\s+not|says\s+no|won'?t)|against\s+(?:our\s+)?policy)\b"
    r"|\b(?:wait|waiting)\s+(?:for\s+)?(?:up\s+to\s+)?\d+\s+(?:working\s+|business\s+)?(?:days|weeks)\b"
    # bureaucratic refusals: "cannot be performed", "can only be done after", "do not take calls", "you must wait"
    r"|\b(?:cannot|can'?t|can\s+not|won'?t|will\s+not)\s+be\s+(?:\w+ed|done|made|given|issued|changed|waived|reversed|overridden|performed)\b"
    r"|\b(?:can|will|could)\s+only\s+be\s+\w+\s+(?:after|once|when|if|by)\b"
    r"|\b(?:do|does|don'?t|doesn'?t)\s+(?:not\s+)?(?:take|accept|handle|deal\s+with|cover|offer|provide|answer)\s+(?:any\s+)?(?:incoming\s+|customer\s+|direct\s+)?(?:calls?|requests?|queries|complaints?|phone\s+calls?|that|those|this)\b"
    r"|\byou\s+(?:must|will\s+have\s+to|have\s+to|need\s+to)\s+(?:wait|pay|accept|live\s+with|just)\b"
    # blaming the customer
    r"|\byour\s+(?:own\s+)?(?:fault|responsibility|equipment|router|setup|side|end|mistake|wiring|device|microphone|headset)\b.{0,40}\b(?:problem|cause|reason|fault|issue|broken|wrong)"
    r"|\b(?:that'?s|that\s+is|this\s+is|it'?s)\s+(?:on\s+you|your\s+(?:fault|problem|responsibility))\b|\byou\s+(?:should\s+have|shouldn'?t\s+have|must\s+have|ought\s+to\s+have)\b"
    # sending the customer away
    r"|\b(?:go|drive|head|travel|walk|take\s+it)\s+(?:down\s+)?to\s+(?:a|the|your|an?\s+\w+)\s+(?:local\s+)?(?:store|shop|branch|retail|office)\b"
    r"|\b(?:you\s+(?:will|'ll|would|need\s+to|have\s+to|must|should)|please)\s+(?:need\s+to\s+|have\s+to\s+)?(?:contact|call|ring|speak\s+to|get\s+in\s+touch\s+with|reach\s+out\s+to|take\s+it\s+up\s+with|ask)\s+"
    r"(?:the|your|an?|their|them)\b",
    re.I)


def _agent_lines(call: NCall):
    return [(t, ln) for t, ln in role_lines(call) if t.role == "agent"]


def v2gate(call: NCall) -> List[str]:
    """v2 behaviour: the old phrase list and regex."""
    turns = [("Agent" if t.role == "agent" else "Customer", ln.split(": ", 1)[1]) for t, ln in role_lines(call)]
    text = W.ownership_candidates(turns, MAX_LINES)
    return [text] if text else []


def _trim(text: str) -> str:
    w = text.split()
    return text if len(w) <= MAX_LINE_WORDS else " ".join(w[:MAX_LINE_WORDS]) + " ..."


def wide(call: NCall) -> List[str]:
    """v2's gate OR the wider wording families. At most six agent lines, in call order."""
    hits = []
    for t, ln in _agent_lines(call):
        low = t.text.lower()
        if any(p in low for p in W._OWNERSHIP_PHRASES) or W._OWNERSHIP_RE.search(t.text) or _WIDE.search(t.text):
            hits.append(f"Agent: {_trim(t.text)}")
    return ["\n".join(hits[:MAX_LINES])] if hits else []


VARIANTS: Dict[str, Callable[[NCall], List[str]]] = {"v2gate": v2gate, "wide": wide}
