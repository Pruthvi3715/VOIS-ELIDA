@echo off
echo ========================================
echo Starting ELIDA Backend Server
echo ========================================

cd /d "%~dp0"
cd backend

echo.
echo [1/2] Activating Python environment...
if exist venv\Scripts\activate.bat (
    call venv\Scripts\activate.bat
) else (
    echo No virtual environment found. Using system Python.
)

echo.
echo [2/2] Starting FastAPI server on http://localhost:8000
echo Press Ctrl+C to stop the server
echo.

python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

pause
