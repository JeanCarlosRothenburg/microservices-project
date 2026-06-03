import os
import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from prometheus_fastapi_instrumentator import Instrumentator

from app.controller.pedido_controller import router as pedido_router
from app.infrastructure.database.connection import Base, engine
from app.infrastructure.messaging.rabbitmq.connection import RabbitMQConnection
from app.infrastructure.messaging.rabbitmq.consumer import Consumer
import app.infrastructure.database.models

logger = logging.getLogger(__name__)

SWAGGER_ENABLED = os.getenv("SWAGGER_ENABLED", "true").lower() == "true"

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


app = FastAPI(
    title="Pedido Service",
    lifespan=lifespan,
    root_path="/pedidos",
    docs_url="/docs" if SWAGGER_ENABLED else None,
    redoc_url="/redoc" if SWAGGER_ENABLED else None,
    openapi_url="/openapi.json" if SWAGGER_ENABLED else None,
)

# Expõe /metrics para o Prometheus
Instrumentator().instrument(app).expose(
    app, include_in_schema=False, endpoint="/metrics"
)


@app.get("/health", include_in_schema=False)
def health():
    return {"message": "Pedido Service funcionando"}


app.include_router(pedido_router, prefix="/pedidos", tags=["Pedidos"])

if os.getenv("DISABLE_AUTH", "false").lower() == "true":
    from app.infrastructure.security.auth_dependency import get_current_user

    app.dependency_overrides[get_current_user] = lambda: {"email": "user@email.com"}
