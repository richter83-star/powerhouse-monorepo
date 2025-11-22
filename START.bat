
@echo off
echo ========================================
echo Starting POWERHOUSE
echo ========================================
echo.

echo Starting backend on port 8000...
start "POWERHOUSE Backend" cmd /k "cd backend && python app.py"
timeout /t 3 /nobreak >nul

echo Starting frontend on port 3001...
start "POWERHOUSE Frontend" cmd /k "cd frontend\app && yarn dev --port 3001"

echo.
echo POWERHOUSE is starting...
echo Backend: http://localhost:8000
echo Frontend: http://localhost:3001
echo.
echo Press any key to open frontend in browser...
pause >nul
start http://localhost:3001
