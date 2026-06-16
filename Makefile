ifeq ($(OS),Windows_NT)
    VENV = venv
    PYTHON = $(VENV)\Scripts\python.exe
    PIP = $(VENV)\Scripts\pip.exe
    ACTIVATE = $(VENV)\Scripts\activate
else
    VENV = venv
    PYTHON = $(VENV)/bin/python
    PIP = $(VENV)/bin/pip
    ACTIVATE = $(VENV)/bin/activate
endif

.PHONY: install run dev help

help:
	@echo "Comandos disponiveis:"
	@echo "  make install - Cria o ambiente virtual e instala as dependencias"
	@echo "  make run     - Inicia a Pizzaria 404"

$(ACTIVATE):
	python -m venv $(VENV)

install: $(ACTIVATE)
	$(PIP) install -r backend/requirements.txt

run dev: install
	$(PYTHON) backend/app.py
