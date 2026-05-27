from abc import ABC, abstractmethod
from typing import List
from backend.domain.entity.pedido import Pedido
from backend.domain.entity.pedido_item import PedidoItem

class PedidoRepository(ABC):
    @abstractmethod
    def get_open_pedido(self, usuario_id: int) -> Pedido:
        """Busca o pedido ativo de domínio (com status 'ABERTO') do usuário"""
        pass

    @abstractmethod
    def save_pedido(self, pedido: Pedido) -> int:
        """Cria/salva um novo pedido no banco de dados e retorna o ID gerado"""
        pass

    @abstractmethod
    def save_item(self, item: PedidoItem) -> None:
        """Salva/adiciona um item ao pedido no banco de dados"""
        pass

    @abstractmethod
    def get_open_pedido_items(self, usuario_id: int) -> List[PedidoItem]:
        """Retorna todos os itens de domínio do carrinho/pedido aberto do usuário logado"""
        pass

    @abstractmethod
    def delete_item_from_open_pedido(self, pedido_item_id: int, usuario_id: int) -> None:
        """Remove um item específico do pedido aberto do usuário"""
        pass

    @abstractmethod
    def finalize_open_pedido(self, usuario_id: int) -> None:
        """Marca o pedido aberto atual do usuário como FINALIZADO"""
        pass

    @abstractmethod
    def get_finalized_pedidos(self, usuario_id: int) -> List[Pedido]:
        """Retorna todos os pedidos de domínio finalizados do usuário"""
        pass

    @abstractmethod
    def get_pedido_items(self, pedido_id: int) -> List[PedidoItem]:
        """Retorna todos os itens de domínio de um pedido específico"""
        pass
