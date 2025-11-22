
@echo off
echo ========================================
echo USE EXISTING POSTGRESQL INSTALLATION
echo ========================================
echo.
echo It looks like you already have PostgreSQL installed!
echo Let's configure Powerhouse to use it.
echo.

:ask_existing
echo What port is your existing PostgreSQL running on?
set /p EXISTING_PORT="Enter port (usually 5432 or 5433): "

echo %EXISTING_PORT%| findstr /r "^[0-9][0-9]*$" >nul
if errorlevel 1 (
    echo [ERROR] Invalid port number
    goto ask_existing
)

echo.
echo What is your PostgreSQL password?
set /p EXISTING_PASSWORD="Enter password: "

if "!EXISTING_PASSWORD!"=="" (
    echo [ERROR] Password cannot be empty
    goto ask_existing
)

echo.
echo What is your PostgreSQL username?
set /p EXISTING_USER="Enter username (default is 'postgres'): "

if "!EXISTING_USER!"=="" (
    set EXISTING_USER=postgres
)

echo.
echo Testing connection to PostgreSQL...
echo.

REM Update .env file
cd /d "%~dp0"
cd frontend\app

if exist .env (
    copy .env .env.backup >nul 2>&1
)

REM Create new DATABASE_URL
set "NEW_DB_URL=postgresql://%EXISTING_USER%:%EXISTING_PASSWORD%@localhost:%EXISTING_PORT%/powerhouse?schema=public"

echo DATABASE_URL="%NEW_DB_URL%" > .env.temp

REM Replace DATABASE_URL in .env
powershell -Command "(gc .env) -replace 'DATABASE_URL=.*', (gc .env.temp) | Out-File -encoding ASCII .env"
del .env.temp

echo [OK] Configuration updated
echo.
echo Database URL:
echo %NEW_DB_URL%
echo.
echo ========================================
echo NEXT STEPS:
echo ========================================
echo.
echo 1. Make sure your PostgreSQL has a database named 'powerhouse'
echo    If not, create it:
echo      a) Open pgAdmin or psql
echo      b) CREATE DATABASE powerhouse;
echo.
echo 2. Run: SETUP_DATABASE.bat
echo    This will create the necessary tables
echo.
echo 3. Run: START.bat
echo    Launch Powerhouse!
echo.
pause
