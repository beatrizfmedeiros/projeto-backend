from abc import ABC, abstractmethod

class UsuarioRepository(ABC):
    @abstractmethod
    def create_usuario(self, nome, telefone, email, cpf, endereco, referencia, senha_hash):
        """Cadastra um novo usuário no banco de dados"""
        pass

    @abstractmethod
    def get_usuario_by_credentials(self, email, senha_hash):
        """Busca um usuário pelo email e hash da senha para fins de login"""
        pass

    @abstractmethod
    def get_id_by_nome(self, nome):
        """Obtém o Id de um usuário cadastrado pelo seu Nome"""
        pass
