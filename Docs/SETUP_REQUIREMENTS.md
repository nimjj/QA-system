# QA Analysis System - Setup & Requirements Guide

This document provides complete instructions for installing, configuring, and running the Multi-Tenant Automated QA Evaluation System locally or via Docker.

---

## 1. Prerequisites

Before setting up the project, ensure you have:
* **Operating System:** Windows 10/11, macOS, or Linux.
* **Python:** Version **3.10+** (verify with `python --version`).
* **Ollama:** Installed and running on your local machine ([Download Ollama](https://ollama.com/download)).
* **Docker & Docker Compose (Optional):** If running containerized.

---

## 2. Pulling Required Local Models (Ollama)

The QA Engine uses two local models via Ollama:
1. **Generative LLM (`llama3.1:8b` or `llama3.1`):** Handles subjective criteria reasoning (Empathy, Ownership, Rapport, Probing) and dynamic coaching generation.
2. **Embedding Model (`nomic-embed-text`):** Handles zero-LLM vector cosine similarity checks for **Paraphrasing** and **Active Listening**.

Open your terminal and run:

```bash
# Pull LLM for reasoning and coaching
ollama pull llama3.1

# Pull dedicated embedding model for vector engine
ollama pull nomic-embed-text
```

> [!TIP]
> To prevent Ollama from constantly unloading models from memory (which causes cold-start latency), run Ollama with keep-alive enabled:
> ```bash
> # On Linux/macOS
> export OLLAMA_KEEP_ALIVE=-1
> 
> # On Windows PowerShell
> $env:OLLAMA_KEEP_ALIVE="-1"
> ```

---

## 3. Local Installation & Setup

### Step 1: Clone Repository
```bash
git clone https://github.com/nimjj/QA-system.git
cd QA-system
```

### Step 2: Create Virtual Environment & Install Dependencies

**Windows:**
```bat
python -m venv .venv
.venv\Scripts\activate
pip install --upgrade pip
pip install -r requirements.txt
```

**macOS / Linux:**
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

### Step 3: Configure Environment Variables
Copy `.env.example` to `.env`:
```bash
# Windows
copy .env.example .env

# macOS / Linux
cp .env.example .env
```

---

## 4. Environment Variables Configuration (`.env`)

| Variable | Default Value | Description |
|---|---|---|
| `OLLAMA_HOST` | `http://localhost:11434` | Base URL of the running Ollama instance. |
| `LLM_MODEL` | `llama3.1:8b` | The primary reasoning model (e.g., `llama3.1`, `llama3.1:8b`, `qwen2.5:7b`). |
| `EMBEDDING_MODEL` | `nomic-embed-text` | Dedicated embedding model for vector cosine similarity checks. |
| `OLLAMA_TIMEOUT` | `300` | HTTP request timeout in seconds for Ollama API generation calls. |
| `SERVER_HOST` | `0.0.0.0` | Host IP for FastAPI web server. |
| `SERVER_PORT` | `8000` | Port for FastAPI web server. |
| `PROMPT_DYNAMIC_EVALUATION_PATH` | `resources/prompts/dynamic_evaluation_prompt.txt` | Path to the dynamic evaluation prompt template. |

---

## 5. Running the Application

You can start the server using either the main launcher or Uvicorn directly:

### Option A: Using Root Launcher (Recommended)
```bash
python main.py
```

### Option B: Using Uvicorn Directly
```bash
uvicorn src.api.web_app:app --host 0.0.0.0 --port 8000 --reload
```

The web server will start at `http://localhost:8000`. You can access interactive Swagger API documentation at:
* **Interactive Docs:** `http://localhost:8000/docs`
* **Alternative ReDoc:** `http://localhost:8000/redoc`

### Option C: Using Docker Compose
```bash
docker-compose up --build -d
```
This builds and launches both the Ollama container and the FastAPI gateway container.

---

## 6. Verifying & Testing the Installation

### 1. Batch Test Script
Run the automated test runner to evaluate the sample test suite:
```bash
python Scripts/batch_test.py
```
This script queries `/api/evaluate` against multiple transcript edge cases and logs execution times and results.

### 2. Testing via Postman
Import `Docs/postman_collection.json` into Postman and execute:
1. `GET http://localhost:8000/api/samples` (Verify sample input listing)
2. `POST http://localhost:8000/api/preview-prompt` (Verify prompt builder)
3. `POST http://localhost:8000/api/evaluate` (Verify end-to-end evaluation)
