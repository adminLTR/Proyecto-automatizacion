@echo off
chcp 65001 >nul
cls

echo ========================================
echo 🚀 TELEGRAM BOT - SERVIDOR
echo ========================================
echo.
echo ⚡ Iniciando servidor Flask...
echo.

REM Usar el entorno virtual nuevo
venv_new\Scripts\python.exe start.py

echo.
echo ⏹️  Servidor detenido
pause
