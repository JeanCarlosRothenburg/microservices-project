import aio_pika
from aio_pika import Channel


async def setup(channel: Channel):
    # Declara a DLX (Dead Letter Exchange)
    await channel.declare_exchange(
        "dlx.exchange",
        aio_pika.ExchangeType.DIRECT,
        durable=True,
    )

    # Declara a fila principal com dead-letter-exchange
    await channel.declare_queue(
        "estoque.queue",
        durable=True,
        arguments={"x-dead-letter-exchange": "dlx.exchange"},
    )

    # Declara filas de resultado
    result_queues = ["estoque.updated", "estoque.failed"]
    for queue_name in result_queues:
        await channel.declare_queue(queue_name, durable=True)