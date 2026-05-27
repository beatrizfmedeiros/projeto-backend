from backend.domain.repository.usuario_repository import UsuarioRepository
from backend.domain.entity.usuario import Usuario
from backend.infra.storage.sqlite.model.sqlite_usuario_model import SqliteUsuarioModel
from backend.infra.db import get_db

class SqliteUsuarioRepository(UsuarioRepository):
    def save(self, usuario: Usuario) -> None:
        with get_db() as conn:
            conn.execute(
                """INSERT INTO Usuarios (Nome, Telefone, Email, CPF, Endereco, Referencia, Senha)
                   VALUES (?, ?, ?, ?, ?, ?, ?)""",
                (usuario.nome, usuario.telefone, usuario.email, usuario.cpf, usuario.endereco, usuario.referencia, usuario.senha),
            )
            conn.commit()

    def get_by_credentials(self, email: str, senha_hash: str) -> Usuario:
        with get_db() as conn:
            row = conn.execute(
                "SELECT * FROM Usuarios WHERE Email = ? AND Senha = ?",
                (email, senha_hash),
            ).fetchone()
            return SqliteUsuarioModel.to_entity(row)

    def get_by_nome(self, nome: str) -> Usuario:
        with get_db() as conn:
            row = conn.execute("SELECT * FROM Usuarios WHERE Nome = ?", (nome,)).fetchone()
            return SqliteUsuarioModel.to_entity(row)
