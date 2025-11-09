@echo off
echo ========================================
echo   HealthAI Nexus Dashboard v3.0
echo ========================================
echo.
cd /d "%~dp0"
python -m streamlit run healthai_nexus\app_dashboard.py
pause
