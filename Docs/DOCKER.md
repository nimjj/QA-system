# Run the v3 QA service in Docker

One container, pipeline v3, **no database**. The files are `Dockerfile.v3`, `docker-compose.v3.yml`, `requirements-docker.txt` and `.dockerignore`.

> **Status:** the files are prepared but the image has **not been built or run yet** (2026-10-22). What was checked without Docker: the compose file parses; every pinned package has a Linux wheel for Python 3.14 (torch from the CPU index); the pinned Laya commit exists; and the exact start-up (offline, empty model cache, `LAYA_FLOW=v3`, weights from `models/final-softce-3`) loads the model in about 10 s and grades a call. If your first build hits a problem, see the table at the end and tell the maintainer.

The older `docker-compose.yml` (Postgres, QA service, gateway, frontend) is the **v2 stack** and is separate. Use the v3 files for v3.

## What you need
* Docker Desktop (or Docker Engine with the compose plugin), allowed **at least 4 GB of memory** (Windows/Mac: Settings, Resources).
* Internet for the first build only (about 1 GB of packages: CPU-only torch, transformers and so on).
* The model weights in `models/final-softce-3/` inside this repo. They are not in git and not in the image, so every fresh clone needs them copied in once (ask the owner for the zip). How that works: `models/README.md`. Check the copy with `python Scripts/verify_weights.py`: it must end with `ALL FILES MATCH` (the folder holds `model.safetensors`, `encoder/`, `tokenizer/`, `questions.json`, `rl_agent_config.json`).

## Start
From the repo root:

```
docker compose -f docker-compose.v3.yml up -d --build
```

Wait until it is ready (about 10 s after the container starts; the first build takes several minutes):

```
curl http://localhost:8006/ready
```

`"status":"ready"` means it can grade. `503` with `"model loading"` means wait; `"model failed to load"` means the weights are missing or wrong (check the logs).

## Use it
* Swagger page: http://localhost:8006/docs
* One call, plain-language result: `python Scripts/try_call.py "inputs/Main tests/gold_01_excellent_22min.json"`
* A whole folder, one JSON reply per call written to `outputs/`: `python Scripts/send_folder.py "inputs/Main tests"`
* The endpoints (`POST /api/evaluate`, `/api/jobs`, `/health`, `/ready`) are described in [`V3.md`](V3.md). The v3 scripts default to port 8006, which is what the container publishes.

## Optional settings
Put them in a file named `.env` next to `docker-compose.v3.yml` (the file is optional and git-ignored; `.env.example` lists them). The flow and the model path are fixed by the compose file and cannot be changed from `.env`.

| Setting | Meaning |
|---|---|
| `QA_API_KEY` | When set, every `/api/` call must send it in the `x-api-key` header. **Set this before exposing the port beyond your own machine.** |
| `CORS_ORIGINS` | Comma-separated browser origins allowed (unset = any) |
| `QUEUE_MAX` | Calls allowed to wait for the model (default 50; more are answered 503) |
| `EVALUATE_TIMEOUT_SEC` | How long `POST /api/evaluate` waits before answering 503 with a job id (default 120) |
| `MAX_REQUEST_BYTES` | Largest request body (default 2,000,000) |
| `LOG_REQUEST_BODIES` | `1` writes full transcripts into the logs. Leave it off wherever real calls are graded |

After changing `.env`: `docker compose -f docker-compose.v3.yml up -d`.

## Day to day
```
docker compose -f docker-compose.v3.yml logs -f qa-v3      # watch the log
docker compose -f docker-compose.v3.yml stop               # stop (keeps the container)
docker compose -f docker-compose.v3.yml down               # remove the container (logs volume stays)
docker compose -f docker-compose.v3.yml up -d --build      # rebuild after pulling new code
```
Capacity (measured outside Docker, one worker): about 12 s per call; 56 calls sent at once gave 51 queued and 5 refused with 503; the worst case (1,500 turns) took 56 s and peaked at 2.7 GB of memory. The container is limited to 4 GB. One worker is on purpose: the model lives inside that process. To grade faster, run a second container on another port rather than adding workers.

## Good to know
* The container runs as a normal user, offline (`HF_HUB_OFFLINE=1`), and mounts `./models` read-only.
* Logs are in the Docker volume `qa_v3_logs` (`/app/logs`). Request bodies are redacted unless `LOG_REQUEST_BODIES=1`.
* The image includes `inputs/` (so `/api/samples` works) but not `inputs/Test (results)/`, `Docs/`, `tests/`, `.env`, or any weights.
* CPU only. A GPU image is not prepared.
* Results are measured against AI-written keys, not human-labelled ones. Real transcripts have not been tried.

## If something goes wrong
| What you see | Likely cause and fix |
|---|---|
| Build fails at `pip install` of Laya | The machine cannot reach github.com (needed once to fetch the pinned Laya commit). Fix the network or proxy and rebuild |
| Build fails at the torch line | Cannot reach download.pytorch.org, or the machine is ARM (the pinned wheel set was checked for x86-64 Linux; on Apple silicon or ARM servers Docker Desktop builds `linux/arm64`, where torch 2.14.1+cpu also exists, but this was not tested) |
| `/ready` says `model failed to load` | `./models/final-softce-3` is missing or incomplete. Check the folder with `python Scripts/verify_weights.py` (must print `ALL FILES MATCH`), then `docker compose -f docker-compose.v3.yml logs qa-v3` |
| Container restarts or is killed | Out of memory. Give Docker at least 4 GB (see "What you need") |
| `connection refused` on 8006 | The container is still starting (wait for `/ready`) or something else uses port 8006: change the left number in `"8006:8006"` |
| `401` on `/api/...` | `QA_API_KEY` is set; send it in the `x-api-key` header |
