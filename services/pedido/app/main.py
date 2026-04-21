import os
from fastapi import FastAPI
from app.controller.pedido_controller import router as pedido_router
from app.infrastructure.database.connection import Base, engine
import app.infrastructure.database.models

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Pedido Service")


@app.get("/health")
def health():
    return {"message": "Pedido Service funcionando 🚀"}


app.include_router(pedido_router, prefix="/pedidos", tags=["Pedidos"])

if os.getenv("DISABLE_AUTH", "false").lower() == "true":
    from app.infrastructure.security.auth_dependency import get_current_user
    app.dependency_overrides[get_current_user] = lambda: {"email": "user@email.com"}