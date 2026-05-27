from backend.domain.entity.usuario import Usuario

class SqliteUsuarioModel:
    @staticmethod
    def to_entity(row) -> Usuario:
        """Converte uma linha bruta (sqlite3.Row) em uma Entidade de Domínio Usuario"""
        if not row:
            return None
        return Usuario(
            id=row["Id"],
            nome=row["Nome"],
            telefone=row["Telefone"],
            email=row["Email"],
            cpf=row["CPF"],
            endereco=row["Endereco"],
            referencia=row["Referencia"],
            senha=row["Senha"],
            criado_em=row["CriadoEm"]
        )
