# Reference gold set

Each JSON file is one call plus the verdict a reviewer agreed is correct for every check.
`Scripts/accuracy_report.py` runs them against a live service and reports where the scorer
disagrees, with a per-check precision/recall.

**What these labels are — and are not.** They are hand-authored *reference* labels (ground
truth for clear-cut, constructed cases), used for regression and to judge a gate change on
evidence. They are **not** the model's own AI-written keys, and they are **not** a
statistically representative sample of real production calls. Treat the numbers as a sanity
and regression signal, not as a measured production accuracy. Expand this set with
reviewer-labelled real calls to get closer to that.

## File format
```json
{
  "name": "short_id",
  "note": "why this call is here",
  "payload": { "tenant_id": "...", "customer_name": "...", "transcript": [ ... ] },
  "expected_auto_fail": false,
  "expected": { "Check name": "PASS", "Other check": "FAIL" }
}
```
`payload` is sent to `POST /api/evaluate` verbatim. `expected` keys are matched to scorecard
item names case-insensitively; a check with no entry here is not scored.
