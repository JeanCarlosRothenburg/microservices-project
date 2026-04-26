from sqlalchemy import Column, String, Float, Integer, ForeignKey, Enum as SAEnum
from sqlalchemy.orm import relationship
from app.infrastructure.database.connection import Base
from app.domain.pedido import StatusPedido, MetodoPagamento


class PedidoModel(Base):
    __tablename__ = "pedidos"

    id = Column(String, primary_key=True)
    usuario_email = Column(String, nullable=False)
    status = Column(SAEnum(StatusPedido), nullable=False)
    metodo_pagamento = Column(SAEnum(MetodoPagamento), nullable=False)
    itens = relationship("ItemPedidoModel", back_populates="pedido", cascade="all, delete-orphan")


class ItemPedidoModel(Base):
    __tablename__ = "itens_pedido"

    id = Column(Integer, primary_key=True, autoincrement=True)
    pedido_id = Column(String, ForeignKey("pedidos.id"), nullable=False)  # <- estava faltando ForeignKey
    produto_sku = Column(String, nullable=False)
    quantidade = Column(Integer, nullable=False)
    preco_unitario = Column(Float, nullable=False)
    pedido = relationship("PedidoModel", back_populates="itens")