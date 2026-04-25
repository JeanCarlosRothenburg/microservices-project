import json
import logging
import aio_pika
from aio_pika import Channel

logger = logging.getLogger(__name__)


class Publisher:
    def __init__(self, channel: Channel):
        self._channel = channel

    async def publish(self, queue: str, body: dict):
        payload = json.dumps(body).encode()

        await self._channel.default_exchange.publish(
            aio_pika.Message(
                body=payload,
                content_type="application/json",
                delivery_mode=aio_pika.DeliveryMode.PERSISTENT,
            ),
            routing_key=queue,
        )

        logger.info(f'Evento publicado na fila "{queue}"')