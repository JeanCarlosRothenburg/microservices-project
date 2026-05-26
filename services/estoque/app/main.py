import asyncio
import os
from contextlib import asynccontextmanager

from fastapi import FastAPI, Depends
from fastapi.security import HTTPBearer
from prometheus_fastapi_instrumentator import Instrumentator

from app.controller.estoque_controller import router
from app.infrastructure.database.database import engine, Base, SessionLocal
import app.infrastructure.database.produto_model
from app.infrastructure.messaging.rabbitmq.connection import RabbitMQConnection
from app.infrastructure.messaging.rabbitmq.consumer import Consumer
from app.infrastructure.database.produto_repository_postgres import ProdutoRepositoryPostgres
from app.services.estoque_service import EstoqueService

# Controla se o Swagger fica habilitado (DEV=true, HOMOL=false)
SWAGGER_ENABLED = os.getenv("SWAGGER_ENABLED", "true").lower() == "true"


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    produto_repository = ProdutoRepositoryPostgres(db)
    estoque_service = EstoqueService(produto_repository)

    rabbitmq = RabbitMQConnection()
    await rabbitmq.connect()

    channel = await rabbitmq.channel()
    consumer = Consumer(channel, estoque_service)

    task = asyncio.create_task(consumer.start())

    yield

    task.cancel()
    db.close()
    await rabbitmq.close()


security = HTTPBearer()

app = FastAPI(
    title="Estoque Service",
    version="1.0.0",
    lifespan=lifespan,
    root_path="/estoque",
    dependencies=[Depends(security)],
    # Desabilita Swagger em HOMOL
    docs_url="/docs" if SWAGGER_ENABLED else None,
    redoc_url="/redoc" if SWAGGER_ENABLED else None,
    openapi_url="/openapi.json" if SWAGGER_ENABLED else None,
)

# Expõe /metrics para o Prometheus
Instrumentator().instrument(app).expose(app, include_in_schema=False)

app.include_router(router)


@app.get("/health", include_in_schema=False)
def health():
    return {"status": "ok"}
