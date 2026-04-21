from abc import ABC, abstractmethod

from app.domain.pedido import Pedido


class PedidoRepository(ABC):

    @abstractmethod
    def save(self, pedido: Pedido) -> Pedido:
        pass

    @abstractmethod
    def find_by_id(self, pedido_id: str) -> Pedido | None:
        pass

    @abstractmethod
    def find_by_usuario(self, usuario_email: str) -> list[Pedido]:
        pass

    @abstractmethod
    def update(self, pedido: Pedido) -> Pedido:
        pass

    @abstractmethod
    def delete(self, pedido_id: str) -> None:
        pass