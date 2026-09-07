# Enterprise QA System

An asynchronous, multi-tier microservices architecture designed to perform automated Quality Assurance (QA) on customer service transcripts using Large Language Models (LLMs) and deterministic Python rules.

## ?? Architecture Overview

The application is completely decoupled into 6 distinct Docker containers. This ensures that slow LLM inferences do not block fast deterministic rules, and that the API remains responsive under heavy load.

### The 6 Containers:
1. **API Gateway (gateway)**: A FastAPI server. It acts as the bouncer. It takes incoming HTTP requests, assigns a unique Job ID, drops the task into a message broker, and immediately responds to the client.
2. **Redis Message Broker (edis)**: The central nervous system. It holds the queues of pending tasks and temporarily stores the final results.
3. **LLM Worker (llm-worker)**: A Celery worker dedicated solely to talking to the AI models. It runs the heavy, probabilistic analysis.
4. **Logic Worker (logic-worker)**: A Celery worker dedicated to lightning-fast deterministic Python rules (e.g., checking if the agent said "Thank you for calling" or if there was >20s of dead air).
5. **Amalgamation Worker (malgamation-worker)**: The orchestrator. It waits for both the LLM and the Logic workers to finish, merges their findings, checks for auto-fail conditions, and calculates the final scorecard.
6. **Ollama Engine (ollama)**: The actual inference server holding the weights of our local open-source LLMs.

## ?? Request Workflow

1. **Submit**: A user submits a transcript via POST /api/evaluate.
2. **Acknowledge**: The Gateway immediately returns {\"job_id\": \"xyz-123\", \"status\": \"processing\"}.
3. **Process**: Behind the scenes, the workers pull the job from Redis. The Logic Worker parses the text for timestamps and keywords, while the LLM Worker reads it for soft skills and technical knowledge.
4. **Amalgamate**: The Amalgamation Worker merges the outputs and saves the final JSON to Redis.
5. **Retrieve**: The user polls GET /api/status/xyz-123 to get the final QA Scorecard.

---

## ?? Local Setup Guide (From Scratch)

Follow these instructions to spin up the entire distributed system on your local machine.

### Prerequisites
* **Git** installed.
* **Docker** & **Docker Compose** installed (Docker Desktop is recommended for Windows/Mac).

### 1. Clone the Repository
\\\ash
git clone https://github.com/nimjj/QA-system.git
cd QA-system
git checkout version-3
\\\`n
### 2. Boot the Infrastructure
We use Docker Compose to build the images and network the containers automatically.

\\\ash
# This will build the Python environments and start all 6 containers in the background
docker-compose up --build -d
\\\`n
### 3. Install the LLM Model Weights (One-Time Setup)
Because model weights are massive (several gigabytes), they are **not** stored in GitHub. We must tell our running Ollama container to download them from the cloud registry.

Run this command to pull the standard model:
\\\ash
docker exec -it qa-system-ollama-1 ollama pull llama3.1
\\\`n*(Note: Depending on your docker version, the container name might be slightly different. You can run docker ps to find the exact name of the ollama container).*

Wait for the download to hit 100%. The weights are saved to a persistent Docker Volume, so you only ever have to do this once!

---

## ?? Testing the API

Once the model is downloaded and the containers are running, you can test the async workflow.

### Step 1: Submit a Transcript
\\\ash
curl -X POST http://localhost:8000/api/evaluate \
     -H "Content-Type: application/json" \
     -d '{\"transcript\": \"Agent: Thank you for calling S-Net. How can I help?\\\nCustomer: My internet is down.\\\nAgent: Let me fix that. Okay, try now.\\\nCustomer: It works!\\\nAgent: Thank you for choosing S-Net.\"}'
\\\`n
**Response:**
\\\json
{
  "job_id": "53fa97a1-cc0a-4299-8473-bdf52a0a38b1",
  "status": "processing",
  "created_at": "2026-09-07T12:00:00.000Z"
}
\\\`n
### Step 2: Poll for Results
Take the job_id from Step 1 and check its status:
\\\ash
curl http://localhost:8000/api/status/53fa97a1-cc0a-4299-8473-bdf52a0a38b1
\\\`n
Keep polling until "status\": \"completed\", at which point the full JSON scorecard will be returned.

