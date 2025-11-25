@echo off
REM Quick start script for Windows
REM Double-click to run or execute from command prompt

echo ============================================
echo Telegram Automation Bot - Quick Start
echo ============================================
echo.

REM Check if .env exists
if not exist .env (
    echo [1/4] Creando archivo .env...
    copy .env.example .env
    echo.
    echo IMPORTANTE: Edita el archivo .env con tus credenciales!
    echo - Token de Telegram de @BotFather
    echo - Email por defecto
    echo.
    pause
    notepad .env
) else (
    echo [1/4] Archivo .env ya existe
)

echo.
echo [2/4] Verificando credentials.json...
if not exist credentials.json (
    echo.
    echo ERROR: No se encontro credentials.json
    echo.
    echo Por favor:
    echo 1. Ve a Google Cloud Console
    echo 2. Descarga las credenciales OAuth 2.0
    echo 3. Renombralo a credentials.json
    echo 4. Colocalo en esta carpeta
    echo.
    pause
    exit /b 1
) else (
    echo credentials.json encontrado!
)

echo.
echo [3/4] Instalando dependencias...
if not exist venv (
    python -m venv venv
)
call venv\Scripts\activate.bat
pip install -r requirements.txt

echo.
echo [4/4] Verificando autenticacion de Google...
if not exist token.json (
    echo.
    echo Se abrira el navegador para autorizar la aplicacion...
    echo Por favor, acepta los permisos solicitados.
    echo.
    pause
    python run.py
) else (
    echo Token de Google ya existe
    echo.
    echo Todo listo! Puedes ejecutar:
    echo - python run.py  (modo desarrollo)
    echo - docker-compose up -d  (con Docker)
    echo.
)

echo.
echo ============================================
echo Setup completado!
echo ============================================
echo.
pause
