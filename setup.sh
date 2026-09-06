#!/bin/bash
echo "Setting up the QA Analysis System..."

if [ ! -d ".venv" ]; then
    echo "Creating Python virtual environment..."
    python3 -m venv .venv
fi

echo "Activating virtual environment..."
source .venv/bin/activate

echo "Installing requirements..."
pip install --upgrade pip
pip install -r requirements.txt

if [ ! -f ".env" ]; then
    echo "Creating .env from .env.example..."
    cp .env.example .env
fi

echo "Pulling the default LLM (llama3.1) from Ollama..."
ollama pull llama3.1

echo "Setup complete! To run the server:"
echo "1. source .venv/bin/activate"
echo "2. uvicorn src.api.web_app:app --reload"

