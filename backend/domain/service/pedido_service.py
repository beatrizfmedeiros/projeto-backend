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

    def obter_cardapio(self) -> List[Produto]:
        """Obtém todos os produtos cadastrados no cardápio do banco de dados"""
        return self.produto_repo.get_all()

    def obter_produto_por_nome(self, nome: str) -> Produto:
        """Busca um produto do cardápio pelo nome"""
        return self.produto_repo.get_by_nome(nome)

    def adicionar_item(self, usuario_nome: str, dto: AdicionarItemDTO) -> None:
        """Adiciona um item ao carrinho/pedido aberto obtendo dados autênticos do DB"""
        usuario = self.usuario_repo.get_by_nome(usuario_nome)
        if not usuario:
            raise ValueError("Usuário não encontrado.")

        # Busca dados do produto no banco de dados para segurança
        produto = self.produto_repo.get_by_nome(dto.item_nome)
        if not produto:
            raise ValueError(f"O item '{dto.item_nome}' não faz parte do nosso cardápio oficial.")

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

    def obter_itens_carrinho(self, usuario_nome: str) -> List[PedidoItem]:
        """Obtém todos os itens do carrinho do usuário"""
        usuario = self.usuario_repo.get_by_nome(usuario_nome)
        if not usuario:
            return []
        return self.pedido_repo.get_open_pedido_items(usuario.id)

    def remover_item_carrinho(self, usuario_nome: str, pedido_item_id: int) -> None:
        """Remove um item do carrinho do usuário"""
        usuario = self.usuario_repo.get_by_nome(usuario_nome)
        if not usuario:
            raise ValueError("Usuário não encontrado.")
        self.pedido_repo.delete_item_from_open_pedido(pedido_item_id, usuario.id)

    def finalizar_carrinho(self, usuario_nome: str, dto) -> None:
        """Finaliza o carrinho do usuário usando dados de checkout congelados.
        Recebe um DTO contendo endereço, forma de pagamento, valor do frete e total pago.
        """
        usuario = self.usuario_repo.get_by_nome(usuario_nome)
        if not usuario:
            raise ValueError("Usuário não encontrado.")
        # Validação de negócio
        if hasattr(dto, 'validate'):
            dto.validate()
        else:
            raise ValueError('DTO de finalização inválido.')
        # Persiste os dados congelados no pedido
        self.pedido_repo.finalize_open_pedido(
            usuario.id,
            endereco_entrega=dto.endereco_entrega,
            forma_pagamento=dto.forma_pagamento,
            valor_frete=dto.valor_frete,
            total_pago=dto.total_pago,
        )

    def obter_historico(self, usuario_nome: str) -> List[dict]:
        """Retorna o histórico de pedidos finalizados do usuário, incluindo itens de cada pedido"""
        usuario = self.usuario_repo.get_by_nome(usuario_nome)
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

