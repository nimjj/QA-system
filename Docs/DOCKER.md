# Run the QA service in Docker

The step-by-step guide is **[`DEPLOYMENT_PLAN.md`](../DEPLOYMENT_PLAN.md)** (repo root); it is the only copy, so it cannot drift out of date. This page just says what the Docker files are.

| File | What it does |
|---|---|
| `docker-compose.yml` | The one service, `qa-service` (container `qa_service`, port 8006, network `ciap-qa-network`). Sets `LAYA_FLOW=v3`, the fine-tuned checkpoint `models/final-softce-3` (overridable from `.env`), offline Hugging Face mode, a read-only mount of `./models`, a `./logs` mount, a 4 GB memory cap and `restart: unless-stopped`. |
| `Dockerfile` | Two-stage build (Python 3.14, CPU-only PyTorch, Laya from GitHub at a pinned commit), runs as an unprivileged user, health check on `GET /ready`. The weights are **not** copied into the image. |
| `requirements-docker.txt` | Exact versions used in the image. |
| `.dockerignore` | Keeps `.env`, `models/`, logs, tests and docs out of the image. |

The weights come from Google Drive and are checked with `Scripts/verify_weights.py`: see [`models/README.md`](../models/README.md).

The Docker setup is the **v3 pipeline** only (no database required). The old v2 stack (Postgres, gateway) is not part of `docker-compose.yml` any more; v2 is run locally with `python main.py` and `LAYA_FLOW` unset (see the README).

Troubleshooting table: section 11 of `DEPLOYMENT_PLAN.md`.
