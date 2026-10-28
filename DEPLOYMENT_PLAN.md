# Docker Deployment Guide: QA service (pipeline v3)

Builds, starts and checks the QA grading service, **qa-service** (port 8006), with Docker. It is one container: the Python rule checks plus the fine-tuned Laya model, graded on CPU, no GPU, no queue, no LLM server.

> The service is **synchronous**: `POST /api/evaluate` returns the finished scorecard in the same response (a 16 to 22 minute call takes about 4 to 30 seconds). There is no job id and nothing to poll. Tenant scorecards come from PostgreSQL when the database is configured and reachable, and from a built-in 11-item scorecard when it is not.
> **The model weights are not in git and not in the image.** Step 3 gets them from Google Drive. Without them the service stays up but refuses to grade (`/ready` and `/api/evaluate` answer 503 and say why).

Every result in the repo is measured against AI-written answer keys, not independent human grades, and real call recordings have not been tried yet; treat scores as provisional.

---

## 1. What you need

* Docker with Compose v2 (`docker compose version`), at least **4 GB of memory** for Docker (the container uses about 2.1 GB), about 3 GB of disk (image 1.8 GB plus the 808 MB weights).
* Internet access during `docker compose up --build` (downloads Python packages and the CPU build of PyTorch). Nothing is downloaded at run time: the model runs offline.
* Access to the Google Drive folder with the weights (step 3). It is shared inside the company's Google account only.

## 2. Get the code

```bash
git clone https://github.com/nimjj/QA-system.git
cd QA-system          # branch main
mkdir -p logs         # Linux servers: create it yourself, so it is not owned by root
```

## 3. Get the model weights (required, once per machine)

Download the Google Drive folder **final-softce-3**:
<https://drive.google.com/drive/folders/16a8ibMjEJ9CUwDURHmjLPu0fBUhWhdIj>

1. Open the link (work account), right-click the folder, **Download**. Drive gives a zip of about 800 MB.
2. Unzip it so the files sit directly in `models/final-softce-3/` inside the repo. This file must exist: `models/final-softce-3/model.safetensors`.
3. Check the copy, from the repo root (needs only Docker):

```bash
docker compose run --rm --no-deps qa-service python Scripts/verify_weights.py
```

Every line must say `OK` and the last line must be **`ALL FILES MATCH`**. If not (`MISSING`, `WRONG SIZE`, `CHANGED`), download again. Details and a server-without-browser tip: [`models/README.md`](models/README.md).

## 4. Configure (optional)

Docker runs with the defaults and needs **no** `.env` file. Create one only for what you want to change:

```bash
cp .env.example .env
```

| Setting | When you need it |
|---|---|
| `DB_HOST` `DB_PORT` `DB_NAME` `DB_USER` `DB_PASSWORD` | Per-tenant scorecards from PostgreSQL (tables `app.qa_*` and `connect_first.tenants`). Inside Docker `localhost` is the container itself: use the database's host name, or `host.docker.internal` for a PostgreSQL on the Docker host (compose maps it, also on Linux). |
| `QA_API_KEY` | Require `x-api-key: <value>` on every `/api/` call. `/health` and `/ready` stay open. |
| `CORS_ORIGINS`, `MAX_REQUEST_BYTES` | Browser origins allowed (default all), request size limit (default 2 MB, answered with 413). |
| `LOG_REQUEST_BODIES` | Leave `0` in production: customer names and transcripts are redacted from the logs. |

`LAYA_FLOW`, `LAYA_CHECKPOINT` (the fine-tuned weights), `HF_HOME` and `HF_HUB_OFFLINE` are set by `docker-compose.yml` itself; a stale `.env` cannot switch the flow or send the model to the network.

## 5. Start

```bash
docker compose up -d --build
docker logs -f qa_service
```

The first build takes a few minutes. When the weights are in place the log shows:

```text
{"log_type": "APP", "message": "Initializing model weights and warming up..."}
{"log_type": "APP", "message": "Model loaded successfully. Service ready."}
INFO:     Uvicorn running on http://0.0.0.0:8006 (Press CTRL+C to quit)
```

## 6. Health and readiness

```bash
curl http://localhost:8006/health      # {"status":"healthy","service":"qa-service"}
curl http://localhost:8006/ready       # {"status":"ready","flow":"v3","model_ready":true}   (about 10 to 15 s after start)
docker ps --filter name=qa_service     # STATUS ... (healthy)
```

`/ready` answers 503 while the model loads, or permanently with the reason when it could not load (see section 11).

## 7. Acceptance test (do this before connecting the backend)

Grade the bundled excellent call **inside the container** (no Python needed on the host):

```bash
docker compose exec qa-service python Scripts/try_call.py "inputs/Main tests/gold_01_excellent_22min.json"
```

Expected: `FINAL SCORE 100.0 / 100` and, on the last line, `pipeline v3, model final-softce-3`. The four bundled calls in `inputs/Main tests/` score **100.0 / 88.3 / 50.0 / 30.0** with the fine-tuned model (the reference answer key says 100.0 / 88.3 / 56.7 / 13.3; 42 of 44 items agree). If the last line says `model stock` instead, the fine-tuned weights are not in use (with compose this cannot happen by accident: an empty or missing `LAYA_CHECKPOINT` falls back to `models/final-softce-3`; stock Laya scores 88.3 / 83.4 / 66.7 / 30.0 on these calls and is not for production).

## 8. REST example

```bash
curl -X POST http://localhost:8006/api/evaluate -H "Content-Type: application/json" -d '{
  "call_id": "smoke_001", "tenant_id": "208", "channel": "Call", "customer_name": "Alex",
  "transcript": [
    {"speaker": "Agent",    "text": "Thank you for calling S-Net, my name is Sam. How can I help you today?", "start_time_sec": 0},
    {"speaker": "Customer", "text": "My internet has been down since this morning and I am really frustrated.", "start_time_sec": 6, "sentiment_score": -35},
    {"speaker": "Agent",    "text": "I am so sorry about that, Alex, I understand how frustrating that is. First, can you confirm the PIN on your account?", "start_time_sec": 12},
    {"speaker": "Customer", "text": "It is 4417.", "start_time_sec": 20, "sentiment_score": -20},
    {"speaker": "Agent",    "text": "Thank you, Alex, you are verified. What colour is the light on your router?", "start_time_sec": 26},
    {"speaker": "Customer", "text": "It is flashing red.", "start_time_sec": 33, "sentiment_score": -15},
    {"speaker": "Agent",    "text": "Has anything changed recently, like a power cut or moving the router?", "start_time_sec": 39},
    {"speaker": "Customer", "text": "No, nothing at all.", "start_time_sec": 46, "sentiment_score": -10},
    {"speaker": "Agent",    "text": "Thanks. I will reset your line profile from my side now. That is done.", "start_time_sec": 52},
    {"speaker": "Customer", "text": "Okay, hold on.", "start_time_sec": 70, "sentiment_score": -5},
    {"speaker": "Agent",    "text": "Is it working now?", "start_time_sec": 85},
    {"speaker": "Customer", "text": "Yes, the light just turned green and it works. Thank you so much!", "start_time_sec": 92, "sentiment_score": 25},
    {"speaker": "Agent",    "text": "Great, so the issue is resolved. Thank you for choosing S-Net, have a great day!", "start_time_sec": 98}
  ]
}'
```

(On Windows PowerShell put the JSON in a file and use `curl.exe -d "@call.json"`, or use `requests.http` / `Docs/postman_collection.json`.) Real response from this call, shortened:

```json
{
  "call_id": "smoke_001", "tenant_id": "208", "status": "completed",
  "result": {
    "final_score": 90.0, "auto_failed_count": 0,
    "category_summary": [ {"category": "Soft Skills", "passed": 5, "total": 5, "ratio": "05/05"},
                          {"category": "Technical Knowledge", "passed": 5, "total": 6, "ratio": "05/06"} ],
    "scorecard": [ {"category": "Soft Skills", "name": "Branding and Survey Check", "rating": "PASS",
                    "coaching": "Agent successfully used required opening and closing branding scripts.", "evidence_turns": [0, 12]},
                   {"category": "Technical Knowledge", "name": "Paraphrasing", "rating": "FAIL",
                    "coaching": "Failed to paraphrase core issue."}, "..." ],
    "is_auto_fail": false, "auto_fail_reason": null,
    "meta": {"flow": "v3", "model": "final-softce-3", "seconds": 3.5}
  }
}
```

A 13-turn made-up call is only a format example: very short calls are outside what the model was tuned on, so do not judge quality from it (use section 7). Rules to know: `sentiment_score` goes on **customer** turns only (negative = upset); the branding check looks for "thank you for calling / choosing **S-Net**" (the brand is set in `src/v3/config/v3.json`); `transcript` may also be a plain string `"[00:05] Agent: ...\n[00:12] Customer: ..."` (no sentiment, so Empathy never triggers). Errors: 401 wrong key, 413 too large, 422 unusable transcript, 503 model not ready.

## 9. Tenant scorecards (PostgreSQL)

```bash
curl http://localhost:8006/api/tenants/208/criteria
curl -X PATCH http://localhost:8006/api/tenants/208/criteria/item-branding/toggle -H "Content-Type: application/json" -d '{"is_active": false}'
```

With a reachable database, `/api/evaluate` grades each tenant against its own active items and the weights re-balance. **Without one the service silently grades every tenant against the built-in scorecard** (so toggles are ignored and the response does not say so) and the toggle route answers 500. After setting `DB_*` check that `GET /api/tenants/<id>/criteria` returns that tenant's items, not `"version": "default-v3"`.

## 10. Day-to-day

| Task | Command |
|---|---|
| Logs | `docker logs -f qa_service`, and `./logs/app.log` on the host (JSON lines) |
| Restart | `docker compose restart qa-service` |
| Update the code | `git pull && docker compose up -d --build` (the weights in `./models` are not touched) |
| New weights | replace `./models/final-softce-3`, run the check in step 3, `docker compose restart qa-service` |
| Stop / remove | `docker compose down` (add `--rmi local` to drop the image) |

Capacity: one model answers one question at a time, so simultaneous calls share it (4 simultaneous calls all returned after about 35 s) and there is no queue. Callers should use a timeout of at least 120 s and keep concurrency low (2 to 4). Memory about 2.1 GB per container; cap in compose is 4 GB.

## 11. Troubleshooting

| Symptom | Cause and fix |
|---|---|
| `/ready` 503, `"load_error": "... LAYA_CHECKPOINT is not a folder: /app/models/final-softce-3"` | The weights are missing or in the wrong place. Do step 3; `models/final-softce-3/model.safetensors` must exist on the host. Then `docker compose restart qa-service`. |
| `/ready` 503, `"... does not contain 'rl_agent_config.json'"` | The folder exists but is empty or nested one level too deep (`models/final-softce-3/final-softce-3/...`). Move the files up one level. |
| `verify_weights.py` prints `WRONG SIZE` or `CHANGED` | Incomplete or damaged download. Download the Drive folder again. |
| `/api/evaluate` 503 "model is still loading" | Normal for about 10 to 15 s after start. Retry. |
| `meta.model` says `stock` (scores 88.3 / 83.4 / 66.7 / 30.0 on the bundled calls) | Someone started the image outside compose with an empty `LAYA_CHECKPOINT` (for example `docker run -e LAYA_CHECKPOINT=`). Start it with `docker compose up -d` or set `LAYA_CHECKPOINT=models/final-softce-3`. |
| `/api/evaluate` 413 or 422 | Body over 2 MB, or no readable turns in the transcript. The message says which. |
| Every tenant gets the same 11 items | PostgreSQL is not reachable and the service fell back (section 9). Check `DB_HOST` (not `localhost` inside Docker), credentials, and that the tables exist. |
| Branding FAIL on every call for another company | The rule only recognises the brand in `src/v3/config/v3.json` (`s-net`). Change `brand` there and rebuild. |
| `Bind for 0.0.0.0:8006 failed: port is already allocated` | Something else uses 8006: stop it, or change the left side of `"8006:8006"` in `docker-compose.yml`. |
| Start-up prints `WARNING: cannot write /app/logs/app.log` | Not fatal: the service logs to the console only (`docker logs`). On Linux the `logs` folder was created by Docker as root: `mkdir -p logs` yourself (as your user) before the first start, or `sudo chown -R 1000 logs`, to get the log file. |
| Build fails fetching packages | The build needs internet (PyPI, the PyTorch CPU index, GitHub for the pinned Laya commit). Check proxy settings. |
