.PHONY: install run dev help

VENV = venv
PYTHON = $(VENV)/bin/python
PIP = $(VENV)/bin/pip

help:
	@echo "Comandos disponíveis:"
	@echo "  make install - Cria o ambiente virtual e instala as dependências"
	@echo "  make run     - Inicia a Pizzaria 404 com as variáveis do .env"

$(VENV)/bin/activate:
	python -m venv $(VENV)

install: $(VENV)/bin/activate
	$(PIP) install -r backend/requirements.txt

run dev: install
	@if [ -f .env ]; then \
		echo "Carregando variáveis do arquivo .env..."; \
		export $$(cat .env | grep -v '^#' | xargs) && PYTHONPATH=. $(PYTHON) backend/app.py; \
	else \
		PYTHONPATH=. $(PYTHON) backend/app.py; \
	fi
