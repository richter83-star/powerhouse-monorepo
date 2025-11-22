
@echo off
echo ========================================
echo   POWERHOUSE - QUICK REINSTALL
echo   Fixing FastAPI/Pydantic Compatibility
echo ========================================
echo.

:: Get the directory where this script is located
set "SCRIPT_DIR=%~dp0"
cd /d "%SCRIPT_DIR%"

echo Current directory: %CD%
echo.

:: Stop any running processes
echo [1/4] Stopping any running processes...
taskkill /F /IM python.exe 2>nul
taskkill /F /IM uvicorn.exe 2>nul
timeout /t 2 /nobreak >nul
echo Done!
echo.

:: Delete old virtual environment
echo [2/4] Removing old virtual environment...
if exist venv (
    rd /s /q venv
    echo Old venv deleted!
) else (
    echo No existing venv found.
)
echo.

:: Create fresh virtual environment
echo [3/4] Creating fresh virtual environment...
python -m venv venv
if errorlevel 1 (
    echo ERROR: Failed to create virtual environment!
    echo Make sure Python is installed and in your PATH.
    pause
    exit /b 1
)
echo Virtual environment created!
echo.

:: Install dependencies with fixed versions
echo [4/4] Installing compatible packages (this may take a few minutes)...
call venv\Scripts\activate.bat
python -m pip install --upgrade pip --no-cache-dir
pip install --no-cache-dir -r backend\requirements.txt
if errorlevel 1 (
    echo.
    echo ERROR: Package installation failed!
    echo Please check the error messages above.
    pause
    exit /b 1
)
echo.

echo ========================================
echo   REINSTALL COMPLETE!
echo ========================================
echo.
echo Fixed issue: FastAPI/Pydantic compatibility
echo.
echo Next step: Run START.bat to launch the platform
echo.
pause
