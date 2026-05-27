from backend.domain.repository.usuario_repository import UsuarioRepository
from backend.infra.db import get_db

class SqliteUsuarioRepository(UsuarioRepository):
    def create_usuario(self, nome, telefone, email, cpf, endereco, referencia, senha_hash):
        with get_db() as conn:
            conn.execute(
                """INSERT INTO Usuarios (Nome, Telefone, Email, CPF, Endereco, Referencia, Senha)
                   VALUES (?, ?, ?, ?, ?, ?, ?)""",
                (nome, telefone, email, cpf, endereco, referencia, senha_hash),
            )
            conn.commit()

    def get_usuario_by_credentials(self, email, senha_hash):
        with get_db() as conn:
            return conn.execute(
                "SELECT * FROM Usuarios WHERE Email = ? AND Senha = ?",
                (email, senha_hash),
            ).fetchone()

    def get_id_by_nome(self, nome):
        with get_db() as conn:
            usuario = conn.execute("SELECT Id FROM Usuarios WHERE Nome = ?", (nome,)).fetchone()
            return usuario["Id"] if usuario else None
