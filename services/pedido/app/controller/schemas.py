from pydantic import BaseModel


class ItemPedidoRequest(BaseModel):
    produto_sku: str
    quantidade: int
    preco_unitario: float


class CriarPedidoRequest(BaseModel):
    itens: list[ItemPedidoRequest]


class ItemPedidoResponse(BaseModel):
    produto_sku: str
    quantidade: int
    preco_unitario: float


class PedidoResponse(BaseModel):
    id: str
    usuario_email: str
    itens: list[ItemPedidoResponse]
    status: str
    valor_total: float