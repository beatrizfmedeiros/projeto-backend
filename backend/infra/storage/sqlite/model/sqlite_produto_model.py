import json

class SqliteProdutoModel:
    @staticmethod
    def to_entity(row) -> Produto:
        """Converte uma linha crua do SQLite em uma entidade de domínio Produto"""
        if not row:
            return None
        return Produto(
            id=row["Id"],
            nome=row["Nome"],
            preco=row["Preco"],
            foto=row["Foto"],
            descricao=row["Descricao"],
            categoria=row["Categoria"],
            tags=json.loads(row["Tags"]) if row["Tags"] else [],
            ativo=bool(row["Ativo"]) if "Ativo" in row.keys() else True
        )
