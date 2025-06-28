@echo off
echo Starting NLP Key-Value Extractor...
cd %~dp0
call .venv\Scripts\activate.bat
python run_app.py
pause
