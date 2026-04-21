from sqlalchemy.orm import Session

from app.domain.produto import Produto
from app.repositories.produto_repository import ProdutoRepository
from app.infrastructure.database.produto_model import ProdutoModel


def _to_domain(model: ProdutoModel) -> Produto:
    return Produto(
        id=model.id,
        nome=model.nome,
        quantidade=model.quantidade,
        preco=model.preco,
        sku=model.sku,
    )


def _to_model(produto: Produto) -> ProdutoModel:
    return ProdutoModel(
        nome=produto.nome,
        quantidade=produto.quantidade,
        preco=produto.preco,
        sku=produto.sku,
    )


class ProdutoRepositoryPostgres(ProdutoRepository):
    _db: Session

    def __init__(self, db: Session):
        self._db = db

    def save(self, produto: Produto) -> Produto:
        model = _to_model(produto)
        self._db.add(model)
        self._db.commit()
        self._db.refresh(model)
        return _to_domain(model)

    def find_by_id(self, id: int) -> Produto | None:
        model = self._db.query(ProdutoModel).filter(
            ProdutoModel.id == id).first()
        return _to_domain(model) if model else None

    def find_by_sku(self, sku: str) -> Produto | None:
        model = self._db.query(ProdutoModel).filter(
            ProdutoModel.sku == sku).first()
        return _to_domain(model) if model else None

    def find_all(self) -> list[Produto]:
        models = self._db.query(ProdutoModel).all()
        return [_to_domain(m) for m in models]

    def update(self, produto: Produto) -> Produto:
        model = self._db.query(ProdutoModel).filter(
            ProdutoModel.id == produto.id).first()
        if not model:
            raise ValueError("Produto não encontrado")
        model.nome = produto.nome
        model.quantidade = produto.quantidade
        model.preco = produto.preco
        model.sku = produto.sku
        self._db.commit()
        self._db.refresh(model)
        return _to_domain(model)

    def delete(self, id: int) -> bool:
        model = self._db.query(ProdutoModel).filter(
            ProdutoModel.id == id).first()
        if not model:
            return False
        self._db.delete(model)
        self._db.commit()
        return True
