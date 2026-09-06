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

echo Downloading K2 Horizon GGUF model via huggingface-hub...
python download_model.py

echo Setup complete! To run the server, type:
echo .venv\Scripts\activate
echo uvicorn src.api.web_app:app --reload
pause

