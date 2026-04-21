import os
import httpx

ESTOQUE_URL = os.getenv("ESTOQUE_URL", "http://estoque:8000")


def verificar_disponibilidade(sku: str, quantidade: int) -> bool:
    try:
        response = httpx.get(
            f"{ESTOQUE_URL}/estoque/{sku}/disponibilidade",
            params={"quantidade": quantidade}
        )
        if response.status_code == 200:
            return response.json().get("disponivel", False)
        return False
    except httpx.RequestError:
        return False


# SAGA - reservar
def reservar_estoque(sku: str, quantidade: int) -> bool:
    try:
        response = httpx.post(
            f"{ESTOQUE_URL}/estoque/{sku}/reservar",
            json={"quantidade": quantidade}
        )
        return response.status_code == 200
    except httpx.RequestError:
        return False


# SAGA - compensação
def liberar_estoque(sku: str, quantidade: int) -> bool:
    try:
        response = httpx.post(
            f"{ESTOQUE_URL}/estoque/{sku}/liberar",
            json={"quantidade": quantidade}
        )
        return response.status_code == 200
    except httpx.RequestError:
        return False


# (opcional manter)
def atualizar_estoque(sku: str, quantidade: int) -> bool:
    try:
        response = httpx.patch(
            f"{ESTOQUE_URL}/estoque/{sku}/quantidade",
            json={"quantidade": quantidade}
        )
        return response.status_code == 200
    except httpx.RequestError:
        return False