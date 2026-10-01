# Local Docker Deployment Plan: Automated QA Evaluation System

This guide outlines the steps to build, configure, run, and verify the **Automated QA Evaluation Platform & API Gateway** locally using Docker.

---

## Architecture Overview

```
                      [ Host Browser / Client / Postman ]
                                       │
                                       ▼ :8005
                   ┌────────────────────────────────────────┐
                   │          qa_gateway (Port 8005)        │
                   │         (Reverse Proxy & Router)       │
                   └───────────────────┬────────────────────┘
                                       │ http://qa_service:8006
                                       ▼
                   ┌────────────────────────────────────────┐
                   │          qa_service (Port 8006)        │
                   │      (FastAPI Core QA Engine)          │
                   └───────┬────────────────────────┬───────┘
                           │                        │
       http://qa_ollama:11434                       │ host.docker.internal:5432
                           ▼                        ▼
       ┌───────────────────────────┐      ┌─────────────────────────┐
       │   qa_ollama (Port 11434)  │      │   PostgreSQL Database   │
       │ (llama3.1 + nomic-embed)  │      │   (Host or Container)   │
       │ Persistent ./ollama_cache │      └─────────────────────────┘
       └───────────────────────────┘
```

---

## 1. Prerequisites & Directory Setup

Ensure Docker is running and create the necessary host directories for audit logs and persistent model caching:

```bash
# Create host directories for logs and persistent Ollama models
mkdir -p logs ollama_cache

# Create Docker bridge network
docker network create qa-network
```

> **Why `./ollama_cache`?**
> The `ollama_cache` folder persists LLM weights (`llama3.1` and `nomic-embed-text`) on your host machine (`./ollama_cache`). The models are downloaded only once; subsequent container launches will load models locally without re-downloading.

---

## 2. Environment Configuration

Copy the example environment file if you haven't already:

```bash
# Windows PowerShell / CMD:
copy .env.example .env

# Linux / macOS:
cp .env.example .env
```

Ensure the credentials in `.env` match your local environment.

### Key Variables in `.env`:
| Variable | Value for Docker Network | Description |
| :--- | :--- | :--- |
| `OLLAMA_HOST` | `http://qa_ollama:11434` | Internal URL to Ollama container |
| `LLM_MODEL` | `llama3.1` | Main LLM for QA evaluation |
| `EMBED_MODEL` | `nomic-embed-text` | Embedding model for semantic checks |
| `DB_HOST` | `host.docker.internal` | Host machine PostgreSQL address |
| `DB_PORT` | `5432` | PostgreSQL port |
| `DB_NAME` | `ciap` | Database name |
| `DB_USER` | `postgres` | Database username |
| `DB_PASSWORD` | `your_actual_password` | Database password (**Kept in .env only!**) |
| `APP_URL` | `http://qa_service:8006` | Gateway target backend address |
| `GATEWAY_PORT` | `8005` | Gateway public port |
| `SERVER_PORT` | `8006` | QA Service internal/public port |

---

## 3. Build Base Docker Image

Build the shared base image containing Python 3.11-slim and all project dependencies (`fastapi`, `uvicorn`, `psycopg2-binary`, `httpx`, `pydantic`):

```bash
docker build -f Dockerfile.base -t qa-base:v1 --no-cache .
```

---

## 4. Build Microservice Images

Build the service images using the shared base image:

```bash
# Build QA Service image
docker build -t qa-service:v1 .

# Build API Gateway image
docker build -f Dockerfile.gateway -t qa-gateway:v1 .
```

---

## 5. Run Ollama & Pull Models

### A. Start Ollama Container (Port 11434)
```bash
docker run -d \
  --name qa_ollama \
  --network qa-network \
  -p 11434:11434 \
  -v "${PWD}/ollama_cache:/root/.ollama" \
  ollama/ollama:latest
```

### B. Pull Required Models (One-Time Setup)
```bash
# Pull Llama 3.1 LLM
docker exec -it qa_ollama ollama pull llama3.1

# Pull Nomic Embed Text Embedding model
docker exec -it qa_ollama ollama pull nomic-embed-text
```

Verify downloaded models:
```bash
docker exec -it qa_ollama ollama list
```

---

## 6. Run Core Microservices

### A. Run QA Backend Service (Port 8006)
```bash
docker run -d \
  --name qa_service \
  --network qa-network \
  -p 8006:8006 \
  --add-host host.docker.internal:host-gateway \
  --env-file .env \
  -v "${PWD}/logs:/app/logs" \
  -v "${PWD}/inputs:/app/inputs" \
  qa-service:v1
```

### B. Run API Gateway (Port 8005)
```bash
docker run -d \
  --name qa_gateway \
  --network qa-network \
  -p 8005:8005 \
  --add-host host.docker.internal:host-gateway \
  --env-file .env \
  -v "${PWD}/logs:/app/logs" \
  qa-gateway:v1
```

---

## 7. Health Check Verification

Verify that all services are operational:

```bash
# 1. Check API Gateway
curl http://localhost:8005/health

# 2. Check QA Backend Service
curl http://localhost:8006/health

# 3. Check Ollama Service
curl http://localhost:11434/api/tags
```

**Expected Responses:**
- Gateway: `{"status":"healthy","service":"api-gateway","target_app":"http://qa_service:8006"}`
- QA Service: `{"status":"healthy","service":"qa-service"}`
- Ollama: JSON object listing `llama3.1:latest` and `nomic-embed-text:latest`

---

## 8. API Testing

### Test 1: Fetch Tenants via Gateway
```bash
curl -X GET http://localhost:8005/api/tenants
```

### Test 2: Evaluate Customer Support Interaction
```bash
curl -X POST http://localhost:8005/api/evaluate \
  -H "Content-Type: application/json" \
  -d '{
    "tenant_id": "tenant-abc",
    "channel": "Call",
    "customer_name": "Grace",
    "transcript": "[00:00] Agent: Thank you for calling S-Net. My name is Alex. How can I help you today?\n[00:05] Client: My router keeps resetting.\n[00:08] Agent: Could I verify your PIN and billing address?\n[00:12] Client: PIN 5521, 42 Main St.\n[00:15] Agent: Verified, thank you Grace. Let me reset your line profile.\n[00:25] Agent: Line reset complete. Is the connection working now?\n[00:30] Client: Yes, perfect, thanks Alex!\n[00:35] Agent: Thank you for choosing S-Net, have a great day!"
  }'
```

---

## 9. Alternative: One-Command Docker Compose

If you prefer using Docker Compose, the repository includes a hardened `docker-compose.yml` that pulls all database credentials directly from `.env` without hardcoding:

```bash
# Start all containers in background
docker compose up -d

# Check logs
docker compose logs -f

# Stop containers
docker compose down
```

---

## 10. Teardown / Cleanup

Stop and remove all running containers:

```bash
docker stop qa_gateway qa_service qa_ollama
docker rm qa_gateway qa_service qa_ollama
```

Remove the Docker network (optional):

```bash
docker network rm qa-network
```
