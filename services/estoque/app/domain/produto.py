from dataclasses import dataclass


@dataclass
class Produto:
    id: int
    nome: str
    quantidade: int
    preco: float
    sku: str  # código único do produto

    def esta_disponivel(self) -> bool:
        return self.quantidade > 0

    def tem_estoque_suficiente(self, quantidade: int) -> bool:
        return self.quantidade >= quantidade