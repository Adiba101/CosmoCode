@echo off
python -m unittest discover tests
IF %ERRORLEVEL% NEQ 0 pause
