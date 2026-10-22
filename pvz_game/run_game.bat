@echo off
title Plantas vs Zombies - Python Edition
cd /d "%~dp0"
python main.py
if errorlevel 1 (
    echo.
    echo El juego se ha cerrado o ha ocurrido un error.
    pause
)
