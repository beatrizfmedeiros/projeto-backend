from typing import List
from backend.domain.entity.pedido_item import PedidoItem

class Pedido:
    def __init__(self, id=None, usuario_id=None, status="RECEBIDO", criado_em=None,
                 endereco_entrega=None, forma_pagamento=None, valor_frete=None, total_pago=None, itens: List[PedidoItem] = None):
        self.id = id
        self.usuario_id = usuario_id
        self.status = status
        self.criado_em = criado_em
        self.endereco_entrega = endereco_entrega
        self.forma_pagamento = forma_pagamento
        self.valor_frete = valor_frete
        self.total_pago = total_pago
        self.itens = itens or []

    # Status progression sequence
    STATUS_SEQUENCE = ["RECEBIDO", "PREPARANDO", "EM_ROTA_DE_ENTREGA", "ENTREGUE"]

    def next_status(self) -> str | None:
        """Return the next status in the sequence, or None if already final."""
        try:
            idx = self.STATUS_SEQUENCE.index(self.status)
            return self.STATUS_SEQUENCE[idx + 1] if idx + 1 < len(self.STATUS_SEQUENCE) else None
        except ValueError:
            return None

    @property
    def total(self) -> float:
        """Calcula o valor total acumulado de todos os itens do pedido"""
        return sum(item.subtotal for item in self.itens)

    @property
    def total_formatado(self) -> str:
        """Formata o valor total no padrão de moeda brasileira"""
        return f"{self.total:.2f}".replace('.', ',')
