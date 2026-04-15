from app.infrastructure.security.encrypt_service import encrypt_password
from app.domain.user import User


def get_users_stub():
    return [
        User(1, "João Stub", "joao@gmail.com", encrypt_password("joao")),
        User(1, "Maria Stub", "maria@gmail.com", encrypt_password("maria")),
    ]
