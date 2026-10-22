"""App v3: a new pipeline around the Laya model, built beside (never inside) the frozen v2 modules.

The frozen modules (src/services/laya_inputs.py, rule_engine.py, laya_windows.py and the question wording in
dynamic_evaluator.py) are hashed into the training data, so v3 imports them and never edits them. Select v3 with LAYA_FLOW=v3.
"""
import json
import os

_CONFIG_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "config", "v3.json")
_CRITERIA_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "config", "criteria.json")
_config = None
_criteria = None


def load_criteria() -> dict:
    """The one set of criteria every call is graded against (11 items, two categories, their deductions and weights). No database."""
    global _criteria
    if _criteria is None:
        with open(_CRITERIA_PATH, encoding="utf-8") as fh:
            _criteria = json.load(fh)
    return json.loads(json.dumps(_criteria))                 # a copy, so a caller cannot change the shared default


def load_config() -> dict:
    """The versioned v3 settings (limits, role labels, thresholds). Read once."""
    global _config
    if _config is None:
        with open(_CONFIG_PATH, encoding="utf-8") as fh:
            _config = json.load(fh)
    return _config
