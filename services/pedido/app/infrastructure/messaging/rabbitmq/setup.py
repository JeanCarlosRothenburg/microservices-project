import aio_pika
from aio_pika import Channel


async def setup(channel: Channel):
    await channel.declare_exchange(
        "dlx.exchange",
        aio_pika.ExchangeType.DIRECT,
        durable=True,
    )

    # Fanout exchange: copia order.created para todas as filas inscritas
    order_exchange = await channel.declare_exchange(
        "order.created.exchange",
        aio_pika.ExchangeType.FANOUT,
        durable=True,
    )

    # Fila exclusiva do pedido-service para receber order.created (se necessário no futuro)
    order_queue = await channel.declare_queue(
        "order.created.pedido",
        durable=True,
        arguments={"x-dead-letter-exchange": "dlx.exchange"},
    )
    await order_queue.bind(order_exchange)

    # Filas que o pedido-service consome (resultados dos outros microsserviços)
    for queue_name in ["stock.reserved", "stock.reserve.failed", "payment.approved", "payment.failed"]:
        await channel.declare_queue(
            queue_name,
            durable=True,
            arguments={"x-dead-letter-exchange": "dlx.exchange"},
        )