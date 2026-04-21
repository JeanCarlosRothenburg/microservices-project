import os
import httpx

PAYMENT_URL = os.getenv("PAYMENT_URL", "http://payment:8000")


def processar_pagamento(pedido_id: str, valor: float) -> bool:
    try:
        response = httpx.post(f"{PAYMENT_URL}/payments", json={"pedido_id": pedido_id, "valor": valor})
        return response.status_code == 200
    except httpx.RequestError:
        return False


def reembolsar_pagamento(pedido_id: str) -> bool:
    try:
        response = httpx.post(f"{PAYMENT_URL}/payments/{pedido_id}/refund")
        return response.status_code == 200
    except httpx.RequestError:
        return False