import json
import logging
import aio_pika
from aio_pika import Channel

logger = logging.getLogger(__name__)


class Publisher:
    def __init__(self, channel: Channel):
        self._channel = channel

    async def publish_order_created(self, body: dict):
        exchange = await self._channel.get_exchange("order.created.exchange")
        payload = json.dumps(body).encode()

        await exchange.publish(
            aio_pika.Message(
                body=payload,
                content_type="application/json",
                delivery_mode=aio_pika.DeliveryMode.PERSISTENT,
            ),
            routing_key="",  # fanout ignora routing_key
        )

        logger.info('Evento publicado no exchange "order.created.exchange"')