@echo off
echo ========================================
echo    HealthAI Nexus - Starting App
echo ========================================
echo.

REM Check if virtual environment exists
if exist "healthai_nexus\venv\Scripts\activate.bat" (
    echo Activating virtual environment...
    call healthai_nexus\venv\Scripts\activate.bat
) else (
    echo No virtual environment found. Using system Python.
)

echo.
echo Starting HealthAI Nexus Enhanced Application...
echo.
echo The app will open in your browser automatically.
echo Press Ctrl+C to stop the server.
echo.

streamlit run healthai_nexus\app_enhanced.py

pause
