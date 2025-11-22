
@echo off
setlocal enabledelayedexpansion
cd /d "%~dp0"

echo ========================================
echo POWERHOUSE B2B PLATFORM - INSTALLATION
echo ========================================
echo.
echo This will install all dependencies for Powerhouse.
echo Installation may take 10-15 minutes.
echo.
pause

REM Backend Installation
echo.
echo [1/3] Installing Backend Dependencies...
echo ========================================
cd backend

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed or not in PATH
    echo Please install Python 3.11 from https://www.python.org/downloads/
    pause
    exit /b 1
)

echo Creating virtual environment...
if exist venv (
    echo Removing old virtual environment...
    rmdir /s /q venv
)
python -m venv venv

echo Activating virtual environment...
call venv\Scripts\activate.bat

echo Installing Python packages (this may take several minutes)...
python -m pip install --upgrade pip --no-cache-dir
pip install --no-cache-dir -r requirements.txt

if errorlevel 1 (
    echo [ERROR] Backend installation failed
    pause
    exit /b 1
)

echo [OK] Backend dependencies installed
cd ..

REM Frontend Installation
echo.
echo [2/3] Installing Frontend Dependencies...
echo ========================================
cd frontend\app

REM Check if Node.js is installed
node --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Node.js is not installed or not in PATH
    echo Please install Node.js 18+ from https://nodejs.org/
    pause
    exit /b 1
)

REM Check if Yarn is installed
yarn --version >nul 2>&1
if errorlevel 1 (
    echo [WARNING] Yarn is not installed. Installing...
    npm install -g yarn
)

echo Installing Node.js packages (this may take several minutes)...
call yarn install

if errorlevel 1 (
    echo [ERROR] Frontend installation failed
    pause
    exit /b 1
)

echo [OK] Frontend dependencies installed
cd ..\..

REM Database Setup Check
echo.
echo [3/3] Database Setup Check...
echo ========================================

netstat -an | find ":5432" >nul
if errorlevel 1 (
    echo.
    echo [NOTICE] PostgreSQL database is not detected on port 5432
    echo.
    echo Powerhouse requires PostgreSQL for:
    echo   - User authentication
    echo   - Data storage
    echo   - Workflow management
    echo.
    echo NEXT STEPS:
    echo 1. Run DATABASE_SETUP_WINDOWS.bat to install PostgreSQL
    echo 2. Run SETUP_DATABASE.bat to initialize the database
    echo 3. Run START.bat to launch Powerhouse
    echo.
    echo OR if PostgreSQL is already installed:
    echo 1. Run USE_EXISTING_POSTGRES.bat to configure it
    echo 2. Run SETUP_DATABASE.bat
    echo 3. Run START.bat
    echo.
) else (
    echo [!] WARNING: Port 5432 is already in use!
    echo.
    echo This means you have PostgreSQL or another database already installed.
    echo.
    echo CHOOSE YOUR SOLUTION:
    echo.
    echo Option 1: Use Different Port (RECOMMENDED)
    echo   - Run: PORT_5432_CONFLICT_FIX.bat
    echo   - Install PostgreSQL on port 5433
    echo.
    echo Option 2: Use Existing PostgreSQL
    echo   - Run: USE_EXISTING_POSTGRES.bat
    echo   - Configure Powerhouse to use your existing installation
    echo.
    echo Option 3: Check Port Details
    echo   - Run: CHECK_PORT_5432.bat
    echo   - See what's using the port and get recommendations
    echo.
    echo For detailed help, see: PORT_CONFLICT_GUIDE.txt
    echo.
)

echo ========================================
echo INSTALLATION COMPLETE!
echo ========================================
echo.
echo See WINDOWS_DATABASE_GUIDE.txt for database setup instructions
echo.
pause
