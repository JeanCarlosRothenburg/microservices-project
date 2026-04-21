from app.repositories.pedido_repository import PedidoRepository


class PedidoRepositoryMemory(PedidoRepository):

    def __init__(self):
        self._pedidos = []

    def save(self, pedido):
        self._pedidos.append(pedido)
        return pedido

    def update(self, pedido):
        for i, p in enumerate(self._pedidos):
            if p.id == pedido.id:
                self._pedidos[i] = pedido
                return pedido
        return pedido

    def find_by_id(self, pedido_id):
        for pedido in self._pedidos:
            if pedido.id == pedido_id:
                return pedido
        return None

    def find_by_usuario(self, usuario_email):
        return [
            p for p in self._pedidos
            if p.usuario_email == usuario_email
        ]

    def delete(self, pedido_id):
        self._pedidos = [
            p for p in self._pedidos
            if p.id != pedido_id
        ]