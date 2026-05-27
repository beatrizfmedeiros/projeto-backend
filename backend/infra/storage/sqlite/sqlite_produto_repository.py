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

    def get_all(self) -> List[Produto]:
        with get_db() as conn:
            rows = conn.execute("SELECT * FROM Produtos ORDER BY Id ASC").fetchall()
            return [SqliteProdutoModel.to_entity(r) for r in rows]

    def get_by_nome(self, nome: str) -> Produto:
        with get_db() as conn:
            row = conn.execute("SELECT * FROM Produtos WHERE Nome = ? LIMIT 1", (nome,)).fetchone()
            return SqliteProdutoModel.to_entity(row)

    def create_produto(self, produto: Produto) -> int:
        import json
        with get_db() as conn:
            cur = conn.execute(
                """INSERT OR REPLACE INTO Produtos (Nome, Preco, Foto, Descricao, Categoria, Tags, Ativo) VALUES (?, ?, ?, ?, ?, ?, ?)""",

                (
                    produto.nome,
                    float(produto.preco),
                    produto.foto,
                    produto.descricao,
                    produto.categoria,
                    json.dumps(produto.tags) if produto.tags else None,
                    1 if produto.ativo else 0,
                ),
            )
            conn.commit()
            return cur.lastrowid

    def update_produto(self, produto_id: int, produto: Produto) -> None:
        import json
        with get_db() as conn:
            conn.execute(
                """UPDATE Produtos SET Preco = ?, Foto = ?, Descricao = ?, Categoria = ?, Tags = ?, Ativo = ? WHERE Id = ?""",
                (
                    float(produto.preco),
                    produto.foto,
                    produto.descricao,
                    produto.categoria,
                    json.dumps(produto.tags) if produto.tags else None,
                    1 if produto.ativo else 0,
                    produto_id,
                ),
            )
            conn.commit()

    def delete_produto(self, produto_id: int) -> None:
        with get_db() as conn:
            conn.execute("DELETE FROM Produtos WHERE Id = ?", (produto_id,))
            conn.commit()
