@echo off
echo Setting up the QA Analysis System...

IF NOT EXIST ".venv" (
    echo Creating Python virtual environment...
    python -m venv .venv
)

echo Activating virtual environment...
call .venv\Scripts\activate.bat

echo Installing requirements...
pip install --upgrade pip
pip install -r requirements.txt

IF NOT EXIST ".env" (
    echo Creating .env from .env.example...
    copy .env.example .env
)

echo Pulling the default LLM (llama3.1) from Ollama...
echo Ensure Ollama desktop is running in your system tray!
ollama pull llama3.1

echo Setup complete! To run the server, type:
echo .venv\Scripts\activate
echo uvicorn src.api.web_app:app --reload
pause
