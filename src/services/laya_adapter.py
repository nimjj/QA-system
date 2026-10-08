"""Laya decision engine adapter (replaces the old Ollama llm_adapter).

Laya answers typed questions in one forward pass and never generates text. The evaluator only needs
yes/no probabilities, so this module exposes a single call: predict_yes().

Environment:
    LAYA_MODEL    checkpoint to use (default "english"; always passed explicitly so short snippets
                  are not auto-routed to the multilingual checkpoint)
    LAYA_HF_HOME  folder holding the downloaded Laya weights (Hugging Face cache). Defaults to
                  ../laya-test/hf_home next to this repo when that folder exists.
    LAYA_DEVICE   optional torch device, e.g. "cpu" or "cuda"
"""
import os
import threading
from typing import Any, Dict

LAYA_MODEL = os.getenv("LAYA_MODEL", "english")

_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
_DEFAULT_HF_HOME = os.path.abspath(os.path.join(_ROOT, "..", "laya-test", "hf_home"))

_router = None
_lock = threading.Lock()


def _get_router():
    """Create the Router once. HF_HOME must be set before laya/transformers are imported."""
    global _router
    if _router is None:
        hf_home = os.getenv("LAYA_HF_HOME") or (_DEFAULT_HF_HOME if os.path.isdir(_DEFAULT_HF_HOME) else None)
        if hf_home:
            os.environ.setdefault("HF_HOME", hf_home)
        os.environ.setdefault("HF_HUB_DISABLE_SYMLINKS_WARNING", "1")
        from laya import Router
        _router = Router(device=os.getenv("LAYA_DEVICE") or None, max_loaded=1, default=LAYA_MODEL)
    return _router


def predict_yes(text: str, questions: Dict[str, Dict[str, Any]], label: str = "") -> Dict[str, float]:
    """Return P(true) for each noul question id, judged against `text`.

    A text too long for one window is re-scored with predict_long (overlapping windows, the strongest
    window decides). `label` names the calling check and exists for logging/stubbing.
    """
    with _lock:
        router = _get_router()
        result = router.predict(text, questions, model=LAYA_MODEL)
        if result.get("usage", {}).get("truncated"):
            result = router.predict_long(text, questions, model=LAYA_MODEL)
    return {qid: float(result["answers"][qid]["noul"]) for qid in questions}
