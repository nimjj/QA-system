# ?? Multi-Tenant Automated QA Intelligence Platform

> **Production-grade AI-powered Quality Assurance platform for enterprise contact centers.**  
> Automatically ingests company guideline PDFs into lossless Markdown, dynamically extracts custom criteria weights and auto-fail rules, and audits omni-channel customer interactions (Calls, Emails, Chats) using **Local LLM Inference** and **Deterministic Python Rule Engines**.

---

## ?? Table of Contents

- [Overview](#-overview)
- [Architecture](#-architecture)
- [Key Features](#-key-features)
- [Tech Stack](#-tech-stack)
- [Project Structure](#-project-structure)
- [Prerequisites](#-prerequisites)
- [Getting Started](#-getting-started)
- [Environment Configuration](#-environment-configuration)
- [API Overview](#-api-overview)

---

## ?? Overview

The **Multi-Tenant Automated QA Intelligence Platform** transforms unstructured contact center QA guidelines into dynamic, actionable audit rules. Instead of hardcoded rubrics, the platform parses guideline PDFs, extracts scoring categories, weights, verbatim spiels, and auto-fail conditions. 

Auditors and managers can audit interactions across channels with transparent mathematical scoring, SLA gap tracking, and full prompt preview capabilities.

---

## ??? Architecture

The system follows a modular microservice architecture separating document processing, dynamic prompt engineering, and deterministic SLA/rule scoring.

### End-to-End Workflow:
1. **Guideline Ingestion**: PyMuPDF converts PDF guidelines into lossless Markdown tables and sections.
2. **Criteria Extraction**: The LLM parses weights, criteria categories, verbatim scripts, and auto-fail rules into structured JSON.
3. **Interaction Analysis**:
   - **Python Rule Engine** deterministically parses exact timestamps for SLA/Hold violations and fuzzy-matches exact Verbatim Branding scripts.
   - **LLM Evaluator** uses Prompt Caching (KV Cache Bottom-Anchoring) and Map-Reduce chunking to evaluate agent compliance against extracted criteria flawlessly.
4. **Deterministic Scorecard**: Final scores are calculated via strict weighted formulas with instant zero-tolerance auto-fail enforcement.

---

## ? Key Features

- **Multi-Tenant Architecture**: Complete data isolation per company/client with dedicated schemas in PostgreSQL.
- **Lossless PDF-to-Markdown Ingestion**: Ingests complex multi-page guidelines while preserving tables, percentages, and formatting.
- **Dynamic Rule Extraction (Zero Hardcoding)**: Automatically extracts scoring weights (e.g., 30%/45%/25%), line items, scripts, and auto-fail circuit breakers directly from guidelines.
- **Python SLA Engine**: Tracks exact timestamp delays to catch "Dead Air" and "Hold Time" violations deterministically.
- **Dynamic Prompt Builder & UI Preview**: Allows QA auditors to inspect, edit, or copy the generated LLM prompt before triggering evaluation.
- **Deterministic Mathematical Scorecard**:
  $$\text{Final Score} = \sum (\text{Category Score} \times \text{Weight})$$
  *(Automatically resets to 0/100 if any auto-fail condition is met)*.
- **Model Agnostic**: Simply pass any LLM name into the `.env` configuration file to immediately route all logic to the new model.

---

## ??? Tech Stack

| Layer | Technology |
| :--- | :--- |
| **Backend API** | FastAPI, Uvicorn, Pydantic |
| **Frontend UI** | React, Vite, TailwindCSS, Lucide Icons |
| **LLM Inference** | Ollama (Modular `<LLM>` support) |

---

## ?? Project Structure

```text
QA-system/
+-- main.py                          # Server entry point for FastAPI backend
+-- requirements.txt                 # Python dependencies
+-- .env.example                     # Sample environment configuration
+-- SETUP_REQUIREMENTS.md            # Setup guide and instructions
+-- setup.bat                        # Automated setup script for Windows
+-- setup.sh                         # Automated setup script for macOS/Linux
+-- docs/                            # Guides, API samples, and documentation
+-- resources/                       # Architectural diagrams & prompt templates
+-- frontend/                        # React + Vite frontend application
+-- src/                             # Core Python backend package
   +-- api/
      +-- web_app.py               # REST API routers & multi-tenant endpoints
   +-- core/
      +-- llm_client.py            # Ollama Model integration wrapper
   +-- db/
      +-- database.py              # PostgreSQL connection & session manager
      +-- models.py                # SQLAlchemy ORM models
   +-- rag/
      +-- pdf_parser.py            # PDF to Markdown parser
      +-- llm_separator.py         # Dynamic criteria & policy extractor
   +-- services/
       +-- dynamic_evaluator.py     # Evaluation orchestrator & scorecard calculator
       +-- rule_engine.py           # Deterministic Python SLA and Branding engine
       +-- qa_summary.py            # Interaction executive summarization
       +-- qa_suggestions.py        # Coaching recommendations generator
       +-- response_time.py         # Transcript timestamp and latency analyzer
+-- tests/                           # Integration and demo test scripts
```

---

## ? Prerequisites

Before running the application, make sure you have the following installed:

1. **Python 3.10+**
2. **Node.js 18+** & **npm**
3. **PostgreSQL 17** (running on `localhost:5432`)
4. You MUST have Ollama running locally in the background.

---

## ?? Getting Started

### 1. Clone & Configure Environment

```bash
# Clone the repository
git clone https://github.com/nimjj/QA-system.git
cd QA-system
```

### 2. Run Automated Setup

**Windows:**
```cmd
setup.bat
```

**macOS / Linux:**
```bash
chmod +x setup.sh
./setup.sh
```

### 3. Run the Application

Start the services across 3 terminal windows:

#### ?? Terminal 1: Ollama LLM Server
```bash
ollama serve
```

#### ?? Terminal 2: FastAPI Backend Server
```bash
# Activate your virtual environment first!
# Windows: .\.venv\Scripts\activate
# Mac/Linux: source .venv/bin/activate
python main.py
```
> Backend API will be available at **`http://localhost:8000`** (Swagger docs at **`http://localhost:8000/docs`**).

#### ?? Terminal 3: Vite Frontend UI
```bash
cd frontend
npm run dev
```
> Frontend Web UI will be available at **`http://localhost:5173`**.

---

## ?? Environment Configuration

Key configuration parameters in `.env`:

| Variable | Default Value | Description |
| :--- | :--- | :--- |
| `DB_HOST` / `DB_PORT` | `localhost` / `5432` | PostgreSQL host and port |
| `DB_NAME` / `DB_USERNAME` | `qa_database` / `postgres` | Database credentials |
| `OLLAMA_HOST` | `http://localhost:11434` | Ollama service endpoint |
| `LLM_MODEL` | `llama3.1` | Default LLM model identifier |
| `SERVER_PORT` | `8000` | FastAPI server port |

