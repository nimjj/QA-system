# Gemma QA Analysis System

A 100% locally-hosted, microservices-based QA evaluation engine for customer support transcripts. This system uses Llama 3.1 (8B) via Ollama to evaluate soft skills and technical knowledge, combined with a strict Python rule engine to evaluate mathematical SLAs like Dead Air and Hold Time.

## Prerequisites
* **Docker Desktop:** Installed and running (Linux containers mode on Windows).
* **Git:** For cloning the repository.
* **Hardware:** Minimum 16GB RAM recommended for smooth local LLM inference.

---

## 1. Local Setup & Booting

This architecture uses 7 fully decoupled Docker containers (API Gateway, Redis, Ollama, and 4 Celery Workers) to process tasks asynchronously without blocking the user.

1. **Clone the repository and switch to version-3:**
   ``bash
   git clone https://github.com/nimjj/QA-system.git
   cd QA-system
   git checkout version-3
   ``

2. **Boot the environment:**
   We use Docker Compose to build and network all microservices at once. Run this in the root directory:
   ``bash
   docker-compose up --build -d
   ``
   *Note: The -d flag runs the containers in the background.*

---

## 2. LLM Model Setup (One-Time)

Because we removed cloud dependencies, the system relies on an open-source model running on your local machine via the ollama container. 

We use **Llama 3.1 (8B Parameters)**. The model weights are approximately **4.7 GB**. 

**To download and install the model:**
1. Open your local terminal (while the Docker containers are running).
2. Execute the pull command directly inside the running Ollama container:
   ``bash
   docker exec -it gemma-qa-analysis-ollama-1 ollama run llama3.1
   ``
3. **Download Time:** Depending on your internet connection, a 4.7GB file will take anywhere from **5 to 15 minutes** on a standard broadband connection. You will see a progress bar in your terminal.
4. Once it says "success", you can type /bye to exit. The model is now permanently saved inside your Docker volume!

---

## 3. API Documentation & Testing

The Docker containers are configured to bind the FastAPI Gateway to your local **Port 8000**. 

**Localhost API Endpoint:** http://localhost:8000/api/evaluate

### Test it in Postman
You can immediately test the system by sending a properly formatted JSON Array to the API. 

1. Open Postman.
2. Create a new **POST** request to http://localhost:8000/api/evaluate
3. Go to the **Body** tab, select **raw**, and choose **JSON**.
4. Paste the following structured transcript (which includes intentional >20s Dead Air gaps to trigger the rule engine!):

``json
{
  "channel": "Call",
  "transcript": [
    {
      "speaker": "Agent",
      "text": "Thank you for calling S-NET Communications. My name is Alex.",
      "start_time_sec": 0,
      "end_time_sec": 6
    },
    {
      "speaker": "Caller",
      "text": "Hi Alex, I've been trying to connect to my Wi-Fi all morning.",
      "start_time_sec": 8,
      "end_time_sec": 16
    },
    {
      "speaker": "Agent",
      "text": "Let's start with a power cycle. Unplug the router for 30 seconds.",
      "start_time_sec": 18,
      "end_time_sec": 24
    },
    {
      "speaker": "Caller",
      "text": "Okay. It's been about 30 seconds now.",
      "start_time_sec": 55,
      "end_time_sec": 58
    }
  ]
}
``

5. Hit **Send**. You will instantly receive a job_id:
``json
{
    "job_id": "50f45a5d-c53c-43b1-bb6e-7ecf4794caf1",
    "status": "processing",
    "created_at": "2026-09-08T12:00:00"
}
``

6. Create a new **GET** request to http://localhost:8000/api/status/{PASTE_YOUR_JOB_ID_HERE}.
7. Hit **Send** periodically until the status changes from "processing" to "completed" (usually takes 4-6 minutes for a local LLM). You will receive your fully structured JSON scorecard!
