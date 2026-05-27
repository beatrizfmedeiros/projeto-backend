from flask import request, redirect, url_for, render_template, session, jsonify
from backend.domain.dto.pedido_dto import AdicionarItemDTO
from backend.domain.service.pedido_service import PedidoService

class PedidoController:
    def __init__(self, pedido_service: PedidoService):
        self.pedido_service = pedido_service

    def cardapio_page(self):
        nome = session.get("usuario_nome")
        return render_template("cardapio.html", usuario=nome)

    def sobre_page(self):
        nome = session.get("usuario_nome")
        return render_template("sobre.html", usuario=nome)

    def carrinho_page(self):
        nome = session.get("usuario_nome")
        item = (request.args.get("item") or "").strip()
        if not item:
            return redirect(url_for("routes.cardapio_page"))

        valores = {
            "Calabresa": 39.90, "Mussarela": 34.90, "Quatro Queijos": 49.90,
            "Brigadeiro": 29.90, "M&M": 32.90, "Romeu & Julieta": 31.90,
            "Coxinha": 25.90, "Vulcão": 45.90, "Nutella": 37.90,
        }
        valor = valores.get(item, 29.90)
        return render_template(
            "carrinho.html",
            usuario=nome,
            item_nome=item,
            item_valor=f"{valor:.2f}".replace(".", ","),
        )

    def adicionar_item(self):
        nome = session.get("usuario_nome")
        if not nome:
            return redirect(url_for("routes.login_page"))

        item = (request.form.get("item") or "").strip()
        personalizacao = (request.form.get("personalizacao") or "").strip()
        quantidade = request.form.get("quantidade", "1").strip()

        valores = {
            "Calabresa": 39.90, "Mussarela": 34.90, "Quatro Queijos": 49.90,
            "Brigadeiro": 29.90, "M&M": 32.90, "Romeu & Julieta": 31.90,
            "Coxinha": 25.90, "Vulcão": 45.90, "Nutella": 37.90,
        }
        fotos = {
            "Calabresa": "calabresa.jpeg", "Mussarela": "mussarela.jpeg", "Quatro Queijos": "4queijos.jpg",
            "Brigadeiro": "brigadeiro.jpg", "M&M": "mem.jpg", "Romeu & Julieta": "roju.jpg",
            "Coxinha": "espcoxinha.jpg", "Vulcão": "espvulcao.jpg", "Nutella": "espnutella.jpg",
        }

        item_valor = valores.get(item, 29.90)
        item_foto = fotos.get(item, "")

        dto = AdicionarItemDTO(
            item_nome=item, item_foto=item_foto, item_valor=item_valor,
            quantidade=quantidade, observacao=personalizacao
        )
        try:
            dto.validate()  # Valida contrato do input (Single Source of Truth)
            self.pedido_service.adicionar_item(nome, dto)
        except ValueError as e:
            return jsonify({"ok": False, "erro": str(e)}), 400
        except Exception:
            return redirect(url_for("routes.login_page"))

        return redirect(url_for("routes.carrinho_page", item=item) + f"&saved=1&qtd={dto.quantidade}")

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
                "nome": it.item_nome, "foto": it.item_foto, "valor": it.item_valor,
                "quantidade": it.quantidade, "observacao": it.observacao,
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
