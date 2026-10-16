# Plan B: full training plan

Status: approved by Nimithra. Plan A (the smoke test) comes first; this plan starts after it passes.
Times: **me** = working sessions, **you** = Nimithra's effort. ⏸ = you review before the next phase starts.

## Context
After the Round 2 pipeline fixes, Laya's mean score error on the 4 Main calls is 11.7, against Ollama's 9.2, and Laya still ranks the Excellent call below the Good one (`qa-analysis/Docs/LAYA_TEST_LOG.md`). The goal is a fine-tuned copy of the English checkpoint (same 421M weights, new values, saved as a new checkpoint) that matches or beats Ollama, so Ollama can be retired. There is no real call data, so every result is "good on realistic synthetic calls".

## Decisions made
- Rapport uses a **chunked scan** of all agent lines. The 27-phrase gate goes away.
- This folder is the repo **nimjj/laya-finetuning**, which must be **private** (checked: it was public at the time of writing; you switch it in GitHub Settings, and nothing is pushed until you confirm).
- Review load: the **lighter** one (table below).

## Where this plan differs from the original brief
| # | Brief says | Evidence | Change |
|---|---|---|---|
| 1 | Pipeline fixes come first | Already done in Round 2 | Phase 1 is only the *remaining* input changes |
| 2 | Active listening is "working" | Round 2 made it worse (Main 2/4, bulk 30/33); the log ranks it #1 to train | Move it to **train** (400/80). The snippet must include the customer's first answer |
| 3 | Hostility and Escalation at 150/40/40 | Not in `criteria_config.json`, so never scored by the Main or bulk tests | Smaller (100/30/20); they guard against forgetting |
| 4 | Train only on the 9 questions | A full fine-tune can drift on tenant-defined criteria (generic questions from `_batch_check`) | ~300 **replay rows** with the base model's own probabilities as soft targets |
| 5 | The local checkpoint is "the original" | Local snapshot `7b928d82…`; Laya's built-in pin is `55cf4c4e…` | Colab downloads revision **`7b928d82…`** and checks the sha256 against the local file |
| 6 | Score error against today's expected files | Written by Claude, not reviewed | You review the 4 Main scorecards first; **Ollama's error is recomputed** against the reviewed version |
| 7 | Tune cutoffs on Claude dev | Same style as training data | Tune on a small **Gemini dev** slice you label |
| 8 | Synthetic data assumed fine | Style shortcuts are the main risk | **Shortcut probe** in validation (warning for every check; hard gate for Rapport and Paraphrasing) |

## Phases
| Phase | What | Depends on | Time | Gate |
|---|---|---|---|---|
| **0. Ground truth** | You review the 4 Main expected scorecards (44 verdicts) with a sheet I prepare. I re-score Ollama, Laya-v2 and Laya-before against the reviewed version. That sets the real bar | Plan A | you 1.5–2 h, me 1 h | ⏸ you sign off the 44 verdicts |
| **1. Remaining input changes** (qa-analysis) | **a.** One `build_laya_inputs(payload)` used by production *and* the data tools (proof: byte-identical inputs to `probe_laya-v2.json`). **b.** Rapport chunked scan: all agent lines in chunks of ≤8 lines / ≤120 words, FAIL if any chunk is rude. **c.** Active listening snippet = "Agent asked Q1 / Customer answered A1 / Agent later asked Q2"; similarity cut 0.70 → ~0.55. **d.** Probing cutoff 0.60 → 0.70. **e.** Re-run `batch_test.py main` and `bulk` as `laya-v3` = the untrained baseline. **f.** **Freeze:** export `checks_frozen.json`, tag the commit | 0 | me 1–1.5 days, you 1 h | ⏸ you approve wording and snippets. After this, **no extractor or wording change without regenerating data** |
| **2. Labelling guide** | `docs/LABELLING_GUIDE.md`: PASS/FAIL per check, defined on the snippet Laya sees, 4–6 examples, named hard-case types, "unsure → ?" rule | 1 | me 0.5 day, you 1 h | ⏸ you approve |
| **3. Generator and pilot** | Call fragments as payload-shaped JSON from a matrix: ~12 industries (50% S-Net telecom), 8 agent personalities, short/mid/long, customer moods. `roughen.py` adds speech-to-text noise to 30% (scripted, reproducible). Fragments go through `build_laya_inputs`. **Pilot:** 40 per trained check + 10 per regression check (~240) | 2 | me 1 day, you ~1 h skim | ⏸ if you disagree with >10% of a check, I fix the guide or generator and redo that pilot |
| **4. Gemini test set** (alongside 5) | **Nimithra runs Gemini by hand in its chat** (no Gemini CLI is available to her). I write `prompts/gemini_test_prompt.md` and a numbered list of scenario cards, in batches sized to fit one Gemini reply (about 10 short call excerpts each, so roughly 25-30 batches). Per batch she pastes the batch's prompt into Gemini and saves Gemini's reply, unedited, as `data/fragments/gemini/raw/batch_NN.json` (the reply format is JSON so she never retypes anything). `tools/import_gemini.py` validates each file (parses, schema, turn counts, no label words leaked into the text) and prints the exact scenario ids to re-ask if a batch is broken. The Gemini model name and the date go in the manifest by hand. It then builds rows with the same extractors and writes a **blind** label sheet (Gemini's intended label kept apart). Also **~20 full polite calls** (8-12 min) for the Rapport call-level false-positive test, generated the same way, in smaller batches | 2 | me 0.5 day; **you ~2 h running Gemini** + ~5.5 h labelling + ~1.5-2 h skimming polite calls | ⏸ labels done |
| **5. Full generation** | Volumes below, in matched pairs (paraphrase vs echo; rude vs polite with the same trigger words; warm vs cold reply to the same turn; asked-again vs re-checked status), ~40% hard cases | 3 | me 2–3 days | – |
| **6. Validation** | Schema; token budget with the real tokenizer (laya-train truncates states silently); 50/50 balance; hard-case share; near-duplicates across splits; length and trigger-word balance per label; frozen-hash match. **Shortcut probe** (bag-of-words classifier on dev, per check): >0.85 is a **warning** for every check and a **hard fail** for Rapport and Paraphrasing (regenerate) | 5 | me 0.5 day | ⏸ you read the report |
| **7. Split** | `split.py` groups by `call_id` and `pair_id`. Claude data → train/dev 85/15; Gemini data → gemini-dev / test. `manifest.json` with sha256. `test.jsonl` stays **sealed** until Phase 10 | 6, 4 | me 1 h | – |
| **8. Baseline** | `01_baseline.ipynb`: base model on dev, gemini-dev, test; cutoffs tuned on gemini-dev; records base probabilities as the soft targets for replay rows | 7 | Colab ~30 min | – |
| **9. Training** | `02_train.ipynb`. `--out` goes to `/content`; the checkpoint watcher (proven in the smoke test) copies `checkpoint_latest/` to Drive after each epoch, only once it is fully written. **R1** `--loss soft-ce --label-smoothing 0.05 --epochs 4 --max-len 512 --head-max-len 192 --eval dev.jsonl`; **R2** same with `--loss rlcd`. Keep the better on dev. `--dry-run` before each | 8 | Colab, **measured** (smoke cell 9b, L4): 13.7 items/s at 367 mean state tokens, so **~15 min of training + ~2 min load/save for 3,400 items x 4 epochs** per run. R1 and R2 together are under an hour; extra seeds are cheap | ⏸ you review the dev table (R1 vs R2 vs base) |
| **10. Evaluation** | `03_evaluate.ipynb`: re-tune cutoffs on gemini-dev, score **test once**. Balanced accuracy (BA) per check with 95% bootstrap intervals by call; paired comparison with base on regression checks; ECE; replay drift. **Rapport cutoff is tuned at call level**: best chunk BA on gemini-dev, *subject to* ≤5% of polite full calls failing (tuned on ~40 Claude polite dev calls + bulk `b_00`–`b_04`, then **measured** on the 20 held-out Gemini polite calls) | 9 | Colab 30 min, me 0.5 day | ⏸ go / no-go |
| **11. Integration** | Copy the checkpoint locally, set `LAYA_CHECKPOINT`, commit new cutoffs to `LAYA_CHECKS`. Run `batch_test.py main` and `bulk` (`laya-ft1`), `probe_laya.py`, `compare_results.py ollama laya-v3 laya-ft1`. CPU time per call | 10 | CPU ~1 h, me 0.5 day | ⏸ you review scorecards |
| **12. Iteration** | Error analysis on dev and gemini-dev only; targeted data; new run. If the test set has informed decisions more than once, generate a fresh Gemini test v2 | 11 | 1–3 days per round | – |
| **13. Report** | `docs/RESULTS.md`: "good on realistic synthetic calls", with intervals and limits | 11/12 | me 0.5 day | ⏸ you approve |

Elapsed: about 3–4 weeks. Your hours: about 14–16 including running Gemini, labelling and approvals (see "Who does what").

## Who does what: the steps only Nimithra can do
Claude cannot press Run in Colab, cannot use Gemini, and cannot supply human judgement. Everything else is Claude's job.

| # | When | You do | Why only you | Time |
|---|---|---|---|---|
| 1 | End of Phase 1 | Okay the frozen question wording and cutoffs (Claude shows the baseline numbers) | it is your product's grading standard | 10 min |
| 2 | Before Phase 2 | Decide: should Active listening also fail an agent who *ignores what the customer already said*, or only one who re-asks a question? | a requirements decision | 5 min |
| 3 | Phase 2 | Approve `LABELLING_GUIDE.md` (what PASS/FAIL mean per check, with examples) | defines what "correct" means for all later data | ~1 h |
| 4 | Phase 3 | Read the ~240-item pilot and say where you disagree with the labels | first human check on Claude's training data | ~1 h |
| 5 | Phase 4 | **Run Gemini yourself**: paste each batch prompt, save the reply as `batch_NN.json` (about 25-30 batches) | Claude cannot use Gemini; a different model writes the test calls on purpose | ~2 h |
| 6 | Phase 4 | **Label the Gemini items yourself** (~545) and skim ~20 full polite calls | the independent test must be human judgement, not Claude's | ~7-8 h |
| 7 | Phase 6 | Read the validation report | decide if the data is fit to train on | 15 min |
| 8 | Phases 8, 9, 10 | **Press Run** in the three Colab notebooks (`01_baseline`, `02_train`, `03_evaluate`) and paste the summary lines back; connect the `laya-train` kernel first | Claude cannot operate Colab | ~30 min of attention each (runs themselves 15-40 min) |
| 9 | Phase 9 | Download the trained checkpoint from Drive into `laya-training/checkpoints/` | it lives on your Drive | 10 min |
| 10 | Phase 10 | Go / no-go on the results | the decision to retire Ollama is yours | 15 min |
| 11 | Phase 11 | Review the re-run Main and bulk scorecards | sanity check on real behaviour | 30 min |
| 12 | Phase 13 | Approve the report | | 15 min |
| - | any time | Make `nimjj/laya-finetuning` private; delete the duplicate `smoke-20261016-0848/` folder in the repo root | your GitHub and your disk | 5 min |

Total: about **14-16 hours** spread over the weeks, almost all of it labelling (item 6) and Gemini (item 5). Phases 1, 5, 7 and 12 need nothing from you.
If item 6 is too large, cut the label count or share it with a second person *before* Phase 4; the labels must be human judgement for the final claim to hold.

## Data volumes
| Check | Role | Train (Claude) | Dev (Claude) | Gemini dev (you label) | Gemini test (you label) |
|---|---|---|---|---|---|
| Rapport (chunks) | train | 500 | 100 | 35 | 60 (+20 full polite calls) |
| Paraphrasing | train | 500 | 100 | 35 | 60 |
| Active listening | train | 400 | 80 | 35 | 50 |
| Confirmed resolved | train | 400 | 80 | 35 | 50 |
| Empathy | train | 400 | 80 | 35 | 50 |
| Ownership | regression | 150 | 40 | – | 30 |
| Probing | regression | 150 | 40 | – | 30 |
| Hostility | regression | 100 | 30 | – | 20 |
| Escalation | regression | 100 | 30 | – | 20 |
| Replay (generic questions) | drift guard | 300 | 50 | – | – |
| **Total** | | **3,400** | **630** | **175** | **370 + 20 calls** |

### Your review load
| Review | Items | Time |
|---|---|---|
| Label all Gemini rows (dev and test) | 545 | ~5.5 h |
| Skim the Gemini polite full calls ("any rude line anywhere?") | 20 calls | ~1.5–2 h |
| Main scorecards (Phase 0) | 44 verdicts | ~1.5–2 h |
| Pilot skim (Phase 3) | 240 | ~1 h |
| Claude dev, 15% sample (replay excluded) | ~90 | ~30 min |
| **Total** | **~920 items + 20 calls** | **~10–11 h** (+ ~2 h approvals = 12–13 h) |

Test sizes of 50–60 per check give a BA interval of about ±0.09, so intervals are reported, not just point values. With 20 polite calls, 0 false fails still allows a true rate up to ~14%, so the ≤5% Rapport criterion is a direction, reported with its interval.

### Replay rows and laya-train's calibration slice
- **Not excluded.** `split_calibration` (`laya/train.py`) holds out a random 10% of *all* items (at most 400), so about 9% of the calibration slice is replay rows.
- **Impact is small.** Calibration fits one shared temperature for all yes/no questions. A temperature never changes which of two calls scores higher, and every cutoff is re-tuned on gemini-dev after training, so no verdict depends on it. It only affects the raw confidence values, hence ECE.
- **Measured** by ECE on gemini-dev (no replay rows). If ECE misses 0.10, train through `laya.train.finetune` with a wrapped `split_calibration` that holds out only rows asking the 9 frozen questions.

## Success criteria
1. **Main calls:** mean score error against **your reviewed** scorecards is below Ollama's recomputed error and ≤ 9.0, and the 4 calls rank in strict tier order.
2. **Trained checks (Gemini test):** BA ≥ 0.85, lower 95% bound ≥ 0.75.
   - **2b. Rapport, call level:** ≤ 5% of the 20 held-out Gemini polite calls fail Rapport (with interval).
3. **Regression checks:** test BA no more than 0.05 below the base model, no significant paired drop; bulk `b_*` items ≥ 348/372 (Laya-v2's level).
4. **Unlabelled real_long and v8 calls:** scores keep tier order (Spearman ≥ 0.8).
5. **Drift:** ≥ 90% agreement with the base model on replay generic questions.
6. **Calibration:** ECE ≤ 0.10 on gemini-dev (reported).
7. **Speed:** ≤ 15 s per 20-minute call on CPU (now ~8.5 s; Rapport chunks add some).

## Facts about laya-train worth remembering (v0.4.0)
- **Bug on GPUs:** `finetune()` evaluates before training while the model is still on the CPU, so on CUDA it crashes with "Expected all tensors to be on the same device … index_select" (found in the first smoke run, 2026-10-16). Laya's tests run on CPU only. **Every training run here goes through `tools/laya_train_cuda.py`**, which moves the model to the device first and leaves the package untouched. Re-test without the wrapper if laya is ever upgraded.
- Each *question* becomes one training item; a row may ask several questions. Extra row keys (`meta`) are ignored, and the question id never reaches the model.
- States are **silently truncated** to the window (`max_len` minus the question head). `--dry-run` does not report it, so validation measures it.
- Checkpoints are saved as **fp16** (~0.84 GB), the same size as the base.
- The "epoch N/M mean loss" line prints **before** the epoch checkpoint is written, and `model.safetensors` is not written atomically. Anything copying `checkpoint_latest/` must wait until files stop changing.
- After calibration, laya-train rewrites the config in both the output folder and `checkpoint_latest/`, so copy once more after the process exits.
- Give each check its **own question id** in the rows (`"rapport"`, `"probing"`, ...), not `"q"`. With one id for different questions laya-train warns "Conflicting schema detected" and `questions.json` keeps only the first one. Training itself is unaffected (the smoke test used `"q"`).
- The base model's old `temperature_by_options` is dropped; new buckets are written only where enough calibration items exist.

## Folder layout
```
README.md
00_smoke_test.ipynb  01_baseline.ipynb  02_train.ipynb  03_evaluate.ipynb
tools/               local Python (qa-analysis venv)
prompts/             gemini_test_prompt.md
data/frozen/         checks_frozen.json (questions + caps + sha256 + qa-analysis commit)
data/fragments/      claude/<check>/*.json, gemini/raw/*.json
data/review/         sheets you fill (CSV)
data/rows/           train / dev / gemini_dev / test .jsonl + manifest.json
checkpoints/         git-ignored local copies from Drive
runs/<run-id>/       small reports per run (config, metrics), committed
docs/                DATA_PLAN.md  LABELLING_GUIDE.md  RESULTS.md
```
Drive mirror: `MyDrive/laya-finetuning/{checkpoints,data,runs}`.
