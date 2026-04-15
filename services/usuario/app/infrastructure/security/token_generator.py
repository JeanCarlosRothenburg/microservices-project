from functools import lru_cache
import os
from datetime import datetime, timezone, timedelta
import jwt

PRIVATE_KEY_PATH = os.getenv("PRIVATE_KEY_PATH", "/run/secrets/private_key")


@lru_cache
def get_private_key():
    with open(PRIVATE_KEY_PATH) as file:
        return file.read()


def create_token(data: dict):
    payload = data.copy()
    payload["exp"] = datetime.now(timezone.utc) + timedelta(hours=1)

    return jwt.encode(payload, get_private_key(), algorithm="RS256")
