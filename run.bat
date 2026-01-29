@echo off
echo Starting Backend...
start cmd /k "venv\Scripts\activate && uvicorn backend.main:app --reload --port 8000"

echo Starting Frontend...
timeout /t 5
start cmd /k "venv\Scripts\activate && python frontend/app.py"

echo MVP is running!
echo Frontend: http://127.0.0.1:5000
echo Backend Docs: http://127.0.0.1:8000/docs
pause