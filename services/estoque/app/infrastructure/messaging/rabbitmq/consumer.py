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
        queue = await self._channel.get_queue("estoque.queue")

        logger.info("Estoque-Service: aguardando mensagens...")

        async with queue.iterator() as queue_iter:
            async for msg in queue_iter:
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
                await msg.reject(requeue=True)
                return

            try:
                await self._publisher.publish(output["status"], output)
            except Exception as e:
                logger.error(
                    f"Erro ao publicar resultado do pedido {body.get('order_id')}: {e}"
                )
                await msg.reject(requeue=True)
                return

            await msg.ack()