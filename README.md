# Automated QA Evaluation System

A locally hosted Quality Assurance engine for customer-support call transcripts. It grades each call against tenant-configurable criteria and returns a scorecard.

Built with **FastAPI**, a deterministic **Python rule engine** and **Laya**, a local yes/no decision engine. Runs fully offline once the Laya weights are on disk.

> **Version 10 (branches `version-10-laya`, and `version-10.1-laya` with the test round fixes):** Ollama / Llama 3.1 and the `nomic-embed-text` embeddings have been **removed** and replaced by Laya. See [Status & known limitations](#status--known-limitations) before relying on the scores.

> **App v3 (branch `app-v3`, opt-in with `LAYA_FLOW=v3`):** a new pipeline in `src/v3/` with fixed rule checks, input validation, one built-in criteria set (no database), a single-worker job queue (`/api/evaluate` waits, `/api/jobs` submit and poll), a readiness endpoint and unit tests. The v2 flow is untouched and stays the default. See [`Docs/V3.md`](Docs/V3.md). **New to the codebase? Start with [`Docs/CODEBASE_GUIDE.md`](Docs/CODEBASE_GUIDE.md) and [`Docs/FLOW_DIAGRAMS.md`](Docs/FLOW_DIAGRAMS.md).** Run the tests with `python -m unittest discover -s tests/unit -t .`.

---

## Quick start (pipeline v3)

Everything here uses pipeline v3: no database, one model, one worker. **All scores are measured against AI-written answer keys, not human-labelled ones, and real call transcripts have not been tried yet.**

**1. Get the code**
```bash
git clone -b app-v3 https://github.com/nimjj/QA-system.git
cd QA-system
```

**2. Get the model weights (separately, once per machine).** The weights (808 MB) are **not in git**, so a fresh clone cannot grade anything until they are in `models/final-softce-3/`. Ask the project owner for the zip, unzip it there and check it: `python Scripts/verify_weights.py` must end with `ALL FILES MATCH`. How sharing works and why: [`models/README.md`](models/README.md).

**3a. Run it in Docker** (needs Docker with at least 4 GB of memory; the first build downloads about 1 GB)
```bash
docker compose -f docker-compose.v3.yml up -d --build
curl http://localhost:8006/ready        # "status":"ready" after about 10 s
```
Step-by-step guide, optional settings (API key, queue size) and troubleshooting: [`Docs/DOCKER.md`](Docs/DOCKER.md). Note: the files are prepared, but the image has not been built and tried by us yet, so tell the owner if the first build hits a problem.

**3b. Or run it without Docker** (Python 3.10+, developed on 3.14)
```bash
python -m venv .venv && source .venv/bin/activate       # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env                                    # Windows: copy .env.example .env
# in .env set:  LAYA_FLOW=v3   and   LAYA_CHECKPOINT=models/final-softce-3
python main.py                                          # http://localhost:8006  (Swagger at /docs)
```

**4. Try it**
```bash
python Scripts/try_call.py "inputs/Main tests/gold_01_excellent_22min.json"   # one call, plain-language scorecard (expect 100.0)
python Scripts/send_folder.py "inputs/Main tests"        # every call in a folder; one JSON reply per call in outputs/ (git-ignored) + outputs/_summary.csv
```
The same endpoint works from any tool: `POST http://localhost:8006/api/evaluate` (examples in [API](#api), `requests.http` and `Docs/postman_collection.json`). The four golden calls should score 100.0, 88.3, 50.0 and 30.0; saved replies to compare with are in `inputs/Test (results)/Main tests (app-v3)/`. Around 380 more AI-written test calls are in `inputs/` (AG50, AG-T, AG-B, AG-B2, AG-C, Eval50, Tough checks, Bulk tests); their answer keys are in the Laya repo.

### Where the documentation is

| I want to... | Read |
|---|---|
| Master overview: architecture, Flow v2 lifecycle, criteria, and two-repo guide | [`Docs/SYSTEM_AND_FLOW_V2_GUIDE.md`](Docs/SYSTEM_AND_FLOW_V2_GUIDE.md) |
| Autonomous AI handover guide (for Claude Code, Antigravity, LLM agents) | [`Docs/AI_HANDOVER.md`](Docs/AI_HANDOVER.md) (also `CLAUDE.md`) |
| Set up and run the Docker container | [`Docs/DOCKER.md`](Docs/DOCKER.md) |
| Get the weights, verify them, share them with a colleague | [`models/README.md`](models/README.md) |
| Understand what everything is and how the code fits together (plain language) | [`Docs/CODEBASE_GUIDE.md`](Docs/CODEBASE_GUIDE.md), then [`Docs/FLOW_DIAGRAMS.md`](Docs/FLOW_DIAGRAMS.md) (11 diagrams) |
| Understand v3: what it does, settings (`src/v3/config/v3.json`), results, what is not done | [`Docs/V3.md`](Docs/V3.md) |
| Detailed index and catalog of all documents | [`Docs/README.md`](Docs/README.md) (index) |

### Testing it
* **Unit tests (no model, seconds):** `python -m unittest discover -s tests/unit -t .` (106 tests; they must all pass before any change is merged).
* **Real model, whole service:** start it as above, then `Scripts/send_folder.py` or `Scripts/try_call.py`, and compare with the saved replies in `inputs/Test (results)/`. Scripts for comparing result folders: `Scripts/compare_results.py` (see [Testing](#testing)).
* **Heavier checks** (v3 against v2 on all test sets, load and memory test of the server) live in the separate Laya repo `nimjj/laya-finetuning`, cloned next to this one as `../laya-finetuning`: `eval/v3_compare.py`, `eval/v3_service_test.py`, `eval/golden.py`. Run them with this repo's Python. Not needed just to run or try the service.

### Making changes
* Read [`Docs/CODEBASE_GUIDE.md`](Docs/CODEBASE_GUIDE.md) first: section 4 is the runtime architecture and settings, section 5 the map of every folder and file, section 9 how to run and test. v3 lives in `src/v3/` and its switches are in `src/v3/config/v3.json`; the API is `src/api/web_app.py`.
* **Four files are frozen and must not be edited casually:** `src/services/laya_inputs.py`, `rule_engine.py`, `laya_windows.py` and the question wording in `dynamic_evaluator.py`. The model was trained on exactly those questions, so a change silently breaks it. If you must change one, re-freeze with the Laya repo: `python ../laya-finetuning/tools/export_checks.py --check` (details in [`Docs/AI_HANDOVER.md`](Docs/AI_HANDOVER.md) section 4).
* Never commit `.env` or any weights. Production uses customer-side sentiment only. A change counts as better only if it improves results on the test calls without hurting the others, and say that results are against AI-written keys.
* Code changes to the container: edit `src/`, then `docker compose -f docker-compose.v3.yml up -d --build`.

---

## How it works

```
Client / Frontend / Postman
        │  POST /api/evaluate
        ▼
FastAPI QA service (src/api/web_app.py :8006)       ◄── API Gateway (run_gateway.py :8005)
        │
        ├─► Python rules (src/services/rule_engine.py), no model
        │     Branding · Dead air · Verified customer · Personalized call · Profanity auto-fail
        │
        ├─► Python pre-filters cut each judgement down to a short snippet
        │     sentiment drops · rude/deflection phrase lists · similar questions · word caps
        │
        └─► Laya (src/services/laya_adapter.py): one yes/no probability per question
              Empathy · Active listening · Ownership · Rapport · Probing · Paraphrasing
              Confirmed resolved (last 10 lines) · Escalation / Hostility / custom criteria (batched)
```

* Laya cannot generate text, so coaching tips are **static strings** per criterion.
* Every Laya question has explicit yes/no meanings and its own PASS cutoff (`LAYA_CHECKS` in `src/services/dynamic_evaluator.py`).
* Full detail: [`Docs/ARCHITECTURE.md`](Docs/ARCHITECTURE.md). Context for whoever picks this up next: [`Docs/AI_HANDOVER.md`](Docs/AI_HANDOVER.md).

---

## Prerequisites

* **Python 3.10+** (developed on 3.14).
* **The Laya library**, installed by `requirements.txt` from [github.com/NandhaKishorM/laya](https://github.com/NandhaKishorM/laya) at the pinned commit `3cf26cb` (v0.4.0). No local checkout is needed, and the engine is not vendored into this repo. (To work on the library itself, `pip install -e` a clone instead.)
* **The stock Laya weights** (about 1.5 GB), needed only for stock-Laya runs and for the training-data tools. They are read from `LAYA_HF_HOME`, else `../laya-test/hf_home` if that folder exists, else Hugging Face's default cache. A fine-tuned checkpoint (`LAYA_CHECKPOINT`, see `../laya-finetuning/`) is self-contained and does not need them.
* **PostgreSQL**, only if criteria come from the database. Requests that include `criteria_data` don't need it.

Folder layout (two folders, two separate git repos):
```
D:\CIAP\QA\
├── QA-system\          this repo (GitHub nimjj/QA-system): the QA APPLICATION: src/, frontend/, tests/, Docs/, Scripts/, inputs/ (sample calls) ...
│   └── models\final-softce-3   the production Laya weights (git-ignored; see models/README.md)
└── laya-finetuning\    the Laya repo (GitHub nimjj/laya-finetuning): training, fine-tuning, testing, evaluation, test sets, benchmarks, experiment weights
```
The app does not need the Laya folder to run. The Laya folder reads the app's code from `../QA-system`.

---

## Setup

Windows: run `setup.bat`. Linux/macOS: run `./setup.sh`. Or do it by hand:
```bash
python -m venv .venv
.venv\Scripts\activate            # Windows
source .venv/bin/activate         # Linux/macOS
pip install -r requirements.txt   # FastAPI stack, psycopg2-binary, and Laya from GitHub (pinned commit)
copy .env.example .env            # Windows  (cp on Linux/macOS)
```

### Environment (`.env`)
| Variable | Default | Purpose |
|---|---|---|
| `LAYA_MODEL` | `english` | Laya checkpoint for every check (the English one tested best) |
| `LAYA_HF_HOME` | empty → `../laya-test/hf_home` if it exists, else Hugging Face's default cache | Folder holding the stock Laya weights |
| `LAYA_DEVICE` | empty (automatic) | `cpu` or `cuda` |
| `SERVER_HOST` / `SERVER_PORT` | `0.0.0.0` / `8006` | QA service (the gateway and frontend expect 8006) |
| `DB_HOST` `DB_PORT` `DB_NAME` `DB_USER` `DB_PASSWORD` | see `.env.example` | PostgreSQL |
| `GATEWAY_HOST` / `GATEWAY_PORT` / `APP_URL` | `0.0.0.0` / `8005` / `http://localhost:8006` | API gateway |

---

## Running

```bash
python main.py          # QA service on http://localhost:8006  (docs at /docs)
python run_gateway.py   # optional: API gateway on http://localhost:8005
cd frontend && npm install && npm run dev   # optional: React dashboard
```
* The first evaluation loads Laya, which takes about a minute on CPU. After that each Laya check takes about 1 s on CPU.
* Evaluations run one at a time.

> **Docker:** for pipeline v3 (no database) use `docker-compose.v3.yml` and follow [`Docs/DOCKER.md`](Docs/DOCKER.md); the files are prepared but the image has not been built yet. The older `docker-compose.yml` is the v2 stack (Postgres, gateway, frontend) and its QA-service image does **not** include Laya; run v2 locally as above and use that compose file only for Postgres if needed (`docker compose up -d postgres`).

---

## API

### Evaluate a call: `POST /api/evaluate`
```json
{
  "tenant_id": "tenant-abc",
  "customer_name": "Grace",
  "transcript": [
    {"speaker": "Agent", "text": "Thank you for calling S-Net, my name is Alex, how can I help you today?", "start_time_sec": 0, "sentiment_score": 6.0},
    {"speaker": "Customer", "text": "My smart thermostat keeps resetting every evening.", "start_time_sec": 10, "sentiment_score": 6.8}
  ],
  "criteria_data": null
}
```
* `transcript` may also be a raw string (`"[00:00] Agent: …\n[00:05] Customer: …"`). Raw strings carry no sentiment, so Empathy never triggers on them.
* Put `sentiment_score` **on each turn**. A top-level `sentiment_scores` array is ignored.
* If `criteria_data` is omitted, the tenant's active criteria are loaded from PostgreSQL. Disabled items are skipped and category weights re-balance to 100.

Response:
```json
{
  "call_id": "call_…",
  "tenant_id": "tenant-abc",
  "status": "completed",
  "result": {
    "final_score": 90.0,
    "is_auto_fail": false,
    "auto_fail_reason": null,
    "scorecard": [
      {"category": "Soft Skills", "name": "Branding and Survey Check", "rating": "PASS",
       "coaching": "Agent successfully used required opening and closing branding scripts."}
    ]
  }
}
```

### Other endpoints
| Method & path | Purpose |
|---|---|
| `GET /health` | Health check (QA service and gateway) |
| `GET/POST /api/tenants` | List or create tenants |
| `GET/POST /api/categories` | List or create categories |
| `GET /api/criteria`, `POST /api/criteria`, `PUT/DELETE /api/criteria/{id}` | Criteria CRUD |
| `GET /api/tenants/{tenant}/criteria`, `POST /api/tenants/{tenant}/criteria/{id}/toggle` | Per-tenant criteria and on/off toggles |
| `GET /api/samples` | Sample transcripts from `inputs/` |

`/api/preview-prompt` was removed in version 10 (there is no LLM prompt any more). Ready-made requests are in `requests.http` and `Docs/postman_collection.json`.

---

## The 11 default criteria (`resources/criteria_config.json`)

| # | Criterion | How it's judged |
|---|---|---|
| 1 | Branding and Survey Check | Rule: S-Net opening and closing script |
| 2 | Hold time and Dead Air | Rule: 2 or more gaps over 30 s fail (announced holds up to 120 s don't count) |
| 3 | Personalized the call | Rule: customer name used by the agent |
| 4 | Empathy & Acknowledgment | Laya on the 2 worst upset-customer moments |
| 5 | Build rapport / professionalism | Phrase list, then Laya |
| 6 | Paraphrasing | Laya: customer opening plus the first agent lines |
| 7 | Verified customer | Rule: PIN, address or security question within 4 minutes |
| 8 | Probing | Laya on the real (non-boilerplate) agent questions |
| 9 | Took ownership | Phrase list, then Laya |
| 10 | Active listening | Near-identical agent questions, or ones the customer answers with "like I said", then Laya |
| 11 | Confirmed the issue is resolved | Laya on the last 10 lines |

**Auto-fail (score 0):** profanity from a fixed list in any agent line (customer lines are not checked), or a FAIL in a category named "AUTO FAIL".

---

## Status & known limitations

Laya runs **out of the box, without training**. Its starting cutoffs come from a 320-item synthetic test (`../laya-finetuning/laya_eval/RESULTS.md` (`../laya-finetuning/laya_eval/RESULTS.md`, in the Laya repo)). Two rounds on full-length calls (the hand-graded `inputs/Main tests` and the labelled `b_*` bulk calls, October 2026) are logged in `../laya-finetuning/docs/LAYA_TEST_LOG.md` (`../laya-finetuning/docs/LAYA_TEST_LOG.md`, in the Laya repo). After Round 2, Laya matched 36/44 hand-graded items (Ollama 40/44) and 348/372 `b_*` items:

| Check | State |
|---|---|
| Dead air | Good on both sets after the managed-hold fix |
| Probing | Good; a 0.70 cutoff (now 0.60) would separate every test call |
| Active listening | Regressed in Round 2: the attached customer reply lowers Laya's repeat score |
| Confirmed resolved | Cutoff 0.73 chosen on the `b_*` calls; Laya barely separates confirmed from unconfirmed endings |
| Paraphrasing | Doesn't separate good from bad yet |
| Rapport | Inverted: benign trigger phrases score as ruder than truly rude lines |
| Empathy | The 0.78 cutoff still fails 2 of the 4 hand-graded calls |

Next step: Laya training on Active listening, Resolved, Paraphrasing, Rapport and Empathy (in that order, see the log), plus a few hundred human-labelled real calls to re-tune `LAYA_CHECKS`. Until then, treat those scores as provisional.

---

## Fine-tuned Laya and the test results
The fine-tuning work lives in this repo, in `../laya-finetuning/` (`../laya-finetuning/README.md`, in the Laya repo): training data and tools, the Colab notebook, run notes, and the setup guide for a new machine (`docs/NEW_PC_SETUP.md` (`../laya-finetuning/docs/NEW_PC_SETUP.md`, in the Laya repo)). The weights are not in git.

* **Serve the fine-tuned model:** set `LAYA_CHECKPOINT` to the checkpoint folder (`models/final-softce-3`). That also switches on the fine-tuned cutoffs and "flow v2" (`Docs/FLOW_V2.md`). `LAYA_FLOW=v1|v2` overrides the flow.
* **Latest results** (AI-written answer keys, not human-reviewed): on 50 independent 10-20 minute calls (`../laya-finetuning/inputs/AG50`), the 7 model-judged items match the key 72.0% with the original flow and 80.3% with flow v2 (Ollama 78.6%; a development set, so optimistic). The 4 golden calls: 42 of 44 items. Details: `../laya-finetuning/docs/AG50_REPORT.md` (its charts page is generated by `../laya-finetuning/eval/build_ag50_dashboard.py`), `Docs/FLOW_V2.md`, `../laya-finetuning/docs/LAYA_TEST_LOG.md`.

---

## Testing

```bash
python Scripts/check_prompt_sizes.py          # no model, no server: input caps, scorecards, unit checks
python Scripts/check_prompt_sizes.py --live   # real Laya over all sample calls: verdicts and timing
python Scripts/batch_test.py --label laya     # posts inputs/Main tests to a running service
python Scripts/batch_test.py bulk --label laya  # posts inputs/Bulk tests
python Scripts/compare_results.py ollama laya laya-v2  # result folders vs expected grades and the b_* filename defects
python ../laya-finetuning/eval/probe_laya.py out.json           # in-process: every Laya probability per call (no server)
python ../laya-finetuning/eval/laya_cutoffs.py out.json         # best cutoff per check from the b_* filename defects
```
* `batch_test.py` sends the criteria from `resources/criteria_config.json` with every call (`criteria_data`), so it needs no database; `--use-db` turns that off. Results go to `inputs/Test (results)/<suite> (<label>)/`.
* `inputs/Main tests/` holds four hand-graded 16–22 minute calls; their expected scorecards are in `expected/` (see the README there).
* `inputs/Bulk tests/` holds the older samples: `b_*` calls with planted defects named in the filename, `v8_*` and `real_*`. `../laya-finetuning/inputs/Tough checks/` holds three 28-minute trap calls.
* `inputs/Test (results)/` holds the Ollama, Laya and Laya-v2 runs of both suites and the raw Laya probabilities (`Laya probes/`). Older Ollama-era inputs and results were removed in `version-10.1-laya` and remain in git history.

---

## Codebase Map

New to the codebase? Read [`Docs/CODEBASE_GUIDE.md`](Docs/CODEBASE_GUIDE.md) (what everything is) and [`Docs/FLOW_DIAGRAMS.md`](Docs/FLOW_DIAGRAMS.md) (the flow as diagrams) first.

```
QA-system/                       # THIS repo: the QA application
├── main.py                      # QA service launcher (:8006)
├── run_gateway.py               # API gateway launcher (:8005)
├── requirements.txt             # FastAPI stack + psycopg2-binary + Laya (pinned GitHub commit)
├── .env.example                 # every setting, documented (copy to .env, which is git-ignored)
├── setup.bat / setup.sh         # venv + install + .env
├── docker-compose.yml           # Postgres, QA service, gateway, frontend (v2 stack)
├── Dockerfile / Dockerfile.base / Dockerfile.gateway
├── docker-compose.v3.yml / Dockerfile.v3 / requirements-docker.txt / .dockerignore   # v3 container, see Docs/DOCKER.md
├── requests.http                # REST-client requests
├── CLAUDE.md                    # rules for AI assistants working in the repo
├── resources/criteria_config.json   # reference criteria for tenant-abc
├── src/
│   ├── api/                     # web_app.py (endpoints, middleware, v3 queue wiring), logger.py (structured JSON logs)
│   ├── gateway/gateway_app.py   # gateway proxy + direct DB criteria routes
│   ├── db/database.py           # PostgreSQL access (pipeline v2 and the dashboard)
│   ├── services/                # PIPELINE V2 and model access
│   │   ├── dynamic_evaluator.py # orchestration, Laya questions and cutoffs, scoring, static coaching
│   │   ├── laya_inputs.py       # transcript parsing and the window for every check (frozen)
│   │   ├── laya_windows.py      # flow v2 window builders (frozen)
│   │   ├── rule_engine.py       # the 4 rules and snippet extractors (frozen)
│   │   └── laya_adapter.py      # Laya Router singleton: predict_yes()
│   └── v3/                      # PIPELINE V3 (LAYA_FLOW=v3): pipeline, normaliser, rules, scoring, job queue
│       ├── candidates/          # alternative windows per check (Resolved, Ownership on; Paraphrasing, Empathy tried, off)
│       └── config/              # v3.json (limits, rule settings, gate switches), criteria.json (built-in criteria)
├── models/final-softce-3/       # the PRODUCTION Laya weights (git-ignored; models/README.md)
├── tests/
│   ├── unit/                    # 106 automated tests, no model needed
│   └── scoring_test/            # small raw-string test calls
├── Scripts/                     # the app's own tools: batch_test, compare_results, check_prompt_sizes, dump_laya_inputs
├── inputs/                      # the app's sample calls: Main tests, Bulk tests, and their result folders
├── frontend/                    # Vite + React dashboard
├── Docs/                        # the app's docs, index in Docs/README.md
│   ├── CODEBASE_GUIDE.md        # architecture and codebase, in plain language
│   ├── FLOW_DIAGRAMS.md         # Mermaid diagrams of the flow
│   ├── V3.md                    # pipeline v3: status, gates, results
│   ├── ARCHITECTURE.md          # the original version-10 specification (historical)
│   ├── AI_HANDOVER.md           # context and constraints for the next maintainer
│   └── postman_collection.json
```

The Laya repo is a separate folder next to this one (`../laya-finetuning`, GitHub `nimjj/laya-finetuning`); its own README explains it. In short: `data/`, `tools/` and the Colab notebooks (training material, row builders, the freeze check), `eval/` (testing and evaluation scripts), `inputs/` (all test sets AG50, AG-T, AG-B, AG-B2, AG-C, Eval50, Tough checks, with results and probes), `laya_eval/` (the first Laya-vs-Ollama benchmark), `runs/` (results, probe files, hash records; `CHECKPOINTS.md` is the catalogue), `checkpoints/` (experiment weights ft5, ft6) and `docs/` (test log, AG50 report, data plan, labelling guide, new-PC setup).

## Changelog: version 10.1 (Laya test rounds)
* **Tests:** `inputs/Main tests` (4 hand-graded calls with expected scorecards) and `inputs/Bulk tests`; `batch_test.py` posts either suite with inline criteria; `compare_results.py` scores result folders.
* **Fixes:** profanity checks agent lines only; announced holds aren't dead air; the empathy drop is measured against the customer's own turns; Probing and Active listening work on question sentences; Paraphrasing and Probing skip greeting and verification lines; Resolved cutoff 0.80 → 0.73.
* **Laya evidence in the repo:** `../laya-finetuning/laya_eval/` (moved from `../laya-test/qa_eval`), `../laya-finetuning/docs/LAYA_TEST_LOG.md`, result folders and probes.
* **Removed:** pre-version-8 inputs (`Archive/`, `inputs(Batch 1)/`, `Completed_tests/`), Ollama-era results and `test_results.xlsx`, `Docs/pipeline_flowchart_laya.html`.

## Changelog: version 10 (Laya)
* **Laya replaces Ollama.** Added `src/services/laya_adapter.py` and removed `llm_adapter.py`.
* **Input caps.** Empathy uses its top 2 snippets, Probing ≤ 150 words, Resolved the last 10 lines, Paraphrasing ≤ 200 words.
* **Paraphrasing** is now a Laya judgement instead of embedding similarity.
* **Active listening** uses difflib similarity > 0.70 instead of embeddings.
* **Batched criteria** are asked as yes/no questions in one Laya call per batch.
* **Coaching** is static text instead of LLM-generated tips.
* **Removed:**
  - `/api/preview-prompt` and the prompt templates;
  - unused GGUF models and Ollama configuration;
  - Ollama-era deployment docs (`DEPLOYMENT.md`, `Docs/DEPLOYMENT_PLAN.md`, `Docs/SETUP_REQUIREMENTS.md`, old flowchart and diagrams).
