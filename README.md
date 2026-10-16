# Fine-tuning Laya to replace Ollama in the QA grading pipeline

**Document status:** review copy for the AI/ML engineer, written 2026-10-16. Everything below is marked **Done**, **In progress** or **Planned**. Section 9 lists the specific points we want challenged. `docs/DATA_PLAN.md` is the working copy of the phase table and data volumes; if the two ever differ, this README is the one reviewed.

## 1. One-paragraph summary

We grade telephony-support calls against 11 criteria with a service (`qa-analysis`) that combines deterministic Python rules with **Laya**, a local, non-generative yes/no classifier (ModernBERT-large encoder, 421M parameters, English checkpoint). Ollama/llama3.1 was removed in version 10. In a first test on 4 hand-written calls Laya made more mistakes than Ollama (mean score error 11.7 after pipeline fixes vs Ollama's 9.2). We propose a **full fine-tune of Laya's English checkpoint on synthetic, extractor-built examples** for the five checks where it is weak, with replay data and regression checks to avoid breaking the rest, and an **independent test set written by a different LLM (Gemini) and labelled by hand**. There are no real call transcripts and no way to get any, so every result will be reported as "good on realistic synthetic calls", not "proven on real calls". Training runs on a Colab L4 GPU (about 15 minutes per run, measured); serving stays on CPU.

## 2. The system and where Laya sits

`POST /api/evaluate` (FastAPI, synchronous) parses a transcript (turns with speaker, start time, per-turn sentiment score) and grades it:

| Criterion | Decided by | Deduction if FAIL | Category (weight) |
|---|---|---|---|
| Branding and Survey Check | rule (exact phrases in first/last 4 agent lines) | 15 | Soft Skills (0.333) |
| Hold time and Dead Air | rule (gaps >30 s, announced holds exempt) | 15 | Soft Skills |
| Personalized the call | rule (customer name appears in an agent line) | 15 | Soft Skills |
| **Empathy & Acknowledgment** | **Laya** | 35 | Soft Skills |
| **Build rapport / professionalism** | **Laya** | 20 | Soft Skills |
| **Paraphrasing** | **Laya** | 15 | Technical Knowledge (0.667) |
| Verified customer | rule (PIN/address/security question in first 240 s) | 25 | Technical Knowledge |
| **Probing** | **Laya** | 25 | Technical Knowledge |
| **Took ownership** | **Laya** | 25 | Technical Knowledge |
| **Active listening** | **Laya** | 10 | Technical Knowledge |
| **Confirmed the issue is resolved** | **Laya** | 15 | Technical Knowledge |

Each category starts at 100 and loses the deduction per FAIL; final score = Soft x 0.333 + Technical x 0.667. Agent profanity auto-fails to 0. Escalation and Hostility also have Laya questions but are not in the reference criteria set. Tenants can add custom criteria; those go to Laya as generic questions built from the criterion's name and description.

**How Laya is used.** For each check a Python pre-filter cuts a short text snippet from the call (Laya's English checkpoint reads at most 512 tokens including the question), and Laya answers one yes/no question about it in one forward pass, returning P(yes). The service applies a per-check cutoff to P(pass) (P(yes) when "yes" means PASS, else 1 - P(yes)). Laya cannot generate text, so coaching strings are static.

**The model input contains the question text.** Laya's input is `[CLS] noul question: <instructions> [SEP] [MASK] <false-option text> [MASK] <true-option text> [SEP] <snippet> [SEP]`. The instructions and the two option texts (the "criteria") are therefore part of what a fine-tuned model learns. For four of the questions (Empathy, Ownership, Probing, Confirmed resolved) the options carry neutral labels A/B because on the English checkpoint the default "true"/"false" labels can outweigh the text. **Changing any question wording after training data is generated invalidates the data.**

## 3. Evidence so far

All numbers are from `qa-analysis/Docs/LAYA_TEST_LOG.md` and `laya-test/qa_eval/RESULTS.md`.

**Main tests (4 hand-written 16-22 minute calls, expected grades written by Claude, not human-reviewed)**

| | Items matching expected (of 44) | Mean score error | Time per call |
|---|---|---|---|
| Ollama (llama3.1 + embeddings) | 40 (91%) | 9.2 | ~6.4 min |
| Laya, first run | 34 (77%) | 16.3 | ~8.5 s |
| Laya, after Round 2 pipeline fixes ("v2") | 36 (82%) | 11.7 | ~8.5 s |

Laya v2 still ranks the Excellent call (78.3) below the Good call (83.4). On the 35 `b_*` bulk calls (defect named in the file name) v2 matched 348/372 items (94%).

**Where Laya is weak (measured on those calls, small samples):** Active listening (Round 2 made it worse: attaching the customer's "like I said" reply to the pair lowered the repeat score from 0.89 to 0.51, and a status re-check was rated a repeat), Confirmed resolved (scores barely separate: no-confirmation endings 0.66-0.75, confirmed 0.47-0.79; no cutoff is good), Paraphrasing (cannot tell restating the problem from echoing its words), Build rapport (condescension without insults rated polite), Empathy (right order, gap too small for one cutoff). **Working:** Took ownership (0.81 vs 0.29), Probing (once the input was fixed), Hostility, Escalation.

**Earlier synthetic benchmark (320 hand-written snippets, 8 criteria, no training, balanced accuracy on an 18-item test half per criterion):** Laya English 0.82 average vs Ollama 0.79, with the two failing on different criteria. Interval about +/-15 points; synthetic and unreviewed, so optimistic.

**Fine-tuning evidence from Laya's own docs:** on their typed-decisions benchmark a full fine-tune moves accuracy from 0.36 to 0.77-0.79; on MASSIVE intent from 0.73 to 0.94. Those are different tasks and far more data than we have.

## 4. Goal and success criteria

Goal: a fine-tuned English checkpoint that matches or beats Ollama on grading accuracy so Ollama can be fully retired.

Proposed final criteria (all on synthetic data; cutoffs are re-tuned on dev data and the test set is scored once):

1. **Main calls:** mean score error against the answer key is below Ollama's and at most 9.0, and the 4 calls rank in strict tier order. *The key is currently Claude-written and unreviewed (section 7), so this is a sanity gate, not the headline.*
2. **Trained checks, independent test set:** balanced accuracy at least 0.85, with the lower 95% bound at least 0.75.
   - **2b. Rapport at call level:** at most 5% of ~20 held-out full polite calls fail Rapport (reported with its interval; 0 of 20 still allows a true rate near 14%).
3. **Regression checks:** test balanced accuracy no more than 0.05 below the untouched model, with no significant paired drop; bulk `b_*` items at least 348/372.
4. **Unlabelled real-looking calls** (`real_long_*`, `v8_*`): scores keep tier order (Spearman at least 0.8).
5. **Drift:** at least 90% agreement with the untouched model on generic (custom-criteria) questions.
6. **Calibration:** ECE at most 0.10 on the Gemini dev slice (reported).
7. **Speed:** at most 15 s per 20-minute call on CPU.

## 5. Proposed approach

### 5.1 What is trained
- **Full fine-tune** of the English checkpoint (`convaiinnovations/laya`, revision `7b928d828b7b0e022f929d9bd2e44165aa270148`, the snapshot used locally): same architecture and 421M parameters, new values, saved as a **new checkpoint folder**. The original is never overwritten; its sha256 is verified at every stage.
- Trained with Laya's own `laya-train` (v0.4.0, commit `3cf26cb`), not custom code, on JSONL rows `{state, questions, expected | gold}`.
- Checks to train (priority from the test log): **Active listening, Confirmed resolved, Paraphrasing, Rapport, Empathy.** Regression-only (included so training does not damage them): **Ownership, Probing, Hostility, Escalation.** Rule-based checks are not touched.

### 5.2 Inputs: one source of truth
`qa-analysis/src/services/laya_inputs.py::build_laya_inputs(transcript)` builds every Laya input; production and the data tools both call it, so training rows contain exactly what the model sees in production. **Done:** moving it out of the evaluator changed nothing (byte-identical inputs across 80 sample calls). The frozen questions and their inputs:

| Check | Input text (cap) | Cutoff on P(pass) | yes means |
|---|---|---|---|
| Empathy | up to 2 snippets, each an upset customer turn + next 4 turns; one Laya call per snippet; one FAIL fails | 0.78 | PASS |
| Rapport | **all agent lines** in chunks of at most 8 lines / 120 words; one Laya call per chunk; one rude chunk fails | 0.50 (interim, see 7) | FAIL |
| Paraphrasing | customer problem (<=50 words) + first 10 non-setup agent lines (<=150 words) | 0.50 | PASS |
| Probing | customer problem (<=50 words) + agent question sentences (<=100 words, boilerplate removed) | 0.70 | PASS |
| Ownership | agent lines containing a deflection phrase (gate still in place) | 0.52 | FAIL |
| Active listening | up to 3 pairs: *first question / customer's answer (<=40 words) / second question*, pairs of question sentences with difflib ratio > 0.55 or that the customer answered with "like I said" | 0.19 | FAIL |
| Confirmed resolved | last 10 lines | 0.73 | PASS |
| Escalation / Hostility | whole call (windowed `predict_long` if over 512 tokens) | 0.47 / 0.79 | FAIL |

The exact question and option texts are exported to `data/frozen/checks_frozen.json` with a sha256; every training row records the hash. The Ownership phrase gate (about 30 phrases) has the same blind-spot as Rapport had; it is a known limitation and not changed in this phase.

### 5.3 Data (all synthetic)
- **Train/dev (written by Claude):** wide variety across about 12 industries (half S-Net telecom), 8 agent personalities, short/mid/long calls, customer moods, and speech-to-text-style roughening on about 30% (scripted and reproducible). Every example is produced by running a generated call through `build_laya_inputs`; fragments that never reach a check's gate are logged.
- **Matched pairs** so the model learns the skill, not trigger words: restate vs echo the customer's words; rude vs polite lines containing the same words ("obviously", "as I said"); warm vs cold reply to the same upset turn; re-asked information vs re-checked changing status; explicit resolution check vs call that just ends. About 40% hard cases, 50/50 PASS/FAIL.
- **Independent test set:** written by **Gemini** (a different model, to reduce shared style), generated from scenario cards, **labelled blind by a human**. Gemini's intended labels are stored separately for an agreement check. Also about 20 full polite calls for the Rapport call-level false-positive test.
- **Replay rows (drift guard):** about 300 rows with generic custom-criteria questions (as built by `_batch_check`), with the **untouched model's own probabilities as soft targets** (`gold`), so the fine-tune does not drift on tenant-defined criteria.
- **Splits are by call and by pair, never by row** (union-find on `call_id` and `pair_id`). The test file is sealed until the final evaluation.

| Check | Role | Train | Dev (Claude) | Gemini dev | Gemini test |
|---|---|---|---|---|---|
| Rapport (chunks) | train | 500 | 100 | 35 | 60 (+20 full polite calls) |
| Paraphrasing | train | 500 | 100 | 35 | 60 |
| Active listening | train | 400 | 80 | 35 | 50 |
| Confirmed resolved | train | 400 | 80 | 35 | 50 |
| Empathy | train | 400 | 80 | 35 | 50 |
| Ownership | regression | 150 | 40 | - | 30 |
| Probing | regression | 150 | 40 | - | 30 |
| Hostility | regression | 100 | 30 | - | 20 |
| Escalation | regression | 100 | 30 | - | 20 |
| Replay | drift guard | 300 | 50 | - | - |
| **Total** | | **3,400** | **630** | **175** | **370 + 20 calls** |

**Validation before training:** schema; token-budget check with the real tokenizer and question head (`laya-train` truncates a too-long state silently and `--dry-run` does not report it); 50/50 balance; near-duplicates across splits; length and trigger-word balance per label; frozen-hash match; and a **shortcut probe**: a bag-of-words classifier trained on dev must not exceed 0.85 balanced accuracy per check (warning for every check, hard fail for Rapport and Paraphrasing).

### 5.4 Training recipe (planned; speed measured)
- Two runs, keep the better on dev: **R1** `--loss soft-ce --label-smoothing 0.05`; **R2** `--loss rlcd` (Laya's policy-gradient + soft cross-entropy objective). Both: 4 epochs, micro-batch 8 x grad-accum 8 (effective 64), encoder lr 2.5e-5, head lr 1e-4, AdamW with cosine schedule, weight decay 0.01, gradient clip 1.0, fp16 autocast with gradient checkpointing, `max_len 512`, `head_max_len 192` (same as serving), seed 0 (more seeds if time allows), `--eval` on dev.
- `laya-train` holds out min(400, 10%) of the training items before training and fits one temperature per question type on them; this slice **includes replay rows** (about 9% of it). A shared per-type temperature never changes which of two calls scores higher, and every check's cutoff is re-tuned afterwards on Gemini dev, so verdicts do not depend on it. If ECE misses 0.10 we train through `laya.train.finetune` with a calibration split restricted to the nine frozen questions.
- **Measured (smoke test, L4):** 13.7 items/s at 367 mean state tokens; a 3,400-item x 4-epoch run is about 15 minutes plus about 2 minutes of load/save. Checkpoints are fp16, about 0.84 GB.
- **Known laya 0.4.0 bug:** `finetune()` evaluates before training while the model is still on the CPU, so it crashes on any GPU ("tensors on the same device ... index_select"). `tools/laya_train_cuda.py` wraps it (moves the model to the device first; installed package not edited). Verified on CPU with a simulated device mismatch, and then on the Colab GPU.
- Output goes to `/content` and a watcher copies `checkpoint_latest/` to Drive only when its files have stopped changing for 30 s and the epoch-end log line has appeared, via a temp folder and rename.

### 5.5 Cutoffs and evaluation
- After training, every check's cutoff is re-tuned on **Gemini dev** (not on Claude dev, which shares the training data's style). Rapport's cutoff is tuned **at call level**: best chunk balanced accuracy subject to at most 5% of polite full calls failing.
- The test set is then scored **once**. Reported per check: balanced accuracy with 95% bootstrap intervals resampled by call; paired comparison with the untouched model on regression checks; ECE; replay agreement. Also re-run `batch_test.py main` and `bulk` through the service and compare scorecards with Ollama and earlier Laya runs.
- If decisions are made on the test set more than once, a fresh Gemini test set is generated.

### 5.6 Integration
`qa-analysis/src/services/laya_adapter.py` serves a fine-tuned folder when the environment variable `LAYA_CHECKPOINT` is set (served under the `english` name); unset means the stock checkpoint. **Done and tested** on CPU through the real adapter. New cutoffs are committed to `LAYA_CHECKS`.

## 6. Phases and status

| Phase | What | Status |
|---|---|---|
| Plan A | Smoke test: install, download, dry-run, 1-epoch train on 20 rows, reload, predict, save to Drive, load locally on CPU through the adapter | **Done** (passed 2026-10-16) |
| 0 | Answer key for the 4 Main calls | **Done, with a caveat**: key is Claude-written and **not human-reviewed** (section 7) |
| 1 | Remaining pipeline input changes + freeze | **Done** 2026-10-16: frozen at `qa-analysis` tag `laya-inputs-frozen-v1` (commit `53becd8`), `inputs_sha256` `66deff95a20c...` in `data/frozen/checks_frozen.json` |
| 2 | Labelling guide (PASS/FAIL per check, examples, hard-case types, "unsure" rule) | Planned |
| 3 | Generator + pilot of about 240 items for human skim | Planned |
| 4 | Gemini test set: prompts and scenario cards, imported and validated; human labels about 545 items | Planned |
| 5 | Full generation to the volumes above | Planned |
| 6 | Validation (incl. shortcut probe) | Planned |
| 7 | Split by call and pair; seal test | Planned |
| 8 | Baseline of the untouched model on dev, Gemini dev and test | Planned |
| 9 | Training R1/R2 on Colab | Planned |
| 10 | Evaluation, test scored once | Planned |
| 11 | Integration, re-run Main and bulk | Planned |
| 12 | Iteration (error analysis on dev only) | Planned |
| 13 | Report: "good on realistic synthetic calls" | Planned |

Elapsed estimate 3-4 weeks; the human's time is about 14-16 hours (section 8).

## 7. What has been done (facts)

- **Smoke test passed**, run `smoke-20261016-0848` (details in `runs/smoke-20261016-0848/RESULT.md`): base weights downloaded and hash-matched to the local copy; 1 epoch on a Colab L4; checkpoint copied to Drive with verification; reloaded two ways with identical output; served on CPU through `laya_adapter` with a largest difference from the GPU of 0.0057 (tolerance 0.03); original weights verified unchanged.
- **Phase 1 code** (`qa-analysis`, branch `version-10.2-laya-finetune`): `fcc6869` refactor (no behaviour change, proved by byte-identical inputs on 80 calls); `9050b41` Rapport chunk scan (mean 7.9 chunks per call, max 21), Active-listening first-question/answer/second-question snippet and 0.55 similarity (calls with an Active-listening snippet rise from 8 to 19 of 80), Probing cutoff 0.60 to 0.70; `53becd8` interim Rapport cutoff, Round 3 results and docs. Tagged `laya-inputs-frozen-v1`. Self-checks pass.
- **Phase 1 baseline of the untrained model** (full detail in `qa-analysis/Docs/LAYA_TEST_LOG.md`, Round 3; answer key is Claude-written):

  | | Ollama | Laya v2 | Laya v3.1 (final Phase 1) |
  |---|---|---|---|
  | Main items matching (of 44) | 40 | 36 | 37 |
  | Main mean score error | 9.2 | 11.7 | 13.3 |
  | Bulk `b_*` items matching (of 372) | n/a | 348 | 351 |
  | Time per Main call (CPU) | ~6.4 min | ~8.5 s | 22.4 s |

  Probing is now 34/34 on bulk (was 30/34) and Active listening 33/33 (was 30/33). The mean score error rose although more items are right, because two wrong answers on Main call 3 used to cancel. **Rapport: the untrained model has no signal on the chunk question.** Across all 44 labelled calls the highest chunk P(rude) is 0.19-0.22 for rude and polite calls alike (rude calls 0.199-0.217, median polite 0.198), so no cutoff separates them; the first cutoff (0.81) sat on that floor and failed 29 of 33 polite bulk calls. The cutoff is therefore an interim 0.50 that never fails a call until the model is fine-tuned. Active listening has a thin margin (planted repeats 0.82-0.85, all other calls 0.55-0.81, cutoff 0.81) and still misses the genuine repeats in Main call 2.
- **The freeze:** `inputs_sha256` covers the nine question texts, which answer means PASS, the word caps, and the source of `laya_inputs.py` and `rule_engine.py`. Cutoffs are deliberately excluded because they are re-tuned after training. `tools/export_checks.py --check` fails if any of it changes; training data built before such a change must be regenerated.
- **Phase 0 answer key is not human-reviewed.** Two review spreadsheets were produced for the 4 Main calls; both came back with notes written by an assistant that had Claude's grades ("Claude:" / "Claude (not human):"), so neither is an independent human check. Three contested items were re-read by Claude and all stood. `docs/PHASE0_ANSWER_KEY.md` and `data/review/answer_key_main.json` record this. Ollama's 9.2 and Laya's 11.7 are therefore measured against Claude-written grades. Open requirement question: should Active listening also fail an agent who ignores what the customer already said, not only one who re-asks a question?

## 8. Who does what: the steps only the human owner (Nimithra) can do

Claude (the assistant doing the build) cannot press Run in Colab, cannot use Gemini, and cannot supply human judgement. There is **no Gemini CLI**: she runs Gemini by hand in its chat.

| # | When | Action | Time |
|---|---|---|---|
| 1 | End of Phase 1 | Okay the frozen question wording and cutoffs | **done** 2026-10-16 |
| 2 | Before Phase 2 | Decide the Active-listening definition (above) | 5 min |
| 3 | Phase 2 | Approve the labelling guide | ~1 h |
| 4 | Phase 3 | Read the ~240-item pilot; flag disagreements | ~1 h |
| 5 | Phase 4 | **Run Gemini**: paste each batch prompt (about 25-30 batches of ~10 short call excerpts), save each reply unedited as `data/fragments/gemini/raw/batch_NN.json`; an import script validates them and names any scenarios to re-ask | ~2 h |
| 6 | Phase 4 | **Label the ~545 Gemini items herself** and skim ~20 full polite calls | ~7-8 h |
| 7 | Phase 6 | Read the validation report | 15 min |
| 8 | Phases 8, 9, 10 | Press Run in the three Colab notebooks and paste summary lines back | ~30 min each |
| 9 | Phase 9 | Download the trained checkpoint from Drive | 10 min |
| 10 | Phase 10 | Go / no-go on results | 15 min |
| 11 | Phase 11 | Review re-run Main and bulk scorecards | 30 min |
| 12 | Phase 13 | Approve the report | 15 min |

Item 6 is the load-bearing one: the final claim holds only if those labels are genuinely human judgement. The earlier review files show the failure mode (an assistant filling the sheet from Claude's grades makes the result circular).

## 9. Risks, limitations and what we want the ML engineer to challenge

1. **Full fine-tune vs something lighter.** 421M parameters on about 3,400 synthetic rows for 4 epochs. Is full fine-tuning right, or would head-only (`--freeze-encoder`, which Laya documents as gaining much less), a lower encoder learning rate, fewer epochs, or early stopping on dev be safer against overfitting to synthetic style? We plan R1/R2 and dev-based selection only.
2. **Synthetic-to-real gap and style shortcuts.** All training text is written by one LLM family. Mitigations: variety matrix, matched pairs, speech-to-text noise, a different-model test set, a bag-of-words shortcut probe. Are these enough, and is 0.85 the right probe threshold?
3. **Replay as a drift guard.** Soft targets from the untouched model on ~300 generic questions. Is that adequate, or should the replay set be larger or cover more question styles? Is it sound that replay rows enter the calibration slice?
4. **Label noise and size of the independent test set.** 50-60 test items per check gives a balanced-accuracy interval of about +/-0.09. Is that enough to claim 0.85? The labels also come from one person.
5. **Rapport aggregation.** The untrained model scores every chunk 0.19-0.22, so training must create the signal first. "One rude chunk fails the call" over about 8 chunks per call multiplies false positives; we address it by tuning the cutoff at call level against full polite calls (target at most 5%, only ~20 calls). Is a better aggregation (max vs mean vs top-k, overlapping chunks, customer context in the chunk) worth trying?
6. **Latency.** Rapport now makes about 8 Laya calls per call (up to 21). Measured: 22.4 s per Main call on CPU (bulk mean 12.8 s) against a 15 s target. Batching the chunks into one forward pass is the planned fix; is that safe for ModernBERT at 512 tokens, or would you cache or shorten chunks instead?
7. **Active listening is under-defined** (re-asked question vs ignored statement) and its input is a question pair plus one customer answer, which may be too little context for "already gave in their answer".
8. **Answer key for the 4 Main calls is LLM-written.** The headline claim therefore rests on the Gemini test set labelled by hand, not on the Main calls.
9. **Calibration.** One temperature per question type is fitted on at most 400 held-out items (including replay). Cutoffs are re-tuned per check afterwards. Is per-check calibration needed?
10. **Reproducibility.** One seed planned for the main comparison; more seeds only if time allows. Is a seed ensemble or a paired seed comparison needed to trust a 0.02-0.05 difference?
11. **Tooling risk.** `laya-train` v0.4.0 needs a wrapper to run on a GPU (section 5.4). Anything else in it you would distrust (silent state truncation, the `--eval` path, the shared calibration clamp)?
12. **Ownership still uses a phrase gate** (the same weakness Rapport had). Out of scope for this phase; should it be fixed before generating its regression data?

## 10. Environment and reproducibility

| Where | What |
|---|---|
| **Google Colab (L4 GPU, ~23 GB)** | notebooks `0x_*.ipynb`: install, download base, train, evaluate. Pinned: laya commit `3cf26cb`, transformers 5.16.1 |
| **PC (CPU, Windows)** | `tools/*.py` and the `qa-analysis` service. No NVIDIA GPU |
| **Google Drive** `MyDrive/laya-finetuning/` | checkpoints, datasets, run reports (Colab's disk is wiped at session end) |
| **Git (this repo)** | notebooks, tools, prompts, docs, small data. Never weights |

Branches: this repo `plan-a-smoke-test`, `phase-0-ground-truth`; `qa-analysis` `version-10.2-laya-finetune`.

Tools in `tools/`: `export_checks.py` (freeze the production questions with a sha256; `--check` detects drift), `smoke_rows.py` / `smoke_cells/` / `build_smoke_notebook.py` (the smoke test), `check_local_load.py` (CPU check through the adapter), `laya_train_cuda.py` (GPU workaround), `make_review_sheet.py` and `pick_review_subset.py` (Phase 0 sheets). In `qa-analysis/Scripts/`: `dump_laya_inputs.py` records every Laya input without a model and compares two code versions.

Run the smoke test: open `00_smoke_test.ipynb` on Colab, run cells top to bottom (each starts with an "EXPECT" comment), download the `final/` folder and `smoke_preds_ft.json` from Drive into `checkpoints/<run id>/`, then

```powershell
..\qa-analysis\.venv\Scripts\python.exe tools\check_local_load.py `
  --checkpoint checkpoints\<run id>\final --preds checkpoints\<run id>\files\smoke_preds_ft.json
```

To serve any fine-tuned checkpoint in `qa-analysis`, set `LAYA_CHECKPOINT` to its folder before starting the service. `.env` is never edited.

## 11. Rules that keep the data honest
- Question wording and every extractor are **frozen** before data is generated; changing one means regenerating.
- Training inputs come only from `build_laya_inputs`, never written by hand.
- Splits are by call and by pair. The test set is generated by a different model, labelled by a human, and scored once.
- The original checkpoint is never modified; every checkpoint records its base revision and hashes in a manifest.
