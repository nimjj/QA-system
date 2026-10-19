# Stage 1 training run (Colab L4, 2026-10-16) - first fine-tune

Data: train 1,269 rows (1,019 supervised + 250 replay), dev 273, test 396. **All Claude-written and Claude-labelled; not independent.**
Run folder on Drive: `MyDrive/laya-finetuning/checkpoints/smoke-20261016-0848/` (Colab reused the smoke test's run id). Variants: `final-softce` (winner on dev), `final-rlcd`.

## Held-out test set (unseen industries/personas), balanced accuracy at the dev-tuned cutoff [95% interval by pair]

| Check | Untouched | soft-ce | rlcd |
|---|---|---|---|
| Rapport | 0.50 | 0.90 [0.82, 0.97] | 0.92 |
| Paraphrasing | 0.73 | 0.97 [0.92, 1.00] | 0.98 |
| Active listening | 0.50 | 0.90 [0.80, 0.98] | 0.97 |
| Confirmed resolved | 0.52 | 0.97 [0.92, 1.00] | 0.98 |
| Empathy | 0.52 | 0.98 [0.95, 1.00] | 1.00 |
| Ownership / Probing / Hostility | 0.83 / 0.83 / 0.54 | 1.00 / 1.00 / 1.00 | 1.00 |
| Escalation | 0.62 | 0.96 | 1.00 |

ECE 0.022 (untouched 0.136). Replay: same verdict as the untouched model on 80% of custom-criteria questions (target 90%).

## What the real pipeline showed (probe of the Main + bulk calls with `final-softce`, old cutoffs)
- Bulk items correct 354/372 (untrained v3.1: 351, Laya v2: 348); Main 35/44, mean score error 16.3 (v3.1: 13.3, Ollama: 9.2).
- The tuned model is very confident (P near 0.03 or 0.97) and **falsely flags polite real Rapport chunks as rude** (45 of 380 chunks, 13 of 37 labelled calls fail Rapport wrongly).
- Cause found: the training snippets were about half the length of real ones (words: Rapport 44 vs 86, Paraphrasing 58 vs 164, Resolved 52 vs 101, Active listening 37 vs 84, Probing 43 vs 114). Stage 2 pads Rapport/Paraphrasing/Resolved pairs with neutral agent lines (`tools/build_long.py`) and reports a separate padded test (`test_long`).

## Stage 2 (padded rows) and stage 3 (natural calls)
- Stage 2 (`tools/build_long.py`, run `ft2-20261016-1722`): padded Rapport/Paraphrasing/Resolved pairs. Padded-test BA: Rapport 0.92, Paraphrasing 0.98, Resolved 0.98 (untouched 0.50 / 0.65 / 0.52). Real Main+bulk probe with `final-softce` of that run: Main 36/44, mean score error 15.4 (13.8 with Rapport switched off and notebook cutoffs), bulk 356/372 (363 with those settings). Still fails polite natural Rapport chunks in 3 of 4 Main calls.
- Stage 3 (`tools/build_calls.py`, `data/fragments/claude/calls_*.txt`): 44 train / 6 dev / 8 test complete natural-sounding calls written by Claude, snippets cut by the extractors (167 / 31 / 40 rows; train PASS rows capped at 2x FAIL so natural style cannot predict PASS). Note: this data was written AFTER seeing which kinds of lines the stage-2 model got wrong on the Main/bulk calls, so the Main/bulk calls are no longer a clean check (no text from them was copied).
