class FinalizarPedidoDTO:
    def __init__(self, endereco_entrega, forma_pagamento, valor_frete, total_pago):
        self.endereco_entrega = (endereco_entrega or "").strip()
        self.forma_pagamento = (forma_pagamento or "").strip()
        self.valor_frete = valor_frete
        self.total_pago = total_pago

    def validate(self):
        """Valida as regras de negócio para finalização do pedido."""
        if not self.endereco_entrega:
            raise ValueError("O endereço de entrega é obrigatório.")
        if not self.forma_pagamento:
            raise ValueError("A forma de pagamento é obrigatória.")
        try:
            self.valor_frete = float(self.valor_frete)
        except (ValueError, TypeError):
            raise ValueError("O valor do frete deve ser numérico.")
        try:
            self.total_pago = float(self.total_pago)
        except (ValueError, TypeError):
            raise ValueError("O total pago deve ser numérico.")
