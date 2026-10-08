@echo off
echo Setting up the QA Analysis System...

IF NOT EXIST "..\laya-test\laya" (
    echo ERROR: the Laya checkout is expected at ..\laya-test\laya ^(next to this repo^).
    pause
    exit /b 1
)

IF NOT EXIST ".venv" (
    echo Creating Python virtual environment...
    python -m venv .venv
)

echo Activating virtual environment...
call .venv\Scripts\activate.bat

echo Installing requirements (includes Laya from ..\laya-test\laya)...
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
