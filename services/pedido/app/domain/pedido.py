from dataclasses import dataclass, field
from enum import Enum


class StatusPedido(str, Enum):
    PENDENTE = "PENDENTE"
    APROVADO = "APROVADO"
    CANCELADO = "CANCELADO"


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
    status: StatusPedido = field(default=StatusPedido.PENDENTE)

    @property
    def valor_total(self) -> float:
        return sum(i.quantidade * i.preco_unitario for i in self.itens)