"""Flow v2 windows: what Laya is shown for each check, chosen by call structure instead of fixed line counts.

Status: EXPERIMENTAL. Used by Scripts/window_lab.py to compare against the current extractors in
laya_inputs.py / rule_engine.py. Nothing in production imports this module yet. It is deliberately outside the
frozen-inputs hash (laya-training/tools/export_checks.py) until a variant is adopted.

Rules every window follows (see the flow-v2 plan):
  - one purpose per window, at most about 340 words (Laya reads roughly that much of a 512-token state);
  - customer-side sentiment only (production has no usable agent sentiment);
  - compress instead of truncating: drop one- to three-word backchannels, trim long lines.
No model is loaded here.
"""
import re
from typing import List, Optional, Sequence, Tuple

from src.services.rule_engine import _AL_IGNORE_RE, _FRUSTRATION_RE, question_sentences

Turn = Tuple[str, str]                       # (speaker, text)
Times = Sequence[Tuple[int, int]]            # (start, start + 10) per turn, as laya_inputs.parse_transcript builds them

BACKCHANNEL_MAX_WORDS = 3                    # "okay", "mm-hm", "yes thanks"
UPSET_SENTIMENT = -15.0                      # same bar as rule_engine._empathy_candidates


def _trim(text: str, max_words: int) -> str:
    words = text.split()
    return text if len(words) <= max_words else " ".join(words[:max_words]) + " ..."


def _is_customer(spk: str) -> bool:
    return spk.lower() == "customer"


def _is_agent(spk: str) -> bool:
    return spk.lower() == "agent"


# ------------------------------------------------------------------ Empathy
def upset_moments(turns: Sequence[Turn], sentiment_scores: Sequence[float]) -> List[Tuple[int, float]]:
    """(turn index, sentiment) of every upset customer turn: sentiment at or below -15, or a frustration word
    with a negative score. Without sentiment scores only the frustration words are used."""
    out = []
    for i, (spk, txt) in enumerate(turns):
        if not _is_customer(spk):
            continue
        score = sentiment_scores[i] if i < len(sentiment_scores) else None
        if score is None:
            if _FRUSTRATION_RE.search(txt):
                out.append((i, -20.0))
        elif score <= UPSET_SENTIMENT or (score < 0 and _FRUSTRATION_RE.search(txt)):
            out.append((i, float(score)))
    return out


def _span(turns: Sequence[Turn], start: int, n_after: int, line_words: int = 60) -> str:
    return "\n".join(f"{spk}: {_trim(txt, line_words)}" for spk, txt in turns[start:start + 1 + n_after])


def empathy_windows(turns: Sequence[Turn], sentiment_scores: Sequence[float], n_after: int = 6,
                    second: bool = True) -> List[str]:
    """The first upset moment and the next n_after turns, plus (optionally) the most severe later moment.
    The item passes if any window shows an acknowledgement. No upset moment -> no window (PASS)."""
    moments = upset_moments(turns, sentiment_scores)
    if not moments:
        return []
    picks = [moments[0][0]]
    if second:
        worst = min(moments, key=lambda m: (m[1], m[0]))[0]
        if worst - picks[0] > n_after:
            picks.append(worst)
    return [_span(turns, i, n_after) for i in picks]


def upset_flags(turns: Sequence[Turn], sentiment_scores: Sequence[float], use_drop: bool = False) -> List[bool]:
    """True for every customer turn that shows frustration: sentiment at or below -15, a drop of 8 or more against
    the customer's previous three turns, or a frustration word whatever the score (sentiment from RoBERTa can stay
    positive on a clearly annoyed line)."""
    flags, prev = [], []
    for i, (spk, txt) in enumerate(turns):
        if not _is_customer(spk):
            flags.append(False)
            continue
        score = sentiment_scores[i] if i < len(sentiment_scores) else None
        drop = max((p - score for p in prev[-3:]), default=0.0) if score is not None else 0.0
        if score is not None:
            prev.append(score)
        flags.append(bool(_FRUSTRATION_RE.search(txt)) or (score is not None and (score <= UPSET_SENTIMENT or (use_drop and drop >= 8.0))))
    return flags


def outburst_starts(turns: Sequence[Turn], sentiment_scores: Sequence[float], calm_customer_turns: int = 2,
                    min_gap: int = 6, use_drop: bool = False) -> List[int]:
    """Start of each distinct outburst: a flagged customer turn that follows at least calm_customer_turns unflagged
    customer turns (or the call's first flagged turn), at least min_gap turns after the previous start. The many
    consecutive upset turns of one ongoing complaint count as ONE outburst."""
    flags = upset_flags(turns, sentiment_scores, use_drop)
    starts, calm, last = [], calm_customer_turns, -10 ** 6
    for i, (spk, _) in enumerate(turns):
        if not _is_customer(spk):
            continue
        if flags[i]:
            if calm >= calm_customer_turns and i - last >= min_gap:
                starts.append(i)
                last = i
            calm = 0
        else:
            calm += 1
    return starts


def empathy_episode_windows(turns: Sequence[Turn], sentiment_scores: Sequence[float], n_after: int = 4,
                            calm_customer_turns: int = 2, min_gap: int = 6, max_windows: int = 4,
                            use_drop: bool = False) -> List[str]:
    """One window per distinct outburst (strict rubric: every new outburst must be handled). The item fails if ANY
    window shows no acknowledgement. Capped at max_windows, keeping the first and the most recent."""
    starts = outburst_starts(turns, sentiment_scores, calm_customer_turns, min_gap, use_drop)
    if len(starts) > max_windows:
        starts = starts[:max_windows - 1] + starts[-1:]
    return [_span(turns, i, n_after) for i in starts]


# ------------------------------------------------------------------ Ownership
_OWNERSHIP_PHRASES = [
    "not my department", "not my job", "not something i deal", "not something i handle", "that's not my", "thats not my",
    "i don't handle", "i dont handle", "call back", "another department", "another team", "different department",
    "wrong department", "other department", "nothing i can do", "can't do anything", "cant do anything",
    "hope you get", "network team", "billing team", "provisioning team", "that's their", "not our problem",
    "not my problem", "contact them", "you'll have to ask",
]
_OWNERSHIP_RE = re.compile(
    r"\byou('|’)?(ll| will| would|'d| d)( normally| really| just| need to)? have to (ring|call|phone|contact|write|email|speak|go|take|ask|raise|apply|visit|approach|get in touch|chase|deal|sort)\b"
    r"|\bnothing (at all )?to do with (me|us|s-net)\b"
    r"|\bnot (our|my) (department|network|problem|job|fault|responsibility|area|remit|business)\b"
    r"|\b(isn't|is not|aren't|are not) (our|my) (problem|network|department|fault|responsibility|business)\b"
    r"|\bthat'?s between you and\b"
    r"|\btake (that|it|this) up with\b"
    r"|\b(ring|call|contact|write to|email|speak to|ask) (them|their|the (team|department|company|provider|shop|store|bank))\b"
    r"|\bnothing (s-net|we|i) can do\b"
    r"|\b(outside|beyond) (of )?(our|my) (control|remit)\b"
    r"|\bnot something (we|i)\b"
    r"|\b(their|that team'?s|that department'?s) (job|responsibility|problem|fault)\b"
    r"|\b(we|i) (don't|do not|cannot|can't) (deal|handle|cover|do|help with) ",
    re.IGNORECASE)


def ownership_candidates(turns: Sequence[Turn], max_lines: int = 6) -> str:
    """Agent lines that may deflect, in the same agent-only format the model was trained on (one 'Agent: ...' per
    line), found with the old phrase list plus the wordings the AG50 calls showed it lacked."""
    hits = []
    for spk, txt in turns:
        if not _is_agent(spk):
            continue
        low = txt.lower()
        if any(p in low for p in _OWNERSHIP_PHRASES) or _OWNERSHIP_RE.search(txt):
            hits.append(f"Agent: {_trim(txt, 70)}")
    return "\n".join(hits[:max_lines])


# ------------------------------------------------------------------ Paraphrasing
_PARAPHRASE_CUE = re.compile(
    r"(so (just|to|if|what|you|it|your|the|that)\b|just to (confirm|make sure|clarify|check|be sure)"
    r"|let me (just )?(make sure|confirm|recap|check i)|what i('m| am) (hearing|understanding)"
    r"|if i('ve| have) (got|understood)|am i right|did i (get|understand)|to (summari[sz]e|recap)"
    r"|you('re| are) saying|so basically|in other words|correct me|is that (right|correct|accurate|fair)|have i got)",
    re.IGNORECASE)


def paraphrase_window(turns: Sequence[Turn], times: Times, first_seconds: int = 300,
                      max_agent_lines: int = 2) -> Optional[str]:
    """Candidate + verify. None when no agent line in the first minutes carries a restatement cue (the item then
    fails without a model call). Otherwise: the customer's problem statement and the candidate agent line(s), in the
    'CUSTOMER: ... / AGENT: ...' format the model was trained on."""
    cust = next((txt for spk, txt in turns if _is_customer(spk) and len(txt.split()) >= 12), None)
    if cust is None:
        cust = next((txt for spk, txt in turns if _is_customer(spk)), "")
    agent = []
    for i, (spk, txt) in enumerate(turns):
        start = times[i][0] if i < len(times) else 0
        if _is_agent(spk) and start <= first_seconds and _PARAPHRASE_CUE.search(txt):
            agent.append(_trim(txt, 60))
            if len(agent) >= max_agent_lines:
                break
    if not agent:
        return None
    return f"CUSTOMER: {_trim(cust, 80)}\nAGENT: {' '.join(agent)}"


# ------------------------------------------------------------------ Resolved
def resolved_tail_indices(turns: Sequence[Turn], times: Times, tail_seconds: int = 300, max_words: int = 340,
                          keep_last: int = 4, line_words: int = 45) -> List[int]:
    """Indices of the turns kept for the Resolved window (see resolved_tail)."""
    if not turns:
        return []
    end = times[-1][0] if times else 0
    idx = [i for i in range(len(turns)) if (times[i][0] if i < len(times) else 0) >= end - tail_seconds]
    tail_last = set(range(len(turns) - keep_last, len(turns)))
    idx = [i for i in idx if i in tail_last or len(turns[i][1].split()) > BACKCHANNEL_MAX_WORDS]
    words = lambda i: len(_trim(turns[i][1], line_words).split()) + 1
    while len(idx) > keep_last and sum(words(i) for i in idx) > max_words:
        idx.pop(0)
    return idx


def resolved_tail(turns: Sequence[Turn], times: Times, tail_seconds: int = 300, max_words: int = 340,
                  keep_last: int = 4, line_words: int = 45) -> str:
    """The end of the call, compressed: last tail_seconds, one- to three-word backchannels dropped, long lines
    trimmed, earliest lines dropped until it fits max_words. The final keep_last lines are always kept."""
    idx = resolved_tail_indices(turns, times, tail_seconds, max_words, keep_last, line_words)
    return "\n".join(f"{turns[i][0]}: {_trim(turns[i][1], line_words)}" for i in idx)


# ------------------------------------------------------------------ Active listening, second candidate source
_STOP = set("a an the and or but so to of in on at for with from by is are was were be been being it its this that these "
            "those i you your my me we our they them he she his her do does did have has had can could will would should "
            "may might just very really please okay ok yes no yeah right um uh er well then there here what which who "
            "when where why how about any some all if as not up out down over again also still now let me let's get got "
            "going go see check checking tell thanks thank sure".split())


def _content_words(text: str) -> set:
    return {w for w in re.findall(r"[a-z0-9£.\-]+", text.lower()) if w not in _STOP and len(w) > 1}


# Questions that repeat the customer's words on purpose: confirming, summarising or restating what was said
_AL_CONFIRM_RE = re.compile(
    r"\b(have i got that|did i get that|in my own words|just to confirm|to confirm|to summari[sz]e|to recap|"
    r"let me make sure|let me confirm|so you('re| are) saying|are you saying|you want me to)\b", re.IGNORECASE)


def active_listening_pairs_from_customer(turns: Sequence[Turn], top_k: int = 3):
    """Second candidate source: an earlier customer turn sharing at least two content words (numbers and long words
    count extra) with a later agent question. Returns [(score, customer turn index, agent turn index, question)]."""
    out = []
    for j, (spk, txt) in enumerate(turns):
        if not _is_agent(spk):
            continue
        for q in question_sentences(txt):
            if len(q.split()) < 4 or _AL_IGNORE_RE.search(q) or _AL_CONFIRM_RE.search(q):
                continue
            qt = _content_words(q)
            if len(qt) < 2:
                continue
            best = None
            for i in range(j):
                if not _is_customer(turns[i][0]):
                    continue
                inter = qt & _content_words(turns[i][1])
                if len(inter) < 2:
                    continue
                spec = sum(1 for w in inter if re.search(r"\d", w) or len(w) >= 6)
                score = len(inter) / len(qt) + 0.15 * spec
                if best is None or score > best[0]:
                    best = (score, i, j, q)
            if best:
                out.append(best)
    out.sort(reverse=True)
    return out[:top_k]


def active_listening_with_customer_pairs(turns: Sequence[Turn], current: str, max_blocks: int) -> str:
    """Flow v2, switch LAYA_AL_SOURCE2: the current question-pair blocks first, then up to `max_blocks` in total
    filled with "customer said X / agent later asked about X" blocks. The same later question can appear twice
    with different earlier premises: the question-pair extractor often pairs it with an unrelated earlier question,
    and the customer's own statement is the premise the key means. The word-overlap score cannot tell a real repeat
    from a harmless re-check (it fires on most good calls), so every block is judged by the model, one at a time
    (dynamic_evaluator)."""
    blocks = [b for b in current.split("\n\n") if b]
    for _, ci, aj, question in active_listening_pairs_from_customer(turns):
        if len(blocks) >= max_blocks:
            break
        blocks.append(f"Turn {ci} Customer said: {_trim(turns[ci][1], 40)}\nTurn {aj} Agent later asked: {question}")
    return "\n\n".join(blocks)
