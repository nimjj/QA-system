"""Windows for "Confirmed the issue is resolved".

v2 sends the last 10 lines. In real-looking calls those are often mostly goodbyes ("Thanks, take care." / "Goodbye."), so the moment where the
agent says the issue is fixed and the customer agrees is not in the window. These variants differ only in WHICH lines are sent; the question
and the model are unchanged. Each returns a list of windows (one model call each) for the lab to compare against the v2 baseline.
"""
import math
import re
from typing import Callable, Dict, List, Tuple

from src.v3.candidates.common import cap_words, is_closing_line, role_lines
from src.v3.normalise import NCall

# the agent saying the fix worked / the matter is closed
_CUE = re.compile(r"\b(?:fixed|resolved|sorted|restored|working\s+(?:now|again|fine|properly)|back\s+(?:on|up|online)|is\s+working|all\s+(?:set|done)|"
                  r"completed|taken\s+care|anything\s+else|is\s+everything|has\s+it\s+(?:worked|fixed)|did\s+that\s+(?:work|fix))\b", re.I)


def _informative(call: NCall) -> Tuple[List[str], List[str]]:
    """(lines without pure pleasantries, the call's last two lines if they are pleasantries). The last two are kept at the end of the window so
    the model can still see how the call finished."""
    lines = role_lines(call)
    informative = [ln for t, ln in lines if not is_closing_line(t.text)]
    closers = [ln for t, ln in lines[-2:] if is_closing_line(t.text)]
    return informative, closers


def tail10(call: NCall) -> List[str]:
    """v2 behaviour: the last 10 lines."""
    return ["\n".join(ln for _, ln in role_lines(call)[-10:])]


def _informative_window(call: NCall, n_lines: int, max_words: int) -> List[str]:
    informative, closers = _informative(call)
    return ["\n".join(cap_words(informative[-n_lines:], max_words) + closers)]


def subst12(call: NCall) -> List[str]:
    """Last 12 informative lines (pleasantries skipped), at most 260 words, then the call's final pleasantries."""
    return _informative_window(call, 12, 260)


def subst16(call: NCall) -> List[str]:
    """Like subst12 but reaches 16 lines back, at most 320 words."""
    return _informative_window(call, 16, 320)


def cue(call: NCall) -> List[str]:
    """From two lines before the last agent line that sounds like a fix or close-out (searched in the last 40% of the call) to the end."""
    informative, closers = _informative(call)
    idx = None
    for i in range(len(informative) - 1, int(len(informative) * 0.6) - 1, -1):
        if informative[i].startswith("Agent:") and _CUE.search(informative[i]):
            idx = i
            break
    if idx is None:
        return subst12(call)
    return ["\n".join(cap_words(informative[max(0, idx - 2):], 300) + closers)]


def lab_tail300(call: NCall) -> List[str]:
    """The experimental time-based window already in laya_windows (last 300 s, backchannels dropped, at most 340 words), for comparison."""
    from src.services import laya_windows as W
    rl = role_lines(call)
    turns = [("Agent" if t.role == "agent" else "Customer", ln.split(": ", 1)[1]) for t, ln in rl]
    times = [(int(t.start), int(t.start) + 10) for t, _ in rl]
    return [W.resolved_tail(turns, times)]


def mood_usable(call: NCall) -> bool:
    """True when the call carries customer sentiment and at least four scored customer turns (fewer says nothing about 'typical')."""
    return call.sentiment_available and sum(1 for t in call.turns if t.role == "customer" and t.sentiment is not None) >= 4


def end_mood(call: NCall) -> float:
    """How the customer sounded at the end, relative to the rest of the call: mean sentiment of the last three customer turns minus the
    call's own median customer sentiment. 0.0 when the call carries no usable sentiment. Customer side only; no absolute scale is assumed."""
    s = [t.sentiment for t in call.turns if t.role == "customer" and t.sentiment is not None]
    if not mood_usable(call):
        return 0.0
    ordered = sorted(s)
    median = (ordered[len(s) // 2] + ordered[(len(s) - 1) // 2]) / 2
    return sum(s[-3:]) / 3 - median


def mood_score(call: NCall) -> float:
    """end_mood squeezed into 0..1 (0.5 = the customer ended as they spoke on average; above = happier). 10 sentiment points per logistic unit."""
    return 1.0 / (1.0 + math.exp(-end_mood(call) / 10.0))


def blended_score(model_p_pass: float, call: NCall, mood_weight: float) -> float:
    """The Resolved score the cutoff is applied to: the model's P(pass) alone when the call has no usable customer sentiment, otherwise
    (1 - w) * model + w * mood. Only the customer's own sentiment, only relative to that call."""
    if not mood_usable(call):
        return model_p_pass
    return (1.0 - mood_weight) * model_p_pass + mood_weight * mood_score(call)


VARIANTS: Dict[str, Callable[[NCall], List[str]]] = {"tail10": tail10, "tail300": lab_tail300, "subst12": subst12, "subst16": subst16, "cue": cue}
