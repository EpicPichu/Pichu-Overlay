cd /d "%~dp0"

call .venv\Scripts\activate

.venv\Scripts\python.exe update.py

pause
