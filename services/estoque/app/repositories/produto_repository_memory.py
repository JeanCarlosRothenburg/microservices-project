from app.domain.produto import Produto
from app.repositories.produto_repository import ProdutoRepository


class ProdutoRepositoryMemory(ProdutoRepository):
    _produtos: list[Produto]
    _next_id: int

    def __init__(self):
        self._produtos = []
        self._next_id = 1

    def save(self, produto: Produto) -> Produto:
        produto.id = self._next_id
        self._next_id += 1
        self._produtos.append(produto)
        return produto

    def find_by_id(self, id: int) -> Produto | None:
        return next((p for p in self._produtos if p.id == id), None)

    def find_by_sku(self, sku: str) -> Produto | None:
        return next((p for p in self._produtos if p.sku == sku), None)

    def find_all(self) -> list[Produto]:
        return list(self._produtos)

    def update(self, produto: Produto) -> Produto:
        for i, p in enumerate(self._produtos):
            if p.id == produto.id:
                self._produtos[i] = produto
                return produto
        raise ValueError("Produto não encontrado")

    def delete(self, id: int) -> bool:
        for i, p in enumerate(self._produtos):
            if p.id == id:
                self._produtos.pop(i)
                return True
        return False