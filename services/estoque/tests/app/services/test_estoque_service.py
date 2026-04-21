import pytest
from app.services.estoque_service import EstoqueService
from app.repositories.produto_repository_mock import ProdutoRepositoryMock


@pytest.fixture
def service():
    return EstoqueService(ProdutoRepositoryMock())


# ─── RF-01: Cadastrar produto ──────────────────────────────────────────────────

class TestCadastrarProduto:
    def test_cadastra_produto_com_sucesso(self, service):
        produto = service.cadastrar_produto("Boné", 10, 39.90, "BON-001")
        assert produto.id is not None
        assert produto.nome == "Boné"
        assert produto.sku == "BON-001"

    def test_normaliza_sku_para_maiusculo(self, service):
        produto = service.cadastrar_produto("Boné", 10, 39.90, "bon-001")
        assert produto.sku == "BON-001"

    def test_remove_espacos_do_nome(self, service):
        produto = service.cadastrar_produto("  Boné  ", 10, 39.90, "BON-999")
        assert produto.nome == "Boné"

    def test_erro_nome_vazio(self, service):
        with pytest.raises(ValueError, match="Nome"):
            service.cadastrar_produto("", 10, 39.90, "BON-002")

    def test_erro_nome_apenas_espacos(self, service):
        with pytest.raises(ValueError, match="Nome"):
            service.cadastrar_produto("   ", 10, 39.90, "BON-003")

    # RN-01
    def test_erro_quantidade_negativa(self, service):
        with pytest.raises(ValueError, match="negativa"):
            service.cadastrar_produto("Boné", -1, 39.90, "BON-004")

    def test_permite_quantidade_zero(self, service):
        produto = service.cadastrar_produto("Boné", 0, 39.90, "BON-005")
        assert produto.quantidade == 0

    # RN-02
    def test_erro_preco_zero(self, service):
        with pytest.raises(ValueError, match="Preço"):
            service.cadastrar_produto("Boné", 10, 0, "BON-006")

    def test_erro_preco_negativo(self, service):
        with pytest.raises(ValueError, match="Preço"):
            service.cadastrar_produto("Boné", 10, -5.0, "BON-007")

    # RN-03
    def test_erro_sku_duplicado(self, service):
        with pytest.raises(ValueError, match="SKU"):
            service.cadastrar_produto("Outro", 5, 10.0, "CAM-AZU-001")


# ─── RF-02: Listar / buscar produtos ──────────────────────────────────────────

class TestBuscarProdutos:
    def test_lista_todos_os_produtos(self, service):
        produtos = service.listar_produtos()
        assert len(produtos) == 3

    def test_busca_produto_por_id(self, service):
        produto = service.buscar_produto(1)
        assert produto.nome == "Camiseta Azul"

    def test_erro_produto_nao_encontrado(self, service):
        with pytest.raises(ValueError, match="não encontrado"):
            service.buscar_produto(999)


# ─── RF-03: Atualizar quantidade ──────────────────────────────────────────────

class TestAtualizarQuantidade:
    def test_entrada_de_estoque(self, service):
        produto = service.atualizar_quantidade(1, 10)
        assert produto.quantidade == 60

    def test_saida_de_estoque(self, service):
        produto = service.atualizar_quantidade(1, -20)
        assert produto.quantidade == 30

    def test_zerar_estoque(self, service):
        produto = service.atualizar_quantidade(1, -50)
        assert produto.quantidade == 0

    # RN-01
    def test_erro_estoque_insuficiente(self, service):
        with pytest.raises(ValueError, match="Estoque insuficiente"):
            service.atualizar_quantidade(1, -999)

    def test_erro_produto_nao_encontrado(self, service):
        with pytest.raises(ValueError, match="não encontrado"):
            service.atualizar_quantidade(999, 10)


# ─── RF-04: Verificar disponibilidade ─────────────────────────────────────────

class TestVerificarDisponibilidade:
    def test_produto_disponivel(self, service):
        assert service.verificar_disponibilidade(1, 10) is True

    def test_produto_indisponivel_sem_estoque(self, service):
        assert service.verificar_disponibilidade(3, 1) is False

    def test_produto_indisponivel_quantidade_insuficiente(self, service):
        assert service.verificar_disponibilidade(1, 999) is False

    def test_erro_quantidade_invalida(self, service):
        with pytest.raises(ValueError, match="maior que zero"):
            service.verificar_disponibilidade(1, 0)

    def test_erro_produto_nao_encontrado(self, service):
        with pytest.raises(ValueError, match="não encontrado"):
            service.verificar_disponibilidade(999, 1)


# ─── RF-05: Remover produto ───────────────────────────────────────────────────

class TestRemoverProduto:
    def test_remove_produto_com_sucesso(self, service):
        resultado = service.remover_produto(1)
        assert resultado is True

    def test_erro_remover_produto_inexistente(self, service):
        with pytest.raises(ValueError, match="não encontrado"):
            service.remover_produto(999)


# ─── RF-06: Atualizar dados do produto ────────────────────────────────────────

class TestAtualizarProduto:
    def test_atualiza_nome(self, service):
        produto = service.atualizar_produto(1, nome="Camiseta Vermelha")
        assert produto.nome == "Camiseta Vermelha"

    def test_atualiza_preco(self, service):
        produto = service.atualizar_produto(1, preco=59.90)
        assert produto.preco == 59.90

    def test_atualiza_nome_e_preco(self, service):
        produto = service.atualizar_produto(1, nome="Nova Camiseta", preco=79.90)
        assert produto.nome == "Nova Camiseta"
        assert produto.preco == 79.90

    def test_erro_nome_vazio(self, service):
        with pytest.raises(ValueError, match="vazio"):
            service.atualizar_produto(1, nome="")

    def test_erro_preco_invalido(self, service):
        with pytest.raises(ValueError, match="Preço"):
            service.atualizar_produto(1, preco=-10.0)

    def test_erro_produto_nao_encontrado(self, service):
        with pytest.raises(ValueError, match="não encontrado"):
            service.atualizar_produto(999, nome="Teste")