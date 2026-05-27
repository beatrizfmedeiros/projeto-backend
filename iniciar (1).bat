@echo off
title Pizzaria 404
cd /d "%~dp0"

echo.
echo  Verificando dependencias...
pip install -r backend/requirements.txt --quiet

echo.
echo  Iniciando Pizzaria 404...
echo  Acesse: http://localhost:5000
echo  Para fechar: pressione CTRL+C ou feche esta janela
echo.

set PYTHONPATH=.
start "" "http://localhost:5000"
python backend/app.py
pause
