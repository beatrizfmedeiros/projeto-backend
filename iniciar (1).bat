@echo off
title Pizzaria 404
cd /d "%~dp0"

set PYTHON=python
set PIP=pip

if exist venv\Scripts\python.exe (
    set PYTHON=venv\Scripts\python.exe
    set PIP=venv\Scripts\pip.exe
) else if exist .venv\Scripts\python.exe (
    set PYTHON=.venv\Scripts\python.exe
    set PIP=.venv\Scripts\pip.exe
)

echo.
echo  Verificando dependencias...
%PIP% install -r backend/requirements.txt --quiet

echo.
echo  Iniciando Pizzaria 404...
echo  Acesse: http://localhost:5000
echo  Para fechar: pressione CTRL+C ou feche esta janela
echo.

set PYTHONPATH=.
start "" "http://localhost:5000"
%PYTHON% backend/app.py
pause
