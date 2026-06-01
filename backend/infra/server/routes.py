from flask import Blueprint, jsonify, render_template

from backend.infra.storage.sqlite.sqlite_usuario_repository import SqliteUsuarioRepository
from backend.infra.storage.sqlite.sqlite_pedido_repository import SqlitePedidoRepository
from backend.infra.storage.sqlite.sqlite_produto_repository import SqliteProdutoRepository

from backend.domain.service.usuario_service import UsuarioService
from backend.domain.service.pedido_service import PedidoService

from backend.infra.server.controller.usuario_controller import UsuarioController
from backend.infra.server.controller.pedido_controller import PedidoController

from backend.infra.server.controller.admin_produto_controller import AdminProdutoController
from backend.infra.security.jwt_auth import auth_required, admin_required

# ... existing imports above ...

# admin_produto_controller will be instantiated after repo definitions
produto_repo = SqliteProdutoRepository()
admin_produto_controller = AdminProdutoController(produto_repo)
bp = Blueprint("routes", __name__)
@bp.route("/api/admin/produtos", methods=["POST"])
@auth_required
@admin_required
def api_admin_produto_create():
    return admin_produto_controller.criar()

@bp.route("/api/admin/produtos/<int:produto_id>", methods=["PUT"])
@auth_required
@admin_required
def api_admin_produto_update(produto_id: int):
    return admin_produto_controller.atualizar(produto_id)

@bp.route("/api/admin/produtos/<int:produto_id>", methods=["DELETE"])
@auth_required
@admin_required
def api_admin_produto_delete(produto_id: int):
    return admin_produto_controller.remover(produto_id)


# Blueprint already defined earlier

# Setup de injeções (Dependency Injection)
usuario_repo = SqliteUsuarioRepository()
pedido_repo = SqlitePedidoRepository()
produto_repo = SqliteProdutoRepository()
# admin_produto_controller already defined above

usuario_service = UsuarioService(usuario_repo)
pedido_service = PedidoService(pedido_repo, usuario_repo, produto_repo)

usuario_controller = UsuarioController(usuario_service)
pedido_controller = PedidoController(pedido_service)

# ─────────────────────────────────────────────
# Rotas – páginas do frontend
# ─────────────────────────────────────────────

@bp.route("/")
def index():
    return render_template("index.html")

@bp.route("/login")
def login_page():
    return render_template("login.html")

@bp.route("/cadastro")
def cadastro_page():
    return render_template("cadastro.html")

@bp.route("/cardapio")
def cardapio_page():
    produtos = produto_repo.get_all()
    return render_template("cardapio.html", produtos=produtos)

@bp.route("/sobre")
def sobre_page():
    return render_template("sobre.html")

@bp.route("/carrinho")
def carrinho_page():
    from flask import request
    item_nome = request.args.get("item", "")
    produto = produto_repo.get_by_name(item_nome)
    item_valor = float(produto.preco) if produto else 0.0
    return render_template("carrinho.html", item_nome=item_nome, item_valor=item_valor)

@bp.route("/meus-pedidos")
def meus_pedidos_page():
    return render_template("meus_pedidos.html")

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

@bp.route("/api/pedido/<int:pedido_id>/status", methods=["GET"])
@auth_required
def api_pedido_status(pedido_id: int):
    pedido = pedido_repo.get_pedido_by_id(pedido_id)
    if not pedido:
        return jsonify({"error": "Pedido not found"}), 404
    return jsonify({"pedido_id": pedido.id, "status": pedido.status})

@bp.route("/api/pedido/<int:pedido_id>", methods=["GET"])
@auth_required
def api_pedido_detalhes(pedido_id: int):
    from flask import g
    pedido = pedido_repo.get_pedido_by_id(pedido_id)
    if not pedido:
        return jsonify({"ok": False, "erro": "Pedido not found."}), 404
    if pedido.usuario_id != g.current_user.id:
        return jsonify({"ok": False, "erro": "Access denied."}), 403
    itens = pedido_repo.get_pedido_items(pedido_id)
    itens_out = []
    for it in itens:
        itens_out.append({
            "id": it.id,
            "nome": it.item_nome,
            "foto": it.item_foto,
            "valor_unitario": float(it.item_valor),
            "quantidade": int(it.quantidade),
            "observacao": it.observacao,
            "subtotal": float(it.subtotal)
        })
    return jsonify({
        "ok": True,
        "pedido_id": pedido.id,
        "status": pedido.status,
        "data": pedido.criado_em,
        "endereco_entrega": pedido.endereco_entrega,
        "forma_pagamento": pedido.forma_pagamento,
        "valor_frete": float(pedido.valor_frete or 0.0),
        "total_pago": float(pedido.total_pago or 0.0),
        "itens": itens_out
    })

@bp.route("/api/pedidos/historico", methods=["GET"])
@auth_required
def api_pedidos_historico():
    return pedido_controller.obter_historico()
