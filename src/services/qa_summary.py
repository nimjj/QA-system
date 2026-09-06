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

def generate_scalable_summary(transcript_text: str, evaluation_context: str = "No critical failures identified.") -> str:
    """Extract a fast comma-separated list of topics using a lightweight model for RAG.
    
    We use a small, fast model (LLM3:1b or LLM2:2b) to quickly grab the core topics 
    for quick categorization.
    """
    prompt = f"""TRANSCRIPT:
{transcript_text}

INSTRUCTIONS:
You are a highly efficient topic extractor.
Read the transcript above and return ONLY a comma-separated list of the 5 to 10 most important technical issues, topics, or policies discussed.
Do not write sentences. Just output the keywords.
Example: router red light, power cycle, internet connectivity, account verification
"""
    
    # We use a very low num_predict because we only want a short list of keywords
    # Fallback to the main model if FAST_TOPIC_MODEL isn't explicitly set
    return query_llm(prompt, label="topic_extraction")
