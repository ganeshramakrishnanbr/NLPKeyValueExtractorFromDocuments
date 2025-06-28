@echo off
echo =====================================================
echo NLP Key-Value Extractor - Frontend Startup
echo =====================================================
echo.
echo Starting Django frontend on http://127.0.0.1:8080
echo.
cd %~dp0
call .venv\Scripts\activate.bat
cd frontend
python manage.py runserver 127.0.0.1:8080
pause
