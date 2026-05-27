import os
from flask import Flask
from flask_cors import CORS
from backend.infra.db import init_db
from backend.infra.server.routes import bp as routes_bp

def bootstrap_app():
    """Inicializa a aplicação Flask puro como API REST, banco de dados e rotas"""
    app = Flask(__name__)
    app.secret_key = os.environ.get("SECRET_KEY", "pizzaria404_dev_secret_key_secure_32bytes")
    CORS(app)
    # Registra as rotas modularizadas
    app.register_blueprint(routes_bp)

    # Executa a inicialização do banco de dados (tabelas)
    init_db()

    # Inicia o thread de atualização automática de status dos pedidos
    from backend.infra.background.status_updater import start_background_updater
    start_background_updater()
    return app
