@echo off
echo ========================================
echo  Stopping Powerhouse B2B Platform
echo ========================================
echo.

echo Stopping backend (port 8001)...
for /f "tokens=5" %%a in ('netstat -aon ^| findstr :8001 ^| findstr LISTENING') do (
    echo   - Killing process %%a
    taskkill /F /PID %%a >nul 2>&1
)

echo Stopping frontend (port 3000)...
for /f "tokens=5" %%a in ('netstat -aon ^| findstr :3000 ^| findstr LISTENING') do (
    echo   - Killing process %%a
    taskkill /F /PID %%a >nul 2>&1
)

echo.
echo ========================================
echo  ✅ Platform Stopped
echo ========================================
echo.
echo All services have been stopped.
echo You can now close this window.
echo.
pause
