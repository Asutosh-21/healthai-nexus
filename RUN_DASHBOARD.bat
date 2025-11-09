@echo off
echo ========================================
echo   HealthAI Nexus - Dashboard v3.0
echo ========================================
echo.
echo Installing required dependencies...
pip install plotly -q

echo.
echo Starting Dashboard Application...
echo.
echo Features:
echo  - Login/Register System
echo  - Interactive Dashboard
echo  - Health Visualizations
echo  - AI Prescriptions
echo  - Numeric Age/Weight/Height Input
echo.
echo The app will open in your browser.
echo Press Ctrl+C to stop.
echo.

streamlit run healthai_nexus\app_dashboard.py

pause
