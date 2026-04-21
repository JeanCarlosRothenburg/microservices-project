from app.domain.produto import Produto


def get_produtos_stub() -> list[Produto]:
    return [
        Produto(id=1, nome="Camiseta Azul", quantidade=50, preco=49.90, sku="CAM-AZU-001"),
        Produto(id=2, nome="Calça Jeans", quantidade=30, preco=129.90, sku="CAL-JEA-001"),
        Produto(id=3, nome="Tênis Esportivo", quantidade=0, preco=299.90, sku="TEN-ESP-001"),
    ]


def get_produto_stub() -> Produto:
    return Produto(id=1, nome="Camiseta Azul", quantidade=50, preco=49.90, sku="CAM-AZU-001")


def get_produto_sem_estoque_stub() -> Produto:
    return Produto(id=3, nome="Tênis Esportivo", quantidade=0, preco=299.90, sku="TEN-ESP-001")