class Produto:
    def __init__(self, id=None, nome="", preco=0.0, foto="", descricao="", categoria="", tags=None, ativo=True):
        self.id = id
        self.nome = nome
        self.preco = preco
        self.foto = foto
        self.descricao = descricao
        self.categoria = categoria
        self.tags = tags if tags is not None else []
        self.ativo = ativo
