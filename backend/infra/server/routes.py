from flask import Blueprint

from backend.infra.storage.sqlite.sqlite_usuario_repository import SqliteUsuarioRepository
from backend.infra.storage.sqlite.sqlite_pedido_repository import SqlitePedidoRepository
from backend.infra.storage.sqlite.sqlite_produto_repository import SqliteProdutoRepository

from backend.domain.service.usuario_service import UsuarioService
from backend.domain.service.pedido_service import PedidoService

from backend.infra.server.controller.usuario_controller import UsuarioController
from backend.infra.server.controller.pedido_controller import PedidoController

from backend.infra.security.jwt_auth import auth_required

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
# APIs – endpoints de dados 100% RESTful
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

@bp.route("/api/me")
def api_me():
    return usuario_controller.api_me()

@bp.route("/api/carrinho", methods=["GET"])
@auth_required
def api_carrinho():
    return pedido_controller.obter_carrinho()

@bp.route("/api/pedido", methods=["POST"])
@auth_required
def api_pedido():
    return pedido_controller.adicionar_item()

@bp.route("/api/pedido_item/delete/<int:pedido_item_id>", methods=["POST"])
@auth_required
def api_pedido_item_delete(pedido_item_id: int):
    return pedido_controller.remover_item(pedido_item_id)

@bp.route("/api/pedido/finalizar", methods=["POST"])
@auth_required
def api_pedido_finalizar():
    return pedido_controller.finalizar()

@bp.route("/api/pedidos/historico", methods=["GET"])
@auth_required
def api_pedidos_historico():
    return pedido_controller.obter_historico()
