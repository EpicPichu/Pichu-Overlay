@echo off
cd /d "%~dp0"

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Python is not installed or not added to PATH.
    pause
    exit /b
)

REM Create a virtual environment
echo Creating virtual environment...
python -m venv .venv

REM Activate the virtual environment
call .venv\Scripts\activate

REM Check if requirements.txt exists
if not exist requirements.txt (
    echo requirements.txt not found. Please make sure it exists in the current directory.
    pause
    exit /b
)

REM Install requirements
echo Installing requirements...
pip install --upgrade pip
pip install -r requirements.txt

REM Deactivate the virtual environment (optional)
echo Installation complete. Deactivating virtual environment.
call deactivate

pause
