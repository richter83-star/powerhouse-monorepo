
@echo off
echo ========================================
echo PORT 5432 CONFLICT - SOLUTION
echo ========================================
echo.
echo Port 5432 is already in use on your system.
echo This means another database is running.
echo.
echo SOLUTION 1: Use Alternative Port (RECOMMENDED)
echo ========================================
echo We'll install PostgreSQL on port 5433 instead.
echo.
echo Steps:
echo 1. Install PostgreSQL (download from link below)
echo 2. During installation, when asked for port, use: 5433
echo 3. Use password: default
echo 4. After installation, press any key here
echo.
echo Download PostgreSQL:
echo https://www.postgresql.org/download/windows/
echo.
pause
echo.
echo Now updating configuration to use port 5433...
cd /d "%~dp0"
cd frontend\app

REM Backup original .env
if exist .env (
    copy .env .env.backup.5432 >nul 2>&1
)

REM Update DATABASE_URL to use port 5433
powershell -Command "(gc .env) -replace '5432', '5433' | Out-File -encoding ASCII .env"

echo [OK] Configuration updated to use port 5433
echo.
echo Next step: Run SETUP_DATABASE.bat
echo.
pause
