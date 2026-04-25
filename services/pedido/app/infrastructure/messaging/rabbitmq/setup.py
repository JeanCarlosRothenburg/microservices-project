import aio_pika
from aio_pika import Channel


async def setup(channel: Channel):
    await channel.declare_exchange(
        "dlx.exchange",
        aio_pika.ExchangeType.DIRECT,
        durable=True,
    )

    await channel.declare_queue(
        "order.created",
        durable=True,
        arguments={"x-dead-letter-exchange": "dlx.exchange"},
    )

    result_queues = [
        "stock.reserved",
        "stock.reserve.failed",
        "payment.approved",
        "payment.failed",
    ]
    for queue_name in result_queues:
        await channel.declare_queue(queue_name, durable=True)