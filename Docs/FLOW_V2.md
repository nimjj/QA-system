# Flow v2: choosing what Laya sees by call structure (2026-10-19)

Status: **implemented, on by default when a fine-tuned checkpoint is served (`LAYA_CHECKPOINT`), off for stock Laya.** Switch explicitly with `LAYA_FLOW=v1|v2`. Code: `src/services/laya_windows.py`, used from `laya_inputs.build_laya_inputs`; one line in `dynamic_evaluator.py` (Paraphrasing fails without a model call when no restatement cue is found). Experiments: `Scripts/window_lab.py`, `Scripts/empathy_lab.py`; lab report `Docs/FLOW_V2_LAB.md`; regression report `Docs/FLOW_V2_REGRESSION.md`.

## Why
AG50 (50 calls of 10 to 20 minutes) showed fine-tuned Laya behind Ollama, and much of the loss happened before the model: the app cut small, phrase-gated snippets built for short calls. I measured where each criterion's evidence sits in those calls and rebuilt the windows. No retraining was needed for the gains below. Production has **customer-side sentiment only**, so nothing here uses agent sentiment.

## What changed (three checks)
| Check | Before | Flow v2 |
|---|---|---|
| Empathy | The 2 *most severe* of about 12 upset customer turns per call, each judged on the next 4 turns | **One window per distinct outburst** (a flagged customer turn after at least 4 calm customer turns; flagged = sentiment <= -15, or a frustration word whatever the score), the turn plus the next 4 turns, at most 4 windows. Fails if any window shows no acknowledgement |
| Paraphrasing | First 50 customer words + first 150 agent words | **Candidate + verify:** find agent lines with a restatement cue in the first 300 s ("so you're saying", "just to confirm", "what I'm hearing" ...). None found -> FAIL with no model call. Found -> the customer's problem statement + those lines |
| Ownership | Agent lines matching a phrase list | Wider list: "you'll have to ring/call/contact/write/email...", "nothing to do with me/us", "not our department/network/problem", "that's between you and", "take that up with", "ring/call/contact them", "nothing S-Net can do", and so on. "You'll have to wait" is deliberately not a deflection |

Unchanged: Probing, Resolved, Active listening, Rapport, and all rule-based items.

## Owner decision on Empathy
Asked whether Empathy should fail when the agent acknowledges frustration early but brushes off a later outburst, the owner chose **yes: every new outburst must be handled** (strict, per outburst). The AG50 answer key was written with a lenient rule (acknowledging once is enough), so some AG50 "false alarms" are real faults under the strict rubric (example: ag_04, the customer asks "Hello? Are you still there?" and the agent explains a slow screen with no acknowledgement). AG50's Empathy number is therefore a slight understatement of the strict-rubric result.

## Results (fine-tuned checkpoint `final-softce-3`, same cutoffs)
| | Today's flow (v1) | Flow v2 |
|---|---|---|
| **AG50**, 7 judged items matching the key (of 350) | 252 (72.0%) | **281 (80.3%)** |
| AG50 mean final-score error | 12.7 | **9.0** |
| AG50 time per call | 16.2 s | **15.4 s** |
| **Main**, items (of 44) | 41 | **42** |
| **Bulk** b_*, items (of 372) | 358 | **359** |

Per item on AG50 (balanced accuracy, v1 -> v2): Empathy 0.62 -> 0.82, Paraphrasing 0.58 -> 0.86, Ownership 0.79 -> 0.97.
Versus Ollama on AG50: judged items 80.3% against 78.6%, a difference of +1.7 points (95% interval -3.7 to +7.1, McNemar p = 0.58), so **the two cannot be told apart on this data**. Agreement beyond chance (kappa): 0.54 against Ollama's 0.42; score rank agreement 0.87 against 0.84; Ollama's scores sit 11.7 points too high on average, v2's 1.4.

## Limits that matter
- **AG50 is a development set.** The windows were designed after studying these 50 calls, so the AG50 gain (and especially the Ownership phrases, which I added after seeing the six lines the old list missed) is optimistic. **Main and bulk were not used to design flow v2** and did not regress; that is the cleaner evidence. A sealed new test set is still needed (AG-B in the plan).
- Two regressions were found and fixed on the way: the first version looked only for sentiment <= -15 and missed bulk's late outbursts (bulk 358 -> 347), and "you'll have to" matched "you'll have to wait". Both were caught only because Main and bulk were rerun.
- Empathy relies on customer sentiment or frustration words to find an outburst. If RoBERTa scores are flat on real calls, only the word list triggers it. Calls with no flagged turn pass Empathy without a model call.
- Remaining Empathy false alarms: some are model mistakes ("I do appreciate how frustrating..." scored as no acknowledgement, ag_09, ag_12) and some are bad triggers ("Phew, I was worried" is relief). Both need training data and a smarter trigger.
- **Not fixed by flow v2** (need training data and, for some, new windows): Active listening (the fine-tuned model gives P(repeat) of only 0.05 to 0.12 on all 9 true repeats it is shown; 6 of 15 never reach it), Rapport (31% of good AG50 calls fail), Probing (rejected cutoff change: it fits AG50 but gives 12 false fails on bulk), Resolved (the compressed tail window was no clear win).
- Every number is against an AI-written key (Antigravity for AG50, Claude for Main and bulk). None is human-reviewed.

## Freeze
The extractor hash in `laya-finetuning/data/frozen/checks_frozen.json` covers `laya_inputs.py`, `rule_engine.py` and `laya_windows.py` (tag `laya-inputs-frozen-v3`; `inputs_sha256` `49e61755fdb6...`). Training rows built before this still match the v1 extractors, which are unchanged and still used when `LAYA_FLOW=v1`. New training data for the v2 windows must be built with `LAYA_FLOW=v2`. The earlier tag `laya-inputs-frozen-v2` points at a commit whose `laya_inputs.py` lacked the v2 switch (a sync tool reverted the edit before it was committed; fixed in commit 91aea83), so use v3.

## Next steps
1. Antigravity briefs for **AG-T** (training calls) and **AG-B** (sealed test): agent sentiment absent, customer sentiment noisy, late acknowledgements, benign near-repeats in good calls, rude lines hidden in long polite calls.
2. Retrain for Active listening, Paraphrasing (echo vs restatement hard negatives), Rapport (long polite calls) and Empathy ("acknowledgement plus refusal" lines).
3. Run all engines on AG-B; human review of about 30 disagreements; shadow mode.

## Result folders
`inputs/Test (results)/<suite> (laya-ft-v2b)` is the final flow v2 run reported above. `(laya-ft-v2)` is the first version, kept as the record of the regression (bulk 347 of 372) it caused. `Laya probes/window_lab_*.json` and `empathy_lab_*.json` hold every probability used by the lab reports.

## Moving to another PC
See `laya-finetuning/docs/NEW_PC_SETUP.md`.
