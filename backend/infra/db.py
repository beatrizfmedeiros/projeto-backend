import os
import sqlite3

# Define caminho do banco a partir da variável de ambiente
DB_NAME = os.environ.get("DB_NAME", "sistema.db")
backend_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

if os.path.isabs(DB_NAME):
    DB_PATH = DB_NAME
else:
    DB_PATH = os.path.join(backend_dir, DB_NAME)

def get_db():
    """Factory de conexão com o banco de dados"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Inicialização das tabelas do banco de dados"""
    with get_db() as conn:
        # Tabela Usuários
        conn.execute("""
            CREATE TABLE IF NOT EXISTS Usuarios (
                Id         INTEGER PRIMARY KEY AUTOINCREMENT,
                Nome       TEXT    NOT NULL,
                Telefone   TEXT,
                Email      TEXT    NOT NULL UNIQUE,
                CPF        TEXT,
                Endereco   TEXT,
                Referencia TEXT,
                Senha      TEXT    NOT NULL,
                CriadoEm  TEXT    DEFAULT (datetime('now'))
            )
        """)

        # Tabela Pedidos
        conn.execute("""
            CREATE TABLE IF NOT EXISTS Pedidos (
                Id         INTEGER PRIMARY KEY AUTOINCREMENT,
                UsuarioId INTEGER NOT NULL,
                Status    TEXT    NOT NULL DEFAULT 'ABERTO',
                CriadoEm   TEXT   DEFAULT (datetime('now')),
                FOREIGN KEY (UsuarioId) REFERENCES Usuarios(Id)
            )
        """)

        # Tabela Itens do Pedido
        conn.execute("""
            CREATE TABLE IF NOT EXISTS PedidoItens (
                Id         INTEGER PRIMARY KEY AUTOINCREMENT,
                PedidoId  INTEGER NOT NULL,
                ItemNome   TEXT NOT NULL,
                ItemFoto   TEXT,
                ItemValor  REAL NOT NULL,
                Quantidade INTEGER NOT NULL DEFAULT 1,
                Observacao TEXT,
                CriadoEm   TEXT DEFAULT (datetime('now')),
                FOREIGN KEY (PedidoId) REFERENCES Pedidos(Id)
            )
        """)

        conn.commit()
