from app.domain.produto import Produto
from app.repositories.produto_repository import ProdutoRepository


class EstoqueService:
    _produto_repository: ProdutoRepository

    def __init__(self, produto_repository: ProdutoRepository):
        self._produto_repository = produto_repository

    # RF-01: Cadastrar produto no estoque
    def cadastrar_produto(
        self, nome: str, quantidade: int, preco: float, sku: str
    ) -> Produto:
        if not nome or not nome.strip():
            raise ValueError("Nome do produto é obrigatório")

        # RN-01: Quantidade não pode ser negativa
        if quantidade < 0:
            raise ValueError("Quantidade não pode ser negativa")

        # RN-02: Preço deve ser maior que zero
        if preco <= 0:
            raise ValueError("Preço deve ser maior que zero")

        # RN-03: SKU deve ser único
        if self._produto_repository.find_by_sku(sku):
            raise ValueError(f"SKU '{sku}' já está cadastrado")

        produto = Produto(id=0, nome=nome.strip(), quantidade=quantidade, preco=preco, sku=sku.upper())
        return self._produto_repository.save(produto)

    # RF-02: Consultar produtos disponíveis
    def listar_produtos(self) -> list[Produto]:
        return self._produto_repository.find_all()

    def buscar_produto(self, id: int) -> Produto:
        produto = self._produto_repository.find_by_id(id)
        if not produto:
            raise ValueError("Produto não encontrado")
        return produto

    # RF-03: Atualizar quantidade em estoque (entrada/saída)
    def atualizar_quantidade(self, id: int, quantidade: int) -> Produto:
        produto = self.buscar_produto(id)

        # RN-01: Quantidade final não pode ser negativa
        nova_quantidade = produto.quantidade + quantidade
        if nova_quantidade < 0:
            raise ValueError(
                f"Estoque insuficiente. Disponível: {produto.quantidade}, solicitado: {abs(quantidade)}"
            )

        produto.quantidade = nova_quantidade
        return self._produto_repository.update(produto)

    # RF-04: Verificar disponibilidade de produto para pedido
    def verificar_disponibilidade(self, id: int, quantidade: int) -> bool:
        if quantidade <= 0:
            raise ValueError("Quantidade deve ser maior que zero")

        produto = self.buscar_produto(id)
        return produto.tem_estoque_suficiente(quantidade)

    # RF-05: Remover produto do estoque
    def remover_produto(self, id: int) -> bool:
        self.buscar_produto(id)  # valida se existe
        return self._produto_repository.delete(id)

    # RF-06: Atualizar dados do produto
    def atualizar_produto(
        self,
        id: int,
        nome: str | None = None,
        preco: float | None = None,
    ) -> Produto:
        produto = self.buscar_produto(id)

        if nome is not None:
            if not nome.strip():
                raise ValueError("Nome do produto não pode ser vazio")
            produto.nome = nome.strip()

        if preco is not None:
            if preco <= 0:
                raise ValueError("Preço deve ser maior que zero")
            produto.preco = preco

        return self._produto_repository.update(produto)