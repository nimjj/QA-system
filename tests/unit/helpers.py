"""Tiny builders so tests read like the examples in the audit."""
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from src.v3.normalise import normalise  # noqa: E402


def call(*turns, name=""):
    """call(("Agent", "hi", 0), ("Customer", "hello", 5, -20.0), ...) -> normalised call.
    A turn is (speaker, text, start[, sentiment[, end]]); sentiment None means 'no score'."""
    raw = []
    for t in turns:
        d = {"speaker": t[0], "text": t[1], "start_time_sec": t[2]}
        if len(t) > 3 and t[3] is not None:
            d["sentiment_score"] = t[3]
        if len(t) > 4:
            d["end_time"] = t[4]
        raw.append(d)
    return normalise(raw, customer_name=name)
