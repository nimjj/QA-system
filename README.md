# Automated QA Evaluation System

A locally hosted Quality Assurance engine for customer-support call transcripts. It grades each call against tenant-configurable criteria and returns a scorecard.

Built with **FastAPI**, a deterministic **Python rule engine** and **Laya**, a local yes/no decision engine. Runs fully offline once the Laya weights are on disk.

> **Version 10 (branch `version-10-laya`):** Ollama / Llama 3.1 and the `nomic-embed-text` embeddings have been **removed** and replaced by Laya. See [Status & known limitations](#status--known-limitations) before relying on the scores.

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
* **The Laya checkout next to this repo**, at `../laya-test/laya`. `requirements.txt` installs it from there in editable mode.
* **The Laya model weights** (about 1.5 GB). By default they are read from `../laya-test/hf_home`. If that folder is missing, set `LAYA_HF_HOME`, or let Hugging Face download them on first use.
* **PostgreSQL**, only if criteria come from the database. Requests that include `criteria_data` don't need it.

Expected folder layout:
```
QA 2/
├── qa-analysis/        ← this repo
└── laya-test/
    ├── laya/           ← Laya source (pip install -e)
    └── hf_home/        ← downloaded Laya weights
```

---

## Setup

Windows: run `setup.bat`. Linux/macOS: run `./setup.sh`. Or do it by hand:
```bash
python -m venv .venv
.venv\Scripts\activate            # Windows
source .venv/bin/activate         # Linux/macOS
pip install -r requirements.txt   # FastAPI stack, psycopg2-binary, and Laya from ../laya-test/laya
copy .env.example .env            # Windows  (cp on Linux/macOS)
```

### Environment (`.env`)
| Variable | Default | Purpose |
|---|---|---|
| `LAYA_MODEL` | `english` | Laya checkpoint for every check (the English one tested best) |
| `LAYA_HF_HOME` | empty → `../laya-test/hf_home` | Folder holding the Laya weights |
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
| 2 | Hold time and Dead Air | Rule: 2 or more gaps over 30 s fail |
| 3 | Personalized the call | Rule: customer name used by the agent |
| 4 | Empathy & Acknowledgment | Laya on the 2 worst upset-customer moments |
| 5 | Build rapport / professionalism | Phrase list, then Laya |
| 6 | Paraphrasing | Laya: customer opening plus the first agent lines |
| 7 | Verified customer | Rule: PIN, address or security question within 4 minutes |
| 8 | Probing | Laya on the real (non-boilerplate) agent questions |
| 9 | Took ownership | Phrase list, then Laya |
| 10 | Active listening | Near-identical agent questions, then Laya |
| 11 | Confirmed the issue is resolved | Laya on the last 10 lines |

**Auto-fail (score 0):** profanity from a fixed list anywhere in the call, or a FAIL in a category named "AUTO FAIL".

---

## Status & known limitations

Laya runs **out of the box, without training**. Its cutoffs come from a 320-item synthetic test (`../laya-test/qa_eval/RESULTS.md`). Checks on full-length sample calls (October 2026) show:

| Check | State |
|---|---|
| Probing, Active listening, Ownership | Reasonable |
| Confirmed resolved | Fails almost every call; the cutoff doesn't transfer to 10-line endings |
| Rapport | Inverted: benign trigger phrases score as ruder than truly rude lines |
| Empathy | Cutoff too strict (failed every time it ran) |
| Paraphrasing | New; doesn't separate good from bad yet |

Next step: label a few hundred real calls, re-tune the `pass_threshold` values in `LAYA_CHECKS`, and fine-tune Laya where re-tuning isn't enough. Until then, treat these five scores as provisional.

---

## Testing

```bash
python Scripts/check_prompt_sizes.py          # no model, no server: input caps, scorecards, unit checks
python Scripts/check_prompt_sizes.py --live   # real Laya over all sample calls: verdicts and timing
python Scripts/batch_test.py                  # posts every inputs/*.json to a running service
```
* Sample payloads are in `inputs/`. They include `b_*` calls with planted defects named in the filename, `v8_*`, `real_*`, and the version-8 sets in `Archive/`, `Completed_tests/`, `Tough checks/` and `inputs(Batch 1)/`.
* Result files in `inputs/Test (results)/` from before version 10 were produced by Ollama.

---

## Codebase Map

```
qa-analysis/
├── main.py                      # QA service launcher (:8006)
├── run_gateway.py               # API gateway launcher (:8005)
├── requirements.txt             # FastAPI stack + psycopg2-binary + Laya (../laya-test/laya)
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
│   └── test_results.xlsx        # historical scores (Ollama era, v8.1 to v9.1)
├── tests/scoring_test/          # small raw-string test calls
├── inputs/                      # sample payloads and results
├── frontend/                    # Vite + React dashboard
└── Docs/
    ├── ARCHITECTURE.md          # pipeline and criteria in detail
    ├── AI_HANDOVER.md           # context and constraints for the next maintainer
    ├── PIPELINE_FLOWCHART_LAYA.md / pipeline_flowchart_laya.html   # pre-migration analysis (historical)
    └── postman_collection.json
```

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
