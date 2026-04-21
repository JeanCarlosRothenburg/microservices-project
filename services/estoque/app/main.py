from fastapi import FastAPI
from app.controller.estoque_controller import router
from app.infrastructure.database.database import engine, Base
import app.infrastructure.database.produto_model  # garante que o modelo é registrado

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Estoque Service", version="1.0.0")

app.include_router(router)


@app.get("/health")
def health():
    return {"status": "ok"}