import os
import sys

# Garante que a raiz do projeto esteja no sys.path para importações relativas funcionarem em qualquer SO
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from backend.infra.server.app_factory import bootstrap_app

# Inicializa o Flask através da fábrica de inicialização
app = bootstrap_app()

if __name__ == "__main__":
    host = os.environ.get("FLASK_RUN_HOST", "127.0.0.1")
    port = int(os.environ.get("FLASK_RUN_PORT", 5000))
    debug = os.environ.get("FLASK_DEBUG", "True").lower() in ("true", "1", "yes")

    print(f"🍕  Pizzaria 404 → http://{host}:{port}")
    app.run(host=host, port=port, debug=debug)
