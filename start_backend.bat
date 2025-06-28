@echo off
echo =====================================================
echo NLP Key-Value Extractor - Backend Startup
echo =====================================================
echo.
echo Starting FastAPI backend on http://127.0.0.1:8000
echo.
cd %~dp0
call .venv\Scripts\activate.bat
cd backend
python -m uvicorn main:app --host 127.0.0.1 --port 8000
pause
