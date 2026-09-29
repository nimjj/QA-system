# Docker Deployment & Testing Plan

This document outlines the step-by-step procedures to build, deploy, verify, and test the multi-container QA Analysis System using Docker and Docker Compose.

---

## 1. Architecture Overview

| Container | Image / Dockerfile | Exposed Port | Role |
|---|---|---|---|
| **`qa_ollama`** | `ollama/ollama:latest` | `11434:11434` | Local LLM inference (`llama3.1`) & embeddings (`nomic-embed-text`). |
| **`qa_service`** | `Dockerfile` | `8006:8006` | FastAPI core service (evaluator, rule engine, scorer, DB active criteria). |
| **`qa_gateway`** | `Dockerfile.gateway` | `8005:8005` | Reverse proxy + direct fast-path PostgreSQL routes for criteria fetch & toggle. |

* **PostgreSQL:** Runs on the host machine (`host.docker.internal:5432`).
* **Frontend:** Runs locally on port `5173` via Vite or reverse proxy.

---

## 2. Prerequisites

1. Docker Desktop installed and running.
2. PostgreSQL running on port `5432` with database `callIntelligence` (or configured database in `.env`).
3. Ensure `.env` exists in the repository root:
   ```bash
   cp .env.example .env
   ```

---

## 3. Deployment Commands

### Step 1: Build and Launch Containers
Run in the repository root:

```bash
docker-compose up -d --build
```

### Step 2: Verify Running Containers
Check that all 3 containers are healthy and running:

```bash
docker-compose ps
```

Expected output:
```text
NAME         IMAGE                  COMMAND                  SERVICE      CREATED         STATUS         PORTS
qa_gateway   qa-system-gateway      "uvicorn src.gateway…"   gateway      Up ...          Up ...         0.0.0.0:8005->8005/tcp
qa_ollama    ollama/ollama:latest   "/bin/ollama serve"      ollama       Up ...          Up ...         0.0.0.0:11434->11434/tcp
qa_service   qa-system-qa-service   "uvicorn src.api.web…"   qa-service   Up ...          Up ...         0.0.0.0:8006->8006/tcp
```

### Step 3: Inspect Service Logs
```bash
# Stream all logs
docker-compose logs -f

# Or view specific service logs
docker-compose logs -f gateway
docker-compose logs -f qa-service
docker-compose logs -f ollama
```

---

## 4. Model Initialization (First Run Only)

Download the required LLM and embedding models into the `qa_ollama` container volume:

```bash
# Pull LLM for reasoning and dynamic checks
docker exec -it qa_ollama ollama pull llama3.1

# Pull embedding model for vector cosine similarity
docker exec -it qa_ollama ollama pull nomic-embed-text
```

Verify downloaded models:
```bash
docker exec -it qa_ollama ollama list
```

---

## 5. Verification & Testing Commands

### Test 1: API Gateway Health Check
Verify the Gateway container is responsive and connected to target QA Service:

**cURL / Bash:**
```bash
curl -s http://localhost:8005/health
```

**PowerShell:**
```powershell
Invoke-RestMethod -Uri "http://localhost:8005/health" -Method Get
```

**Expected Response:**
```json
{
  "status": "healthy",
  "service": "api-gateway",
  "target_app": "http://qa-service:8006"
}
```

---

### Test 2: Direct Criteria Fetch via Gateway (Fast-Path to DB)
Verify that the Gateway executes direct database queries without routing through QA Service:

**cURL / Bash:**
```bash
curl -s http://localhost:8005/api/tenants/tenant-test/criteria
```

**PowerShell:**
```powershell
Invoke-RestMethod -Uri "http://localhost:8005/api/tenants/tenant-test/criteria" -Method Get
```

---

### Test 3: Direct Criteria Toggle via Gateway (Fast-Path to DB)
Verify toggling a criterion directly through the Gateway:

**cURL / Bash:**
```bash
curl -s -X PATCH http://localhost:8005/api/tenants/tenant-test/criteria/item-branding/toggle \
  -H "Content-Type: application/json" \
  -d '{"is_active": false}'
```

**PowerShell:**
```powershell
Invoke-RestMethod -Uri "http://localhost:8005/api/tenants/tenant-test/criteria/item-branding/toggle" `
  -Method Patch `
  -Headers @{"Content-Type" = "application/json"} `
  -Body '{"is_active": false}'
```

**Expected Response:**
```json
{
  "tenant_id": "tenant-test",
  "line_item_id": "item-branding",
  "is_active": false
}
```

---

### Test 4: End-to-End Evaluation via Gateway (Proxied Path)
Verify that `/api/evaluate` proxies to `qa_service`, runs the rule engine and Ollama, and returns scoring breakdown:

**cURL / Bash:**
```bash
curl -s -X POST http://localhost:8005/api/evaluate \
  -H "Content-Type: application/json" \
  -d '{
    "tenant_id": "tenant-test",
    "channel": "Call",
    "customer_name": "Grace",
    "transcript": "[00:00] Agent: Thank you for calling S-Net. My name is Alex. How can I help you today?\n[00:05] Client: My router keeps resetting.\n[00:08] Agent: Could I verify your PIN and billing address?\n[00:12] Client: PIN 5521, 42 Main St.\n[00:15] Agent: Verified, thank you Grace. Let me reset your line profile.\n[00:25] Agent: Line reset complete. Is the connection working now?\n[00:30] Client: Yes, perfect, thanks Alex!\n[00:35] Agent: Thank you for choosing S-Net, have a great day!"
  }'
```

**PowerShell:**
```powershell
$body = @{
    tenant_id     = "tenant-test"
    channel       = "Call"
    customer_name = "Grace"
    transcript    = "[00:00] Agent: Thank you for calling S-Net. My name is Alex. How can I help you today?`n[00:05] Client: My router keeps resetting.`n[00:08] Agent: Could I verify your PIN and billing address?`n[00:12] Client: PIN 5521, 42 Main St.`n[00:15] Agent: Verified, thank you Grace. Let me reset your line profile.`n[00:25] Agent: Line reset complete. Is the connection working now?`n[00:30] Client: Yes, perfect, thanks Alex!`n[00:35] Agent: Thank you for choosing S-Net, have a great day!"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:8005/api/evaluate" `
  -Method Post `
  -Headers @{"Content-Type" = "application/json"} `
  -Body $body
```

---

### Test 5: Automated Batch Test Suite
Run the batch test runner against the running containerized environment:

```bash
python Scripts/batch_test.py
```

---

## 6. Teardown & Maintenance Commands

### Stop Containers
```bash
docker-compose down
```

### Clean Rebuild (Reset Images & Containers)
```bash
docker-compose down
docker-compose build --no-cache
docker-compose up -d
```

### Full Reset (Includes Model Volume Removal)
> [!CAUTION]
> This command deletes `ollama_data` volume and requires re-pulling models.
```bash
docker-compose down -v
```
