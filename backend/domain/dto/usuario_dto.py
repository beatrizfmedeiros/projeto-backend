import re

# Expressão regular padrão para validação de formato de e-mail (RFC 5322 simplificado)
EMAIL_REGEX = re.compile(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$")

class UsuarioCadastroDTO:
    def __init__(self, nome, email, senha, telefone="", cpf="", endereco="", referencia=""):
        self.nome = (nome or "").strip()
        self.email = (email or "").strip().lower()
        self.senha = senha
        self.telefone = (telefone or "").strip()
        self.cpf = (cpf or "").strip()
        self.endereco = (endereco or "").strip()
        self.referencia = (referencia or "").strip()

    def validate(self):
        """Valida se o payload de cadastro atende às regras do contrato de API"""
        if not self.nome or len(self.nome) < 3:
            raise ValueError("O nome é obrigatório e deve ter no mínimo 3 caracteres.")
        if not self.email or not EMAIL_REGEX.match(self.email):
            raise ValueError("Forneça um formato de e-mail válido.")
        if not self.senha or len(self.senha) < 6:
            raise ValueError("A senha é obrigatória e deve ter no mínimo 6 caracteres.")

class UsuarioLoginDTO:
    def __init__(self, email, senha):
        self.email = (email or "").strip().lower()
        self.senha = senha

    def validate(self):
        """Valida se o payload de login atende às regras do contrato de API"""
        if not self.email or not EMAIL_REGEX.match(self.email):
            raise ValueError("Forneça um formato de e-mail válido.")
        if not self.senha:
            raise ValueError("A senha é obrigatória.")
