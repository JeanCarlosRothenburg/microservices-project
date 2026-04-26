from pydantic import BaseModel
from app.domain.pedido import MetodoPagamento


class ItemPedidoRequest(BaseModel):
    produto_sku: str
    quantidade: int
    preco_unitario: float


class CriarPedidoRequest(BaseModel):
    metodo_pagamento: MetodoPagamento
    itens: list[ItemPedidoRequest]


class ItemPedidoResponse(BaseModel):
    produto_sku: str
    quantidade: int
    preco_unitario: float


class PedidoResponse(BaseModel):
    id: str
    usuario_email: str
    metodo_pagamento: str
    itens: list[ItemPedidoResponse]
    status: str
    valor_total: float