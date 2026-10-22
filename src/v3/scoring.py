"""v3 scoring: category scores from the tenant's own categories and deductions.

v2 trusted the category name written on each rating ("Soft Skills" / "Technical Knowledge") and silently gave 100 when a tenant used other
category names, or when no criteria were active. v3 looks each rated item up by NAME in the tenant's criteria, uses the tenant's deduction,
normalises the category weights, keeps the configured order (deterministic rounding) and refuses to score an empty criteria set.
"""
import re
from typing import Any, Dict, List, Optional, Tuple


class NoCriteria(ValueError):
    """The tenant has no active criteria, so there is nothing to score (HTTP 422, not a perfect score)."""


def name_key(name: Any) -> str:
    s = re.sub(r"<\s*br\s*/?\s*>", " ", str(name or ""), flags=re.I)
    return re.sub(r"\s+", " ", s).strip().lower()


def _deduction(value: Any) -> float:
    try:
        v = float(value)
    except (TypeError, ValueError):
        return 10.0
    return min(max(v, 0.0), 100.0)


def tenant_items(criteria_data: Dict[str, Any]) -> List[Tuple[str, Dict[str, Any]]]:
    """[(category name, line item)] in the tenant's order. Raises NoCriteria when empty."""
    out = []
    for cat in (criteria_data or {}).get("categories", []) or []:
        for item in cat.get("line_items", []) or []:
            if isinstance(item, dict) and name_key(item.get("name")):
                out.append((str(cat.get("name", "")).strip() or "General", item))
    if not out:
        raise NoCriteria("no active criteria for this tenant")
    return out


def score(ratings: List[Dict[str, Any]], criteria_data: Dict[str, Any], is_auto_fail: bool = False) -> Tuple[Dict[str, float], float]:
    """(category scores, final score 0-100, one decimal). Ratings are matched to tenant items by name."""
    items = tenant_items(criteria_data)
    rated = {name_key(r.get("name")): ("PASS" if r.get("rating") in ("PASS", "YES") else "FAIL") for r in ratings}
    order: List[str] = []
    deductions: Dict[str, float] = {}
    for cat, item in items:
        if cat not in deductions:
            order.append(cat)
            deductions[cat] = 0.0
        if rated.get(name_key(item.get("name"))) == "FAIL":
            deductions[cat] += _deduction(item.get("deduction_value"))
    cat_scores = {cat: 0.0 if is_auto_fail else max(0.0, 100.0 - deductions[cat]) for cat in order}
    weights_in = (criteria_data or {}).get("category_weights") or {}
    w = {}
    for cat in order:
        try:
            w[cat] = max(0.0, float(weights_in.get(cat, 1.0)))
        except (TypeError, ValueError):
            w[cat] = 1.0
    total = sum(w.values())
    if total <= 0:
        w = {cat: 1.0 for cat in order}
        total = float(len(order))
    final = 0.0 if is_auto_fail else round(sum(cat_scores[c] * w[c] for c in order) / total, 1)
    return cat_scores, final
