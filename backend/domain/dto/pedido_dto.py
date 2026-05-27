# Lista oficial de itens de menu da Pizzaria 404 (Menu Fechado)
VALID_MENU_ITEMS = {
    "Calabresa", "Mussarela", "Quatro Queijos",
    "Brigadeiro", "M&M", "Romeu & Julieta",
    "Coxinha", "Vulcão", "Nutella"
}

class AdicionarItemDTO:
    def __init__(self, item_nome, item_foto, item_valor, quantidade, observacao):
        self.item_nome = (item_nome or "").strip()
        self.item_foto = (item_foto or "").strip()
        self.item_valor = item_valor
        self.quantidade = quantidade
        self.observacao = (observacao or "").strip()

    def validate(self):
        """Valida se o item e a quantidade atendem às regras do cardápio e do carrinho"""
        if self.item_nome not in VALID_MENU_ITEMS:
            raise ValueError(f"O item '{self.item_nome}' não faz parte do nosso cardápio oficial.")
        
        try:
            qty = int(self.quantidade)
            if qty < 1:
                raise ValueError()
            self.quantidade = qty
        except (ValueError, TypeError):
            raise ValueError("A quantidade de itens deve ser um número inteiro maior ou igual a 1.")
