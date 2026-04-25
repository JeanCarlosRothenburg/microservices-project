import os
import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.controller.pedido_controller import router as pedido_router
from app.infrastructure.database.connection import Base, engine
from app.infrastructure.messaging.rabbitmq.connection import RabbitMQConnection
from app.infrastructure.messaging.rabbitmq.consumer import Consumer
import app.infrastructure.database.models

logger = logging.getLogger(__name__)

Base.metadata.create_all(bind=engine)

rabbitmq = RabbitMQConnection()


@asynccontextmanager
async def lifespan(app: FastAPI):
    await rabbitmq.connect()
    channel = await rabbitmq.channel()
    consumer = Consumer(channel)
    await consumer.start()
    app.state.rabbitmq = rabbitmq
    yield
    await rabbitmq.close()


app = FastAPI(title="Pedido Service", lifespan=lifespan)


@app.get("/health")
def health():
    return {"message": "Pedido Service funcionando 🚀"}


app.include_router(pedido_router, prefix="/pedidos", tags=["Pedidos"])

if os.getenv("DISABLE_AUTH", "false").lower() == "true":
    from app.infrastructure.security.auth_dependency import get_current_user
    app.dependency_overrides[get_current_user] = lambda: {"email": "user@email.com"}