@echo off
REM Quick start script for Windows
REM Double-click to run or execute from command prompt

echo ============================================
echo Telegram Automation Bot - Quick Start
echo ============================================
echo.

REM Check if .env exists
if not exist .env (
    echo [1/3] Creando archivo .env...
    copy .env.example .env
    echo.
    echo IMPORTANTE: Edita el archivo .env con tus credenciales!
    echo - Token de Telegram de @BotFather
    echo - Email por defecto
    echo.
    echo Presiona Enter para abrir el archivo .env
    pause
    notepad .env
    echo.
) else (
    echo [1/3] Archivo .env ya existe
)

echo.
echo [2/3] Usando entorno virtual...
if not exist venv_new\Scripts\python.exe (
    echo Creando entorno virtual nuevo...
    python -m venv venv_new
    if errorlevel 1 (
        echo ERROR: No se pudo crear el entorno virtual
        pause
        exit /b 1
    )
    echo Instalando paquetes...
    venv_new\Scripts\python.exe -m pip install -q --upgrade pip setuptools wheel
    venv_new\Scripts\python.exe -m pip install -r requirements.txt
) else (
    echo Entorno virtual ya existe
)

echo.
echo [3/3] Iniciando el servidor...
echo.
echo NOTA: El servidor se iniciara incluso sin credentials.json
echo      Para usar funciones de Google, necesitas:
echo      1. Descargar credentials.json de Google Cloud Console
echo      2. Colocarlo en esta carpeta
echo      3. Ejecutar el servidor para autenticar
echo.
echo ============================================
echo.
echo El servidor quedara ejecutandose aqui.
echo Abre tu navegador en: http://localhost:5000/health
echo Para detener: presiona CTRL+C
echo.
echo ============================================
echo.

REM Start the server usando el python del entorno virtual limpio
venv_new\Scripts\python.exe start.py

if errorlevel 1 (
    echo.
    echo ERROR al iniciar el servidor
    pause
)

echo.
echo ============================================
echo Servidor detenido
echo ============================================
echo.
pause
