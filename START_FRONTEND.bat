@echo off
echo ========================================
echo Starting ELIDA Frontend
echo ========================================

cd /d "%~dp0"
cd frontend

echo.
echo [1/2] Checking npm installation...
where npm >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: npm not found. Please install Node.js first.
    pause
    exit /b 1
)

echo.
echo [2/2] Starting React development server on http://localhost:5173
echo Press Ctrl+C to stop the server
echo.

npm run dev

pause
