import os
import logging
import aio_pika
from aio_pika import Connection, Channel

from .setup import setup

logger = logging.getLogger(__name__)


class RabbitMQConnection:
    def __init__(self):
        self._url = os.environ.get("RABBITMQ_URL")
        if not self._url:
            raise EnvironmentError("A constante da URL do RabbitMQ não foi encontrada!")

        self._connection: Connection | None = None
        self._channel: Channel | None = None

    async def connect(self):
        self._connection = await aio_pika.connect_robust(self._url)
        self._channel = await self._connection.channel()
        await setup(self._channel)
        logger.info("Conexão com o RabbitMQ estabelecida!")

    async def channel(self) -> Channel:
        if self._channel is None or self._channel.is_closed:
            if self._connection is None or self._connection.is_closed:
                await self.connect()
            else:
                self._channel = await self._connection.channel()
                logger.info("Novo canal aberto no RabbitMQ!")
        else:
            logger.info("Já existe um canal aberto no RabbitMQ!")

        return self._channel

    async def close(self):
        if self._channel and not self._channel.is_closed:
            await self._channel.close()
        if self._connection and not self._connection.is_closed:
            await self._connection.close()
        logger.info("Conexão com o RabbitMQ encerrada!")
