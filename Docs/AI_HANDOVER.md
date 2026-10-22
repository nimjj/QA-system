# AI Handover: S-Net QA system with fine-tuned Laya

Last updated 2026-10-20. If you are an AI assistant (Claude Code or similar) taking over this project, read this file first, then `CLAUDE.md`, `README.md` and the documents named in section 8. `README.md` is the source of truth for setup. This file holds the context, decisions and rules behind the work.

## 1. The project in one paragraph
A synchronous QA service grades telephony support-call transcripts (tenant S-Net) on 11 criteria and returns a scorecard and a final score. Four criteria are deterministic Python rules; seven are judged by **Laya**, a small local yes/no classifier (ModernBERT-large, 421M parameters, 512-token window) that never generates text. The goal is to **replace Ollama (llama3.1)** with a **fine-tuned Laya** that is faster, local and at least as accurate. Ollama is already removed from the code (since version 10). Stock Laya was clearly worse than Ollama, so Laya was fine-tuned on synthetic calls and the way calls are cut into snippets was redesigned ("flow v2").

## 2. Where things stand (2026-10-20)
All numbers are measured against **AI-written answer keys, not human-labelled ones**. Say so whenever you quote them.

| | Stock Laya | Fine-tuned, flow v1 | **Fine-tuned, flow v2** | Ollama |
|---|---|---|---|---|
| AG50: the 7 model-judged items matching the key (of 350) | 64.6% | 72.0% | **80.3%** | 78.6% |
| AG50 mean final-score error / bias (points) | 16.0 / -4.7 | 12.7 / +1.2 | **9.0** / +1.4 | 12.8 / +11.7 |
| Main (4 golden calls): items of 44 | 37 | 41 | **42** | 40 |
| Bulk (64 calls): items of 372 | 351 | 358 | **359** | n/a |
| Time per call (CPU) | 17 s | 16 s | **15 s** (Main 18-22 s) | 386 s |

- Flow v2 versus Ollama on AG50: +1.7 points, 95% interval -3.7 to +7.1, McNemar p = 0.58: **not distinguishable**.
- **AG50 is now a development set** (flow v2 was designed after studying its 50 calls), so its 80.3% is optimistic. Main and bulk were not used to design flow v2 and did not regress.
- Verdict: **not ready to replace Ollama**; suitable for a shadow-mode trial beside it. No number here has been checked by a human.
- **Update 2026-10-22 (rounds 4-8, details in `laya-finetuning/docs/LAYA_TEST_LOG.md` and `laya-finetuning/runs/CHECKPOINTS.md`):** two retrains on Antigravity-written data (ft5, ft6) were tested on sealed exams (AG-B + AG-B2, then AG-C) and are statistically tied with the current model (77.7% to 78.9% of judged items on AG-C; the only significant gain was Rapport for ft5, 56 vs 45 of 62). **Production choice: keep `final-softce-3`.** The biggest remaining errors are in the app (Resolved reads only the last 10 lines, the Ownership phrase gate, Empathy windows opening on any upset-looking line), not the model. Ollama was never run on the sealed sets. AG-B, AG-B2 and AG-C are spent as tests. Next step: shadow mode, then app fixes.
- **Update 2026-10-22 (App v3, branch `app-v3`, `Docs/V3.md`):** shadow mode is not possible (new application), so the owner chose to fix the app instead of retraining. A new pipeline `src/v3/` (opt-in `LAYA_FLOW=v3`; v2 untouched) adds fixed rules, input validation, one built-in criteria set (no database), a single-worker job queue, a readiness endpoint, per-check window gates and 105 unit tests. Real-model checks: the server handled 56 simultaneous submissions (51 queued, 5 refused, 0 failed), a worst-case 1,500-turn call in 56 s, peak 2.7 GB. **Accuracy fixes (stage S4), measured against the AI-written keys:** Resolved (window skips goodbyes, blended with the customer's end-of-call mood relative to the call, cutoff 0.65) and Ownership (wider deflection wordings) are ON; Paraphrasing and Empathy alternatives were worse or mixed and are OFF (config `gates` in `src/v3/config/v3.json`). On the 112 hold-out calls the 11 items matching the key went 1031 -> 1056 (46 better / 21 worse, p = 0.003), mean final-score error 11.0 -> 9.0 points; on the 150 development calls 1389 -> 1407 (p = 0.044). Almost all of the gain is Resolved. Not human-checked; the mood signal rests on AI-written sentiment and may not transfer to real calls. Next: human review of the disagreeing calls, Docker for v3, then retraining only for the checks that remain model-limited (Empathy, Active listening, Resolved).
- Still weak (need training data, not tuning): **Active listening** (0 of 15 faults caught; the fine-tuned model scores true repeats at only 5-12% likelihood), **Rapport** (31% of good AG50 calls fail), **Probing**, **Resolved**.

## 3. What the owner wants now
The owner (Nimithra, a business analyst at Adept Technologies; **use they/them**; a beginner at ML training; short on time) is moving to a new PC. Right now they want that PC **ready to run, set up neatly, with the fine-tuned Laya configured**, but **nothing started**. Testing and training work comes later; until then `laya-finetuning/` is just carried along. When they start work, the next step is section 10.

## 4. Rules for AI assistants (hard)
1. **Honesty about evidence.** Every result is "measured against Claude-written or Antigravity-written keys, not human-labelled". Never call a development-set number a test result. Report failures, skipped steps and your own mistakes plainly, and correct earlier claims when you find they were wrong.
2. **Do not modify the original/stock checkpoint** or anything in the Hugging Face cache. Never edit or print `.env`. Never push to the `bitbucket` remote. **Commit and push only when asked.** Weights never go to GitHub.
3. **Production has customer-side sentiment only** (RoBERTa on the caller transcript). Never use agent sentiment in any logic. (Agent sentiment in the AG50 files is an artifact of how the brief was written.)
4. **Frozen inputs.** The three files `src/services/laya_inputs.py`, `rule_engine.py` and `laya_windows.py`, plus the question wording in `dynamic_evaluator.py`, are hashed (`laya-finetuning/data/frozen/checks_frozen.json`). Changing them invalidates training data built earlier; check with `python laya-finetuning/tools/export_checks.py --check` and re-freeze deliberately (new tag).
5. **Do not train on AG50.** It is a development set; a new sealed test set is needed for any final claim.
6. **Background jobs:** Claude Code's memory watchdog may stop background shells ("system running low on memory"). Never restart a stopped job on your own; report and wait. Heavy runs (Ollama) go detached.
7. **Style with the owner:** short, simple, mid-sized replies; an analogy only when something is genuinely hard; stop and ask only at real decision points (they delegated ML decisions: "think like an ML engineer"); never infer anyone's pronouns.
8. **If the repo sits in a Google Drive synced folder, tracked files can be silently reverted** (this happened twice). Keep it in a plain local folder, commit right after editing, and verify with `grep`/`git diff` that edits are still there.

## 5. Running it with the fine-tuned model
1. Python 3.14 environment: `pip install -r requirements.txt` (installs Laya from GitHub at the pinned commit `3cf26cb`, v0.4.0) and `pip install "transformers==5.16.1"`.
2. **Weights** (not in git): put the folder `final-softce-3` (from Google Drive; `model.safetensors`, `rl_agent_config.json`, `questions.json`, `tokenizer/`, `encoder/`) at `models/final-softce-3`. Verify: `python laya-finetuning/tools/checkpoint_manifest.py verify models/final-softce-3 --manifest laya-finetuning/runs/ft3-stage3/final-softce-3.manifest.json` must print `ALL FILES MATCH` (`model.safetensors` starts `fc6a3f1b793a`).
3. `.env` (git-ignored; copy `.env.example`): add `LAYA_CHECKPOINT=models/final-softce-3` (a relative path is read from the repo root). When this is set the app (a) serves the fine-tuned weights, (b) applies `FINETUNED_CUTOFFS` in `dynamic_evaluator.py`, and (c) uses flow v2. `LAYA_FLOW=v1|v2` overrides (c). Stock Laya (variable unset) keeps v1 and the stock cutoffs.
4. Start: `python main.py` (service on 8006; first call loads the model, about a minute). Optional: `python run_gateway.py` (8005), `cd frontend && npm install && npm run dev`. PostgreSQL is only needed when criteria come from the database; `/api/evaluate` accepts inline `criteria_data`.
5. Smoke test (about 2 minutes): `python Scripts/batch_test.py main --label check`, then `python Scripts/compare_results.py laya-ft-v2b check`. Expect **42 of 44** items and scores about 100 / 88.3 / 50.0 / 30.0 (key 100 / 88.3 / 56.7 / 13.3). 41 of 44 with 76.7 on the second call means flow v2 is **not** active (the checkpoint variable is not being read).
6. Stock weights (1.5 GB, Hugging Face `convaiinnovations/laya` revision `7b928d828b7b0e022f929d9bd2e44165aa270148`) are only needed for stock-Laya runs and for rebuilding training data. Set `LAYA_HF_HOME` to their cache folder.
Details and the new-PC procedure: `laya-finetuning/docs/NEW_PC_SETUP.md`.

## 6. Repository map
```
(repo root)             SEGMENT 1, the QA application
  main.py, run_gateway.py, requirements.txt, .env.example, setup.bat/.sh, docker-compose.yml
  src/api/              FastAPI service (web_app.py)      src/gateway/   API gateway     src/db/   PostgreSQL
  src/services/         rule_engine.py (rules + pre-filters), laya_inputs.py (what Laya is shown), laya_windows.py (flow v2),
                        dynamic_evaluator.py (LAYA_CHECKS, FINETUNED_CUTOFFS, scoring), laya_adapter.py (predict_yes)
  src/v3/               pipeline v3 (Docs/V3.md)
  resources/criteria_config.json   reference criteria for tenant-abc
  models/final-softce-3 the PRODUCTION Laya weights (git-ignored; models/README.md)
  Scripts/              the app's own tools: batch_test.py, compare_results.py, check_prompt_sizes.py, dump_laya_inputs.py
  inputs/               the app's sample calls: Main tests/, Bulk tests/ and their result folders in Test (results)/
  Docs/                 the app's docs (index in Docs/README.md)
  frontend/             React dashboard
  laya-finetuning/      SEGMENT 2, everything about Laya: README.md, data/, tools/, eval/ (testing and evaluation scripts),
                        inputs/ (AG50, AG-T, AG-B, AG-B2, AG-C, Eval50, Tough checks, their results and probes), laya_eval/,
                        runs/, docs/ (test log, AG50 report, NEW_PC_SETUP.md), 0x_*.ipynb (Colab), checkpoints/ (experiment weights, git-ignored)
```

## 7. Test sets (Main and Bulk in the app's `inputs/`; all others in `laya-finetuning/inputs/`; results in `Test (results)/<set> (<engine label>)/` beside each)
| Set | What | Key written by |
|---|---|---|
| `Main tests/` | 4 golden calls, 16-22 min, tiers excellent / good / okay / bad | Claude (not human-reviewed) |
| `Bulk tests/` | 64 calls, defects named in file names (`b_*`) | Claude |
| `Eval50/` | 50 short calls (1-5 min) | Claude |
| `AG50/` | 50 calls of 10-20 min with sentiment, **independent author** | Antigravity (not human-reviewed) |

Engine labels: `laya-stock`, `laya-ft` (fine-tuned, flow v1), `laya-ft-v2b` (fine-tuned, flow v2), `ollama` (an older copy of the app at commit `3035269`, port 8007; recreate with `git worktree add ../qa-analysis-ollama 3035269`). `laya-finetuning/eval/compare_eval.py AG50 <labels...>` compares engines to a key; `laya-finetuning/eval/ag50_analysis.py` then `build_ag50_dashboard.py` regenerate the statistics and dashboard.

## 8. Documents to read, in order
1. `Docs/FLOW_V2.md`: what flow v2 changed, results, limits, next steps.
2. `laya-finetuning/docs/AG50_REPORT.md`: the independent test, statistics, why the model errs (its charts page is generated by `laya-finetuning/eval/build_ag50_dashboard.py`).
3. `laya-finetuning/docs/LAYA_TEST_LOG.md`: every test round (1 to 6). `Docs/FLOW_V2_LAB.md`, `Docs/FLOW_V2_REGRESSION.md`: the lab evidence.
4. `laya-finetuning/README.md` and `runs/*/RESULT.md`: how the model was trained (data built by Claude through the same extractors the app uses; Colab L4; `tools/laya_train_cuda.py` only, because `laya-train` crashes on GPU).
5. `Docs/ARCHITECTURE.md`, `README.md`: pipeline detail and setup.

## 9. How the app decides (summary; code is authoritative)
- **Scoring:** Soft Skills 0.333, Technical Knowledge 0.667. Each category starts at 100 and loses a failed item's deduction: Branding 15, Dead air 15, Personalized 15, Empathy 35, Rapport 20 (soft); Verified 25, Probing 25, Ownership 25, Paraphrasing 15, Resolved 15, Active listening 10 (technical). An agent line containing fuck / shut up / idiot / get lost / stupid / hang up means auto-fail (score 0). Customers may say them freely.
- **Rules (no model):** Branding ("thank you for calling S-Net" in the first 4 agent lines and "thank you for choosing S-Net" in the last 4), Dead air (2 or more gaps over 30 s, measured only from `start_time_sec` assuming each turn lasts 10 s; announced holds up to 120 s are exempt), Verified (PIN, address or security question within the first 240 s), Personalized (agent says the customer's name).
- **Laya checks** (`LAYA_CHECKS`, one yes/no question each, a cutoff on P(pass)): Empathy, Paraphrasing, Active listening, Ownership, Rapport, Probing, Resolved. Laya reads about 340 words per question, so each check gets a short, purpose-built snippet. Flow v1 cut fixed windows; **flow v2** (`laya_windows.py`, used when a fine-tuned checkpoint is served) changes three checks: **Empathy** one window per distinct customer outburst (strict rubric, the owner's decision: every new outburst must be handled), **Paraphrasing** a restatement-cue gate then a tight window (no cue means FAIL without a model call), **Ownership** a wider deflection-phrase list. Probing, Resolved, Active listening and Rapport are unchanged.
- Fine-tuned cutoffs: Empathy 0.49, Paraphrasing 0.47, Active listening 0.50, Resolved 0.42, Rapport 0.20 (call level: any chunk below fails; tuned on Main/bulk, so those are not independent for Rapport). Probing 0.70 and Ownership 0.52 unchanged. A Probing cutoff tuned on AG50 was **rejected** (12 false fails on bulk).

## 10. Next steps (the plan approved on 2026-10-20; SUPERSEDED)
> **Status 2026-10-22:** steps 1 and 2 were carried out (AG-T, AG-B, AG-B2 and AG-C were written, ft4 to ft6 were trained and tested; see `laya-finetuning/runs/CHECKPOINTS.md`). Step 3 was dropped: shadow mode is impossible for a new application. What came next is in `Docs/V3.md`. The text below is kept as the record of the plan.

1. Antigravity briefs for **AG-T** (about 100 training calls) and **AG-B** (50 sealed test calls): agent sentiment absent, customer sentiment noisy as RoBERTa would give, late acknowledgements and confirmations, benign near-repeats in good calls, rude or deflecting lines buried in long polite calls. (The brief `ANTIGRAVITY_TEST_BRIEF.md` was reused with those changes and later removed on 2026-10-22; read it with `git show a7ace67:Docs/<name>`.)
2. Build training rows with the v2 extractors (`LAYA_FLOW=v2`) via `laya-finetuning/tools/build_calls.py`, `build_rows.py`, `make_manifest.py`; retrain on Colab (`01_train_eval.ipynb`, the owner runs it) for Active listening, Paraphrasing (echo versus real restatement), Rapport (long polite calls) and Empathy ("acknowledgement plus refusal"). Keep the replay rows (drift guard).
3. Run stock, fine-tuned and Ollama on AG-B; a human reviews about 30 disagreements; then shadow mode beside Ollama on real calls.

## 11. Writing test transcripts
```json
{"tenant_id": "tenant-abc", "customer_name": "Sarah", "transcript": [
  {"speaker": "Agent", "text": "Thank you for calling S-Net, my name is Alex. How can I help?", "start_time_sec": 0, "start_time": "[00:00]", "end_time": "[00:06]", "sentiment_score": 10.0},
  {"speaker": "Customer", "text": "My internet is completely down.", "start_time_sec": 10, "start_time": "[00:10]", "end_time": "[00:14]", "sentiment_score": -18.0}]}
```
`sentiment_score` goes on each turn (a top-level array is ignored); speakers are exactly `Agent` / `Customer`; keep turns under 30 s (the dead-air rule assumes 10 s); sentiment moves gradually. Remember production has customer sentiment only, so agent turns should carry no meaningful score. Full brief (removed on 2026-10-22; read it with `git show a7ace67:Docs/<name>`): `ANTIGRAVITY_TEST_BRIEF.md`.

## 12. Lessons and pitfalls
- Windows: Python cannot read `/tmp`; keep scripts in files (heredocs mangle backslashes); a scratch file named `dis.py` shadows the standard library; run report scripts with `PYTHONIOENCODING=utf-8`.
- `git stash` and branch switches in a repo with uncommitted work are risky; the Ollama copy is a git worktree of this repo.
- A re-run that does not match the expected numbers usually means the checkpoint variable was not read, or flow v2 is off; check section 5 step 5 before debugging anything else.
- Short-snippet training data made the model fail natural long calls; training rows must come from complete natural calls cut by the same extractors the app uses, and PASS/FAIL must not correlate with style or length.
- The training data and the first two test sets were written by Claude, which flatters the fine-tuned model; AG50 was written by a different AI and showed a smaller, real gain.
