import os
import uuid

from app.domain.pedido import ItemPedido, Pedido, StatusPedido
from app.repositories.pedido_repository import PedidoRepository

if os.getenv("USE_MOCK", "true").lower() == "true":
    from app.infrastructure.http import estoque_client_mock as estoque_client
    from app.infrastructure.http import payment_client_mock as payment_client
else:
    from app.infrastructure.http import estoque_client, payment_client


class PedidoService:

    def __init__(self, repository: PedidoRepository):
        self.repository = repository

    def criar_pedido(self, usuario_email: str, itens: list[dict]) -> Pedido:
        if not itens:
            raise ValueError("O pedido deve conter ao menos 1 item")

        itens_dominio = [ItemPedido(**i) for i in itens]

        for item in itens_dominio:
            if not estoque_client.verificar_disponibilidade(item.produto_sku, item.quantidade):
                raise ValueError(f"Produto {item.produto_sku} sem estoque")

        pedido = Pedido(
            id=str(uuid.uuid4()),
            usuario_email=usuario_email,
            itens=itens_dominio,
        )

        self.repository.save(pedido)

        if os.getenv("AUTO_APPROVE", "false").lower() == "true":
            try:
                for item in pedido.itens:
                    estoque_client.reservar_estoque(item.produto_sku, item.quantidade)

                if not payment_client.processar_pagamento(pedido.id, pedido.valor_total):
                    raise Exception("Pagamento recusado")

                pedido.status = StatusPedido.APROVADO

            except Exception:
                for item in pedido.itens:
                    try:
                        estoque_client.liberar_estoque(item.produto_sku, item.quantidade)
                    except Exception:
                        pass

                pedido.status = StatusPedido.CANCELADO

        return self.repository.update(pedido)

    def cancelar_pedido(self, pedido_id: str, usuario_email: str) -> Pedido:
        pedido = self._buscar_pedido_do_usuario(pedido_id, usuario_email)

        if pedido.status not in (StatusPedido.PENDENTE, StatusPedido.APROVADO):
            raise ValueError("Pedido não pode ser cancelado no status atual")

        if pedido.status == StatusPedido.APROVADO:
            payment_client.reembolsar_pagamento(pedido.id)

        pedido.status = StatusPedido.CANCELADO
        return self.repository.update(pedido)

    def consultar_pedido(self, pedido_id: str, usuario_email: str) -> Pedido:
        return self._buscar_pedido_do_usuario(pedido_id, usuario_email)

    def listar_pedidos(self, usuario_email: str) -> list[Pedido]:
        return self.repository.find_by_usuario(usuario_email)

    def alterar_pedido(self, pedido_id: str, usuario_email: str, itens: list[dict]) -> Pedido:
        pedido = self._buscar_pedido_do_usuario(pedido_id, usuario_email)

        if pedido.status != StatusPedido.PENDENTE:
            raise ValueError("Pedido só pode ser alterado se estiver pendente")

        if not itens:
            raise ValueError("O pedido deve conter ao menos 1 item")

        novos_itens = [ItemPedido(**i) for i in itens]

        for item in novos_itens:
            if not estoque_client.verificar_disponibilidade(item.produto_sku, item.quantidade):
                raise ValueError("Item sem estoque")

        pedido.itens = novos_itens
        return self.repository.update(pedido)

    def deletar_pedido(self, pedido_id: str, usuario_email: str) -> bool:
        pedido = self._buscar_pedido_do_usuario(pedido_id, usuario_email)

        if pedido.status not in (StatusPedido.PENDENTE, StatusPedido.CANCELADO):
            raise ValueError("Pedido só pode ser deletado se estiver pendente ou cancelado")

        self.repository.delete(pedido_id)
        return True

    def _buscar_pedido_do_usuario(self, pedido_id: str, usuario_email: str) -> Pedido:
        pedido = self.repository.find_by_id(pedido_id)

        if not pedido or pedido.usuario_email != usuario_email:
            raise ValueError("Pedido não encontrado")

        return pedido