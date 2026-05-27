from backend.domain.entity.usuario import Usuario
from backend.infra.security.cryptography import SymmetricCryptographer

cryptographer = SymmetricCryptographer()

class SqliteUsuarioModel:
    @staticmethod
    def to_entity(row) -> Usuario:
        """Converte uma linha bruta (sqlite3.Row) em uma Entidade de Domínio Usuario"""
        if not row:
            return None
        
        # Descriptografa o CPF de forma transparente ao converter para Entidade
        cpf_decrypted = cryptographer.decrypt(row["CPF"])
        
        return Usuario(
            id=row["Id"],
            nome=row["Nome"],
            telefone=row["Telefone"],
            email=row["Email"],
            cpf=cpf_decrypted,
            endereco=row["Endereco"],
            referencia=row["Referencia"],
            senha=row["Senha"],
            criado_em=row["CriadoEm"],
            role=row["role"] if "role" in row.keys() else "user"
        )
