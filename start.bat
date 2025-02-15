cd /d "%~dp0"

call .venv\Scripts\activate

start "" /B .venv/Scripts/pythonw.exe main.py