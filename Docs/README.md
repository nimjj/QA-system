# Documentation Directory & Sitemap

> **Status on `main` (27 Oct 2026):** this page describes the earlier `app-v3` branch. On `main` the job queue (`/api/jobs`, `src/v3/jobs.py`) and `docker-compose.v3.yml` were removed: `/api/evaluate` is synchronous, tenant scorecards come from PostgreSQL with the built-in 11 items as fallback, and the Docker setup is `docker-compose.yml` with the fine-tuned weights mounted from `models/`. The current deployment guide is [`DEPLOYMENT_PLAN.md`](../DEPLOYMENT_PLAN.md).

Welcome to the documentation suite for the **Automated QA Analysis System** (`QA-system`). 

> **Quick Orientation:**  
> • If you are an **AI Assistant** (Claude Code, Antigravity, or other LLMs): Read [`AI_HANDOVER.md`](AI_HANDOVER.md) first.  
> • If you are a **Human Engineer / Team Member**: Read [`SYSTEM_AND_FLOW_V2_GUIDE.md`](SYSTEM_AND_FLOW_V2_GUIDE.md) or [`CODEBASE_GUIDE.md`](CODEBASE_GUIDE.md).  
> • If you are looking for **Model Training & Research**: See the sibling repository at `../laya-finetuning/`.

---

## Master Documentation Catalog

| Document | Primary Audience | Description & Key Topics Covered |
|---|---|---|
| [`AI_HANDOVER.md`](AI_HANDOVER.md) | **AI Assistants & Autonomous Agents** | **Comprehensive AI Operational Manual.** Detailed instructions on hard constraints (no agent sentiment, never commit weights, AI provenance disclosure), the frozen file contract, deep code-level architecture of Pipeline v2 & v3, single-worker job queue, the 11 criteria reference table, exact shell verification commands, and debugging recipes. |
| [`SYSTEM_AND_FLOW_V2_GUIDE.md`](SYSTEM_AND_FLOW_V2_GUIDE.md) | **Engineers & Architects** | **Master System Architecture & Flow Guide.** Includes high-level Mermaid system architecture, the complete Flow v2 call grading lifecycle diagram, side-by-side evolution to Pipeline v3, the 11 QA criteria breakdown, the two-repository map (`QA-system` vs `laya-finetuning`), and deployment runbooks. |
| [`CODEBASE_GUIDE.md`](CODEBASE_GUIDE.md) | **New Team Members** | **Plain-Language Onboarding Guide.** Walkthrough explaining the system in simple terms, untangling terminology (v1 vs v2 vs v3, Flow v1 vs Flow v2, model checkpoints), the runtime architecture, and file locations. |
| [`FLOW_DIAGRAMS.md`](FLOW_DIAGRAMS.md) | **Developers & Designers** | **Visual Process Maps.** Contains 11 Mermaid diagrams detailing the whole stack: system map, pipeline selection logic, pipeline v2 vs v3 requests, one model call, side-by-side check comparisons, scoring math, candidate gates, and model provenance. |
| [`QA_System_Handover_v3.pdf`](QA_System_Handover_v3.pdf) | **Tech Lead & Integrators** | **Backend Integration Handover.** Architecture, request flow, the REST endpoints with a real request and response example, the scoring model, where to download the weights, and run notes. Start here to connect the service to the main backend. |
| [`../DEPLOYMENT_PLAN.md`](../DEPLOYMENT_PLAN.md) | **DevOps & Infrastructure** | **Docker Deployment Guide.** Step-by-step runbook: download the weights from Google Drive, `docker compose up -d --build`, readiness, acceptance test, REST example, tenant scorecards, troubleshooting. |
| [`DOCKER.md`](DOCKER.md) | **DevOps & Infrastructure** | **What each Docker file does.** Short pointer to `DEPLOYMENT_PLAN.md` for `docker-compose.yml` (fine-tuned weights mounted read-only from `models/`), the `Dockerfile` and `requirements-docker.txt`. |
| [`V3.md`](V3.md) | **Developers & Reviewers** | **Pipeline v3 Technical Specification.** Implementation details of `src/v3/` (job queue, input normalizer, question mark restoration, schema-driven scoring), plus accuracy findings on Candidate Gates (Resolved and Ownership). |
| [`FLOW_V2.md`](FLOW_V2.md) | **ML Engineers & QA** | **Flow v2 Window Selection Rationale.** Documents why call-structure snippet windowing replaced fixed line counts, the owner's decision on strict per-outburst Empathy, and benchmark accuracy lifts on `AG50`. |
| [`FLOW_V2_LAB.md`](FLOW_V2_LAB.md) & [`FLOW_V2_REGRESSION.md`](FLOW_V2_REGRESSION.md) | **ML Engineers** | **Laboratory Findings & Regression Safety.** Detailed logs of candidate window experiments and regression safety checks on bulk calls ensuring Flow v2 caused no regressions. |
| [`ARCHITECTURE.md`](ARCHITECTURE.md) | **Database & Legacy Specs** | **Historical Version-10 Specification.** Original system architecture document; the sole location containing the PostgreSQL database schema and tenant table layout. |
| [`postman_collection.json`](postman_collection.json) | **API Testers** | **Postman Collection.** Ready-to-import REST requests for `POST /api/evaluate`, `POST /api/jobs`, `GET /api/jobs/{id}`, `/health`, and `/ready`. |

---

## Sibling Research Repository Documentation (`../laya-finetuning/`)

All documentation regarding model fine-tuning, training datasets, and experimental runs lives in the sibling repository `../laya-finetuning`:

| Sibling Document | Path | Description |
|---|---|---|
| **Data Plan** | `../laya-finetuning/docs/DATA_PLAN.md` | The synthetic data generation roadmap, industry/persona matrix, and 3-stage volume ramp. |
| **Labelling Guide** | `../laya-finetuning/docs/LABELLING_GUIDE.md` | Ground-truth rubrics for all criteria ("tone beats words", snippet-level judging). |
| **Generation Notes** | `../laya-finetuning/docs/GENERATION_NOTES.md` | Discovery of synthetic shortcuts (length & word markers) and mandatory countermeasure rules. |
| **New PC Setup** | `../laya-finetuning/docs/NEW_PC_SETUP.md` | Cloning both repositories side-by-side, setting up environments, and Google Drive weights setup. |
| **Phase 0 Answer Key** | `../laya-finetuning/docs/PHASE0_ANSWER_KEY.md` | Provenance disclosure and resolution of contested verdicts for the 4 Main golden calls. |
| **Laya Test Log** | `../laya-finetuning/docs/LAYA_TEST_LOG.md` | Historical test logs across all model rounds (Rounds 1–8). |
| **AG50 Report** | `../laya-finetuning/docs/AG50_REPORT.md` | Analysis of the independent 50-call benchmark evaluated against Ollama. |
| **Checkpoints Catalogue** | `../laya-finetuning/runs/CHECKPOINTS.md` | Catalogue and status of all trained checkpoints (`final-softce-3`, `ft5`, `ft6`). |

---

## Archival Record (Cleaned up 2026-10-22)

Task-specific briefs whose goals are completed were archived to git history (available via `git show 8a6842b:Docs/<name>` or `a7ace67`):
* `ANTIGRAVITY_AGT_BRIEF.md`, `ANTIGRAVITY_AGB_BRIEF.md`, `ANTIGRAVITY_AGB2_BRIEF.md`, `ANTIGRAVITY_AGC_BRIEF.md` (AI call-writing task briefs).
* `ANTIGRAVITY_TEST_BRIEF.md`, `ANTIGRAVITY_V2_COMMON.md`, `ANTIGRAVITY_V2_EXAMPLES.md` (AI authoring rulebooks).
* `AG50_RESULTS.md`, `EVAL50_RESULTS.md`, `LAYA_ROUND4_COMPARISON.md` (Regenerable per-call result tables).
