from backend.domain.repository.usuario_repository import UsuarioRepository
from backend.domain.entity.usuario import Usuario
from backend.infra.storage.sqlite.model.sqlite_usuario_model import SqliteUsuarioModel
from backend.infra.security.cryptography import SymmetricCryptographer
from backend.infra.db import get_db

cryptographer = SymmetricCryptographer()

class SqliteUsuarioRepository(UsuarioRepository):
    def save(self, usuario: Usuario) -> None:
        # Criptografa o CPF de forma transparente antes de persistir no SQLite
        cpf_encrypted = cryptographer.encrypt(usuario.cpf)
        
        with get_db() as conn:
            conn.execute(
                """INSERT INTO Usuarios (Nome, Telefone, Email, CPF, Endereco, Referencia, Senha, role)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                (usuario.nome, usuario.telefone, usuario.email, cpf_encrypted, usuario.endereco, usuario.referencia, usuario.senha, usuario.role),
            )
            conn.commit()

    def get_by_credentials(self, email: str, senha_hash: str) -> Usuario:
        with get_db() as conn:
            row = conn.execute(
                "SELECT * FROM Usuarios WHERE Email = ? AND Senha = ?",
                (email, senha_hash),
            ).fetchone()
            return SqliteUsuarioModel.to_entity(row)

    def get_by_name(self, nome: str) -> Usuario:
        with get_db() as conn:
            row = conn.execute("SELECT * FROM Usuarios WHERE Nome = ?", (nome,)).fetchone()
            return SqliteUsuarioModel.to_entity(row)
