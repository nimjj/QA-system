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

echo "Downloading K2 Horizon GGUF model via huggingface-hub..."
python download_model.py

echo "Setup complete! To run the server, type:"
echo "source .venv/bin/activate"
echo "uvicorn src.api.web_app:app --host 0.0.0.0 --port 8000 --reload"

