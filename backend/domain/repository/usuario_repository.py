from abc import ABC, abstractmethod
from backend.domain.entity.usuario import Usuario

class UsuarioRepository(ABC):
    @abstractmethod
    def save(self, usuario: Usuario) -> None:
        """Cadastra ou salva um usuário de domínio no banco de dados"""
        pass

    @abstractmethod
    def get_by_credentials(self, email: str, senha_hash: str) -> Usuario:
        """Busca um usuário de domínio pelo email e hash da senha para fins de login"""
        pass

    @abstractmethod
    def get_by_name(self, nome: str) -> Usuario:
        """Obtém o usuário de domínio cadastrado pelo seu Nome"""
        pass
