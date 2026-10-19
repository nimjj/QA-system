# Stage 3 training run `ft2-20261017-0354` (Colab L4) and real-pipeline check

Data: train 1,796 rows (incl. 360 padded, 167 natural-call, 250 replay), dev 419, test 396, test_long 180, test_calls 40. **All Claude-written and Claude-labelled; not independent.** Winner on dev: `softce` (Drive: `MyDrive/laya-finetuning/checkpoints/ft2-20261017-0354/final-softce`). The executed notebook with all outputs is `01_train_eval.ipynb`.

## Notebook test results, balanced accuracy (untouched -> softce)
Rapport 0.50 -> 0.88 [0.80, 0.95]; Paraphrasing 0.73 -> 0.97; Active listening 0.50 -> 0.97; Resolved 0.52 -> 0.98; Empathy 0.52 -> 1.00; regression checks 0.54-0.83 -> 0.96-1.00.
Natural-call test (n=40 rows, wide intervals): Rapport 0.94, Paraphrasing 0.90, Resolved 0.73. ECE 0.052 (untouched 0.136). Replay: same verdict as untouched model on 82% of custom-criteria questions (target 90%: not met).

## Real pipeline (`qa-analysis`, service on CPU, `LAYA_CHECKPOINT` set, cutoffs `FINETUNED_CUTOFFS`)
| | Ollama | Laya v2 | untrained v3.1 | fine-tuned |
|---|---|---|---|---|
| Main items (of 44) | 40 | 36 | 37 | **41** |
| Main mean score error | 9.2 | 11.7 | 13.3 | **8.75** |
| Bulk b_* items (of 372) | n/a | 348 | 351 | **358** |
| Time per Main call | ~6.4 min | ~8.5 s | 22.4 s | 21.4 s |

Progress across rounds (Main items / error / bulk): stage 1 35 / 16.3 / 354; stage 2 36 / 15.4 / 356 (not retuned); stage 3 39 / 12.9 / 358 with the old cutoffs, 41 / 8.75 / 358 with the new ones.

## Limits
- Whole project is Claude-authored: data, test sets and the Main/bulk answer key. No human-labelled number exists.
- The Rapport cutoff 0.20 was chosen on the Main/bulk calls; they are no longer independent. Rapport still marks dismissive lines in the ownership/empathy-defect bulk calls as rude.
- Speed target (15 s per call) not met; Active listening and Probing each miss one Main item.
