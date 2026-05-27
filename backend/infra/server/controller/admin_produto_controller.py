from flask import jsonify, request, g
from backend.infra.security.jwt_auth import admin_required

class AdminProdutoController:
    """Controller for admin CRUD operations on products."""

    def __init__(self, produto_repo):
        self.produto_repo = produto_repo

    @admin_required
    def criar(self):
        data = request.get_json()
        if not data:
            return jsonify({"ok": False, "erro": "Payload JSON requerido."}), 400
        # Expect fields: nome, preco, foto, descricao, categoria, tags, ativo
        from backend.domain.entity.produto import Produto
        produto = Produto(
            nome=data.get("nome", ""),
            preco=data.get("preco", 0.0),
            foto=data.get("foto", ""),
            descricao=data.get("descricao", ""),
            categoria=data.get("categoria", ""),
            tags=data.get("tags", []),
            ativo=data.get("ativo", True),
        )
        prod_id = self.produto_repo.create_produto(produto)
        return jsonify({"ok": True, "mensagem": "Produto criado.", "id": prod_id}), 201

    @admin_required
    def atualizar(self, produto_id: int):
        data = request.get_json()
        if not data:
            return jsonify({"ok": False, "erro": "Payload JSON requerido."}), 400
        from backend.domain.entity.produto import Produto
        produto = Produto(
            id=produto_id,
            nome=data.get("nome", ""),
            preco=data.get("preco", 0.0),
            foto=data.get("foto", ""),
            descricao=data.get("descricao", ""),
            categoria=data.get("categoria", ""),
            tags=data.get("tags", []),
            ativo=data.get("ativo", True),
        )
        self.produto_repo.update_produto(produto_id, produto)
        return jsonify({"ok": True, "mensagem": "Produto atualizado."}), 200

    @admin_required
    def remover(self, produto_id: int):
        self.produto_repo.delete_produto(produto_id)
        return jsonify({"ok": True, "mensagem": "Produto removido."}), 200
