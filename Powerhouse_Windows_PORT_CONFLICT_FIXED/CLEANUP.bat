@echo off
echo ========================================
echo  Cleanup Bad Virtual Environment
echo ========================================
echo.

REM Check if venv exists in System32 (the wrong location)
if exist "C:\Windows\System32\venv" (
    echo Found incorrect venv in System32!
    echo.
    echo This venv was created in the wrong location.
    echo It's safe to delete it.
    echo.
    echo Removing C:\Windows\System32\venv...
    
    rmdir /s /q "C:\Windows\System32\venv"
    
    if errorlevel 1 (
        echo.
        echo ERROR: Failed to remove venv from System32
        echo You may need to run this as Administrator
        echo.
        pause
        exit /b 1
    )
    
    echo [SUCCESS] Removed incorrect venv from System32
    echo.
) else (
    echo No incorrect venv found in System32
    echo.
)

REM Get the directory where THIS batch file is located
set "SCRIPT_DIR=%~dp0"
cd /d "%SCRIPT_DIR%"

echo Current directory: %CD%
echo.

REM Check if backend has a venv
if exist "backend\venv" (
    echo Found venv in backend folder
    echo.
    choice /C YN /M "Do you want to delete backend\venv and reinstall"
    
    if errorlevel 2 (
        echo Keeping existing backend\venv
        echo.
    ) else (
        echo Removing backend\venv...
        cd backend
        rmdir /s /q venv
        cd ..
        echo [SUCCESS] Removed backend\venv
        echo.
    )
) else (
    echo No venv found in backend folder (this is normal before installation)
    echo.
)

echo ========================================
echo  Cleanup Complete
echo ========================================
echo.
echo Next step: Run INSTALL.bat to install correctly
echo.
pause
