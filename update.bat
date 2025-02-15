cd /d "%~dp0"

call .venv\Scripts\activate

.venv\Scripts\python.exe update.py

pip install -r requirements.txt

pause
