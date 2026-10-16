@echo off
title JARVIS AI - Virtual Mouse
echo ==========================================
echo   JARVIS AI - Touchless Desktop Controller
echo ==========================================
echo.
echo Starting application...
pip install -r requirements.txt
streamlit run app.py
pause
