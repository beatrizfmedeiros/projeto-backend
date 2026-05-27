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
    def save(self, produto: Produto) -> int:
        """Salva ou atualiza um produto no banco de dados e retorna seu ID"""
        pass
