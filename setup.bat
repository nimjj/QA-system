@echo off
echo Setting up the QA Analysis System...

IF NOT EXIST ".venv" (
    echo Creating Python virtual environment...
    python -m venv .venv
)

echo Activating virtual environment...
call .venv\Scripts\activate.bat

echo Installing requirements (includes Laya from GitHub, pinned commit)...
python -m pip install --upgrade pip
pip install -r requirements.txt

IF NOT EXIST ".env" (
    echo Creating .env from .env.example...
    copy .env.example .env
)

echo Setup complete! To run the server (port 8006), type:
echo .venv\Scripts\activate
echo python main.py
pause
