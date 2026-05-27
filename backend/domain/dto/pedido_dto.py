class AdicionarItemDTO:
    def __init__(self, item_nome, quantidade, observacao):
        self.item_nome = (item_nome or "").strip()
        self.quantidade = quantidade
        self.observacao = (observacao or "").strip()

    def validate(self):
        """Valida regras puramente sintáticas da requisição do usuário"""
        if not self.item_nome:
            raise ValueError("O nome do item é obrigatório.")
        
        try:
            qty = int(self.quantidade)
            if qty < 1:
                raise ValueError()
            self.quantidade = qty
        except (ValueError, TypeError):
            raise ValueError("A quantidade de itens deve ser um número inteiro maior ou igual a 1.")
