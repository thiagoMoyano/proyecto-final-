@echo off
title Clima MDZ - Reporte Meteorologico Interactivo
color 0b

echo ========================================================
echo      INICIANDO CLIMA MDZ - PRONOSTICO INTERACTIVO
echo ========================================================
echo.

cd /d "%~dp0"
python main.py

if errorlevel 1 (
    echo.
    echo Ocurrio un error al ejecutar el programa.
    pause
)
