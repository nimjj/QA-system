"""Input layer: turn whatever the caller sent into one clean, validated list of turns.

Fixes found in the audit: null or fractional start times, null sentiment, an `end_time` that the API model used to drop (every turn was
assumed to last 10 s), speaker labels other than Agent/Customer ("Rep", "IVR", "Agent 2"), "[hh:mm:ss]" stamps read as minutes, and
no limit on input size. Nothing here loads a model.
"""
import math
import re
from dataclasses import dataclass, field
from typing import Any, List, Optional, Union

from src.v3 import load_config


class InvalidTranscript(ValueError):
    """The transcript cannot be graded (HTTP 422)."""


class TranscriptTooLarge(ValueError):
    """The transcript exceeds a configured limit (HTTP 413)."""


@dataclass
class NTurn:
    index: int                     # position in the normalised list
    role: str                      # "agent" | "customer" | "other"
    speaker: str                   # the original label
    text: str
    start: float                   # seconds from the start of the call
    end: float                     # seconds; estimated from the word count when the input has none
    end_estimated: bool
    sentiment: Optional[float]     # None when the input has no usable score (customer turns only; agents never carry one)


@dataclass
class NCall:
    turns: List[NTurn]
    customer_name: str = ""
    sentiment_available: bool = False
    warnings: List[str] = field(default_factory=list)

    def role_turns(self, role: str) -> List[NTurn]:
        return [t for t in self.turns if t.role == role]


_TS_RE = re.compile(r"^\s*[\[\(]?\s*(\d{1,2}):(\d{2})(?::(\d{2}))?(?:[.,](\d+))?\s*[\]\)]?\s*$")
_LINE_RE = re.compile(r"^\s*(?:[\[\(]\s*(\d{1,2}:\d{2}(?::\d{2})?(?:[.,]\d+)?)\s*[\]\)]\s*)?([^:\n]{1,40}?)\s*:\s*(.+)$")


def parse_seconds(value: Any) -> Optional[float]:
    """Seconds from an int, a float, "75", "1:15", "[01:15]" or "[1:02:03]". None when it cannot be read."""
    if value is None or isinstance(value, bool):
        return None
    if isinstance(value, (int, float)):
        return float(value) if math.isfinite(value) and value >= 0 else None
    s = str(value).strip()
    try:
        v = float(s)
        return v if math.isfinite(v) and v >= 0 else None
    except ValueError:
        pass
    m = _TS_RE.match(s)
    if not m:
        return None
    a, b, c, frac = m.groups()
    secs = int(a) * 60 + int(b) if c is None else int(a) * 3600 + int(b) * 60 + int(c)
    return secs + (float("0." + frac) if frac else 0.0)


def classify_role(label: str, roles: Optional[dict] = None) -> str:
    """Map a speaker label to agent / customer / other. "Agent 2", "Rep-3" and "Customer (Mr Smith)" resolve by their first word."""
    roles = roles or load_config()["roles"]
    first = re.split(r"[\s_\-(:/#]+", (label or "").strip().lower())[0] if (label or "").strip() else ""
    first = re.sub(r"\d+$", "", first)
    for role in ("other", "agent", "customer"):
        if first in roles[role]:
            return role
    return "other"


def _estimate_end(start: float, text: str, seconds_per_word: float) -> float:
    return start + max(1.0, len(text.split()) * seconds_per_word)


def _clean_sentiment(value: Any) -> Optional[float]:
    if value is None or isinstance(value, bool):
        return None
    try:
        v = float(value)
    except (TypeError, ValueError):
        return None
    return v if math.isfinite(v) else None


def _from_string(text: str) -> List[dict]:
    """"[00:09] Agent: hello" lines (stamps may also be concatenated on one line) -> raw turn dicts."""
    pre = re.sub(r"(\s*)([\[\(]\s*\d{1,2}:\d{2}(?::\d{2})?\s*[\]\)])", r"\n\2", text.strip())
    out = []
    for raw_line in pre.splitlines():
        line = raw_line.strip()
        if not line:
            continue
        m = _LINE_RE.match(line)
        if not m:
            if out:                                   # a wrapped line belongs to the previous turn
                out[-1]["text"] += " " + line
            continue
        stamp, spk, body = m.groups()
        out.append({"speaker": spk.strip(), "text": body.strip(), "start_time": stamp})
    return out


def normalise(transcript: Union[str, List[Any]], customer_name: Optional[str] = None, config: Optional[dict] = None) -> NCall:
    """Validate and normalise a transcript (list of turn dicts, objects with the same attributes, or a text block)."""
    cfg = config or load_config()
    lim = cfg["limits"]
    if isinstance(transcript, str):
        raw_turns = _from_string(transcript)
    elif isinstance(transcript, list):
        raw_turns = []
        for t in transcript:
            if hasattr(t, "model_dump"):
                t = t.model_dump()
            elif hasattr(t, "dict") and not isinstance(t, dict):
                t = t.dict()
            if not isinstance(t, dict):
                raise InvalidTranscript("every transcript turn must be an object with speaker and text")
            raw_turns.append(t)
    else:
        raise InvalidTranscript("transcript must be a list of turns or a text block")
    if not raw_turns:
        raise InvalidTranscript("the transcript has no turns")
    if len(raw_turns) > lim["max_turns"]:
        raise TranscriptTooLarge(f"{len(raw_turns)} turns; the limit is {lim['max_turns']}")

    total_chars, turns, warnings = 0, [], []
    prev_start, prev_end = 0.0, 0.0
    sec_per_word = cfg["speech_seconds_per_word"]
    for raw in raw_turns:
        text = raw.get("text")
        text = "" if text is None else str(text).strip()
        if len(text) > lim["max_chars_per_turn"]:
            raise TranscriptTooLarge(f"a turn has {len(text)} characters; the limit is {lim['max_chars_per_turn']}")
        total_chars += len(text)
        if total_chars > lim["max_total_chars"]:
            raise TranscriptTooLarge(f"the transcript exceeds {lim['max_total_chars']} characters")
        if not text:
            continue                                            # an empty turn carries nothing to grade
        start = parse_seconds(raw.get("start_time_sec"))
        if start is None:
            start = parse_seconds(raw.get("start_time"))
        if start is None:
            start = prev_end                                   # no usable time: assume it follows the previous turn directly
            warnings.append("a turn had no readable start time")
        if start > lim["max_call_seconds"]:
            raise InvalidTranscript(f"a start time of {start:.0f}s is beyond the {lim['max_call_seconds']}s limit")
        start = max(start, 0.0)
        end = parse_seconds(raw.get("end_time_sec"))
        if end is None:
            end = parse_seconds(raw.get("end_time"))
        estimated = end is None or end < start
        if estimated:
            end = _estimate_end(start, text, sec_per_word)
        label = str(raw.get("speaker") or "")
        role = classify_role(label, cfg["roles"])
        sent = _clean_sentiment(raw.get("sentiment_score")) if role == "customer" else None
        turns.append(NTurn(index=len(turns), role=role, speaker=label, text=text, start=start, end=end, end_estimated=estimated, sentiment=sent))
        prev_start, prev_end = start, end
    if not turns:
        raise InvalidTranscript("the transcript has no text")
    if not any(t.role == "agent" for t in turns):
        warnings.append("no agent turns were recognised; check the speaker labels")
    cust = [t.sentiment for t in turns if t.role == "customer"]
    available = sum(s is not None for s in cust) >= max(3, len(cust) // 2) and any(abs(s) > 1e-9 for s in cust if s is not None)
    if not available:
        warnings.append("no usable customer sentiment scores; sentiment features are off")
    return NCall(turns=turns, customer_name=(customer_name or "").strip(), sentiment_available=available, warnings=warnings)
