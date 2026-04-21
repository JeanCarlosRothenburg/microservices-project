from unittest.mock import patch
import pytest

from app.domain.pedido import StatusPedido
from app.repositories.pedido_repository_memory import PedidoRepositoryMemory
from app.services.pedido_service import PedidoService
from tests.app.stubs.pedido_stub import (
    get_itens_stub,
    get_pedido_aprovado_stub,
    get_pedido_cancelado_stub,
    get_pedido_pendente_stub,
)

USUARIO = "user@email.com"
OUTRO_USUARIO = "outro@email.com"

ESTOQUE_PATCH = "app.services.pedido_service.estoque_client"
PAYMENT_PATCH = "app.services.pedido_service.payment_client"


@pytest.fixture
def service():
    return PedidoService(PedidoRepositoryMemory())


# =========================
# RF-01 / RN-02 / RN-05
# =========================

def test_criar_pedido_aprovado(service):
    with patch.dict("os.environ", {"AUTO_APPROVE": "true"}), \
         patch(ESTOQUE_PATCH) as mock_estoque, \
         patch(PAYMENT_PATCH) as mock_payment:
        mock_estoque.verificar_disponibilidade.return_value = True
        mock_payment.processar_pagamento.return_value = True

        pedido = service.criar_pedido(USUARIO, get_itens_stub())

        assert pedido.status == StatusPedido.APROVADO
        assert pedido.usuario_email == USUARIO

def test_criar_pedido_pagamento_falha_cancela(service):
    with patch.dict("os.environ", {"AUTO_APPROVE": "true"}), \
         patch(ESTOQUE_PATCH) as mock_estoque, \
         patch(PAYMENT_PATCH) as mock_payment:
        mock_estoque.verificar_disponibilidade.return_value = True
        mock_payment.processar_pagamento.return_value = False

        pedido = service.criar_pedido(USUARIO, get_itens_stub())

        assert pedido.status == StatusPedido.CANCELADO


def test_criar_pedido_sem_itens_levanta_erro(service):
    with pytest.raises(ValueError, match="ao menos 1 item"):
        service.criar_pedido(USUARIO, [])


def test_criar_pedido_sem_estoque_levanta_erro(service):
    with patch(ESTOQUE_PATCH) as mock_estoque:
        mock_estoque.verificar_disponibilidade.return_value = False

        with pytest.raises(ValueError, match="sem estoque"):
            service.criar_pedido(USUARIO, get_itens_stub())


def test_criar_pedido_multiplos_itens(service):
    itens = get_itens_stub() + get_itens_stub()

    with patch(ESTOQUE_PATCH) as mock_estoque, patch(PAYMENT_PATCH) as mock_payment:
        mock_estoque.verificar_disponibilidade.return_value = True
        mock_payment.processar_pagamento.return_value = True

        pedido = service.criar_pedido(USUARIO, itens)

        assert len(pedido.itens) == 2


# =========================
# RF-02 / RN-03
# =========================

def test_cancelar_pedido_pendente(service):
    pedido = get_pedido_pendente_stub()
    service.repository.save(pedido)

    with patch(PAYMENT_PATCH):
        resultado = service.cancelar_pedido(pedido.id, USUARIO)

    assert resultado.status == StatusPedido.CANCELADO


def test_cancelar_pedido_aprovado_solicita_reembolso(service):
    pedido = get_pedido_aprovado_stub()
    service.repository.save(pedido)

    with patch(PAYMENT_PATCH) as mock_payment:
        mock_payment.reembolsar_pagamento.return_value = True
        resultado = service.cancelar_pedido(pedido.id, USUARIO)

    assert resultado.status == StatusPedido.CANCELADO
    mock_payment.reembolsar_pagamento.assert_called_once_with(pedido.id)


def test_cancelar_pedido_ja_cancelado_levanta_erro(service):
    pedido = get_pedido_cancelado_stub()
    service.repository.save(pedido)

    with pytest.raises(ValueError):
        service.cancelar_pedido(pedido.id, USUARIO)


def test_cancelar_pedido_inexistente(service):
    with pytest.raises(ValueError):
        service.cancelar_pedido("id-invalido", USUARIO)


def test_cancelar_pedido_outro_usuario(service):
    pedido = get_pedido_pendente_stub()
    service.repository.save(pedido)

    with pytest.raises(ValueError):
        service.cancelar_pedido(pedido.id, OUTRO_USUARIO)


# =========================
# RF-03
# =========================

def test_consultar_pedido_existente(service):
    pedido = get_pedido_pendente_stub()
    service.repository.save(pedido)

    resultado = service.consultar_pedido(pedido.id, USUARIO)

    assert resultado.id == pedido.id
    assert resultado.status == StatusPedido.PENDENTE


def test_consultar_pedido_inexistente(service):
    with pytest.raises(ValueError):
        service.consultar_pedido("id-invalido", USUARIO)


def test_consultar_pedido_outro_usuario(service):
    pedido = get_pedido_pendente_stub()
    service.repository.save(pedido)

    with pytest.raises(ValueError):
        service.consultar_pedido(pedido.id, OUTRO_USUARIO)


# =========================
# RF-04
# =========================

def test_listar_pedidos_do_usuario(service):
    service.repository.save(get_pedido_pendente_stub())
    service.repository.save(get_pedido_aprovado_stub())

    pedidos = service.listar_pedidos(USUARIO)

    assert len(pedidos) == 2


def test_listar_pedidos_usuario_sem_pedidos(service):
    pedidos = service.listar_pedidos("sem@email.com")

    assert pedidos == []


def test_listar_pedidos_multiplos_usuarios(service):
    service.repository.save(get_pedido_pendente_stub())

    pedido_outro = get_pedido_pendente_stub()
    pedido_outro.usuario_email = OUTRO_USUARIO
    service.repository.save(pedido_outro)

    pedidos = service.listar_pedidos(USUARIO)

    assert len(pedidos) == 1


# =========================
# Regras extras
# =========================

def test_reembolso_falha_mesmo_assim_cancela(service):
    pedido = get_pedido_aprovado_stub()
    service.repository.save(pedido)

    with patch(PAYMENT_PATCH) as mock_payment:
        mock_payment.reembolsar_pagamento.return_value = False

        resultado = service.cancelar_pedido(pedido.id, USUARIO)

    assert resultado.status == StatusPedido.CANCELADO


def test_valor_total_calculado_corretamente():
    pedido = get_pedido_pendente_stub()

    assert pedido.valor_total == 100.0


def test_valor_total_multiplos_itens():
    pedido = get_pedido_pendente_stub()
    pedido.itens.append(pedido.itens[0])

    assert pedido.valor_total == 200.0


def test_criar_pedido_estoque_lancando_excecao(service):
    with patch(ESTOQUE_PATCH) as mock_estoque:
        mock_estoque.verificar_disponibilidade.side_effect = Exception()

        with pytest.raises(Exception):
            service.criar_pedido(USUARIO, get_itens_stub())


def test_criar_pedido_pagamento_lancando_excecao(service):
    with patch.dict("os.environ", {"AUTO_APPROVE": "true"}), \
         patch(ESTOQUE_PATCH) as mock_estoque, \
         patch(PAYMENT_PATCH) as mock_payment:
        mock_estoque.verificar_disponibilidade.return_value = True
        mock_payment.processar_pagamento.side_effect = Exception()

        pedido = service.criar_pedido(USUARIO, get_itens_stub())

        assert pedido.status == StatusPedido.CANCELADO
# =========================
# RF-05
# =========================

def test_alterar_pedido_pendente(service):
    pedido = get_pedido_pendente_stub()
    service.repository.save(pedido)

    novos_itens = get_itens_stub()

    with patch(ESTOQUE_PATCH) as mock_estoque:
        mock_estoque.verificar_disponibilidade.return_value = True

        resultado = service.alterar_pedido(
            pedido.id,
            USUARIO,
            novos_itens
        )

    assert resultado.itens[0].produto_sku == novos_itens[0]["produto_sku"]


def test_alterar_pedido_sem_itens(service):
    pedido = get_pedido_pendente_stub()
    service.repository.save(pedido)

    with pytest.raises(ValueError):
        service.alterar_pedido(pedido.id, USUARIO, [])


def test_alterar_pedido_nao_pendente(service):
    pedido = get_pedido_aprovado_stub()
    service.repository.save(pedido)

    with pytest.raises(ValueError):
        service.alterar_pedido(pedido.id, USUARIO, get_itens_stub())


def test_alterar_pedido_sem_estoque(service):
    pedido = get_pedido_pendente_stub()
    service.repository.save(pedido)

    with patch(ESTOQUE_PATCH) as mock_estoque:
        mock_estoque.verificar_disponibilidade.return_value = False

        with pytest.raises(ValueError):
            service.alterar_pedido(
                pedido.id,
                USUARIO,
                get_itens_stub()
            )


def test_alterar_pedido_outro_usuario(service):
    pedido = get_pedido_pendente_stub()
    service.repository.save(pedido)

    with pytest.raises(ValueError):
        service.alterar_pedido(
            pedido.id,
            OUTRO_USUARIO,
            get_itens_stub()
        )

# =========================
# RF-06
# =========================

def test_deletar_pedido_pendente(service):
    pedido = get_pedido_pendente_stub()
    service.repository.save(pedido)

    resultado = service.deletar_pedido(pedido.id, USUARIO)

    assert resultado is True
    assert service.repository.find_by_id(pedido.id) is None


def test_deletar_pedido_nao_pendente(service):
    pedido = get_pedido_aprovado_stub()
    service.repository.save(pedido)

    with pytest.raises(ValueError):
        service.deletar_pedido(pedido.id, USUARIO)


def test_deletar_pedido_outro_usuario(service):
    pedido = get_pedido_pendente_stub()
    service.repository.save(pedido)

    with pytest.raises(ValueError):
        service.deletar_pedido(pedido.id, OUTRO_USUARIO)


def test_deletar_pedido_inexistente(service):
    with pytest.raises(ValueError):
        service.deletar_pedido("id-invalido", USUARIO)