from flask import request, jsonify, g
from backend.domain.dto.pedido_dto import AdicionarItemDTO
from backend.domain.service.pedido_service import PedidoService

class PedidoController:
    def __init__(self, pedido_service: PedidoService):
        self.pedido_service = pedido_service

    def obter_carrinho(self):
        """Retorna todos os itens do carrinho ativo do usuário em formato JSON estruturado"""
        nome = g.current_user.nome
        try:
            itens = self.pedido_service.obter_itens_carrinho(nome)
            total = 0.0
            itens_out = []
            for it in itens:
                total += it.subtotal
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
                "itens": itens_out,
                "total": float(total)
            })
        except Exception as e:
            return jsonify({"ok": False, "erro": f"Erro ao buscar carrinho: {str(e)}"}), 500

    def adicionar_item(self):
        """Adiciona um item ao carrinho via form-data ou JSON payload"""
        nome = g.current_user.nome
        
        # Suporta tanto form-data tradicional quanto payloads JSON
        dados = request.get_json(silent=True) or {}
        item = request.form.get("item")
        if not item:
            item = dados.get("item")
        item = (item or "").strip()

        personalizacao = request.form.get("personalizacao")
        if not personalizacao:
            personalizacao = dados.get("personalizacao")
        personalizacao = (personalizacao or "").strip()

        quantidade = request.form.get("quantidade")
        if not quantidade:
            quantidade = dados.get("quantidade")
        quantidade = str(quantidade or "1").strip()

        dto = AdicionarItemDTO(
            item_nome=item,
            quantidade=quantidade,
            observacao=personalizacao
        )
        try:
            dto.validate()  # Valida contrato sintático (Single Source of Truth)
            self.pedido_service.adicionar_item(nome, dto)
            return jsonify({
                "ok": True,
                "mensagem": f"Item '{dto.item_nome}' adicionado ao carrinho com sucesso!"
            }), 201
        except ValueError as e:
            return jsonify({"ok": False, "erro": str(e)}), 400
        except Exception as e:
            return jsonify({"ok": False, "erro": f"Erro interno no servidor: {str(e)}"}), 500

    def remover_item(self, pedido_item_id):
        """Remove um item específico do carrinho"""
        nome = g.current_user.nome
        try:
            self.pedido_service.remover_item_carrinho(nome, pedido_item_id)
            return jsonify({
                "ok": True,
                "mensagem": "Item removido do carrinho com sucesso!"
            })
        except ValueError as e:
            return jsonify({"ok": False, "erro": str(e)}), 400
        except Exception as e:
            return jsonify({"ok": False, "erro": f"Erro ao remover item: {str(e)}"}), 500

    def finalizar(self):
        """Finaliza o carrinho ativo (Checkout)"""
        nome = g.current_user.nome
        try:
            self.pedido_service.finalizar_carrinho(nome)
            return jsonify({
                "ok": True,
                "mensagem": "Pedido finalizado com sucesso!"
            })
        except ValueError as e:
            return jsonify({"ok": False, "erro": str(e)}), 400
        except Exception as e:
            return jsonify({"ok": False, "erro": f"Erro ao finalizar pedido: {str(e)}"}), 500

    def obter_historico(self):
        """Retorna o histórico de pedidos finalizados do usuário em JSON"""
        nome = g.current_user.nome
        try:
            historico = self.pedido_service.obter_historico(nome)
            return jsonify({
                "ok": True,
                "historico": historico
            })
        except Exception as e:
            return jsonify({"ok": False, "erro": f"Erro ao buscar histórico: {str(e)}"}), 500
