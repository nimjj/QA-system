# Multi-Tenant Automated QA Intelligence Platform

> **Production-grade AI-powered Quality Assurance platform for enterprise contact centers.**  
> Audits omni-channel customer interactions (Calls, Emails, Chats) using **Local LLM Inference** and **Deterministic Python Rule Engines** without relying on complex external databases or heavy cloud resources.

---

## Table of Contents

- [Overview](#overview)
- [Architecture](#architecture)
- [Key Features](#key-features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Prerequisites](#prerequisites)
- [Getting Started](#getting-started)
- [Environment Configuration](#environment-configuration)

---

## Overview

The **Automated QA Intelligence Platform** transforms contact center evaluations into a lightning-fast, stateless audit. 

Auditors and managers can audit interactions across channels with transparent mathematical scoring, SLA gap tracking, and full prompt preview capabilities.

---

## Architecture

The system follows a modular, stateless microservice architecture separating dynamic prompt engineering and deterministic SLA/rule scoring.

### End-to-End Workflow:
1. **Interaction Analysis**:
   - **Python Rule Engine** deterministically parses exact timestamps for SLA/Hold violations and fuzzy-matches exact Verbatim Branding scripts.
   - **LLM Evaluator** uses Prompt Caching (KV Cache Bottom-Anchoring) and Map-Reduce chunking to evaluate agent compliance against extracted criteria flawlessly.
2. **Deterministic Scorecard**: Final scores are calculated via strict weighted formulas with instant zero-tolerance auto-fail enforcement.

---

## Key Features

- **Stateless Execution**: Incredibly fast evaluations requiring no external relational databases or document parsers.
- **Python SLA Engine**: Tracks exact timestamp delays to catch "Dead Air" and "Hold Time" violations deterministically.
- **Dynamic Prompt Builder & UI Preview**: Allows QA auditors to inspect, edit, or copy the generated LLM prompt before triggering evaluation.
- **Deterministic Mathematical Scorecard**:
  $$\text{Final Score} = \sum (\text{Category Score} \times \text{Weight})$$
  *(Automatically resets to 0/100 if any auto-fail condition is met)*.
- **Model Agnostic**: Simply pass any LLM name into the `.env` configuration file to immediately route all logic to the new model.

---

## Tech Stack

| Layer | Technology |
| :--- | :--- |
| **Backend API** | FastAPI, Uvicorn, Pydantic |
| **Frontend UI** | React, Vite, TailwindCSS, Lucide Icons |
| **LLM Inference** | Ollama (Modular `<LLM>` support) |

---

## Project Structure

```text
QA-system/
+-- main.py                          # Server entry point for FastAPI backend
+-- requirements.txt                 # Python dependencies
+-- .env.example                     # Sample environment configuration
+-- SETUP_REQUIREMENTS.md            # Setup guide and instructions
+-- setup.bat                        # Automated setup script for Windows
+-- setup.sh                         # Automated setup script for macOS/Linux
+-- frontend/                        # React + Vite frontend application
+-- src/                             # Core Python backend package
   +-- api/
      +-- web_app.py               # REST API stateless endpoints
   +-- core/
      +-- llm_client.py            # Embedded llama.cpp integration wrapper
   +-- services/
       +-- dynamic_evaluator.py     # Evaluation orchestrator & scorecard calculator
       +-- rule_engine.py           # Deterministic Python SLA and Branding engine
       +-- qa_summary.py            # Interaction executive summarization
       +-- qa_suggestions.py        # Coaching recommendations generator
       +-- response_time.py         # Transcript timestamp and latency analyzer
+-- tests/                           # Integration and demo test scripts
```

---

## Prerequisites

Before running the application, make sure you have the following installed:

1. **Python 3.10+**
2. **Node.js 18+** & **npm**

---

## Getting Started

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

#### Terminal 1: Ollama LLM Server
```bash
ollama serve
```

#### Terminal 2: FastAPI Backend Server
```bash
# Activate your virtual environment first!
# Windows: .\.venv\Scripts\activate
# Mac/Linux: source .venv/bin/activate
python main.py
```
> Backend API will be available at **`http://localhost:8000`**.

#### Terminal 2: Vite Frontend UI
```bash
cd frontend
npm run dev
```
> Frontend Web UI will be available at **`http://localhost:5173`**.

---

## Environment Configuration

Key configuration parameters in `.env`:

| Variable | Default Value | Description |
| :--- | :--- | :--- |
| `SERVER_HOST` | `0.0.0.0` | FastAPI server host interface (0.0.0.0 allows remote/Tailscale access) |
| `SERVER_PORT` | `8000` | FastAPI server port |

