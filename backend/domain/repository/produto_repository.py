from abc import ABC, abstractmethod
from typing import List
from backend.domain.entity.produto import Produto

class ProdutoRepository(ABC):
    @abstractmethod
    def get_all(self) -> List[Produto]:
        """Recupera todos os produtos do cardápio cadastrados no banco"""
        pass

    @abstractmethod
    def get_by_nome(self, nome: str) -> Produto:
        """Busca um produto específico pelo nome único"""
        pass

    @abstractmethod
    def create_produto(self, produto: Produto) -> int:
        """Cria um novo produto no banco de dados e retorna seu ID"""
        pass

    def update_produto(self, produto_id: int, produto: Produto) -> None:
        """Atualiza os campos de um produto existente"""
        pass

    def delete_produto(self, produto_id: int) -> None:
        """Remove o produto do banco de dados"""
        pass
