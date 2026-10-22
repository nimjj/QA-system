# Codebase guide: what this system is, how it is built, and where everything lives

Written 2026-10-22 for the team, on branch `app-v3`. Pair it with [`FLOW_DIAGRAMS.md`](FLOW_DIAGRAMS.md), which draws the same system as flow charts. Every file named here exists in the repo; every number comes from code or from a result file named next to it.

> **Read this first.** Every accuracy figure in this repo is measured against answer keys written by an AI (Claude or Antigravity). No human has checked them, and we have no real call recordings with human grades. So the numbers say "how closely the system agrees with an AI's grading of AI-written calls", not "how accurate it is on real calls".

Contents: [1 In one minute](#1-in-one-minute) · [2 Untangling the names](#2-untangling-the-names-v2-v3-flow-model) · [3 The 11 criteria](#3-the-11-criteria) · [4 Runtime architecture](#4-runtime-architecture) · [5 Codebase map](#5-codebase-map) · [6 Where the weights live](#6-where-the-weights-live) · [7 How the model got here](#7-how-the-model-got-here) · [8 Results so far](#8-results-so-far) · [9 Run it and test it](#9-run-it-and-test-it) · [10 State of the repo](#10-state-of-the-repo) · [11 Talking points for the team](#11-talking-points-for-the-team)

---

## 1. In one minute

**What it does.** You send it a call transcript (who said what, when, and how upset the customer sounded at each line). It grades the call on **11 criteria** (for example: did the agent greet properly, verify the customer, show empathy, confirm the issue was resolved), subtracts points for each failure, and returns a **scorecard** and a **0 to 100 score**.

**How it grades.** Two engines:

* **Plain Python rules** (4 criteria): exact, fast, explainable. Greeting and closing script, long silences, identity check, using the customer's name. Plus an automatic zero if the agent swears at or insults the customer.
* **A small AI model called Laya** (7 criteria). Laya is a classifier: given a short piece of the call and one yes/no question ("Is any agent line rude?"), it answers with a probability. It cannot write text, so the coaching tips are fixed sentences. We **fine-tuned** it (trained it further on our own kind of calls) and the version in use is called `final-softce-3`.

**The important idea.** The model can only read a few hundred words at a time. So the app first decides **which lines of the call to show it for each question** (a "window"), and the model only judges those. **Most of the mistakes we found came from the app showing the model the wrong lines, not from the model itself.**

**Where we are today.**

* The original grading pipeline (**pipeline v2**) is still the default and still works.
* This session added a new pipeline (**pipeline v3**) beside it, switched on with `LAYA_FLOW=v3`. It adds safer rules, input checks, a job queue so one slow call cannot freeze the service, no database, tests, and better windows for two checks (Resolved and Ownership).
* On the AI-written test calls v3 agrees with the answer keys more often than v2 (section 8). A person has not yet reviewed the calls where they disagree.
* Nothing is deployed yet. There is no Docker image for v3.

---

## 2. Untangling the names: v2, v3, flow, model

"v2" is used for three different things in the older notes. Here they are separated.

| Name | What it really is | Where you see it |
|---|---|---|
| **App versions 1 to 10.2** | Git branches of the whole application over time (`version-1` ... `version-10.2-laya-finetune`). Version 10 replaced Ollama (a text-generating model) with Laya. | `git branch -r`, README changelog |
| **Pipeline v2** | The current default grader: the function `evaluate_interaction` in `src/services/dynamic_evaluator.py`. Reads criteria from the request or from PostgreSQL. | default behaviour |
| **Pipeline v3** | The new grader in `src/v3/`, written this session. Built-in criteria, a job queue, new rules and gates. | `LAYA_FLOW=v3` |
| **Flow v1 / flow v2** | A *different* thing: how a call is cut into snippets for the model. Flow v1 = the original fixed cuts. Flow v2 = cuts chosen by the call's structure (`src/services/laya_windows.py`). Used automatically when a fine-tuned checkpoint is set. | `flow_version()` in `src/services/laya_inputs.py`, `Docs/FLOW_V2.md` |
| **Model names** | *stock Laya* = the downloaded model, never trained by us. `final-softce-3` = our fine-tune, **in production**. `ft5`, `ft6` = later experiments that did not beat it. (`ft4` was a rejected run; its weights were deleted on 2026-10-22.) "old" in test logs means `final-softce-3`. | `laya-finetuning/runs/CHECKPOINTS.md` |

So the production setup today is: **pipeline v2, using flow v2 snippets, answered by the `final-softce-3` model**. Pipeline v3 reuses the flow v2 snippets for checks it has not changed.

### Glossary

| Term | Plain meaning |
|---|---|
| **Laya** | The small local AI model (ModernBERT-large, 421 million parameters) that answers one yes/no question about a short text. It runs on a normal CPU. |
| **Checkpoint** | A saved copy of the model's weights. A folder of files, about 0.8 to 1.6 GB. |
| **Fine-tuning** | Training an existing model a bit more on examples of our task, so it answers our questions better. |
| **Window / snippet** | The few lines of the call shown to the model for one question. |
| **Question** | The exact yes/no sentence the model is asked, e.g. "Is any agent line rude...?" The wording is fixed in `LAYA_CHECKS`. |
| **Cutoff** | The probability the model's answer must reach for the check to PASS. One per check. |
| **Gate** | The rule that decides which lines become the window, or whether the model is asked at all. Changing a gate changes what the model sees. |
| **Answer key / expected scorecard** | The "right answer" for a test call: the 11 PASS/FAIL ratings. Ours are all written by an AI. |
| **Development set** | Test calls we used while designing, so results on them are optimistic (AG-T, AG50). |
| **Hold-out set** | Test calls kept back to confirm a choice (AG-B, AG-B2, AG-C). Once looked at repeatedly they stop being clean tests. |
| **Frozen** | Four pieces of code and wording that the training data depends on. If they change, old training data no longer matches the app. They must not be edited without re-freezing (`export_checks.py --check`). |
| **Sentiment score** | A number per customer line for how positive or negative it sounds. Production provides the **customer side only**; we never use the agent's. |

---

## 3. The 11 criteria

Deductions and weights are in `resources/criteria_config.json` (v2 reference set) and `src/v3/config/criteria.json` (v3), which hold the same values. A FAIL subtracts its deduction from its category; see [diagram 7](FLOW_DIAGRAMS.md#7-how-the-score-is-built).

| # | Criterion | Category | Deduction | Decided by | What the model sees in v2 | What changed in v3 |
|---|---|---|---|---|---|---|
| 1 | Branding and Survey Check | Soft Skills | 15 | Rule | n/a: "thank you for calling S-Net" in the first 4 agent lines and "thank you for choosing S-Net" in the last 4 | Accepts speech-to-text spellings (S net, Snet, s dash net); greeting and closing must be two different lines; IVR lines do not use up the slots |
| 2 | Hold time and Dead Air | Soft Skills | 15 | Rule | n/a: 2 or more gaps over 30 s fail; announced holds excused | Uses real turn end times (v2 guessed 10 s per turn); customer look-ups and acknowledged holds excused; a single silence of 2 minutes or more fails |
| 3 | Personalized the call | Soft Skills | 15 | Rule | n/a: customer name appears in an agent line (substring) | Whole-word match (Sam no longer matches Samsung); small spelling errors tolerated on longer names |
| 4 | Empathy and Acknowledgment | Soft Skills | 35 | Model | Up to 4 windows: each upset customer line (sentiment at or below -15, or a frustration word) plus the next 4 turns; one FAIL fails the check | Unchanged. A call-relative trigger was tried and rejected |
| 5 | Build rapport and professionalism | Soft Skills | 20 | Model | Every agent line, in chunks of up to 8 lines or 120 words; one rude chunk fails the check | Unchanged |
| 6 | Paraphrasing | Technical Knowledge | 15 | Model | The customer's problem plus the agent line with a restatement phrase in the first 300 s; none found = FAIL without asking the model | Unchanged. A wider search was tried; results mixed, not adopted |
| 7 | Verified customer | Technical Knowledge | 25 | Rule | n/a: agent says "pin", "address" or "security question" in the first 240 s | The agent must *ask* for a PIN, address or security answer; "email address", "IP address" and "I don't need your PIN" do not count. Date of birth, account number and postcode are off |
| 8 | Probing | Technical Knowledge | 25 | Model | The customer's problem (50 words) plus the agent's question sentences (100 words) without greeting and wrap-up questions; no question mark in the call = FAIL | Same, but a "?" is restored on speech-to-text questions that lack one |
| 9 | Took ownership of the problem | Technical Knowledge | 25 | Model | Only agent lines containing a listed phrase ("not my department", ...), at most 6; none = PASS | **New gate:** a much wider set of deflection wordings opens the window; the model still decides |
| 10 | Active listening | Technical Knowledge | 10 | Model | Pairs of similar agent questions (similarity above 0.55), at most 3 pairs; none = PASS | Same, with restored question marks |
| 11 | Confirmed the issue is resolved | Technical Knowledge | 15 | Model | The last 10 lines of the call | **New gate:** the last 16 informative lines (goodbyes skipped), blended 50/50 with how the customer's mood ended relative to their own call; cutoff 0.65 |

Auto-fail (not one of the 11): an agent line that insults, swears or threatens to hang up sets the whole score to 0. v2 matches substrings; v3 matches word patterns with an allow-list, so "that's not a stupid question" no longer zeroes a call.

Category weights: Soft Skills 0.333, Technical Knowledge 0.667 (rescaled to add to 1).

---

## 4. Runtime architecture

### Components

| Component | Port | Started by | Role |
|---|---|---|---|
| QA service (FastAPI) | 8006 | `python main.py` | All endpoints, both pipelines, the model |
| API gateway | 8005 | `python run_gateway.py` | Forwards `/api/*` to the QA service; serves the criteria list and toggle straight from the DB |
| Dashboard frontend (React + Vite) | 5173 | `cd frontend && npm run dev` | Manage tenants and criteria, send sample calls |
| PostgreSQL | 5432 | your DB or `docker-compose` | Tenants, categories, criteria. Needed by pipeline v2 and the dashboard; **not needed by v3** |
| Laya model | in the QA service process | loaded on first use (v2) or at startup (v3) | About 1.95 GB of RAM once loaded |

### Endpoints of the QA service (`src/api/web_app.py`)

| Endpoint | What it does | Pipeline |
|---|---|---|
| `POST /api/evaluate` | Grade one call and return the result. In v3 it waits up to 120 s, then returns 503 with a job id | both |
| `POST /api/jobs`, `GET /api/jobs/{id}` | Submit a call without waiting; poll for the result | v3 only |
| `GET /health` | Alive? | both |
| `GET /ready` | v3: the model has loaded. Otherwise: the database answers | both |
| `GET/POST /api/tenants`, `/api/categories`, `/api/criteria`, `.../criteria/{id}/toggle`, `PUT/DELETE /api/criteria/{id}` | Manage tenants and criteria in PostgreSQL | v2 and the dashboard |
| `GET /api/samples` | Sample calls from `inputs/` for the dashboard | dev tool |

Request body (both pipelines): `transcript` (a list of turns `{speaker, text, start_time_sec, sentiment_score}` or one text block), `customer_name`, `tenant_id`, `call_id`, optional `criteria_data` (ignored by v3). Response: `{call_id, tenant_id, status, result: {final_score, scorecard[], is_auto_fail, auto_fail_reason}}`; v3 adds `meta` and per-item `evidence_turns`.

### Settings (environment variables, in `.env`, never committed)

| Variable | Default | Meaning |
|---|---|---|
| `LAYA_CHECKPOINT` | unset = stock model | Folder of the fine-tuned weights, e.g. `laya-finetuning/checkpoints/final-softce-3`. Also switches on the fine-tuned cutoffs and flow v2 |
| `LAYA_FLOW` | unset | `v3` = new pipeline. `v1` / `v2` force the snippet-cutting rule |
| `LAYA_AL_SOURCE2` | off | Extra Active-listening candidates; only for ft5 / ft6, off in production |
| `LAYA_MODEL` | `english` | Which Laya variant name to serve |
| `LAYA_HF_HOME` | unset | Where the stock weights are cached; falls back to the Hugging Face default cache |
| `LAYA_DEVICE` | auto | e.g. `cpu` |
| `QA_API_KEY` | unset = open | If set, every `/api/*` call must send header `x-api-key` |
| `QUEUE_MAX` | 50 | v3: calls allowed to wait in line |
| `EVALUATE_TIMEOUT_SEC` | 120 | v3: how long `/api/evaluate` waits before answering 503 with a job id |
| `MAX_REQUEST_BYTES` | 2,000,000 | Largest request body |
| `CORS_ORIGINS` | `*` | Comma-separated allowed browser origins |
| `LOG_REQUEST_BODIES` | off | Off keeps transcripts and customer names out of the logs |
| `SERVER_HOST/PORT`, `GATEWAY_HOST/PORT`, `APP_URL` | 0.0.0.0, 8006 / 8005, `http://localhost:8006` | Where things listen |
| `DB_HOST/PORT/NAME/USER/PASSWORD` | localhost, 5432, `qa_database`, `postgres`, ... | PostgreSQL |

---

## 5. Codebase map

```
QA-system/                     the repository (GitHub nimjj/QA-system, working branch app-v3)
├── main.py                    starts the QA service (port 8006)
├── run_gateway.py             starts the gateway (port 8005)
├── requirements.txt           Python dependencies (Laya is installed from GitHub at a pinned commit)
├── setup.bat / setup.sh       one-shot environment setup
├── .env.example               every setting, documented; copy to .env (git-ignored)
├── Dockerfile, Dockerfile.base, Dockerfile.gateway, docker-compose.yml   v2 stack; no v3 image yet
├── requests.http              sample REST calls
├── CLAUDE.md                  rules for AI assistants working in this repo
│
├── src/
│   ├── api/                   web_app.py (all endpoints, middleware, v3 queue wiring), logger.py (JSON logs)
│   ├── gateway/               gateway_app.py (proxy)
│   ├── db/                    database.py (PostgreSQL access)
│   ├── services/              PIPELINE V2 and the shared model access
│   │   ├── dynamic_evaluator.py   evaluate_interaction, the 11 questions and cutoffs (LAYA_CHECKS), scoring   [question wording is FROZEN]
│   │   ├── laya_inputs.py         parse a transcript, build every check's window                              [FROZEN]
│   │   ├── laya_windows.py        flow v2 window builders                                                      [FROZEN]
│   │   ├── rule_engine.py         the 4 rules and the older snippet extractors                                 [FROZEN]
│   │   └── laya_adapter.py        loads the model once, predict_yes(): one question, one probability
│   └── v3/                    PIPELINE V3 (new; imports the frozen files, never edits them)
│       ├── pipeline.py            evaluate_v3: the whole v3 grading in one function
│       ├── normalise.py           clean and validate the transcript (times, roles, sentiment, limits)
│       ├── rules.py               the 4 v3 rules and the auto-fail
│       ├── scoring.py             category scores and the final score, by item name
│       ├── text.py                restores missing question marks
│       ├── jobs.py                the single-worker job queue
│       ├── candidates/            alternative windows per check: resolved.py, ownership.py (adopted); paraphrase.py, empathy.py (tried, off); common.py
│       └── config/                v3.json (limits, role words, rule settings, the gate switches), criteria.json (the built-in 11 criteria)
│
├── tests/
│   ├── unit/                  106 automated tests, no model needed (v3 rules, normaliser, scoring, queue, API, gates)
│   └── scoring_test/          a few small raw-text calls used by Scripts/check_prompt_sizes.py
│
├── Scripts/                   command-line tools, see the table below
├── inputs/                    all test calls, see the table below
├── resources/criteria_config.json   reference criteria for the demo tenant
├── frontend/                  the React dashboard
├── laya_eval/                 the first synthetic benchmark of Laya vs Ollama (evidence behind the starting cutoffs)
├── laya-finetuning/           everything about training the model, see below
├── Docs/                      documentation, index in Docs/README.md
└── logs/                      runtime logs (git-ignored)
```

### `Scripts/`: which tool, when

| Script | Use it to | Needs the model? |
|---|---|---|
| `v3_compare.py` | Run v2 and v3 on a folder of calls, list every item where they differ, score both against the keys | yes |
| `v3_gate_lab.py` | Try candidate windows for one check against the keys (dev and hold-out reported apart) | yes |
| `v3_service_test.py` | Start the real server and test a request, bad input, a full queue, 20 simultaneous calls, a worst-case call, and memory | yes |
| `golden.py` | Compare the 4 rule checks of v2 and v3 over all call sets | no |
| `validate_calls.py` | Check a set of AI-written calls and their keys for format errors | no |
| `probe_laya.py` | Record every model probability on a set of calls (the raw material for choosing cutoffs) | yes |
| `choose_cutoffs.py`, `cutoff_eval.py`, `laya_cutoffs.py` | Pick and score per-check cutoffs from probe files | no |
| `dump_laya_inputs.py`, `check_prompt_sizes.py` | See exactly what the model is sent for each call | no (or stub) |
| `batch_test.py`, `compare_results.py`, `compare_eval.py` | Post a folder of calls to a running service and compare with expected scorecards | service |
| `window_lab.py`, `empathy_lab.py`, `al_reach_lab.py` | The labs that designed flow v2 (kept as evidence) | mostly no |
| `ag50_analysis.py`, `build_ag50_dashboard.py` | Statistics and dashboard page for the AG50 set | no |

### `inputs/`: the test calls

All are AI-written; none has been reviewed by a human.

| Folder | Calls | What it is | Role |
|---|---|---|---|
| `Main tests/` | 4 | Long calls (16 to 22 min) of tiers excellent, good, okay, bad, with expected scorecards | Smoke test: production should score 42 of 44 items |
| `Bulk tests/` | 64 | Calls whose file names say the defect (`b_*`); no keys | Regression checks |
| `Eval50/` | 50 | Short calls (1 to 5 min), keys written by Claude | First Laya vs Ollama rounds |
| `Tough checks/` | 3 | Long raw call transcripts (28 min) | Early stress samples |
| `AG50/` | 50 | 10 to 20 min calls by Antigravity with sentiment, keys in `expected/` | **Development set.** Flow v2 was designed on it. Never train on it |
| `AG-T/` | 100 | Antigravity training calls with `markers` (where each key moment is) | Training data for ft5 / ft6; **development set for v3 gates** (not used to train `final-softce-3`) |
| `AG-B/`, `AG-B2/`, `AG-C/` | 50, 12, 50 | Antigravity test calls written without sight of the models | **Hold-out sets.** Used for the model exams and now looked at repeatedly, so no longer clean tests |
| `Test (results)/` | 924 files | Every result of every earlier round, by engine label (`AG50 (laya-ft-v2b)`, `Main tests (ollama)`, ...) and the probe files | History |

### What an answer key looks like

One file per call, `inputs/<set>/expected/expected_<call>.json`, written by the AI author. Turn numbers below are 0-based positions in the call's `transcript` list.

| Part | Contents |
|---|---|
| `call_id`, `tenant_id`, `status` | identifiers; `status` is always `completed` |
| `result` | What the app should return: `final_score`, `is_auto_fail`, `auto_fail_reason`, and `scorecard`, the 11 items each with `category`, `name`, `rating` (PASS or FAIL) and `coaching` |
| `grader` | The author's working: `graded_by`, `graded_on`, `scenario`, `tier` (a quality label; its wording differs between sets), `duration_sec`, `notes`, `hard_cases`, and `items` (the 11 items again, each with a one-line `evidence` and a `confidence`) |
| `grader.markers` | **Where the key moments are** (present in AG-T, AG-B, AG-B2 and AG-C; AG50 has none), so training rows and checks can find them without re-reading the call |

The marker kinds, as found in the 212 keys that have markers:

| Check | Kinds | Fields |
|---|---|---|
| Active listening | `repeat` (a fault), `harmless_recheck` (looks like a repeat, is not) | `premise_turn`, `agent_turn`, optional `reworded` |
| Paraphrasing | `restatement`, `not_a_restatement` | `agent_turn` |
| Rapport | `rude`, `blunt_but_ok` (curt or using words like "obviously", but respectful) | `agent_turn` |
| Empathy | `handled`, `unhandled`, `no_outburst` (looks upset, is not) | `customer_turn`, `agent_turn`, `with_refusal` |

Two tools read the markers: `Scripts/validate_calls.py` checks that a key is well formed, that its markers agree with its ratings and that the four rule items match what the app's own rule code computes; `laya-finetuning/tools/build_ag_rows.py` turns the markers into labelled training rows. The original label rules, with worked examples, are in git history (`git show a7ace67:Docs/ANTIGRAVITY_V2_COMMON.md`).

### `laya-finetuning/`: training the model

| Folder | Contents |
|---|---|
| `checkpoints/` | The model weights (git-ignored). See section 6 |
| `data/` | `fragments/claude/` (Claude-written call fragments), `rows/` (training rows), `frozen/` (the frozen questions and hashes), `review/` (review sheets from the pilot; the completed one was filled in by Claude, so it is not an independent human check), `eval50/` |
| `tools/` | Row builders (`build_ag_rows.py`, `build_rows.py`, `make_mix2.py`), the Colab notebook builder, the trainer (`laya_train_cuda.py`), `checkpoint_manifest.py` (hash records), `export_checks.py` (the freeze check) |
| `0x_*.ipynb` | Colab notebooks that train a checkpoint on a GPU (`01` first model, `02` to `04` the Antigravity-data rounds) |
| `runs/` | One folder per training round with results (`RESULT.md`), probe files and hash records; `CHECKPOINTS.md` is the catalogue and the decision; `runs/v3/` holds the v3 lab and test outputs |
| `docs/` | Data plan, labelling guide, how to set up a new PC |

### `Docs/`

Start from [`Docs/README.md`](README.md) (the index). The ones to know: this guide and [`FLOW_DIAGRAMS.md`](FLOW_DIAGRAMS.md); [`V3.md`](V3.md) (pipeline v3 status and results); [`AI_HANDOVER.md`](AI_HANDOVER.md) (rules and context for whoever continues); [`LAYA_TEST_LOG.md`](LAYA_TEST_LOG.md) (every test round); [`FLOW_V2.md`](FLOW_V2.md) (what flow v2 changed). [`ARCHITECTURE.md`](ARCHITECTURE.md) is the original version-10 specification and does not describe flow v2 or v3; it is still the only place with the database schema. The instructions that were written for the AI authors of the test sets (the rulebook, the key and marker format, worked examples, and one task brief per set) were removed on 2026-10-22 once the sets were sealed, together with some generated report files; the index lists each one and how to get it back. The structure of an answer key is described in section 5 below.

---

## 6. Where the weights live

| What | Where | Size on disk | In git? | Used for |
|---|---|---|---|---|
| **Production model** `final-softce-3` | `laya-finetuning/checkpoints/final-softce-3/` (`model.safetensors`, `encoder/`, `tokenizer/`, `questions.json`, `rl_agent_config.json`) | 0.8 GB (about 1.95 GB in RAM) | No | `LAYA_CHECKPOINT` in `.env` points here |
| Experiment `ft5` | `laya-finetuning/checkpoints/ft5-20261021-1621/` (`final-softce`, `final-softce_ag3`, `files/`) | 1.6 GB | No | Tested in rounds 7 and 8; the alternative if Rapport false fails become the main complaint |
| Experiment `ft6` | `laya-finetuning/checkpoints/ft6-20261022-0453/` (`final-softce`, `final-softce_ag2`, `files/`) | 1.6 GB | No | Tested in round 8; not better than `final-softce-3` |
| `ft4` | **deleted 2026-10-22** | none | | Rejected run (trained on padded data). Its results and hash record stay in `runs/ft4-ag/` |
| Stock Laya | Hugging Face cache, `C:\Users\<you>\.cache\huggingface\hub\models--convaiinnovations--laya` (`LAYA_HF_HOME` is unset) | 0.8 GB | No | Only for stock-model runs and for building training data |
| Originals and backups | Google Drive (the Colab output folders) | | | Source of every checkpoint |
| Hash records | `laya-finetuning/runs/*/…manifest.json` | tiny | **Yes** | Prove a copy is intact |

* **Weights never go to GitHub.** `laya-finetuning/checkpoints/` is git-ignored.
* Check that the production copy is intact (prints `ALL FILES MATCH`):
  `python laya-finetuning/tools/checkpoint_manifest.py verify laya-finetuning/checkpoints/final-softce-3 --manifest laya-finetuning/runs/ft3-stage3/final-softce-3.manifest.json`
* Moving to a new PC: copy the `final-softce-3` folder, set `LAYA_CHECKPOINT`, verify. See `laya-finetuning/docs/NEW_PC_SETUP.md`.

---

## 7. How the model got here

1. **Starting point.** Stock Laya was clearly worse than the old Ollama (Llama 3.1) setup (64.6% against 78.6% of judged items on AG50).
2. **Training data.** An AI writes calls and answer keys (the briefs that told the author what to write, including the rulebook and the key format, are in git history; see the index in `Docs/README.md`); `validate_calls.py` checks them; the row builders cut them with the **same window code the app uses**, so the model trains on exactly what it will see. The hash in `data/frozen/` makes sure the app and the data stay in step.
3. **Training.** A Colab notebook fine-tunes Laya on a GPU and saves the checkpoint to Google Drive; it is downloaded into `checkpoints/` and its hashes recorded.
4. **Exams.** Cutoffs are chosen on development data and written down **before** a test set is opened; then one exam on calls the model never saw, scored with a paired test (McNemar).
5. **Result.** Flow v2 plus fine-tuning brought the model level with Ollama on AG50 (80.3% against 78.6%, not statistically different). Two further retrains (ft5, ft6) did not beat `final-softce-3` (round 8 on AG-C: `final-softce-3` 78.0%, ft5 78.9%, ft6 77.7% of judged items, no significant differences); ft4 was rejected earlier because its training data was padded. **Decision 2026-10-22: production stays on `final-softce-3`.**
6. **Pivot to the app.** The remaining mistakes were mostly in what the app shows the model, and shadow mode (running beside the old system) was not possible for a new application. So the work moved to the pipeline: v3.

Details: `Docs/LAYA_TEST_LOG.md`, `laya-finetuning/runs/CHECKPOINTS.md`, `laya-finetuning/runs/ft5-ag/RESULT.md`, `runs/ft6/RESULT.md`.

---

## 8. Results so far

All against AI-written keys. "Items matching the key" counts the 11 ratings per call.

**Production model, pipeline v2** (from `Docs/AI_HANDOVER.md` and `runs/ft6/RESULT.md`): AG50 judged items 80.3% (development set, optimistic); AG-C exam 273 of 350 judged items (78.0%); mean final-score error 11.5 points on AG-C.

**Pipeline v3 against pipeline v2, end to end** (`Docs/V3.md`, `laya-finetuning/runs/v3/e2e_*.jsonl`):

| Set group | Calls | 11 items matching the key, v2 -> v3 | Better / worse | p | Mean final-score error |
|---|---|---|---|---|---|
| Development (AG-T, AG50) | 150 | 1389 -> 1407 of 1650 | 45 / 27 | 0.044 | 10.5 -> 9.9 points |
| Hold-out (AG-B, AG-B2, AG-C) | 112 | 1031 -> 1056 of 1232 | 46 / 21 | 0.003 | 11.0 -> 9.0 points |

* Almost all of the gain is **Resolved** (hold-out 57 -> 84 of 112 correct; v2's version was close to a coin flip there). **Ownership** now detects about half of the real deflections instead of almost none, but it also flags more good calls, so on items it is even (12 better, 11 worse).
* Caveats: the Resolved hold-out was read before the variant was finally chosen; Resolved uses the customer's sentiment scores, which in these calls were written by the same AI that wrote the calls, so it may not transfer to real recordings.

**Service tests with the real model** (`laya-finetuning/runs/v3/service_test.json`): model load 7 s; about 12 s per call on this PC (Core Ultra 7, 14 threads); 56 calls submitted at once gave 51 queued and graded, 5 refused with "busy, retry later", 0 failed; a worst-case 1,500-turn call graded in 56 s; peak memory 2.72 GB (4.48 GB committed), under the 8 GB target but not tested under an enforced 8 GB limit. Expect 20 to 30 s per call on a slower cloud CPU.

**Still weak** (the model, not the windows): Empathy (strict, fails many good calls), Active listening, and the model's own ability on Resolved.

**Not done yet:** a person reviewing the calls where v2 and v3 disagree; a Docker image for v3; pinned dependency versions; testing on real transcripts; the `ft5`-for-Rapport idea (on hold).

---

## 9. Run it and test it

Windows PowerShell, from the repo root, after `setup.bat` and filling in `.env`:

```
python main.py                                  # pipeline v2 (the default)
$env:LAYA_FLOW = "v3"; python main.py           # pipeline v3
python run_gateway.py                           # optional gateway on 8005
cd frontend; npm install; npm run dev           # optional dashboard on 5173

python -m unittest discover -s tests/unit -t .  # 106 tests, no model, about 1 second
python laya-finetuning/tools/export_checks.py --check          # the frozen files still match
python Scripts/v3_compare.py inputs/AG-T --out laya-finetuning/runs/v3/e2e_AG-T.jsonl   # v2 vs v3 with the model
python Scripts/v3_gate_lab.py resolved          # try window variants for one check
python Scripts/v3_service_test.py --out laya-finetuning/runs/v3/service_test.json       # server, load and memory test
```

A first call (v3 needs no database):

```
POST http://localhost:8006/api/evaluate
{ "transcript": [ {"speaker": "Agent", "text": "Thank you for calling S-Net...", "start_time_sec": 0},
                  {"speaker": "Customer", "text": "My internet is down", "start_time_sec": 8, "sentiment_score": -30.0} ],
  "customer_name": "Alex", "tenant_id": "tenant-abc", "call_id": "demo-1" }
```

---

## 10. State of the repo

Audited and tidied on 2026-10-22.

**Checked and correct:** production weights are where `.env`, the README and the catalogue say, and verify as `ALL FILES MATCH`; `LAYA_CHECKPOINT` points at `final-softce-3`; the frozen files still match their freeze (`inputs_sha256` 4021ce6d6740...); 106 unit tests pass; nothing in `src/services/` was edited by v3.

**Changed in this tidy-up:**

* Deleted the four Google Drive zips of ft5 and ft6 in `Downloads` (5.8 GB), after re-verifying the installed copies against their hash records, and the rejected `ft4` weights (1.6 GB). `checkpoints/` is now 4.0 GB.
* Deleted generated or empty leftovers: the root `__pycache__/` and an empty `tests/golden/`.
* Moved the side folders that sat next to the repo (`_incoming`, `_quarantine`, the earlier clean-up archive) under one `D:\CIAP\QA\_archive\`. The quarantined paste is untouched.
* Refreshed the README folder map, `.env.example` (v3 settings), the stale paths in `laya-finetuning/README.md`, added a banner to `Docs/ARCHITECTURE.md`, and indexed the new documents.
* Removed thirteen finished-task or regenerable documents from `Docs/` in two steps: ten first, then the author rulebook, key format and worked examples (the four AI-author task briefs for AG-T, AG-B, AG-B2 and AG-C; the AG50 dashboard, stats and results table; the Eval50 and Round 4 result tables; the Ollama-era flowchart). The index in `Docs/README.md` lists each one with the command that regenerates it and `git show 8a6842b:Docs/<name>` to read the original.
* Earlier the same day: 56 loose helper scripts and 29 run logs were moved out of the repo root into the archive, and the repo was pushed to a new branch `app-v3`.

**Left as they are on purpose:** `inputs/Test (results)/` (history; scripts and docs point into it), `laya_eval/` (evidence behind the starting cutoffs), the experiment labs in `Scripts/`, the v2 database code and tenant endpoints (v2 and the dashboard still use them), the Docker files (v3 image still to do), and ft5 / ft6 weights (the docs and probe commands use those paths).

**Known loose ends:** `laya-finetuning/docs/DATA_PLAN.md` mentions files that no longer exist; it is a partly superseded plan and was not rewritten. `Docs/ARCHITECTURE.md` predates flow v2 and v3.

---

## 11. Talking points for the team

* **What it is:** a call grader. Four rule checks and seven checks answered by a small local AI model; no cloud, no text generation.
* **The insight:** the model is only as good as the lines we show it. Most errors were in choosing those lines.
* **What we built this session:** a new pipeline beside the old one: safer rules, input checks, a queue, no database, tests, and better line selection for the two checks where it mattered most.
* **What we can honestly say:** on AI-written calls graded by AI-written keys, v3 matches the keys better than v2 (hold-out: 1056 against 1031 of 1232 ratings; final-score error 9.0 against 11.0 points).
* **What we cannot say yet:** how it does on real calls. No human has reviewed the keys or the disagreements, and we have no real recordings.
* **What is next:** a person reviews the disagreeing calls; a Docker image for v3; try real transcripts when we have them; retrain only for the checks that remain model-limited (Empathy, Active listening).
