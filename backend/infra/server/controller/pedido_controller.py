from flask import request, redirect, url_for, render_template, session, jsonify
from backend.domain.dto.pedido_dto import AdicionarItemDTO
from backend.domain.service.pedido_service import PedidoService

class PedidoController:
    def __init__(self, pedido_service: PedidoService):
        self.pedido_service = pedido_service

    def cardapio_page(self):
        nome = session.get("usuario_nome")
        produtos = self.pedido_service.obter_cardapio()
        return render_template("cardapio.html", usuario=nome, produtos=produtos)

    def sobre_page(self):
        nome = session.get("usuario_nome")
        return render_template("sobre.html", usuario=nome)

    def carrinho_page(self):
        nome = session.get("usuario_nome")
        item_nome = (request.args.get("item") or "").strip()
        if not item_nome:
            return redirect(url_for("routes.cardapio_page"))

        produto = self.pedido_service.obter_produto_por_nome(item_nome)
        if not produto:
            return redirect(url_for("routes.cardapio_page"))

        return render_template(
            "carrinho.html",
            usuario=nome,
            item_nome=produto.nome,
            item_valor=f"{produto.preco:.2f}".replace(".", ","),
        )

    def adicionar_item(self):
        nome = session.get("usuario_nome")
        if not nome:
            return redirect(url_for("routes.login_page"))

        item = (request.form.get("item") or "").strip()
        personalizacao = (request.form.get("personalizacao") or "").strip()
        quantidade = request.form.get("quantidade", "1").strip()

        dto = AdicionarItemDTO(
            item_nome=item,
            quantidade=quantidade,
            observacao=personalizacao
        )
        try:
            dto.validate()  # Valida contrato do input (Single Source of Truth)
            self.pedido_service.adicionar_item(nome, dto)
        except ValueError as e:
            return jsonify({"ok": False, "erro": str(e)}), 400
        except Exception:
            return redirect(url_for("routes.login_page"))

        return redirect(url_for("routes.carrinho_page", item=dto.item_nome) + f"&saved=1&qtd={dto.quantidade}")

    def meus_pedidos(self):
        nome = session.get("usuario_nome")
        if not nome:
            return redirect(url_for("routes.login_page"))

        itens = self.pedido_service.obter_itens_carrinho(nome)
        total = 0.0
        itens_out = []
        for it in itens:
            total += it.subtotal
            itens_out.append({
                "id": it.id,
                "nome": it.item_nome,
                "foto": it.item_foto,
                "valor": it.item_valor,
                "quantidade": it.quantidade,
                "observacao": it.observacao,
                "valor_formatado": it.valor_formatado,
            })

        total_formatado = f"{total:.2f}".replace('.', ',')
        return render_template(
            "meus_pedidos.html",
            usuario=nome, itens=itens_out, total_formatado=total_formatado
        )

    def remover_item(self, pedido_item_id):
        nome = session.get("usuario_nome")
        if not nome:
            return redirect(url_for("routes.login_page"))
        try:
            self.pedido_service.remover_item_carrinho(nome, pedido_item_id)
        except Exception:
            return redirect(url_for("routes.login_page"))
        return redirect(url_for("routes.meus_pedidos"))

    def finalizar(self):
        nome = session.get("usuario_nome")
        if not nome:
            return redirect(url_for("routes.login_page"))
        try:
            self.pedido_service.finalizar_carrinho(nome)
        except Exception:
            return redirect(url_for("routes.login_page"))
        return redirect(url_for("routes.meus_pedidos"))
