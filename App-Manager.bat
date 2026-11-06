@echo off
cd /d "%~dp0"
where python >nul 2>nul || (echo Python nao encontrado. Instale em https://www.python.org/downloads/ marcando "Add python.exe to PATH". & pause & exit /b 1)
if not exist index.json if not exist indice.json python scan.py
start "" pythonw app.py
