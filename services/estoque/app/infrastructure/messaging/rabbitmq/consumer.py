import json
import logging

import aio_pika
from aio_pika import Channel, IncomingMessage

from .publisher import Publisher

logger = logging.getLogger(__name__)


class Consumer:
    def __init__(self, channel: Channel, estoque_uc):
        self._channel = channel
        self._estoque_uc = estoque_uc
        self._publisher = Publisher(channel)

    async def start(self):
        # Anterior: queue = await self._channel.get_queue("estoque.queue")
        # INFORM: Fica "escutando" mensagens da fila "order.created.pedido"
        queue = await self._channel.get_queue("order.created.pedido")

        logger.info("Estoque-Service: aguardando mensagens...")

        async with queue.iterator() as queue_iter:
            async for msg in queue_iter:
                # INFORM: Quando recebe uma mensagem que um pedido foi criado, faz o processamento
                await self._handle(msg)

    async def _handle(self, msg: IncomingMessage):
        async with msg.process(ignore_processed=True):
            try:
                body = json.loads(msg.body)
            except json.JSONDecodeError as e:
                logger.error(f"Falha ao converter o JSON recebido: {e}")
                await msg.reject(requeue=False)
                return

            try:
                output = await self._estoque_uc.update_stock(body)
            except Exception as e:
                logger.error(f"Erro ao processar estoque: {e}")
                # INFORM: Caso ocorra algum erro ao reservar os itens do estoque, envia uma mensagem na fila "estoque.failed"
                await self._publish(
                    "estoque.failed", {"order_id": body.get("order_id")}
                )
                await msg.reject(requeue=False)
                return

            try:
                # INFORM: Caso o estoque for atualizado com sucesso, envia uma mensagem na fila "estoque.reserved"
                await self._publish("estoque.reserved", output)
            except Exception as e:
                logger.error(
                    f"Erro ao publicar na fila estoque.reserved para o pedido {body.get('order_id')}: {e}"
                )
                await msg.reject(requeue=True)
                return

            await msg.ack()

    async def _publish(self, queue: str, body: dict):
        try:
            await self._publisher.publish(queue, body)
        except Exception as e:
            logger.error(f"Erro ao publicar na fila {queue}: {e}")
            raise
