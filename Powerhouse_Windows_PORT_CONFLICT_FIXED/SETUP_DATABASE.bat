
@echo off
cd /d "%~dp0"
echo ========================================
echo SETTING UP POWERHOUSE DATABASE
echo ========================================
echo.

REM Check if PostgreSQL is running
echo Checking if PostgreSQL is running...
netstat -an | find ":5432" >nul
if errorlevel 1 (
    echo [ERROR] PostgreSQL is not running on port 5432
    echo Please run DATABASE_SETUP_WINDOWS.bat first
    pause
    exit /b 1
)

echo [OK] PostgreSQL detected on port 5432
echo.

REM Navigate to frontend
cd frontend\app

REM Generate Prisma Client
echo Generating Prisma Client...
call yarn prisma generate
if errorlevel 1 (
    echo [ERROR] Failed to generate Prisma Client
    pause
    exit /b 1
)

echo [OK] Prisma Client generated
echo.

REM Push database schema
echo Creating database tables...
call yarn prisma db push
if errorlevel 1 (
    echo [ERROR] Failed to create database tables
    echo Make sure PostgreSQL is running with these settings:
    echo   Host: localhost
    echo   Port: 5432
    echo   Database: powerhouse
    echo   User: default
    echo   Password: default
    pause
    exit /b 1
)

echo [OK] Database tables created
echo.

REM Seed database (optional)
echo Seeding database with initial data...
call yarn prisma db seed 2>nul
echo.

cd ..\..

echo ========================================
echo DATABASE SETUP COMPLETE!
echo ========================================
echo.
echo You can now run START.bat to launch Powerhouse
echo.
pause
