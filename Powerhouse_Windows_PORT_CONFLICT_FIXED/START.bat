@echo off
setlocal enabledelayedexpansion

echo ========================================
echo  Starting Powerhouse B2B Platform
echo ========================================
echo.

REM Get the directory where THIS batch file is located
set "SCRIPT_DIR=%~dp0"

REM Remove trailing backslash if present
if "%SCRIPT_DIR:~-1%"=="\" set "SCRIPT_DIR=%SCRIPT_DIR:~0,-1%"

echo [DEBUG] Script location: %SCRIPT_DIR%
echo.

REM Change to the script directory
cd /d "%SCRIPT_DIR%"

echo [DEBUG] Working directory: %CD%
echo.

REM ============================================================================
REM  VERIFY INSTALLATION
REM ============================================================================

REM Check if venv exists in ROOT directory (where INSTALL.bat creates it)
if not exist "venv\Scripts\python.exe" (
    echo.
    echo ============================================================
    echo  ERROR: Backend not installed!
    echo ============================================================
    echo.
    echo The virtual environment was not found at:
    echo   %CD%\venv
    echo.
    echo Please run INSTALL.bat first to install dependencies.
    echo.
    pause
    exit /b 1
)

REM Check if frontend is installed
if not exist "frontend\app\node_modules" (
    echo.
    echo ============================================================
    echo  ERROR: Frontend not installed!
    echo ============================================================
    echo.
    echo The node_modules folder was not found at:
    echo   %CD%\frontend\app\node_modules
    echo.
    echo Please run INSTALL.bat first to install dependencies.
    echo.
    pause
    exit /b 1
)

echo [SUCCESS] Installation verified
echo   - Virtual environment found at: %CD%\venv
echo   - Frontend packages found at: %CD%\frontend\app\node_modules
echo.

REM ============================================================================
REM  START BACKEND
REM ============================================================================

echo Starting backend on port 8001...
echo.

REM Use ROOT venv (where INSTALL.bat created it)
set "BACKEND_DIR=%SCRIPT_DIR%\backend"
set "VENV_PYTHON=%SCRIPT_DIR%\venv\Scripts\python.exe"

echo Backend directory: %BACKEND_DIR%
echo Python executable: %VENV_PYTHON%
echo.

REM Verify Python exists in venv
if not exist "%VENV_PYTHON%" (
    echo ERROR: Python not found at %VENV_PYTHON%
    pause
    exit /b 1
)

REM Start backend in new window using ROOT venv
start "Powerhouse Backend" cmd /k "cd /d "%BACKEND_DIR%" && "%VENV_PYTHON%" -m uvicorn api.main:app --host 0.0.0.0 --port 8001 --reload"

echo [SUCCESS] Backend starting...
echo Waiting 5 seconds for backend to initialize...
timeout /t 5 /nobreak > nul

echo.

REM ============================================================================
REM  START FRONTEND
REM ============================================================================

echo Starting frontend on port 3000...
echo.

REM Use absolute path for frontend
set "FRONTEND_DIR=%SCRIPT_DIR%\frontend\app"

echo Frontend directory: %FRONTEND_DIR%
echo.

REM Start frontend in new window with absolute path
start "Powerhouse Frontend" cmd /k "cd /d "%FRONTEND_DIR%" && npm run dev"

echo [SUCCESS] Frontend starting...
echo Waiting 5 seconds for frontend to initialize...
timeout /t 5 /nobreak > nul

echo.

REM ============================================================================
REM  PLATFORM READY
REM ============================================================================

echo ========================================
echo  🚀 Platform Starting!
echo ========================================
echo.
echo Two terminal windows have opened:
echo   🔹 Powerhouse Backend  (port 8001)
echo   🔹 Powerhouse Frontend (port 3000)
echo.
echo ⚠️  Keep both windows open while using the platform
echo.
echo 🌐 URLs:
echo   Frontend:  http://localhost:3000
echo   Backend:   http://localhost:8001
echo   API Docs:  http://localhost:8001/docs
echo.
echo 📝 Default Login:
echo   Email:    demo@powerhouse.ai
echo   Password: demo123
echo.
echo Opening browser in 5 seconds...
timeout /t 5 /nobreak > nul

start http://localhost:3000

echo.
echo ✅ Platform is now running!
echo.
echo To stop: Run STOP.bat or close both terminal windows
echo.
pause
