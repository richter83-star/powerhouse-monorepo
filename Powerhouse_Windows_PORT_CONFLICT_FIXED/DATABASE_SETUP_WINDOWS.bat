
@echo off
echo ========================================
echo POWERHOUSE DATABASE SETUP FOR WINDOWS
echo ========================================
echo.
echo This script will help you set up PostgreSQL database for Powerhouse.
echo.
echo OPTION 1: Install PostgreSQL (Recommended)
echo ----------------------------------------
echo 1. Download PostgreSQL from: https://www.postgresql.org/download/windows/
echo 2. Run the installer and remember your password
echo 3. Default port is 5432 (use this)
echo 4. After installation, come back here and press any key
echo.
pause
echo.
echo OPTION 2: Use Docker (Advanced)
echo ----------------------------------------
echo If you have Docker Desktop installed:
echo   docker run --name powerhouse-db -e POSTGRES_PASSWORD=default -e POSTGRES_USER=default -e POSTGRES_DB=powerhouse -p 5432:5432 -d postgres:15
echo.
echo ========================================
echo After PostgreSQL is running, run SETUP_DATABASE.bat
echo ========================================
pause
