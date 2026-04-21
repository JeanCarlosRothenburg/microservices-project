from abc import ABC, abstractmethod
from app.domain.produto import Produto


class ProdutoRepository(ABC):

    @abstractmethod
    def save(self, produto: Produto) -> Produto:
        pass

    @abstractmethod
    def find_by_id(self, id: int) -> Produto | None:
        pass

    @abstractmethod
    def find_by_sku(self, sku: str) -> Produto | None:
        pass

    @abstractmethod
    def find_all(self) -> list[Produto]:
        pass

    @abstractmethod
    def update(self, produto: Produto) -> Produto:
        pass

    @abstractmethod
    def delete(self, id: int) -> bool:
        pass