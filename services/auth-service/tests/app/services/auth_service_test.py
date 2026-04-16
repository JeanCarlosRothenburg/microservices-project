from unittest.mock import patch

import pytest

from app.repositories.user_repository_mock import UserRepositoryMock
from app.services.auth_service import AuthService


@pytest.fixture
def auth_service() -> AuthService:
    return AuthService(UserRepositoryMock())


# Realiza o login com um e-mail inválido
def test_login_with_invalid_email(auth_service):
    with pytest.raises(ValueError, match="E-mail inválido"):
        auth_service.login("joao@", "joao")


# Realiza o login com um usuário inexistente
def test_login_with_nonexistent_user(auth_service):
    with pytest.raises(ValueError, match="Usuário não encontrado"):
        auth_service.login("teste@gmail.com", "teste")


# Realiza o login com um usuário existente e com a senha incorreta
@patch("app.services.auth_service.create_token")
def test_login_with_existent_user_and_valid_password(token_mock, auth_service):
    token_mock.return_value = "fake_token"

    assert auth_service.login("joao@gmail.com", "joao") == "fake_token"


# Realiza o login com um usuário existente e com a senha correta
def test_login_with_existent_user_and_invalid_password(auth_service):
    with pytest.raises(ValueError, match="Dados incorretos"):
        auth_service.login("joao@gmail.com", "123")
