
@echo off
setlocal enabledelayedexpansion
echo ========================================
echo CUSTOM PORT CONFIGURATION
echo ========================================
echo.
echo This will help you configure PostgreSQL to use a custom port.
echo.

:ask_port
set /p CUSTOM_PORT="Enter the port you want to use (e.g., 5433, 5434, 15432): "

REM Validate port number
echo %CUSTOM_PORT%| findstr /r "^[0-9][0-9]*$" >nul
if errorlevel 1 (
    echo [ERROR] Invalid port number. Please enter numbers only.
    goto ask_port
)

if %CUSTOM_PORT% LSS 1024 (
    echo [WARNING] Ports below 1024 may require administrator privileges
)

if %CUSTOM_PORT% GTR 65535 (
    echo [ERROR] Port number must be less than 65536
    goto ask_port
)

echo.
echo Checking if port %CUSTOM_PORT% is available...
netstat -ano | findstr ":%CUSTOM_PORT%" >nul
if errorlevel 1 (
    echo [OK] Port %CUSTOM_PORT% is available!
) else (
    echo [ERROR] Port %CUSTOM_PORT% is already in use
    echo.
    echo Ports in use:
    netstat -ano | findstr ":%CUSTOM_PORT%"
    echo.
    goto ask_port
)

echo.
echo ========================================
echo CONFIGURATION STEPS:
echo ========================================
echo.
echo 1. Install PostgreSQL from:
echo    https://www.postgresql.org/download/windows/
echo.
echo 2. During installation, when asked for port, enter: %CUSTOM_PORT%
echo.
echo 3. Use password: default
echo.
echo 4. After installation, come back here and press any key
echo.
pause

echo.
echo Updating Powerhouse configuration to use port %CUSTOM_PORT%...
cd /d "%~dp0"
cd frontend\app

REM Backup original .env
if exist .env (
    copy .env .env.backup >nul 2>&1
    echo [OK] Backed up .env to .env.backup
)

REM Update DATABASE_URL to use custom port
powershell -Command "(gc .env) -replace 'localhost:5432', 'localhost:%CUSTOM_PORT%' | Out-File -encoding ASCII .env"

echo [OK] Configuration updated to use port %CUSTOM_PORT%
echo.
echo Updated database URL:
type .env | findstr DATABASE_URL
echo.
echo ========================================
echo CONFIGURATION COMPLETE!
echo ========================================
echo.
echo Next steps:
echo 1. Make sure PostgreSQL is running on port %CUSTOM_PORT%
echo 2. Run: SETUP_DATABASE.bat
echo 3. Run: START.bat
echo.
pause
