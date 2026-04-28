from functools import lru_cache
import os
import jwt
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError

JWT_SECRET = os.getenv("JWT_SECRET")

def validate_token(token: str) -> dict:
    try:
        return jwt.decode(token, JWT_SECRET, algorithms="HS256")
    except ExpiredSignatureError:
        raise ValueError("Token expirado")
    except InvalidTokenError:
        raise ValueError("Token inválido")