from functools import lru_cache
import os
import jwt
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError

PUBLIC_KEY_PATH = os.getenv("PUBLIC_KEY_PATH", "/run/secrets/public_key")


@lru_cache
def get_public_key() -> str:
    with open(PUBLIC_KEY_PATH) as file:
        return file.read()


def validate_token(token: str) -> dict:
    try:
        return jwt.decode(token, get_public_key(), algorithms="RS256")
    except ExpiredSignatureError:
        raise ValueError("Token expirado")
    except InvalidTokenError:
        raise ValueError("Token inválido")