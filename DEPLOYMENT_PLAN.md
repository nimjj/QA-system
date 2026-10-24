# Local Docker Deployment Plan

This guide builds, runs, and verifies the Python ML QA Analysis service in this repo —
**qa-service** (:8006) — locally with Docker.

> Pipeline v3 provides high-performance, synchronous QA evaluation with auto-fail
> short-circuiting, in-memory LRU caching, and multi-tenant criteria weighting. It
> is called directly by **ciap-api** or upstream orchestrators via synchronous REST.
> There is no async job queue or polling required.

---

## 1. Prerequisites & Directory Setup

Ensure Docker is running and create the host directories for audit logs and the persistent
model cache:

```bash
mkdir -p logs models
docker network create ciap-network
```

> `models` persists the Laya weights and Hugging Face cache on the host (`./models`). The
> ~1.7 GB model downloads once; later launches load locally in a couple of seconds.

---

## 2. Environment Configuration

```bash
cp .env.example .env
```

Review the key settings in `.env`:
- `LAYA_FLOW=v3` — Enables the optimized Pipeline v3 evaluation engine.
- `LAYA_CHECKPOINT=""` — Leave empty to load the stock Laya model, or specify a custom checkpoint path under `models/`.
- `SERVER_PORT=8006` — Service port.
- `SERVER_HOST=0.0.0.0` — Bind host.
- `DB_HOST`, `DB_PORT`, `DB_NAME`, `DB_USER`, `DB_PASSWORD` — Optional PostgreSQL connection for dynamic tenant criteria toggles (defaults gracefully to built-in `criteria.json` if database is unavailable).

---

## 3. Build Docker Image

Build the production multi-stage image (Python 3.14, PyTorch CPU, Hugging Face Transformers, Laya, FastAPI):

```bash
docker build -t qa-service:v3 --no-cache .
```

---

## 4. Run the Service

### Option A: Docker Run CLI
> - `-t` allocates a pseudo-TTY so the model-download progress updates cleanly in place.
> - `-v "${PWD}/models:/app/models"` persists the weights on the host.
> - `-v "${PWD}/logs:/app/logs"` stores rolling application audit logs.

```bash
docker run -d -t \
  --name qa_service \
  --network ciap-network \
  -p 8006:8006 \
  --env-file .env \
  -v "${PWD}/logs:/app/logs" \
  -v "${PWD}/models:/app/models" \
  qa-service:v3
```

### Option B: Docker Compose
Alternatively, launch using Docker Compose:

```bash
docker compose up -d --build
```

---

## 5. Monitor Model Download & Container Logs

```bash
docker logs -f qa_service
```

**Sample Output:**
```text
{"log_type": "APP", "message": "Starting LLM QA Analysis Service..."}
INFO:     Started server process [1]
INFO:     Waiting for application startup.
{"log_type": "APP", "message": "Initializing model weights and warming up..."}
Fetching 5 files: 100%|##########| 5/5 [00:00<00:00, 797.37it/s]
{"log_type": "APP", "message": "Model loaded successfully. Service ready."}
{"log_type": "APP", "message": "Stateless QA Service started. Logging live to logs/app.log."}
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8006 (Press CTRL+C to quit)
```

---

## 6. Health & Readiness Verification

```bash
# Liveness Check (:8006)
curl http://localhost:8006/health

# Readiness Check (:8006 - confirms model is loaded into memory)
curl http://localhost:8006/ready
```

**Expected Responses:**
```json
{"status": "healthy", "service": "qa-service"}
{"status": "ready", "flow": "v3", "model_ready": true}
```

---

## 7. Smoke Test (Synchronous Evaluation)

Evaluate a call transcript for **Tenant 208 (ADEPT Tech)**:

```bash
curl -X POST http://localhost:8006/api/evaluate \
  -H "Content-Type: application/json" \
  -d '{
    "call_id": "call_test_001",
    "tenant_id": "208",
    "channel": "Call",
    "customer_name": "Alex",
    "transcript": [
      {"speaker": "Agent", "text": "Thank you for calling ADEPT Tech, my name is Sam.", "start_time_sec": 0},
      {"speaker": "Customer", "text": "My internet is down and I am very upset.", "start_time_sec": 5, "sentiment_score": -35},
      {"speaker": "Agent", "text": "I am so sorry to hear your internet is down. Can you confirm your account PIN?", "start_time_sec": 10},
      {"speaker": "Customer", "text": "It is 1234.", "start_time_sec": 18, "sentiment_score": -10},
      {"speaker": "Agent", "text": "Thanks Alex. What colour is the light on your router?", "start_time_sec": 24},
      {"speaker": "Customer", "text": "It is flashing red.", "start_time_sec": 30, "sentiment_score": -5},
      {"speaker": "Agent", "text": "I have reset the line profile from our end. Is it working now?", "start_time_sec": 45},
      {"speaker": "Customer", "text": "Yes, it just turned green and works now! Thank you so much.", "start_time_sec": 55, "sentiment_score": 25},
      {"speaker": "Agent", "text": "Glad to help! Thank you for choosing ADEPT Tech, have a great day.", "start_time_sec": 65}
    ]
  }'
```

**Sample Response:**
```json
{
  "call_id": "call_test_001",
  "tenant_id": "208",
  "status": "completed",
  "result": {
    "final_score": 100.0,
    "auto_failed_count": 0,
    "category_summary": [
      {
        "category": "Soft Skills",
        "passed": 4,
        "total": 4,
        "ratio": "04/04"
      },
      {
        "category": "Technical Knowledge",
        "passed": 6,
        "total": 6,
        "ratio": "06/06"
      }
    ],
    "scorecard": [
      ...
    ],
    "is_auto_fail": false,
    "auto_fail_reason": null,
    "meta": {
      "flow": "v3",
      "model": "stock",
      "seconds": 0.01
    }
  }
}
```

---

## 8. Tenant Criteria Management & Toggle Test

Check and toggle criteria for Tenant 208 dynamically:

```bash
# Get active criteria for Tenant 208
curl http://localhost:8006/api/tenants/208/criteria

# Toggle Branding criterion OFF for Tenant 208
curl -X PATCH http://localhost:8006/api/tenants/208/criteria/item-branding/toggle \
  -H "Content-Type: application/json" \
  -d '{"is_active": false}'

# Toggle Branding criterion ON for Tenant 208
curl -X PATCH http://localhost:8006/api/tenants/208/criteria/item-branding/toggle \
  -H "Content-Type: application/json" \
  -d '{"is_active": true}'
```

---

## 9. Teardown / Cleanup

```bash
docker stop qa_service
docker rm qa_service
docker network rm ciap-network   # optional
```
