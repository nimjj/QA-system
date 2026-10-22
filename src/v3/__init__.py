"""App v3: a new pipeline around the Laya model, built beside (never inside) the frozen v2 modules.

The frozen modules (src/services/laya_inputs.py, rule_engine.py, laya_windows.py and the question wording in
dynamic_evaluator.py) are hashed into the training data, so v3 imports them and never edits them. Select v3 with LAYA_FLOW=v3.
"""
import json
import os

_CONFIG_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "config", "v3.json")
_config = None


def load_config() -> dict:
    """The versioned v3 settings (limits, role labels, thresholds). Read once."""
    global _config
    if _config is None:
        with open(_CONFIG_PATH, encoding="utf-8") as fh:
            _config = json.load(fh)
    return _config
