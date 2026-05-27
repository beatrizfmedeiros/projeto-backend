from typing import List
from backend.domain.entity.pedido_item import PedidoItem

class Pedido:
    def __init__(self, id=None, usuario_id=None, status="ABERTO", criado_em=None, itens: List[PedidoItem] = None):
        self.id = id
        self.usuario_id = usuario_id
        self.status = status
        self.criado_em = criado_em
        self.itens = itens or []

    @property
    def total(self) -> float:
        """Calcula o valor total acumulado de todos os itens do pedido"""
        return sum(item.subtotal for item in self.itens)

    @property
    def total_formatado(self) -> str:
        """Formata o valor total no padrão de moeda brasileira"""
        return f"{self.total:.2f}".replace('.', ',')
