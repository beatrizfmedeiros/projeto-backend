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

    # Executa a inicialização do banco de dados (tabelas)
    init_db()

    # Registra as rotas modularizadas
    app.register_blueprint(routes_bp)

    return app
