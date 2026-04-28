from functools import lru_cache
import os
from datetime import datetime, timezone, timedelta
import jwt

JWT_SECRET = os.getenv("JWT_SECRET")


def create_token(data: dict):
    payload = data.copy()
    payload["exp"] = datetime.now(timezone.utc) + timedelta(hours=1)

    return jwt.encode(payload, JWT_SECRET, algorithm="HS256")
