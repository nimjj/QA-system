"""Everything Laya is shown, built in one place.

`build_laya_inputs()` parses a transcript and returns the text each Laya check receives. Production
(`dynamic_evaluator.evaluate_interaction`) and the training-data tools both call it, so training rows contain
exactly what the model sees in production. Change an extractor here and any training data built before the change
must be regenerated.

No model is loaded here; this module only turns a transcript into text.
"""
import re
from dataclasses import dataclass, field
from typing import Any, List, Optional, Tuple, Union

from src.services.rule_engine import (
    extract_active_listening_snippets, extract_empathy_snippet_list, extract_ownership_snippets,
    extract_probing_inputs, extract_rapport_snippets, without_detail_answers, without_setup_lines,
)

# Size limits on what each model call receives (Laya reads roughly 340 words per question)
EMPATHY_MAX_SNIPPETS = 2          # most severe upset-customer moments checked, one call each
PROBING_PROBLEM_MAX_WORDS = 50    # customer-problem text sent with the probing check
PROBING_QUESTIONS_MAX_WORDS = 100 # agent questions sent with the probing check
RESOLVED_TAIL_LINES = 10          # last N lines sent to the "resolved" batch (B2)
PARAPHRASE_CUSTOMER_MAX_WORDS = 50
PARAPHRASE_AGENT_MAX_WORDS = 150


@dataclass
class LayaInputs:
    """A parsed call plus the text for every Laya check. Empty string / empty list / None mean "nothing to ask"."""
    turns: List[Tuple[str, str]]
    times: List[Tuple[int, int]]
    customer_name: str
    agent_text: str = ""                                   # every agent line, "Agent: ..." per line (profanity check)
    empathy: List[str] = field(default_factory=list)       # one Laya call per snippet
    paraphrasing: str = ""
    active_listening: str = ""
    ownership: str = ""
    rapport: List[str] = field(default_factory=list)       # one Laya call per snippet
    probing: Optional[str] = None                          # None: the agent asked no questions at all
    resolved: str = ""                                     # last RESOLVED_TAIL_LINES lines
    batch_agent_only: str = ""                             # customer context + agent lines (generic batch items)
    batch_full: str = ""                                   # the whole call (escalation, hostility)


def parse_transcript(transcript_data: Union[str, List[dict]], caller: Optional[str] = None):
    """(turns, times, clean_lines, agent_lines, customer_lines, customer_name, sentiment_scores)."""
    turns, parsed_times, clean_lines, agent_lines, customer_lines = [], [], [], [], []
    customer_name = caller or ""
    sentiment_scores = [t.get('sentiment_score', 0.0) for t in transcript_data] if isinstance(transcript_data, list) else []

    if isinstance(transcript_data, list):
        for turn in transcript_data:
            spk = turn.get("speaker", "Unknown")
            txt = turn.get("text", "")
            st_sec = turn.get("start_time_sec", 0)
            turns.append((spk, txt))
            parsed_times.append((st_sec, st_sec + 10))
            clean_lines.append(f"{spk}: {txt}")
            if spk.lower() == "agent":
                agent_lines.append(txt)
            elif spk.lower() == "customer":
                customer_lines.append(txt)
    else:
        # Pre-split inline timestamps like [00:09] if they are concatenated on a single line
        normalized_text = re.sub(r'(\s*)([\[\(]\s*\d{1,2}:\d{2}(?::\d{2})?\s*[\]\)])', r'\n\2', transcript_data.strip())
        for line in normalized_text.splitlines():
            line = line.strip()
            if not line:
                continue
            time_match = re.match(r'^[\[\(]\s*(\d{1,2}):(\d{2})(?::(\d{2}))?\s*[\]\)]\s*', line)
            t_sec = int(time_match.group(1)) * 60 + int(time_match.group(2)) if time_match else 0

            line = re.sub(r"^[\[\(]\s*\d{1,2}:\d{2}(?::\d{2})?\s*[\]\)]\s*", "", line)
            clean_lines.append(line)
            if ":" in line:
                spk, txt = line.split(":", 1)
                spk_clean = spk.strip()
                txt_clean = txt.strip()
                turns.append((spk_clean, txt_clean))
                parsed_times.append((t_sec, t_sec + 10))

                spk_lower = spk_clean.lower()
                if spk_lower in ["agent", "rep", "representative", "specialist"]:
                    agent_lines.append(txt_clean)
                elif spk_lower in ["customer", "client", "caller", "user"]:
                    customer_lines.append(txt_clean)
    return turns, parsed_times, clean_lines, agent_lines, customer_lines, customer_name, sentiment_scores


def build_laya_inputs(transcript_data: Union[str, List[dict]], caller: Optional[str] = None) -> LayaInputs:
    turns, parsed_times, clean_lines, agent_lines, customer_lines, customer_name, sentiment_scores = \
        parse_transcript(transcript_data, caller)

    clean_transcript = "\n".join(clean_lines)
    agent_only_transcript = "\n".join([f"Agent: {x}" for x in agent_lines])
    first_10_cust = " ".join(customer_lines[:10])
    problem_lines = without_detail_answers(customer_lines) or customer_lines

    out = LayaInputs(turns=turns, times=parsed_times, customer_name=customer_name, agent_text=agent_only_transcript)

    out.empathy = extract_empathy_snippet_list(turns, sentiment_scores, EMPATHY_MAX_SNIPPETS)

    # greeting, verification and account-detail turns would otherwise fill most of both word budgets
    para_cust = " ".join(" ".join(problem_lines).split()[:PARAPHRASE_CUSTOMER_MAX_WORDS])
    para_agent_lines = (without_setup_lines(agent_lines) or agent_lines)[:10]
    para_agent = " ".join(" ".join(para_agent_lines).split()[:PARAPHRASE_AGENT_MAX_WORDS])
    out.paraphrasing = f"CUSTOMER: {para_cust}\nAGENT: {para_agent}"

    out.active_listening = extract_active_listening_snippets(turns)
    out.ownership = extract_ownership_snippets(turns)
    rapport = extract_rapport_snippets(turns)
    out.rapport = [rapport] if rapport else []

    agent_questions = [txt for spk, txt in turns if spk.lower() == "agent" and "?" in txt]
    if agent_questions:
        problem_text, probe_questions = extract_probing_inputs(
            turns, problem_lines, PROBING_PROBLEM_MAX_WORDS, PROBING_QUESTIONS_MAX_WORDS)
        q_txt = "\n".join(f"- {q}" for q in probe_questions)
        out.probing = f"CUSTOMER PROBLEM: {problem_text}\n\nThe agent asked these questions during the call:\n{q_txt}"

    out.resolved = "\n".join(clean_lines[-RESOLVED_TAIL_LINES:])
    out.batch_agent_only = f"CUSTOMER PROBLEM CONTEXT:\n{first_10_cust}\n\n" + agent_only_transcript
    out.batch_full = clean_transcript
    return out
