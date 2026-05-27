class PedidoItem:
    def __init__(self, id=None, pedido_id=None, item_nome="", item_foto="", item_valor=0.0, quantidade=1, observacao="", criado_em=None):
        self.id = id
        self.pedido_id = pedido_id
        self.item_nome = item_nome
        self.item_foto = item_foto
        self.item_valor = item_valor
        self.quantidade = quantidade
        self.observacao = observacao
        self.criado_em = criado_em

    @property
    def subtotal(self) -> float:
        """Retorna o subtotal acumulado para este item"""
        return self.item_valor * self.quantidade

    @property
    def valor_formatado(self) -> str:
        """Formata o subtotal no padrão de moeda brasileira"""
        return f"{self.subtotal:.2f}".replace('.', ',')
