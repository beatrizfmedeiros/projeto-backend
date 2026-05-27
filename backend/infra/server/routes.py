from flask import Blueprint

from backend.infra.storage.sqlite.sqlite_usuario_repository import SqliteUsuarioRepository
from backend.infra.storage.sqlite.sqlite_pedido_repository import SqlitePedidoRepository
from backend.domain.service.usuario_service import UsuarioService
from backend.domain.service.pedido_service import PedidoService
from backend.infra.server.controller.usuario_controller import UsuarioController
from backend.infra.server.controller.pedido_controller import PedidoController

from backend.infra.storage.sqlite.sqlite_produto_repository import SqliteProdutoRepository

bp = Blueprint("routes", __name__)

# Setup de injeções (Dependency Injection)
usuario_repo = SqliteUsuarioRepository()
pedido_repo = SqlitePedidoRepository()
produto_repo = SqliteProdutoRepository()

usuario_service = UsuarioService(usuario_repo)
pedido_service = PedidoService(pedido_repo, usuario_repo, produto_repo)

usuario_controller = UsuarioController(usuario_service)
pedido_controller = PedidoController(pedido_service)

# ─────────────────────────────────────────────
# Rotas – páginas
# ─────────────────────────────────────────────

@bp.route("/")
def index():
    return usuario_controller.index()

@bp.route("/login")
def login_page():
    return usuario_controller.login_page()

@bp.route("/cadastro")
def cadastro_page():
    return usuario_controller.cadastro_page()

@bp.route("/cardapio")
def cardapio_page():
    return pedido_controller.cardapio_page()

@bp.route("/sobre")
def sobre_page():
    return pedido_controller.sobre_page()

@bp.route("/carrinho")
def carrinho_page():
    return pedido_controller.carrinho_page()

@bp.route("/api/pedido", methods=["POST"])
def api_pedido():
    return pedido_controller.adicionar_item()

# ─────────────────────────────────────────────
# APIs – endpoints de dados
# ─────────────────────────────────────────────

@bp.route("/api/cadastro", methods=["POST"])
def api_cadastro():
    return usuario_controller.cadastrar()

@bp.route("/api/login", methods=["POST"])
def api_login():
    return usuario_controller.autenticar()

@bp.route("/api/logout", methods=["POST"])
def api_logout():
    return usuario_controller.logout()

@bp.route("/meus-pedidos")
def meus_pedidos_page():
    return pedido_controller.meus_pedidos()

@bp.route("/api/me")
def api_me():
    return usuario_controller.api_me()

@bp.route("/api/pedido_item/delete/<int:pedido_item_id>", methods=["POST"])
def api_pedido_item_delete(pedido_item_id: int):
    return pedido_controller.remover_item(pedido_item_id)

@bp.route("/api/pedido/finalizar", methods=["GET", "POST"])
def api_pedido_finalizar():
    return pedido_controller.finalizar()
