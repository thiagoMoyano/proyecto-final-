@echo off
title Generador de Reportes Meteorologicos
color 0b

echo ========================================================
echo       INICIANDO REPORTE METEOROLOGICO VISUAL
echo ========================================================
echo.

:: Nos aseguramos de situarnos en la carpeta del proyecto
cd /d "%~dp0"

:: Ejecutamos el script orquestador con Python
python main.py

:: Si el grafico se genero correctamente, lo abrimos automaticamente en pantalla
if exist clima_hoy.png (
    echo.
    echo -> Abriendo el reporte visual en el visor de imagenes...
    start clima_hoy.png
)

echo.
echo ========================================================
echo El programa finalizo correctamente.
echo Presiona cualquier tecla para cerrar esta ventana...
echo ========================================================
pause > nul
