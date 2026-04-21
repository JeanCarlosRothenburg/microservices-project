from pydantic import BaseModel, field_validator


class CadastrarProdutoRequest(BaseModel):
    nome: str
    quantidade: int
    preco: float
    sku: str


class AtualizarQuantidadeRequest(BaseModel):
    quantidade: int  # positivo = entrada, negativo = saída


class AtualizarProdutoRequest(BaseModel):
    nome: str | None = None
    preco: float | None = None


class ProdutoResponse(BaseModel):
    id: int
    nome: str
    quantidade: int
    preco: float
    sku: str
    disponivel: bool


class DisponibilidadeResponse(BaseModel):
    id: int
    disponivel: bool
    quantidade_em_estoque: int