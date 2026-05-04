import uuid
from app.domain.pedido import ItemPedido, MetodoPagamento, Pedido, StatusPedido


def _criar_itens():
    return [ItemPedido(produto_sku="SKU-001", quantidade=2, preco_unitario=50.0)]


def get_itens_stub():
    return [{"produto_sku": "SKU-001", "quantidade": 2, "preco_unitario": 50.0}]


def get_pedido_pendente_stub() -> Pedido:
    return Pedido(
        id=str(uuid.uuid4()),
        usuario_email="user@email.com",
        itens=_criar_itens(),
        metodo_pagamento=MetodoPagamento.PIX,
        status=StatusPedido.PENDENTE,
    )


def get_pedido_aprovado_stub() -> Pedido:
    return Pedido(
        id=str(uuid.uuid4()),
        usuario_email="user@email.com",
        itens=_criar_itens(),
        metodo_pagamento=MetodoPagamento.PIX,
        status=StatusPedido.APROVADO,
    )


def get_pedido_cancelado_stub() -> Pedido:
    return Pedido(
        id=str(uuid.uuid4()),
        usuario_email="user@email.com",
        itens=_criar_itens(),
        metodo_pagamento=MetodoPagamento.PIX,
        status=StatusPedido.CANCELADO,
    )