@echo off
echo ===================================================
echo   CODE CONSTELLATION - Starting AI Galaxy Visualizer
echo ===================================================
echo.
echo Launching default web browser at http://localhost:8000...
start "" "http://localhost:8000"
echo.
echo Launching Python Tornado Server...
python server.py
if %errorlevel% neq 0 (
    echo.
    echo ERROR: Python failed to start. Please check if Python 3 is installed and on your PATH.
    pause
)
