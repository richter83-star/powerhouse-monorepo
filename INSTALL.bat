
@echo off
echo ========================================
echo POWERHOUSE Installation Script
echo ========================================
echo.

echo [1/5] Checking prerequisites...
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python not found. Please install Python 3.10+
    pause
    exit /b 1
)

node --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Node.js not found. Please install Node.js 18+
    pause
    exit /b 1
)

echo [2/5] Installing backend dependencies...
cd backend
python -m pip install --no-cache-dir -r requirements.txt
if errorlevel 1 (
    echo ERROR: Failed to install backend dependencies
    pause
    exit /b 1
)
cd ..

echo [3/5] Installing frontend dependencies...
cd frontend\app
call yarn install
if errorlevel 1 (
    echo ERROR: Failed to install frontend dependencies
    pause
    exit /b 1
)
cd ..\..

echo [4/5] Setting up environment files...
if not exist backend\.env (
    copy backend\.env.example backend\.env
    echo Created backend\.env - PLEASE EDIT THIS FILE WITH YOUR CREDENTIALS
)

if not exist frontend\app\.env.local (
    echo NEXT_PUBLIC_API_URL=http://localhost:8000 > frontend\app\.env.local
    echo Created frontend\app\.env.local
)

echo [5/5] Installation complete!
echo.
echo NEXT STEPS:
echo 1. Edit backend\.env with your database and enterprise credentials
echo 2. Set up your PostgreSQL database
echo 3. Configure SSO (optional)
echo 4. Run START.bat to launch POWERHOUSE
echo.
pause
