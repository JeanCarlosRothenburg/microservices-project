import json
import logging

from aio_pika import Channel, IncomingMessage

from app.repositories.pedido_repository_postgres import PedidoRepositoryPostgres
from app.infrastructure.database.connection import SessionLocal
from app.domain.pedido import StatusPedido

logger = logging.getLogger(__name__)


class Consumer:
    def __init__(self, channel: Channel):
        self._channel = channel

    async def start(self):
        queues = [
            ("stock.reserved", self._handle_stock_reserved),
            ("stock.reserve.failed", self._handle_stock_failed),
            ("payment.approved", self._handle_payment_approved),
            ("payment.failed", self._handle_payment_failed),
        ]

        for queue_name, handler in queues:
            queue = await self._channel.get_queue(queue_name)
            await queue.consume(handler)
            logger.info(f"Consumindo fila: {queue_name}")

    async def _handle_stock_reserved(self, msg: IncomingMessage):
        async with msg.process(ignore_processed=True):
            body = self._parse(msg)
            if not body:
                return
            pedido_id = body.get("order_id")
            logger.info(f"Estoque reservado para pedido {pedido_id}, aguardando pagamento...")

    async def _handle_stock_failed(self, msg: IncomingMessage):
        async with msg.process(ignore_processed=True):
            body = self._parse(msg)
            if not body:
                return
            pedido_id = body.get("order_id")
            logger.warning(f"Reserva de estoque falhou para pedido {pedido_id}, cancelando...")
            self._atualizar_status(pedido_id, StatusPedido.CANCELADO)

    async def _handle_payment_approved(self, msg: IncomingMessage):
        async with msg.process(ignore_processed=True):
            body = self._parse(msg)
            if not body:
                return
            pedido_id = body.get("order_id")
            logger.info(f"Pagamento aprovado para pedido {pedido_id}, aprovando...")
            self._atualizar_status(pedido_id, StatusPedido.APROVADO)

    async def _handle_payment_failed(self, msg: IncomingMessage):
        async with msg.process(ignore_processed=True):
            body = self._parse(msg)
            if not body:
                return
            pedido_id = body.get("order_id")
            logger.warning(f"Pagamento falhou para pedido {pedido_id}, cancelando...")
            self._atualizar_status(pedido_id, StatusPedido.CANCELADO)

    def _atualizar_status(self, pedido_id: str, novo_status: StatusPedido):
        db = SessionLocal()
        try:
            repo = PedidoRepositoryPostgres(db)
            pedido = repo.find_by_id(pedido_id)
            if pedido:
                pedido.status = novo_status
                repo.update(pedido)
                logger.info(f"Pedido {pedido_id} atualizado para {novo_status}")
            else:
                logger.error(f"Pedido {pedido_id} não encontrado no banco")
        finally:
            db.close()

    def _parse(self, msg: IncomingMessage) -> dict | None:
        try:
            return json.loads(msg.body)
        except json.JSONDecodeError as e:
            logger.error(f"Falha ao converter JSON: {e}")
            return None