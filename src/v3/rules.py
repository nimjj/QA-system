"""v3 rule checks: Branding, Hold time and Dead air, Verified customer, Personalized, and the profanity auto-fail.

Each function takes a normalised call (src/v3/normalise.NCall) and returns a rating dict shaped like the v2 ones
({category, name, rating, score, deduction_value?, coaching}) plus `evidence`, the normalised turn indexes behind the verdict.
Every rule here replaces a behaviour the audit proved wrong; the examples are in tests/unit/. No model is used.
"""
import difflib
import re
import unicodedata
from typing import Dict, List, Optional, Tuple

from src.v3 import load_config
from src.v3.normalise import NCall

SOFT, TECH = "Soft Skills", "Technical Knowledge"


def _rating(category: str, name: str, ok: bool, coaching: str, evidence: Optional[List[int]] = None) -> Dict:
    return {"category": category, "name": name, "rating": "PASS" if ok else "FAIL", "score": 100 if ok else 0,
            "coaching": "" if ok else coaching, "evidence": evidence or []}


def _fold(s: str) -> str:
    """lower case, accents removed, dashes and punctuation turned into spaces: robust to speech-to-text noise."""
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode("ascii").lower()
    return re.sub(r"\s+", " ", re.sub(r"[^a-z0-9 ]", " ", s)).strip()


# ---------------------------------------------------------------- branding
def _brand_regex(brand: str) -> str:
    """"s-net" -> matches "s net", "snet", "s-net", "s dash net", "s  net" after folding."""
    parts = [re.escape(p) for p in re.split(r"[^a-z0-9]+", brand.lower()) if p]
    return r"\s*(?:dash\s*)?".join(parts)


def evaluate_branding(call: NCall, brand: Optional[str] = None) -> Dict:
    """Greeting 'thank you for calling <brand>' in the first 4 agent lines and 'thank you for choosing <brand>' in the last 4,
    on two different lines. IVR/bot lines do not use up the first slots (they are not agent turns here)."""
    brand = brand or load_config()["brand"]
    b = _brand_regex(brand)
    greet = re.compile(rf"\bthank you for calling,?\s*{b}\b")
    close = re.compile(rf"\bthank you for choosing,?\s*{b}\b")
    agent = call.role_turns("agent")
    if not agent:
        return _rating(SOFT, "Branding and Survey Check", False, "No agent lines found in the transcript.")
    g = next((t.index for t in agent[:4] if greet.search(_fold(t.text))), None)
    c = next((t.index for t in agent[-4:] if close.search(_fold(t.text)) and t.index != g), None)
    missed = [m for m, v in (("Greeting", g), ("Closing", c)) if v is None]
    return _rating(SOFT, "Branding and Survey Check", not missed, f"Agent missed the required script for: {', '.join(missed)}",
                   [i for i in (g, c) if i is not None])


# ---------------------------------------------------------------- dead air and holds
_HOLD_ANNOUNCE = re.compile(
    r"\b(?:(?:place|placing|put|putting)\s+you\s+on\s+(?:a\s+)?(?:brief\s+|short\s+|quick\s+|temporary\s+)?hold"
    r"|please\s+hold(?:\s+(?:the\s+line|on))?"
    r"|bear\s+with\s+me"
    r"|(?:one|a)\s+moment\s+(?:while|please)"
    r"|give\s+me\s+(?:a|one|just\s+a)\s+(?:moment|minute|second|sec)\s+(?:while|to)"
    r"|(?:a|one)\s+(?:moment|minute)\s+to\s+(?:check|look|pull|find|see|verify))\b", re.I)
_HOLD_RETURN = re.compile(
    r"\b(?:thank(?:s| you)(?: so much| very much)? for (?:holding|waiting|your patience|bearing with me|hanging on|staying (?:on the line|with me))"
    r"|(?:sorry|apologies|apologi[sz]e)(?: for| about)(?: the)? wait(?:ing)?|sorry to keep you waiting|i(?:'m| am) back)\b", re.I)
_CHASING = re.compile(r"\bhello\b\s*\?|\b(?:are )?you still there\b|\banyone there\b|\bcan you hear me\b", re.I)
_CUSTOMER_TASK = re.compile(
    r"\b(?:can|could|would|will) you (?:please |just )?(?:check|find|look|grab|get|go|open|read|try|plug|unplug|restart|reboot|turn|press|dial|locate|bring|have a look)\b"
    r"|\b(?:please |just )?(?:check|look|find|grab|unplug|plug|restart|reboot|press|go to|open)\b[^.?!]{0,40}\byour\b"
    # a plain instruction at the start of a sentence: "Just reboot it. Unplug it, wait, plug it back in."
    r"|(?:^|[.!?]\s+)(?:just |now |then |first |next |please )?(?:reboot|restart|unplug|plug|press|turn|switch|power|reset|check|look|try|open|go|read|hold down|log|click|tap|select|wait)\b",
    re.I)


def evaluate_dead_air(call: NCall, cfg: Optional[dict] = None) -> Dict:
    """Gaps are real (start of a turn minus the end of the one before; end estimated from the word count when the input has none).
    A gap over the limit is excused when it is an announced hold that is acknowledged or returned from (up to the hold maximum), or when
    the agent had just asked the customer to go and do something. FAIL on 2 or more unexcused gaps, or on any single one over the
    single-gap limit (the old rule let one ten-minute silence pass)."""
    d = (cfg or load_config())["dead_air"]
    turns = call.turns
    bad: List[Tuple[int, float]] = []
    for i in range(1, len(turns)):
        gap = turns[i].start - turns[i - 1].end
        if gap <= d["gap_seconds"]:
            continue
        prev, cur = turns[i - 1], turns[i]
        within_hold = gap <= d["managed_hold_max_seconds"]
        chasing = cur.role == "customer" and bool(_CHASING.search(cur.text))
        announced = prev.role == "agent" and bool(_HOLD_ANNOUNCE.search(prev.text))
        returned = cur.role == "agent" and bool(_HOLD_RETURN.search(cur.text))
        customer_task = (cur.role == "customer" and prev.role == "agent" and bool(_CUSTOMER_TASK.search(prev.text)))
        if within_hold and not chasing and (announced or returned or customer_task):
            continue
        bad.append((i, gap))
    longest = max((g for _, g in bad), default=0.0)
    fail = len(bad) >= d["breaches_to_fail"] or longest >= d["single_gap_fail_seconds"]
    return _rating(SOFT, "Hold time and Dead Air", not fail,
                   f"Dead air: {len(bad)} unmanaged silence(s) over {d['gap_seconds']}s (longest {longest:.0f}s).", [i for i, _ in bad])


# ---------------------------------------------------------------- verification
_VERIF = {
    # a bare "passcode" is not identity verification ("your voicemail passcode"); only a security/account one is
    "pin": r"\b(?:p\.?i\.?n\.?|pin(?:\s*(?:number|code))?|(?:security|account|verification|memorable)\s+(?:passcode|passphrase|password))\b",
    "security": r"\bsecurity\s+(?:questions?|answers?|codes?|words?|phrases?|details|checks?)\b|\bmemorable\s+(?:word|date|information)\b",
    "address": r"(?<!email )(?<!e mail )(?<!ip )(?<!mac )(?<!web )(?<!url )\baddress\b",
}
# business-policy extras, off by default (the owner's rule is PIN, address or security question); switch on in config/v3.json
_VERIF_OPTIONAL = {"date_of_birth": r"\bdate of birth\b|\bbirth ?date\b|\bdob\b", "account_number": r"\baccount\s+(?:number|no)\b",
                   "postcode": r"\bpost\s*code\b|\bzip\s*code\b"}
_REQUEST = re.compile(r"\?|\b(?:confirm|provide|give|tell|verify|read|state|spell|share|need|can i (?:have|get|take)|may i (?:have|take)|could i (?:have|take)|what(?:'s| is)|ask you)\b", re.I)
_NEGATED = re.compile(r"\b(?:don't|do not|won't|will not|no need|not going to|without|didn't|never|not)\b[^.?!]{0,30}$", re.I)


def evaluate_verified(call: NCall, cfg: Optional[dict] = None) -> Dict:
    """The agent REQUESTS a PIN, a security answer or an address within the window, measured from the agent's first line (so an IVR
    or hold lead-in does not eat the 240 s). 'email/IP/MAC address' and 'I don't need your PIN' do not count."""
    v = (cfg or load_config())["verification"]
    patterns = dict(_VERIF)
    if v.get("accept_date_of_birth"):
        patterns["dob"] = _VERIF_OPTIONAL["date_of_birth"]
    if v.get("accept_account_number"):
        patterns["acct"] = _VERIF_OPTIONAL["account_number"]
    if v.get("accept_postcode"):
        patterns["postcode"] = _VERIF_OPTIONAL["postcode"]
    agent = call.role_turns("agent")
    if not agent:
        return _rating(TECH, "Verified customer", False, "No agent lines found in the transcript.")
    t0 = agent[0].start
    for t in agent:
        if t.start - t0 > v["window_seconds"]:
            break
        for sentence in re.split(r"(?<=[.!?])\s+", t.text):
            for pat in patterns.values():
                m = re.search(pat, sentence, re.I)
                if m and _REQUEST.search(sentence) and not _NEGATED.search(sentence[:m.start()]):
                    return _rating(TECH, "Verified customer", True, "", [t.index])
    return _rating(TECH, "Verified customer", False, f"Agent did not ask for a PIN, address or security answer within the first {v['window_seconds'] // 60} minutes.")


# ---------------------------------------------------------------- personalised
_TITLES = {"mr", "mrs", "ms", "miss", "dr", "mx", "sir", "madam", "prof"}


def _name_tokens(name: str) -> List[str]:
    return [t for t in _fold(name).split() if t not in _TITLES and len(t) >= 2]


def evaluate_personalized(call: NCall) -> Dict:
    """The agent says the customer's name as a whole word (any of its words: 'Hi Sam' counts for 'Sam Smith'), tolerating small
    speech-to-text spelling errors on longer names. 'Sam' no longer matches 'Samsung' and 'Al' no longer matches 'also'."""
    tokens = _name_tokens(call.customer_name)
    if not tokens:
        r = _rating(SOFT, "Personalized the call/ticket appropriately", True, "")
        r["note"] = "not checked: no customer name supplied"
        return r
    for t in call.role_turns("agent"):
        words = _fold(t.text).split()
        for tok in tokens:
            if tok in words:
                return _rating(SOFT, "Personalized the call/ticket appropriately", True, "", [t.index])
            if len(tok) >= 6 and any(len(w) >= 5 and difflib.SequenceMatcher(None, tok, w).ratio() >= 0.85 for w in words):
                return _rating(SOFT, "Personalized the call/ticket appropriately", True, "", [t.index])
    return _rating(SOFT, "Personalized the call/ticket appropriately", False,
                   f"Agent never used the customer's name '{call.customer_name}' during the call.")


# ---------------------------------------------------------------- auto-fail
_INSULT_FRAME = re.compile(r"(?:don'?t|do not|stop|quit)\s+(?:be|being)\s+(?:an?\s+|so\s+|such\s+an?\s+|that\s+)?$", re.I)
_NEG_LOOKBACK = re.compile(r"\b(?:not|never|no|don'?t|do not|won'?t|isn'?t|wasn'?t|aren'?t|nothing|without|n't)\b[^.?!]{0,20}$", re.I)
_AUTOFAIL = [
    ("fuck", re.compile(r"\bf+u+c+k\w*|\bf[\*@#]{1,3}(?:c|u)?k\w*|\bf\*+ing\b", re.I), True),
    ("shut up", re.compile(r"\bshut[\s\-]*up\b", re.I), True),
    ("idiot", re.compile(r"\bidiots?\b(?!\s*-?\s*proof)", re.I), True),
    ("stupid", re.compile(r"\bstupid(?:ly)?\b", re.I), True),
    # "get lost" only as an order to the customer, not "don't get lost in the menu" or "you might get lost"
    ("get lost", re.compile(r"(?:^|[.!?,;]\s*|\band\s+|\bjust\s+|\bgo\s+and\s+|\byou\s+(?:can|could)\s+(?:just\s+)?|\bfeel\s+free\s+to\s+|\bthen\s+"
                            r"|\bwhy\s+don'?t\s+you\s+(?:just\s+)?)get lost\b", re.I), False),
    # "hang up" only when the agent threatens it, does it to the customer, or tells the customer to ("Just hang up and stop wasting my time"),
    # not "don't hang up", "I'll hang up the old line" or "hang up and call us back"
    ("hang up", re.compile(r"\b(?:i(?:'ll| will|'m going to| am going to|'m gonna)|i'm|i am|going to|gonna|we(?:'ll| will))\s+(?:just\s+)?hang(?:ing)?\s+up\b(?!\s+(?:the|your|that|this|old|on the line)\b)"
                           r"|\bhang(?:ing)?\s+up\s+on\s+you\b|\bhung\s+up\s+on\s+you\b"
                           r"|(?:^|[.!?,;]\s*|\bjust\s+|\byou\s+can\s+(?:just\s+)?|\bfeel\s+free\s+to\s+)hang\s+up\b"
                           r"(?!\s+(?:the|your|that|this|old|on the line|and\s+(?:call|dial|try|redial|ring|phone|then\s+call))\b)", re.I), True),
]


def check_auto_fail(call: NCall) -> Tuple[bool, Optional[str], Optional[int]]:
    """(is_auto_fail, reason, turn index). Agent lines only; the customer's language never fails the agent."""
    for t in call.role_turns("agent"):
        for word, rx, use_neg in _AUTOFAIL:
            for m in rx.finditer(t.text):
                back = t.text[max(0, m.start() - 30):m.start()]
                if use_neg and _NEG_LOOKBACK.search(back) and not _INSULT_FRAME.search(back):
                    continue
                return True, f"Auto-Fail Triggered: Profanity/Discourtesy detected ('{word}')", t.index
    return False, None, None
