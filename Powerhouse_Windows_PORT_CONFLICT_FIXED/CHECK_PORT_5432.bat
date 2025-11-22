
@echo off
echo ========================================
echo CHECKING WHAT'S USING PORT 5432
echo ========================================
echo.

REM Check if port 5432 is in use
netstat -ano | findstr ":5432" >nul
if errorlevel 1 (
    echo [OK] Port 5432 is FREE and available
    echo You can install PostgreSQL on the default port 5432
    echo.
    echo Next step: Run DATABASE_SETUP_WINDOWS.bat
) else (
    echo [!] Port 5432 is IN USE
    echo.
    echo Details:
    netstat -ano | findstr ":5432"
    echo.
    echo What's using it:
    for /f "tokens=5" %%a in ('netstat -ano ^| findstr ":5432"') do (
        echo Process ID: %%a
        tasklist /FI "PID eq %%a" 2>nul | findstr /V "Image"
    )
    echo.
    echo ========================================
    echo SOLUTIONS:
    echo ========================================
    echo.
    echo OPTION 1: Use Different Port (EASIEST)
    echo   - Run: PORT_5432_CONFLICT_FIX.bat
    echo   - Install PostgreSQL on port 5433
    echo.
    echo OPTION 2: Stop the Existing Service
    echo   - Open Services (services.msc)
    echo   - Find PostgreSQL or the service using port 5432
    echo   - Stop it
    echo   - Then run DATABASE_SETUP_WINDOWS.bat
    echo.
    echo OPTION 3: Uninstall Existing Database
    echo   - If you don't need the existing database
    echo   - Uninstall it from Control Panel
    echo   - Then run DATABASE_SETUP_WINDOWS.bat
    echo.
)

pause
