from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.controller.schemas import (
    CadastrarProdutoRequest,
    AtualizarQuantidadeRequest,
    AtualizarProdutoRequest,
    ProdutoResponse,
    DisponibilidadeResponse,
)
from app.services.estoque_service import EstoqueService
from app.infrastructure.database.produto_repository_postgres import ProdutoRepositoryPostgres
from app.infrastructure.database.database import get_db
from app.infrastructure.database.database import get_db
from app.infrastructure.security.auth_dependency import get_current_user

router = APIRouter()


def get_service(db: Session = Depends(get_db)) -> EstoqueService:
    return EstoqueService(ProdutoRepositoryPostgres(db))


@router.post("/produtos", response_model=ProdutoResponse, status_code=201)
def cadastrar_produto(
    body: CadastrarProdutoRequest,
    service: EstoqueService = Depends(get_service),
    _: dict = Depends(get_current_user),
):
    try:
        produto = service.cadastrar_produto(
            nome=body.nome,
            quantidade=body.quantidade,
            preco=body.preco,
            sku=body.sku,
        )
        return ProdutoResponse(
            id=produto.id,
            nome=produto.nome,
            quantidade=produto.quantidade,
            preco=produto.preco,
            sku=produto.sku,
            disponivel=produto.esta_disponivel(),
        )
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))


@router.get("/produtos", response_model=list[ProdutoResponse])
def listar_produtos(
    service: EstoqueService = Depends(get_service),
    _: dict = Depends(get_current_user),
):
    produtos = service.listar_produtos()
    return [
        ProdutoResponse(
            id=p.id,
            nome=p.nome,
            quantidade=p.quantidade,
            preco=p.preco,
            sku=p.sku,
            disponivel=p.esta_disponivel(),
        )
        for p in produtos
    ]


@router.get("/produtos/{id}", response_model=ProdutoResponse)
def buscar_produto(
    id: int,
    service: EstoqueService = Depends(get_service),
    _: dict = Depends(get_current_user),
):
    try:
        produto = service.buscar_produto(id)
        return ProdutoResponse(
            id=produto.id,
            nome=produto.nome,
            quantidade=produto.quantidade,
            preco=produto.preco,
            sku=produto.sku,
            disponivel=produto.esta_disponivel(),
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.patch("/produtos/{id}/quantidade", response_model=ProdutoResponse)
def atualizar_quantidade(
    id: int,
    body: AtualizarQuantidadeRequest,
    service: EstoqueService = Depends(get_service),
    _: dict = Depends(get_current_user),
):
    try:
        produto = service.atualizar_quantidade(id, body.quantidade)
        return ProdutoResponse(
            id=produto.id,
            nome=produto.nome,
            quantidade=produto.quantidade,
            preco=produto.preco,
            sku=produto.sku,
            disponivel=produto.esta_disponivel(),
        )
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))


@router.get("/produtos/{id}/disponibilidade", response_model=DisponibilidadeResponse)
def verificar_disponibilidade(
    id: int,
    quantidade: int = 1,
    service: EstoqueService = Depends(get_service),
    _: dict = Depends(get_current_user),
):
    try:
        disponivel = service.verificar_disponibilidade(id, quantidade)
        produto = service.buscar_produto(id)
        return DisponibilidadeResponse(
            id=id,
            disponivel=disponivel,
            quantidade_em_estoque=produto.quantidade,
        )
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))


@router.patch("/produtos/{id}", response_model=ProdutoResponse)
def atualizar_produto(
    id: int,
    body: AtualizarProdutoRequest,
    service: EstoqueService = Depends(get_service),
    _: dict = Depends(get_current_user),
):
    try:
        produto = service.atualizar_produto(
            id, nome=body.nome, preco=body.preco)
        return ProdutoResponse(
            id=produto.id,
            nome=produto.nome,
            quantidade=produto.quantidade,
            preco=produto.preco,
            sku=produto.sku,
            disponivel=produto.esta_disponivel(),
        )
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))


@router.delete("/produtos/{id}", status_code=204)
def remover_produto(
    id: int,
    service: EstoqueService = Depends(get_service),
    _: dict = Depends(get_current_user),
):
    try:
        service.remover_produto(id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
