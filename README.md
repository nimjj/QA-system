# Automated QA Evaluation System

A fast, lightweight, locally-hosted Quality Assurance (QA) engine for customer support transcripts. 

Built with **FastAPI**, **Ollama** (Llama 3.1 & nomic-embed-text), and a deterministic **Python Rule Engine**. Runs 100% locally with zero external cloud dependencies.

---

## Architecture

No Redis, no Celery, no background message queues. The service is a synchronous, in-process FastAPI application that directly evaluates transcripts against dynamic criteria:

```
Client / Postman
       │
       ▼  POST /api/evaluate
FastAPI Service (src/api/web_app.py :8000)
       │
       ├──► Python Rule Engine (src/services/rule_engine.py)
       │    └── Verbatim Branding, Dead Air, Customer Verification (0 tokens)
       │
       ├──► Vector Engine (src/services/llm_adapter.py)
       │    └── Paraphrasing Cosine Similarity via nomic-embed-text
       │
       └──► Local Ollama LLM (http://localhost:11434)
            └── Snippet Verifications (Empathy, Ownership, Rapport, Probing) & Coaching
```

---

## Prerequisites & Quickstart

### Prerequisites
* **Python 3.10+**
* **Ollama** installed and running locally ([ollama.com](https://ollama.com))

### 1. Pull Required Models
```bash
ollama pull llama3.1
ollama pull nomic-embed-text
```

### 2. Install & Configure
```bash
git clone https://github.com/nimjj/QA-system.git
cd QA-system

# Virtual environment
python -m venv .venv
# Windows:
.venv\Scripts\activate
# Linux/macOS:
source .venv/bin/activate

# Install dependencies (fastapi, uvicorn, pydantic, python-dotenv)
pip install -r requirements.txt

# Environment config
copy .env.example .env    # Windows
cp .env.example .env      # Linux/macOS
```

### 3. Run the Server
```bash
python main.py
```
Server runs at `http://localhost:8000`. Interactive docs at `http://localhost:8000/docs`.

---

## API Endpoints

### 1. Evaluate Interaction
* **Endpoint:** `POST /api/evaluate`
* **Payload:**
```json
{
  "tenant_id": "tenant-abc",
  "channel": "Call",
  "customer_name": "Grace",
  "transcript": "[00:00] Agent: Thank you for calling S-Net. My name is Alex. How can I help you today?\n[00:05] Client: My router keeps resetting.\n[00:08] Agent: Could I verify your PIN and billing address?\n[00:12] Client: PIN 5521, 42 Main St.\n[00:15] Agent: Verified, thank you Grace. Let me reset your line profile.\n[00:25] Agent: Line reset complete. Is the connection working now?\n[00:30] Client: Yes, perfect, thanks Alex!\n[00:35] Agent: Thank you for choosing S-Net, have a great day!"
}
```

> **Note on Multi-Tenancy:** If `criteria_data` is omitted, criteria are retrieved directly from the PostgreSQL database (`tenants`, `categories`, `line_items`, `tenant_lines`). Any criteria toggled off (`is_active = FALSE`) for a tenant are omitted from evaluation with zero deductions, and active category weights dynamically re-balance to 100.0%.

* **Response:**
```json
{
  "status": "completed",
  "result": {
    "final_score": 100.0,
    "is_auto_fail": false,
    "auto_fail_reason": null,
    "scorecard": [
      {
        "category": "Soft Skills",
        "name": "Branding and Survey Check",
        "rating": "PASS",
        "coaching": "Agent successfully used required opening and closing branding scripts."
      },
      {
        "category": "Soft Skills",
        "name": "Hold time and Dead Air",
        "rating": "PASS",
        "coaching": "Agent maintained active communication without excessive dead air (>30s)."
      },
      {
        "category": "Soft Skills",
        "name": "Personalized the call/ticket appropriately",
        "rating": "PASS",
        "coaching": "Agent addressed customer by their verified name during the interaction."
      },
      {
        "category": "Technical Knowledge",
        "name": "Verified customer",
        "rating": "PASS",
        "coaching": "Agent verified customer identity within the required time window."
      }
    ]
  }
}
```

### 2. Preview Evaluation Prompt
* **Endpoint:** `POST /api/preview-prompt`
* **Description:** Previews the exact generated LLM prompt without executing Ollama inference.

### 3. List Samples
* **Endpoint:** `GET /api/samples`
* **Description:** Lists all sample transcript files from `inputs/`.

---

## The 11 Evaluation Criteria

### Soft Skills (Default Weight: 33.3%)
1. **Branding and Survey Check:** Verbatim opening (`"thank you for calling s-net"`) and closing scripts (Rule Engine).
2. **Hold time and Dead Air:** Turn pauses $>30\text{s}$. Up to 2 allowed; $\ge 3$ fails (Rule Engine).
3. **Personalized the call/ticket appropriately:** Agent uses customer's name (Rule Engine).
4. **Empathy & Acknowledgment Statement:** Validates frustration on sentiment drops (Snippet LLM).
5. **Build rapport and observed professionalism:** Flags rude/condescending language (Violation LLM).

### Technical Knowledge (Default Weight: 66.7%)
6. **Paraphrasing:** Embedding cosine similarity $\ge 0.50$ between customer and agent problem turns (Vector Engine).
7. **Verified customer:** Validates credentials (PIN/address) within first 4 minutes (Rule Engine).
8. **Probing:** Checks that agent asked diagnostic questions investigating root cause (Contextual LLM).
9. **Took ownership of the problem:** Flags deflection or blaming other departments (Violation LLM).
10. **Active listening:** Flags redundant, repeated agent questions (Hybrid Snippet LLM).
11. **Confirmed the issue is resolved:** Confirms verbal resolution in final turns (Sliced LLM).

### Auto-Fail Circuit Breakers
Immediate **0 score** if:
* Profanity/abuse detected (`"fuck"`, `"shut up"`, `"idiot"`, etc.).
* Extreme hostility ($\ge 3$ harsh agent statements).

---

## Dynamic Weight Normalization

When a tenant or request disables categories, active weights are dynamically re-balanced:

$$W_{\text{active}} = \sum_{i=1}^{k} w_i \quad\implies\quad w_i' = \frac{w_i}{W_{\text{active}}}$$

$$\text{Final Score} = \sum_{i=1}^{k} \left(\text{Score}_{C_i} \times w_i'\right)$$

The maximum possible score remains **100.0%** regardless of which categories are evaluated.

---

## Testing

Run the automated batch test script against pre-recorded sample files:
```bash
python Scripts/batch_test.py
```
Or import `Docs/postman_collection.json` into Postman.

---

## Codebase Map

```
QA-system/
├── main.py                         # QA Service server launcher (:8006)
├── run_gateway.py                  # API Gateway launcher (:8005)
├── docker-compose.yml              # Multi-container orchestration (Gateway, QA Service, Ollama)
├── Dockerfile                      # QA Service Dockerfile
├── Dockerfile.gateway              # API Gateway Dockerfile
├── requirements.txt                # Dependencies (fastapi, uvicorn, pydantic, python-dotenv, psycopg2-binary, httpx)
├── .env.example                    # Environment template (Server, Gateway, DB, Ollama)
├── resources/
│   ├── criteria_config.json        # Default tenant criteria & deduction values
│   └── prompts/                    # LLM prompt templates
├── src/
│   ├── api/
│   │   ├── web_app.py              # Core QA FastAPI endpoints (/api/evaluate, criteria CRUD, samples)
│   │   └── logger.py               # Structured JSON logger
│   ├── gateway/
│   │   └── gateway_app.py          # API Gateway (Direct DB criteria/toggle routes + reverse proxy)
│   ├── db/
│   │   └── database.py             # PostgreSQL data access layer
│   └── services/
│       ├── dynamic_evaluator.py    # Core evaluator, normalization & pass descriptions
│       ├── rule_engine.py          # Deterministic Python rules (branding, dead air, verification)
│       └── llm_adapter.py          # Singleton Ollama client (chat & embeddings)
├── frontend/                       # Vite + React UI dashboard
├── Scripts/
│   └── batch_test.py               # Automated test runner
├── inputs/                         # Sample transcript test cases
└── Docs/                           # Architecture, setup guide, Postman collection
```
