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
        # Create Usuarios table
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS Usuarios (
                Id INTEGER PRIMARY KEY AUTOINCREMENT,
                Nome TEXT NOT NULL,
                Telefone TEXT,
                Email TEXT NOT NULL UNIQUE,
                CPF TEXT,
                Endereco TEXT,
                Referencia TEXT,
                Senha TEXT NOT NULL,
                CriadoEm TEXT DEFAULT (datetime('now'))
            )
            """
        )

        # Ensure role column exists
        cursor = conn.execute("PRAGMA table_info(Usuarios)")
        columns = [row['name'] for row in cursor.fetchall()]
        if 'role' not in columns:
            conn.execute("ALTER TABLE Usuarios ADD COLUMN role TEXT NOT NULL DEFAULT 'user'")

        # Tabela Pedidos
        conn.execute("""
            CREATE TABLE IF NOT EXISTS Pedidos (
                Id         INTEGER PRIMARY KEY AUTOINCREMENT,
                UsuarioId INTEGER NOT NULL,
                Status    TEXT    NOT NULL DEFAULT 'RECEBIDO',
                CriadoEm   TEXT   DEFAULT (datetime('now')),
                FOREIGN KEY (UsuarioId) REFERENCES Usuarios(Id)
            )
        """
        )
        # Migration: update old statuses if present
        conn.execute("UPDATE Pedidos SET Status = 'RECEBIDO' WHERE Status = 'ABERTO'")
        conn.execute("UPDATE Pedidos SET Status = 'ENTREGUE' WHERE Status = 'FINALIZADO'")
        # Garantir colunas de congelamento no Pedido caso não existam
        cursor = conn.execute("PRAGMA table_info(Pedidos)")
        columns = [row['name'] for row in cursor.fetchall()]
        if 'EnderecoEntrega' not in columns:
            conn.execute("ALTER TABLE Pedidos ADD COLUMN EnderecoEntrega TEXT")
        if 'FormaPagamento' not in columns:
            conn.execute("ALTER TABLE Pedidos ADD COLUMN FormaPagamento TEXT")
        if 'ValorFrete' not in columns:
            conn.execute("ALTER TABLE Pedidos ADD COLUMN ValorFrete REAL")
        if 'TotalPago' not in columns:
            conn.execute("ALTER TABLE Pedidos ADD COLUMN TotalPago REAL")

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

        # Tabela Produtos
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS Produtos (
                Id INTEGER PRIMARY KEY AUTOINCREMENT,
                Nome TEXT NOT NULL UNIQUE,
                Preco REAL NOT NULL,
                Foto TEXT,
                Descricao TEXT,
                Categoria TEXT NOT NULL
            )
            """
        )

        conn.execute("DELETE FROM Produtos")
        # Garantir colunas tags e ativo na tabela Produtos caso não existam
        cursor = conn.execute("PRAGMA table_info(Produtos)")
        columns = [row['name'] for row in cursor.fetchall()]
        if 'tags' not in columns:
            conn.execute("ALTER TABLE Produtos ADD COLUMN tags TEXT")
        if 'ativo' not in columns:
            conn.execute("ALTER TABLE Produtos ADD COLUMN ativo INTEGER NOT NULL DEFAULT 1")


        # Popula produtos iniciais se a tabela estiver vazia
        cursor = conn.execute("SELECT COUNT(*) FROM Produtos")
        if cursor.fetchone()[0] == 0:
            produtos_iniciais = [
                ("Calabresa", 39.90, "calabresa.jpeg", "Calabresa, cebola e orégano", "Populares"),
                ("Mussarela", 34.90, "mussarela.jpeg", "Molho fresco e mussarela premium", "Populares"),
                ("Quatro Queijos", 49.90, "4queijos.jpg", "Quatro queijos irresistíveis", "Populares"),
                ("Brigadeiro", 29.90, "brigadeiro.jpg", "Massa crocante com brigadeiro", "Doces"),
                ("M&M", 32.90, "mem.jpg", "Chocolate branco e confeitos", "Doces"),
                ("Romeu & Julieta", 31.90, "roju.jpg", "Goiabada com queijo minas", "Doces"),
                ("Coxinha", 25.90, "espcoxinha.jpg", "Frango desfiado com catupiry", "Especiais"),
                ("Vulcão", 45.90, "espvulcao.jpg", "Borda recheada que explode de sabor", "Especiais"),
                ("Nutella", 37.90, "espnutella.jpg", "Nutella com morangos frescos", "Especiais"),
            ]
            conn.executemany(
                "INSERT INTO Produtos (Nome, Preco, Foto, Descricao, Categoria) VALUES (?, ?, ?, ?, ?)",
                produtos_iniciais
            )

        conn.commit()
