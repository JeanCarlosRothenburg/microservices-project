from sqlalchemy.orm import Session
from app.domain.pedido import Pedido, ItemPedido, StatusPedido
from app.infrastructure.database.models import PedidoModel, ItemPedidoModel
from app.repositories.pedido_repository import PedidoRepository


def _to_domain(model: PedidoModel) -> Pedido:
    itens = [
        ItemPedido(
            produto_sku=i.produto_sku,
            quantidade=i.quantidade,
            preco_unitario=i.preco_unitario,
        )
        for i in model.itens
    ]
    return Pedido(
        id=model.id,
        usuario_email=model.usuario_email,
        itens=itens,
        status=model.status,
        metodo_pagamento=model.metodo_pagamento,
    )


class PedidoRepositoryPostgres(PedidoRepository):

    def __init__(self, session: Session):
        self.session = session

    def save(self, pedido: Pedido) -> Pedido:
        model = PedidoModel(
            id=pedido.id,
            usuario_email=pedido.usuario_email,
            status=pedido.status,
            metodo_pagamento=pedido.metodo_pagamento,
        )
        model.itens = [
            ItemPedidoModel(
                pedido_id=pedido.id,
                produto_sku=i.produto_sku,
                quantidade=i.quantidade,
                preco_unitario=i.preco_unitario,
            )
            for i in pedido.itens
        ]
        self.session.add(model)
        self.session.commit()
        return _to_domain(model)

    def find_by_id(self, pedido_id: str) -> Pedido | None:
        model = self.session.query(PedidoModel).filter_by(id=pedido_id).first()
        return _to_domain(model) if model else None

    def find_by_usuario(self, usuario_email: str) -> list[Pedido]:
        models = (
            self.session.query(PedidoModel).filter_by(usuario_email=usuario_email).all()
        )
        return [_to_domain(m) for m in models]

    def update(self, pedido: Pedido) -> Pedido:
        model = self.session.query(PedidoModel).filter_by(id=pedido.id).first()
        model.status = pedido.status
        model.itens = [
            ItemPedidoModel(
                pedido_id=pedido.id,
                produto_sku=i.produto_sku,
                quantidade=i.quantidade,
                preco_unitario=i.preco_unitario,
            )
            for i in pedido.itens
        ]
        self.session.commit()
        return _to_domain(model)

    def delete(self, pedido_id: str):
        model = self.session.query(PedidoModel).filter_by(id=pedido_id).first()
        if model:
            self.session.delete(model)
            self.session.commit()
