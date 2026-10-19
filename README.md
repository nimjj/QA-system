# Automated QA Evaluation System

A locally hosted Quality Assurance engine for customer-support call transcripts. It grades each call against tenant-configurable criteria and returns a scorecard.

Built with **FastAPI**, a deterministic **Python rule engine** and **Laya**, a local yes/no decision engine. Runs fully offline once the Laya weights are on disk.

> **Version 10 (branches `version-10-laya`, and `version-10.1-laya` with the test round fixes):** Ollama / Llama 3.1 and the `nomic-embed-text` embeddings have been **removed** and replaced by Laya. See [Status & known limitations](#status--known-limitations) before relying on the scores.

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
* **The stock Laya weights** (about 1.5 GB), needed only for stock-Laya runs and for the training-data tools. They are read from `LAYA_HF_HOME`, else `../laya-test/hf_home` if that folder exists, else Hugging Face's default cache. A fine-tuned checkpoint (`LAYA_CHECKPOINT`, see `laya-finetuning/`) is self-contained and does not need them.
* **PostgreSQL**, only if criteria come from the database. Requests that include `criteria_data` don't need it.

Folder layout (one repository):
```
<repo root>/            the QA application (src/, Scripts/, inputs/, Docs/ ...)
└── laya-finetuning/    fine-tuning work: data, tools, Colab notebook, run notes
    └── checkpoints/    fine-tuned weights (git-ignored, copy them in; see laya-finetuning/docs/NEW_PC_SETUP.md)
```

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

> **Docker:** `docker-compose.yml` no longer contains Ollama. The QA-service image does **not** yet include Laya, because the local `../laya-test` path is outside the Docker build context. Run the service locally as above; use compose only for Postgres if needed (`docker compose up -d postgres`).

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

Laya runs **out of the box, without training**. Its starting cutoffs come from a 320-item synthetic test ([`laya_eval/RESULTS.md`](laya_eval/RESULTS.md)). Two rounds on full-length calls (the hand-graded `inputs/Main tests` and the labelled `b_*` bulk calls, October 2026) are logged in [`Docs/LAYA_TEST_LOG.md`](Docs/LAYA_TEST_LOG.md). After Round 2, Laya matched 36/44 hand-graded items (Ollama 40/44) and 348/372 `b_*` items:

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
The fine-tuning work lives in this repo, in [`laya-finetuning/`](laya-finetuning/README.md): training data and tools, the Colab notebook, run notes, and the setup guide for a new machine ([`docs/NEW_PC_SETUP.md`](laya-finetuning/docs/NEW_PC_SETUP.md)). The weights are not in git.

* **Serve the fine-tuned model:** set `LAYA_CHECKPOINT` to the checkpoint folder (`laya-finetuning/checkpoints/final-softce-3`). That also switches on the fine-tuned cutoffs and "flow v2" (`Docs/FLOW_V2.md`). `LAYA_FLOW=v1|v2` overrides the flow.
* **Latest results** (AI-written answer keys, not human-reviewed): on 50 independent 10-20 minute calls (`inputs/AG50`), the 7 model-judged items match the key 72.0% with the original flow and 80.3% with flow v2 (Ollama 78.6%; a development set, so optimistic). The 4 golden calls: 42 of 44 items. Details: `Docs/AG50_REPORT.md`, `Docs/AG50_DASHBOARD.html`, `Docs/FLOW_V2.md`, `Docs/LAYA_TEST_LOG.md`.

---

## Testing

```bash
python Scripts/check_prompt_sizes.py          # no model, no server: input caps, scorecards, unit checks
python Scripts/check_prompt_sizes.py --live   # real Laya over all sample calls: verdicts and timing
python Scripts/batch_test.py --label laya     # posts inputs/Main tests to a running service
python Scripts/batch_test.py bulk --label laya  # posts inputs/Bulk tests
python Scripts/compare_results.py ollama laya laya-v2  # result folders vs expected grades and the b_* filename defects
python Scripts/probe_laya.py out.json           # in-process: every Laya probability per call (no server)
python Scripts/laya_cutoffs.py out.json         # best cutoff per check from the b_* filename defects
```
* `batch_test.py` sends the criteria from `resources/criteria_config.json` with every call (`criteria_data`), so it needs no database; `--use-db` turns that off. Results go to `inputs/Test (results)/<suite> (<label>)/`.
* `inputs/Main tests/` holds four hand-graded 16–22 minute calls; their expected scorecards are in `expected/` (see the README there).
* `inputs/Bulk tests/` holds the older samples: `b_*` calls with planted defects named in the filename, `v8_*` and `real_*`. `inputs/Tough checks/` holds three 28-minute trap calls.
* `inputs/Test (results)/` holds the Ollama, Laya and Laya-v2 runs of both suites and the raw Laya probabilities (`Laya probes/`). Older Ollama-era inputs and results were removed in `version-10.1-laya` and remain in git history.

---

## Codebase Map

```
qa-analysis/
├── main.py                      # QA service launcher (:8006)
├── run_gateway.py               # API gateway launcher (:8005)
├── requirements.txt             # FastAPI stack + psycopg2-binary + Laya (pinned GitHub commit)
├── .env.example                 # Laya, server, Postgres and gateway settings
├── setup.bat / setup.sh         # venv + install + .env
├── docker-compose.yml           # Postgres, QA service, gateway, frontend (no Ollama; QA image lacks Laya)
├── Dockerfile / Dockerfile.base / Dockerfile.gateway
├── requests.http                # REST-client requests
├── resources/
│   └── criteria_config.json     # reference criteria for tenant-abc
├── src/
│   ├── api/web_app.py           # FastAPI endpoints
│   ├── api/logger.py            # structured JSON logger
│   ├── gateway/gateway_app.py   # gateway proxy + direct DB criteria routes
│   ├── db/database.py           # PostgreSQL access
│   └── services/
│       ├── dynamic_evaluator.py # orchestration, Laya questions and cutoffs, scoring, static coaching
│       ├── rule_engine.py       # rules and snippet pre-filters
│       └── laya_adapter.py      # Laya Router singleton: predict_yes()
├── Scripts/
│   ├── check_prompt_sizes.py    # verification (stub or --live)
│   ├── batch_test.py            # batch runner against the API
│   ├── compare_results.py       # result folders vs expected grades and b_* defects
│   ├── probe_laya.py            # records every Laya probability per call
│   └── laya_cutoffs.py          # cutoff per check from a probe file
├── laya_eval/                   # synthetic gold set + Laya-vs-Ollama benchmark (RESULTS.md)
├── tests/scoring_test/          # small raw-string test calls
├── inputs/                      # Main tests, Bulk tests, Tough checks, Test (results)
├── frontend/                    # Vite + React dashboard
└── Docs/
    ├── ARCHITECTURE.md          # pipeline and criteria in detail
    ├── AI_HANDOVER.md           # context and constraints for the next maintainer
    ├── LAYA_TEST_LOG.md         # Ollama vs Laya test rounds and the Laya training focus
    ├── PIPELINE_FLOWCHART_LAYA.md   # pre-migration analysis (historical)
    └── postman_collection.json
```

## Changelog: version 10.1 (Laya test rounds)
* **Tests:** `inputs/Main tests` (4 hand-graded calls with expected scorecards) and `inputs/Bulk tests`; `batch_test.py` posts either suite with inline criteria; `compare_results.py` scores result folders.
* **Fixes:** profanity checks agent lines only; announced holds aren't dead air; the empathy drop is measured against the customer's own turns; Probing and Active listening work on question sentences; Paraphrasing and Probing skip greeting and verification lines; Resolved cutoff 0.80 → 0.73.
* **Laya evidence in the repo:** `laya_eval/` (moved from `../laya-test/qa_eval`), `Docs/LAYA_TEST_LOG.md`, result folders and probes.
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
