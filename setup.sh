#!/bin/bash
echo "Setting up the QA Analysis System..."

if [ ! -d "../laya-test/laya" ]; then
    echo "ERROR: the Laya checkout is expected at ../laya-test/laya (next to this repo)."
    exit 1
fi

if [ ! -d ".venv" ]; then
    echo "Creating Python virtual environment..."
    python3 -m venv .venv
fi

echo "Activating virtual environment..."
source .venv/bin/activate

echo "Installing requirements (includes Laya from ../laya-test/laya)..."
pip install --upgrade pip
pip install -r requirements.txt

if [ ! -f ".env" ]; then
    echo "Creating .env from .env.example..."
    cp .env.example .env
fi

echo "Setup complete! To run the server (port 8006), type:"
echo "source .venv/bin/activate"
echo "python main.py"
