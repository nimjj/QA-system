"""Small text helpers for noisy speech-to-text.

Speech-to-text output often has no punctuation at all, so "when did it start and which lights are red" contains no "?" and the v2 window
builders (which find questions by the "?") saw an agent who asked nothing: Probing failed without a model call and Active listening passed
without a look. add_question_marks() restores a "?" only where the turn is plainly a question, so the existing builders work unchanged.
"""
import re

# strong interrogative openings only; weak ones ("have", "do", "any") also start ordinary statements ("have a good day")
_STRONG = re.compile(
    r"^\W*(?:(?:okay|ok|so|and|alright|right|well|now|just|please|sorry|thanks|thank you)[\s,]+)*"
    r"(?:what|when|where|which|who|whom|whose|why|how|can you|could you|would you|will you|do you|did you|does it|does that|have you|has it|"
    r"are you|is it|is there|is that|was it|were you|may i|can i|could i|shall i|tell me|let me know)\b", re.I)


def add_question_marks(text: str) -> str:
    """Return the text with a "?" added after a punctuation-free turn that opens like a question. Turns that already contain
    sentence punctuation are left alone."""
    t = text.strip()
    if not t or "?" in t or re.search(r"[.!]", t.rstrip(".!")):
        return text
    if _STRONG.match(t):
        return t.rstrip(".!") + "?"
    return text
