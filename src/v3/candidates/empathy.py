"""Windows for "Empathy & Acknowledgment Statement".

v2 opens a window at the START of each stretch of customer lines whose sentiment is at or below a fixed -15 (or that contain a frustration
word) and shows the next four turns. Two weaknesses: a fixed number assumes the real sentiment scale, which we have not seen, and the first
line of a long complaint is often not the moment the customer is most upset, so the agent's actual reaction to the worst line falls outside the
window. These variants rank customer lines by how far they sit below THAT CALL's own typical sentiment (robust z-score, no absolute scale),
fall back to frustration words when the call has no usable sentiment, and anchor the window on the deepest line of each episode.
Customer-side sentiment only.
"""
from typing import Callable, Dict, List, Tuple

from src.services import laya_windows as W
from src.v3.candidates.common import role_lines
from src.v3.normalise import NCall

N_AFTER = 4
MAX_WINDOWS = 4
MIN_Z = 1.5            # how many "typical wobbles" below the call's median a line must sit to count as an outburst
MIN_SPREAD = 4.0       # floor for the wobble, so a flat, calm call does not turn small dips into outbursts
LINE_WORDS = 60


def _median(xs: List[float]) -> float:
    s = sorted(xs)
    n = len(s)
    return (s[n // 2] + s[(n - 1) // 2]) / 2


def _lines(call: NCall):
    """[(turn, speaker, text)] for agent/customer turns; the list index is the position used by the window."""
    return [(t, "Agent" if t.role == "agent" else "Customer", ln.split(": ", 1)[1]) for t, ln in role_lines(call)]


def _span(rows, start: int, n_after: int) -> str:
    return "\n".join(f"{spk}: {W._trim(txt, LINE_WORDS)}" for _, spk, txt in rows[start:start + 1 + n_after])


def v2episodes(call: NCall) -> List[str]:
    """v2 behaviour (flow v2): fixed -15 bar, window starts at the first line of each episode."""
    rows = _lines(call)
    turns = [(spk, txt) for _, spk, txt in rows]
    sent = [(t.sentiment if t.sentiment is not None else 0.0) for t, _, _ in rows]
    return W.empathy_episode_windows(turns, sent, n_after=4, calm_customer_turns=4)


def _depths(rows) -> Tuple[Dict[int, float], bool]:
    """position -> how far below the call's median customer sentiment (in robust spreads); True when sentiment was usable."""
    cust = [(i, t.sentiment) for i, (t, spk, _) in enumerate(rows) if spk == "Customer" and t.sentiment is not None]
    if len(cust) < 4 or not any(abs(s) > 1e-9 for _, s in cust):
        return {}, False
    vals = [s for _, s in cust]
    med = _median(vals)
    mad = _median([abs(v - med) for v in vals])
    spread = max(1.4826 * mad, MIN_SPREAD)
    return {i: (med - s) / spread for i, s in cust}, True


def _episodes(rows, trigger: Dict[int, bool], calm: int) -> List[List[int]]:
    """Group triggered customer positions into episodes: a new episode starts after `calm` customer turns without a trigger."""
    eps, cur, quiet = [], [], calm
    for i, (_, spk, _) in enumerate(rows):
        if spk != "Customer":
            continue
        if trigger.get(i):
            if cur and quiet >= calm:
                eps.append(cur)
                cur = []
            cur.append(i)
            quiet = 0
        else:
            quiet += 1
    if cur:
        eps.append(cur)
    return eps


def _anchors(rows, anchor_deepest: bool, calm: int = 2) -> List[int]:
    """Positions (in `rows`) where the windows start: one per episode of triggered customer lines, at most MAX_WINDOWS (deepest episodes kept),
    in call order. Trigger = at least MIN_Z spreads below the call's median sentiment, or a frustration word on a line below the median; with no
    usable sentiment, a frustration word alone."""
    depth, usable = _depths(rows)
    trigger = {}
    for i, (_, spk, txt) in enumerate(rows):
        if spk != "Customer":
            continue
        lexical = bool(W._FRUSTRATION_RE.search(txt))
        d = depth.get(i)
        trigger[i] = ((d is not None and d >= MIN_Z) or (lexical and d is not None and d > 0)) if usable else lexical
    found = []
    for ep in _episodes(rows, trigger, calm):
        anchor = max(ep, key=lambda i: (depth.get(i, 0.0), -i)) if (usable and anchor_deepest) else ep[0]
        found.append((max((depth.get(i, 0.0) for i in ep), default=0.0), ep[0], anchor))
    if len(found) > MAX_WINDOWS:
        found = sorted(sorted(found, key=lambda f: -f[0])[:MAX_WINDOWS], key=lambda f: f[1])
    return [anchor for _, _, anchor in found]


def rel_first(call: NCall) -> List[str]:
    """Relative trigger (call-median based), window at the first line of each episode."""
    rows = _lines(call)
    return [_span(rows, i, N_AFTER) for i in _anchors(rows, anchor_deepest=False)]


def rel_deep(call: NCall) -> List[str]:
    """Relative trigger, window anchored on the deepest line of each episode."""
    rows = _lines(call)
    return [_span(rows, i, N_AFTER) for i in _anchors(rows, anchor_deepest=True)]


def covered_source_turns(call: NCall, variant: str) -> List[Tuple[int, int]]:
    """(first, last) turn numbers in the caller's own list covered by each window of a variant, for the gate-recall check against the keys' markers."""
    rows = _lines(call)
    if variant == "v2episodes":
        turns = [(spk, txt) for _, spk, txt in rows]
        sent = [(t.sentiment if t.sentiment is not None else 0.0) for t, _, _ in rows]
        starts = W.outburst_starts(turns, sent, 4, 6, False)
        if len(starts) > MAX_WINDOWS:
            starts = starts[:MAX_WINDOWS - 1] + starts[-1:]
    else:
        starts = _anchors(rows, anchor_deepest=(variant == "rel_deep"))
    return [(rows[i][0].source_index, rows[min(len(rows) - 1, i + N_AFTER)][0].source_index) for i in starts]


VARIANTS: Dict[str, Callable[[NCall], List[str]]] = {"v2episodes": v2episodes, "rel_first": rel_first, "rel_deep": rel_deep}
