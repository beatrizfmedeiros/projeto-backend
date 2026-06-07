from typing import List
from backend.domain.entity.pedido import Pedido
from backend.domain.entity.pedido_item import PedidoItem
from backend.domain.entity.produto import Produto
from backend.domain.dto.pedido_dto import AdicionarItemDTO
from backend.domain.repository.pedido_repository import PedidoRepository
from backend.domain.repository.usuario_repository import UsuarioRepository
from backend.domain.repository.produto_repository import ProdutoRepository

class PedidoService:
    def __init__(self, pedido_repo: PedidoRepository, usuario_repo: UsuarioRepository, produto_repo: ProdutoRepository):
        self.pedido_repo = pedido_repo
        self.usuario_repo = usuario_repo
        self.produto_repo = produto_repo

    def get_menu(self) -> List[Produto]:
        """Retrieves all products in the menu from the database"""
        return self.produto_repo.get_all()

    def get_product_by_name(self, nome: str) -> Produto:
        """Finds a product in the menu by name"""
        return self.produto_repo.get_by_name(nome)

    def add_item(self, user_name: str, dto: AdicionarItemDTO) -> None:
        """Adds an item to the cart/open order using authenticated DB data"""
        usuario = self.usuario_repo.get_by_name(user_name)
        if not usuario:
            raise ValueError("User not found.")

        # Securely fetch product data from the database
        produto = self.produto_repo.get_by_name(dto.item_nome)
        if not produto:
            raise ValueError(f"Item '{dto.item_nome}' is not in our official menu.")

        # Busca ou cria o pedido aberto
        pedido = self.pedido_repo.get_open_pedido(usuario.id)
        if not pedido:
            new_pedido = Pedido(usuario_id=usuario.id)
            pedido_id = self.pedido_repo.save_pedido(new_pedido)
        else:
            pedido_id = pedido.id

        # Adiciona item ao pedido utilizando o valor e foto autenticados pelo DB
        item = PedidoItem(
            pedido_id=pedido_id,
            item_nome=produto.nome,
            item_foto=produto.foto,
            item_valor=produto.preco,
            quantidade=dto.quantidade,
            observacao=dto.observacao
        )
        self.pedido_repo.save_item(item)

    def get_cart_items(self, user_name: str) -> List[PedidoItem]:
        """Retrieves all items in the user's cart"""
        usuario = self.usuario_repo.get_by_name(user_name)
        if not usuario:
            return []
        return self.pedido_repo.get_open_pedido_items(usuario.id)

    def remove_cart_item(self, user_name: str, pedido_item_id: int) -> None:
        """Removes an item from the user's cart"""
        usuario = self.usuario_repo.get_by_name(user_name)
        if not usuario:
            raise ValueError("User not found.")
        self.pedido_repo.delete_item_from_open_pedido(pedido_item_id, usuario.id)

    def checkout_cart(self, user_name: str, dto) -> None:
        """Finalizes the user's cart using frozen checkout data.
        Receives a DTO containing address, payment method, shipping cost, and total paid.
        """
        usuario = self.usuario_repo.get_by_name(user_name)
        if not usuario:
            raise ValueError("User not found.")
        # Business validation
        if hasattr(dto, 'validate'):
            dto.validate()
        else:
            raise ValueError('Invalid checkout DTO.')
        # Persiste os dados congelados no pedido
        self.pedido_repo.finalize_open_pedido(
            usuario.id,
            endereco_entrega=dto.endereco_entrega,
            forma_pagamento=dto.forma_pagamento,
            valor_frete=dto.valor_frete,
            total_pago=dto.total_pago,
        )

    def get_history(self, user_name: str) -> List[dict]:
        """Returns the user's finalized order history, including items for each order"""
        usuario = self.usuario_repo.get_by_name(user_name)
        if not usuario:
            return []
        pedidos = self.pedido_repo.get_finalized_pedidos(usuario.id)
        historico = []
        for pedido in pedidos:
            itens = self.pedido_repo.get_pedido_items(pedido.id)
            historico.append({
                "pedido_id": pedido.id,
                "data": pedido.criado_em,
                "status": pedido.status,
                "itens": [
                    {
                        "id": it.id,
                        "nome": it.item_nome,
                        "foto": it.item_foto,
                        "valor": float(it.item_valor),
                        "quantidade": int(it.quantidade),
                        "observacao": it.observacao,
                        "subtotal": float(it.subtotal)
                    }
                    for it in itens
                ]
            })
        return historico

