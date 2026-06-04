@echo off
REM Script para iniciar rápidamente la API

echo ====================================================
echo Generador de Respuestas Aleatorias - Inicio Rápido
echo ====================================================
echo.

REM Verificar si Python está instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python no está instalado o no está en el PATH
    echo Por favor instala Python desde https://www.python.org
    pause
    exit /b 1
)

echo [1/3] Verificando dependencias...
pip show fastapi >nul 2>&1
if errorlevel 1 (
    echo [2/3] Instalando dependencias (puede tomar un minuto)...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo Error al instalar dependencias
        pause
        exit /b 1
    )
) else (
    echo Dependencias ya instaladas
)

echo.
echo [3/3] Iniciando servidor...
echo.
echo ====================================================
echo Servidor iniciado en http://localhost:8000
echo Interfaz Swagger: http://localhost:8000/docs
echo ====================================================
echo.

python main.py

pause
