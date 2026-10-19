# Generation notes (Phase 3 pilot -> Phase 5 full data)

What the pilot taught us, and the rules the full generation must follow. Written 2026-10-16 after running `tools/shortcut_probe.py` on `data/rows/pilot.jsonl` (240 rows, 20 matched pairs per trained check, 5 per regression check).

## How rows are made (unchanged)
Fragments in `data/fragments/claude/*.txt` -> `tools/build_rows.py` -> `data/rows/*.jsonl`. Each fragment runs through the frozen `build_laya_inputs` and is **dropped, with a logged reason**, if production would not send it to Laya as intended (gate not reached, more than one snippet, decision line missing, does not fit the 512-token window). Roughening (about 30%) is decided **per pair**, never per member, so it cannot leak the label.

## Gates that shape what can be written
| Check | What must hold or production never sends it |
|---|---|
| Active listening | the two questions look alike (difflib above 0.55) or the customer answers with "like I said / I told you / I already ..."; exactly one pair per fragment |
| Empathy | one upset customer turn (sentiment at most -15 and a drop of 8+ from the customer's own earlier turns); **no agent line in the next 3 turns may contain sorry, apologize, understand, frustrating, apologies, "let me help"** (production treats those as already empathetic); no second upset turn |
| Ownership | an agent line contains one of the ~30 deflection phrases |
| Probing | the agent asks at least one question (no questions = fails without the model) |
| Rapport | one chunk of up to 8 agent lines / 120 words per fragment (or mark the rude line and the builder picks its chunk) |
| Resolved | the decision line is within the last 10 lines |
| Hostility / Escalation | whole call must fit the window |

## Shortcut findings at pilot size (bag-of-words / length-only balanced accuracy, 5-fold grouped by pair)
| Check | BoW | Length | Read |
|---|---|---|---|
| Rapport | 0.60 | 0.57 | good: the same trigger words appear on both sides |
| Active listening | 0.65 | 0.57 | good |
| Paraphrasing | 0.80 | 0.72 | acceptable, watch it (restatements say "so", "is that right", "correct") |
| **Empathy** | 0.88 | **0.88** | **length shortcut**: warm replies are long, cold replies are short |
| **Confirmed resolved** | **0.93** | 0.68 | **word shortcut**: PASS endings say "resolved/fixed/yes", FAIL endings never do |
| Probing, Escalation, Hostility, Ownership | 0.80-1.00 | 0.60-0.90 | only 5 pairs each, too noisy to read |

## Rules for the full generation (Phase 5)
1. **Balance length per label.** For every check, PASS and FAIL snippets must have overlapping length distributions (target: mean word count within 10% of each other). Empathy needs long cold replies (a long procedural or dismissive explanation) and short warm ones ("That sounds awful. Let's fix it.").
2. **Break the lexical markers with hard cases (at least 30% of each check):**
   - Resolved: FAIL endings that *contain* "resolved" or "fixed" (agent says "I'll mark it resolved on my side", customer says "it's not fixed"); PASS confirmations phrased without those words ("So everything's working for you again?" "Yes.").
   - Paraphrasing: restatements without a trailing "is that right?"; echo questions that end with "right?" or "correct?" ("It's the router, correct?").
   - Empathy: warm replies without the common warm words, cold replies containing "I hear you" used as a brush-off.
   - Rapport / Ownership / Hostility / Escalation: polite and rude lines of the same length and with the same trigger words.
3. **Pairs stay matched** (same customer opening, same call, only the decision differs) and a pair is never split across train, dev and test.
4. **Variety matrix:** 12 industries (half S-Net telecom), 8 agent personas, short / mid / long, customer moods; rotate so no persona or industry predicts a label.
5. **Regression checks need at least 100 rows each** at full size (the pilot has 10), with the same pairing rules.
6. Re-run `tools/shortcut_probe.py` on the full set. Above 0.85 is a warning for every check and a **hard fail for Rapport and Paraphrasing** (regenerate those).
