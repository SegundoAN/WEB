@echo off
title Agente Estadistico EPT 2026
echo ========================================================
echo   Iniciando Agente Estadistico EPT 2026
echo ========================================================
echo.
cd /d "%~dp0"
start http://localhost:5000
python app.py
pause
