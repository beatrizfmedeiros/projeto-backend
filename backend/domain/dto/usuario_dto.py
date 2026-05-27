class UsuarioCadastroDTO:
    def __init__(self, nome, email, senha, telefone="", cpf="", endereco="", referencia=""):
        self.nome = nome
        self.email = email
        self.senha = senha
        self.telefone = telefone
        self.cpf = cpf
        self.endereco = endereco
        self.referencia = referencia

class UsuarioLoginDTO:
    def __init__(self, email, senha):
        self.email = email
        self.senha = senha
