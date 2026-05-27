from typing import List
from backend.domain.entity.pedido import Pedido
from backend.domain.entity.pedido_item import PedidoItem
from backend.domain.dto.pedido_dto import AdicionarItemDTO
from backend.domain.repository.pedido_repository import PedidoRepository
from backend.domain.repository.usuario_repository import UsuarioRepository

class PedidoService:
    def __init__(self, pedido_repo: PedidoRepository, usuario_repo: UsuarioRepository):
        self.pedido_repo = pedido_repo
        self.usuario_repo = usuario_repo

    def adicionar_item(self, usuario_nome: str, dto: AdicionarItemDTO) -> None:
        """Adiciona um item ao carrinho/pedido aberto do usuário logado"""
        usuario = self.usuario_repo.get_by_nome(usuario_nome)
        if not usuario:
            raise ValueError("Usuário não encontrado.")

        # Busca ou cria o pedido aberto
        pedido = self.pedido_repo.get_open_pedido(usuario.id)
        if not pedido:
            new_pedido = Pedido(usuario_id=usuario.id)
            pedido_id = self.pedido_repo.save_pedido(new_pedido)
        else:
            pedido_id = pedido.id

        # Adiciona item ao pedido
        item = PedidoItem(
            pedido_id=pedido_id,
            item_nome=dto.item_nome,
            item_foto=dto.item_foto,
            item_valor=dto.item_valor,
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

    def finalizar_carrinho(self, usuario_nome: str) -> None:
        """Finaliza o carrinho do usuário marcando o pedido correspondente como finalizado"""
        usuario = self.usuario_repo.get_by_nome(usuario_nome)
        if not usuario:
            raise ValueError("Usuário não encontrado.")
        self.pedido_repo.finalize_open_pedido(usuario.id)
