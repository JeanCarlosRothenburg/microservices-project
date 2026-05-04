import pytest
import jwt
import os

from app.infrastructure.security.token_generator import create_token


@pytest.fixture
def jwt_secret() -> str:
    return os.getenv("JWT_SECRET")


def test_generate_token(jwt_secret):
    payload = {"email": "teste@gmail.com"}

    token = create_token(payload)
    decoded_data = jwt.decode(token, jwt_secret, algorithms=["HS256"])
    print(decoded_data)

    assert decoded_data["email"] == payload["email"]
