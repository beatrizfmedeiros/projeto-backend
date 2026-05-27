from typing import List
from backend.domain.repository.produto_repository import ProdutoRepository
from backend.domain.entity.produto import Produto
from backend.infra.storage.sqlite.model.sqlite_produto_model import SqliteProdutoModel
from backend.infra.db import get_db

class SqliteProdutoRepository(ProdutoRepository):
    def get_all(self) -> List[Produto]:
        with get_db() as conn:
            rows = conn.execute("SELECT * FROM Produtos ORDER BY Id ASC").fetchall()
            return [SqliteProdutoModel.to_entity(r) for r in rows]

    def get_by_nome(self, nome: str) -> Produto:
        with get_db() as conn:
            row = conn.execute("SELECT * FROM Produtos WHERE Nome = ? LIMIT 1", (nome,)).fetchone()
            return SqliteProdutoModel.to_entity(row)

    def save(self, produto: Produto) -> int:
        with get_db() as conn:
            cur = conn.execute(
                """INSERT INTO Produtos (Nome, Preco, Foto, Descricao, Categoria)
                   VALUES (?, ?, ?, ?, ?)""",
                (produto.nome, float(produto.preco), produto.foto, produto.descricao, produto.categoria)
            )
            conn.commit()
            return cur.lastrowid
