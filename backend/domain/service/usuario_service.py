import hashlib
from backend.domain.entity.usuario import Usuario
from backend.domain.dto.usuario_dto import UsuarioCadastroDTO, UsuarioLoginDTO
from backend.domain.repository.usuario_repository import UsuarioRepository

class UsuarioService:
    def __init__(self, usuario_repo: UsuarioRepository):
        self.usuario_repo = usuario_repo

    def _hash_senha(self, senha: str) -> str:
        return hashlib.sha256(senha.encode()).hexdigest()

    def cadastrar(self, dto: UsuarioCadastroDTO) -> None:
        """Processa e executa o cadastro de um novo usuário de domínio"""
        senha_hash = self._hash_senha(dto.senha)
        usuario = Usuario(
            nome=dto.nome,
            telefone=dto.telefone,
            email=dto.email,
            cpf=dto.cpf,
            endereco=dto.endereco,
            referencia=dto.referencia,
            senha=senha_hash
        )
        self.usuario_repo.save(usuario)

    def autenticar(self, dto: UsuarioLoginDTO) -> Usuario:
        """Autentica o usuário validando as credenciais e retornando a entidade de domínio correspondente"""
        senha_hash = self._hash_senha(dto.senha)
        return self.usuario_repo.get_by_credentials(dto.email, senha_hash)

    def obter_por_nome(self, nome: str) -> Usuario:
        """Busca o usuário por nome na base de dados e retorna a entidade"""
        return self.usuario_repo.get_by_nome(nome)
