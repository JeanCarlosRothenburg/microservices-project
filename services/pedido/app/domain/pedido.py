from dataclasses import dataclass, field
from enum import Enum


class StatusPedido(str, Enum):
    PENDENTE = "PENDENTE"
    APROVADO = "APROVADO"
    CANCELADO = "CANCELADO"


class MetodoPagamento(str, Enum):
    CARTAO_CREDITO = "CARTAO_CREDITO"
    CARTAO_DEBITO = "CARTAO_DEBITO"
    PIX = "PIX"
    BOLETO = "BOLETO"


@dataclass
class ItemPedido:
    produto_sku: str
    quantidade: int
    preco_unitario: float


@dataclass
class Pedido:
    id: str
    usuario_email: str
    itens: list[ItemPedido]
    metodo_pagamento: MetodoPagamento
    status: StatusPedido = field(default=StatusPedido.PENDENTE)

    @property
    def valor_total(self) -> float:
        return sum(i.quantidade * i.preco_unitario for i in self.itens)