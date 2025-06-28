@echo off
echo =====================================================
echo NLP Key-Value Extractor - Quick Start
echo =====================================================
echo.
echo This script will start both backend and frontend in separate windows
echo.
echo Press any key to continue...
pause > nul

echo Starting backend...
start cmd /k "%~dp0\start_backend.bat"

echo.
echo Waiting 3 seconds for backend to initialize...
timeout /t 3 /nobreak > nul

echo.
echo Starting frontend...
start cmd /k "%~dp0\start_frontend.bat"

echo.
echo Both services should now be running in separate windows.
echo.
echo  - Backend API: http://127.0.0.1:8000
echo  - Frontend:    http://127.0.0.1:8080
echo.
echo You can close this window, but keep the other windows open
echo to keep the application running.
echo =====================================================
