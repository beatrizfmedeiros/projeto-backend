import os
from flask import Flask
from flask_cors import CORS
from backend.infra.db import init_db
from backend.infra.server.routes import bp as routes_bp

def bootstrap_app():
    """Inicializa (bootstrap) a aplicação Flask, banco de dados e rotas"""
    # Mapeia o diretório raiz do repositório
    server_dir = os.path.dirname(os.path.abspath(__file__))
    root_dir = os.path.abspath(os.path.join(server_dir, "..", "..", ".."))
    
    app = Flask(
        __name__,
        template_folder=os.path.join(root_dir, "frontend", "templates"),
        static_folder=os.path.join(root_dir, "frontend", "static")
    )
    app.secret_key = os.environ.get("SECRET_KEY", "pizzaria404_dev_secret")
    CORS(app)

    # Executa a inicialização do banco de dados (tabelas)
    init_db()

    # Registra as rotas modularizadas
    app.register_blueprint(routes_bp)

    return app
