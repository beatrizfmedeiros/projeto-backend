class Usuario:
    def __init__(self, id=None, nome="", telefone="", email="", cpf="", endereco="", referencia="", senha="", criado_em=None, role="user"):
        self.id = id
        self.nome = nome
        self.telefone = telefone
        self.email = email
        self.cpf = cpf
        self.endereco = endereco
        self.referencia = referencia
        self.senha = senha  # Armazena a hash da senha
        self.criado_em = criado_em
        self.role = role
