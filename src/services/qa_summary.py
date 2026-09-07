"""PART 2: LLM writes a plain summary of the whole call.

One small LLM request -- just the summary, nothing else (keeps tokens low).
"""

import os
import sys

_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
_SRC = os.path.join(_ROOT, "src")
_TESTS = os.path.join(_ROOT, "tests")
for _path in [_ROOT, _SRC, _TESTS]:
    if _path not in sys.path:
        sys.path.insert(0, _path)

from src.core.llm_client import query_llm

def load_summary_prompt():
    prompt_path = os.getenv("PROMPT_SUMMARY_PATH", "resources/prompts/summary_prompt.txt")
    full_path = os.path.join(_ROOT, prompt_path)
    with open(full_path, "r", encoding="utf-8") as f:
        return f.read()

def format_transcript(transcript):
    return "\n".join(f"{speaker}: {text}" for speaker, text in transcript)

SUMMARY_PROMPT = load_summary_prompt()

def extract_topic_keywords(transcript_text: str) -> str:
    prompt = f"""TRANSCRIPT:
{transcript_text}

INSTRUCTIONS:
You are a highly efficient topic extractor.
Read the transcript above and return ONLY a comma-separated list of the 5 to 10 most important technical issues, topics, or policies discussed.
Do not write sentences. Just output the keywords.
"""
    return query_llm(prompt, label="topic_extraction")

def generate_short_story_summary(transcript_text: str, evaluation_context: str = "No critical failures identified.") -> str:
    prompt = load_summary_prompt().format(
        transcript=transcript_text,
        evaluation_context=evaluation_context
    )
    return query_llm(prompt, label="story_summary")
