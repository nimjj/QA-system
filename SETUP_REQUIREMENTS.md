# QA Analysis System - Setup & Requirements

## Prerequisites
- **Python 3.10+** installed
- **Ollama** installed (https://ollama.com)

## Plug & Play Setup
The easiest way to get started is to use the provided setup scripts. These scripts will automatically create a virtual environment, install Python dependencies, configure your environment variables, and pull the required default LLM (`llama3.1`) from Ollama.

**For Windows:**
Double click `setup.bat` or run:
```bat
setup.bat
```

**For macOS/Linux:**
```bash
chmod +x setup.sh
./setup.sh
```

## Running the Server
Once setup is complete, you can start the FastAPI backend:

**Windows:**
```bat
.venv\Scripts\activate
uvicorn src.api.web_app:app --reload
```

**macOS/Linux:**
```bash
source .venv/bin/activate
uvicorn src.api.web_app:app --reload
```

## How to Change the LLM (Modular Model Support)
This codebase is completely model-agnostic. You can hot-swap the underlying LLM simply by modifying the `.env` file.

1. Open the `.env` file.
2. Change the `LLM_MODEL` variable. For example:
   ```ini
   LLM_MODEL=qwen2.5:1.5b
   ```
3. Ensure you pull the new model via Ollama:
   ```bash
   ollama pull qwen2.5:1.5b
   ```

## Note on Llama-Specific Optimizations
While the system is modular and supports any model, you should be aware of a few internal optimizations heavily tuned for **Llama 3.x**:

1. **Parser Resilience (`src/services/dynamic_evaluator.py`)**: The `parse_dynamic_ratings` function uses strict regex matching designed for Llama 3.1's highly structured output format (e.g., `PASS` or `FAIL` at the start of a line). Extremely small models (like 1b or 2b parameters) may fail to follow this strict output schema and trigger the fallback parser mechanism.
2. **Bottom-Anchoring Prompt Structure (`resources/prompts/dynamic_evaluation_prompt.txt`)**: The prompt is specifically structured with the static `[TRANSCRIPT]` at the top, and dynamic `[EVALUATION LINE ITEMS]` at the bottom. This leverages Ollama's KV Caching engine, which works perfectly with Llama 3.1 to give massive speedups during chunked map-reduce requests.
