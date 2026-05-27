.PHONY: install run dev help

VENV = venv
PYTHON = $(VENV)/bin/python
PIP = $(VENV)/bin/pip

help:
	@echo "Comandos disponíveis:"
	@echo "  make install - Cria o ambiente virtual e instala as dependências"
	@echo "  make run     - Inicia a Pizzaria 404 (Flask app)"
	@echo "  make dev     - Inicia em modo de desenvolvimento"

$(VENV)/bin/activate:
	python -m venv $(VENV)

install: $(VENV)/bin/activate
	$(PIP) install -r backend/requirements.txt

run dev: install
	$(PYTHON) backend/app.py
