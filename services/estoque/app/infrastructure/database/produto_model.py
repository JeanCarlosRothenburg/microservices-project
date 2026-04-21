from sqlalchemy import Column, Integer, String, Float
from app.infrastructure.database.database import Base


class ProdutoModel(Base):
    __tablename__ = "produtos"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    quantidade = Column(Integer, nullable=False)
    preco = Column(Float, nullable=False)
    sku = Column(String, unique=True, nullable=False, index=True)