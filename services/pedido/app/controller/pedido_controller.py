from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session

from app.controller.schemas import CriarPedidoRequest, PedidoResponse
from app.infrastructure.database.connection import SessionLocal
from app.infrastructure.messaging.rabbitmq.publisher import Publisher
from app.infrastructure.security.auth_dependency import get_current_user
from app.repositories.pedido_repository_postgres import PedidoRepositoryPostgres
from app.services.pedido_service import PedidoService

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_service(db: Session = Depends(get_db)) -> PedidoService:
    return PedidoService(PedidoRepositoryPostgres(db))


def _to_response(pedido) -> PedidoResponse:
    return PedidoResponse(
        id=pedido.id,
        usuario_email=pedido.usuario_email,
        itens=[{"produto_sku": i.produto_sku, "quantidade": i.quantidade, "preco_unitario": i.preco_unitario} for i in pedido.itens],
        status=pedido.status,
        valor_total=pedido.valor_total,
    )


@router.post("/", response_model=PedidoResponse, status_code=201)
async def criar_pedido(
    request: Request,
    body: CriarPedidoRequest,
    user: dict = Depends(get_current_user),
    service: PedidoService = Depends(get_service),
):
    try:
        itens = [i.model_dump() for i in body.itens]
        pedido = service.criar_pedido(user["email"], itens, body.metodo_pagamento)

        rabbitmq = request.app.state.rabbitmq
        channel = await rabbitmq.channel()
        publisher = Publisher(channel)
        await publisher.publish_order_created({
            "order_id": pedido.id,
            "usuario_email": pedido.usuario_email,
            "metodo_pagamento": pedido.metodo_pagamento,
            "valor_total": pedido.valor_total,
            "itens": itens,
        })

        return _to_response(pedido)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.patch("/{pedido_id}/cancelar", response_model=PedidoResponse)
def cancelar_pedido(pedido_id: str, user: dict = Depends(get_current_user), service: PedidoService = Depends(get_service)):
    try:
        pedido = service.cancelar_pedido(pedido_id, user["email"])
        return _to_response(pedido)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{pedido_id}", response_model=PedidoResponse)
def consultar_pedido(pedido_id: str, user: dict = Depends(get_current_user), service: PedidoService = Depends(get_service)):
    try:
        pedido = service.consultar_pedido(pedido_id, user["email"])
        return _to_response(pedido)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/", response_model=list[PedidoResponse])
def listar_pedidos(user: dict = Depends(get_current_user), service: PedidoService = Depends(get_service)):
    pedidos = service.listar_pedidos(user["email"])
    return [_to_response(p) for p in pedidos]


@router.patch("/{pedido_id}", response_model=PedidoResponse)
def alterar_pedido(pedido_id: str, request: CriarPedidoRequest, user: dict = Depends(get_current_user), service: PedidoService = Depends(get_service)):
    try:
        pedido = service.alterar_pedido(pedido_id, user["email"], [i.model_dump() for i in request.itens])
        return _to_response(pedido)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{pedido_id}")
def deletar_pedido(pedido_id: str, user: dict = Depends(get_current_user), service: PedidoService = Depends(get_service)):
    try:
        service.deletar_pedido(pedido_id, user["email"])
        return {"message": "Pedido deletado com sucesso"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))