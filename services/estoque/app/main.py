import asyncio
from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.controller.estoque_controller import router
from app.infrastructure.database.database import engine, Base, SessionLocal
import app.infrastructure.database.produto_model
from app.infrastructure.messaging.rabbitmq.connection import RabbitMQConnection
from app.infrastructure.messaging.rabbitmq.consumer import Consumer
from app.repositories.produto_repository import ProdutoRepository
from app.services.estoque_service import EstoqueService


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Cria tabelas no banco
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    produto_repository = ProdutoRepository(db)
    estoque_service = EstoqueService(produto_repository)

    # Conecta ao RabbitMQ
    rabbitmq = RabbitMQConnection()
    await rabbitmq.connect()

    channel = await rabbitmq.channel()
    consumer = Consumer(channel, estoque_service)

    task = asyncio.create_task(consumer.start())

    yield 
    
    task.cancel()
    db.close()
    await rabbitmq.close()


app = FastAPI(title="Estoque Service", version="1.0.0", lifespan=lifespan)

app.include_router(router)


@app.get("/health")
def health():
    return {"status": "ok"}