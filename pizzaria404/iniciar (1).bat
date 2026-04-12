@echo off
title Pizzaria 404
cd /d "%~dp0"

echo.
echo  Verificando dependencias...
pip install -r requirements.txt --quiet

echo.
echo  Iniciando Pizzaria 404...
echo  Acesse: http://localhost:5000
echo  Para fechar: pressione CTRL+C ou feche esta janela
echo.

start "" "http://localhost:5000"
python app.py
pause
