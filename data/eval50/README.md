# Eval50: 50 test calls with Claude's expected scorecards

Written and graded by Claude on 2026-10-17, **before** any model (Ollama, stock Laya, fine-tuned Laya) was run on them, and frozen by commit + `manifest.json` (sha256 of every payload and expected file). Not human-reviewed; a blind human check of about 20 calls is the planned independent check.

- Sources: `calls_01.txt` ... `calls_09.txt` (one block per call with `@labels`, `@notes` explaining every FAIL, optional `@autofail`).
- Built by `tools/build_eval50.py` into `qa-analysis/inputs/Eval50/eval_NN.json` (app request payload) and `qa-analysis/inputs/Eval50/expected/expected_eval_NN.json` (the app's response format, with the final score computed by the app's own scoring function).
- The rule-based items (branding, dead air, verification, name) were cross-checked against the app's rule code: no disagreements.

Spread: 8 all-PASS calls, then calls with 1-2, 3-4 and 5+ faults, and 3 auto-fails. FAIL counts per item over the 50 calls: Branding 9, Dead air 8, Verified 10, Personalized 9, Empathy 16, Paraphrasing 16, Active listening 9, Ownership 14, Rapport 15, Probing 11, Resolved 20.

## Grading rules used (where the criteria leave room)
- **Resolved:** a technical fault must be verified working on the call (customer confirms). If the fix depends on a later event (delivery, repair, engineer, a "request" to another team) it is FAIL, even if next steps are confirmed. Admin and billing requests count as resolved once the change is made and the customer confirms it.
- **Empathy:** FAIL only when the customer shows clear frustration or distress and the agent never acknowledges it. A calm customer means PASS.
- **Ownership:** FAIL for a line that blames another team or a third party, or tells the customer to contact someone else, even if the agent later does something useful. Handing a request to another team while keeping it is PASS.
- **Active listening:** FAIL when the agent asks again for information the customer has already given. Re-checking something that may have changed (a light after a restart, a speed after a fix) is PASS.
- **Rapport:** FAIL for one clearly rude, condescending, dismissive or sarcastic agent line.
- **Branding / dead air / verification / name:** as the app's rules define them (verbatim scripts; two or more unannounced silences over 30 s; PIN, address or security question in the first 4 minutes; customer's name used by the agent).

## Known limits
- Calls are shorter (1-5 minutes) than the 16-22 minute Main calls.
- All S-Net (the tenant's brand), written by the same model that wrote the fine-tuned model's training data, so the key may favour the fine-tuned model.
