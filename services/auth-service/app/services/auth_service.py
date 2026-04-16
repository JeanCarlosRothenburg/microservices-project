from app.repositories.user_repository import UserRepository
from app.infrastructure.security.encrypt_service import verify_password
from email_validator import validate_email

from app.infrastructure.security.token_generator import create_token


class AuthService:
    user_repository: UserRepository

    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def login(self, email: str, password: str) -> bool:
        try:
            validate_email(email)
        except Exception as e:
            raise ValueError("E-mail inválido")

        user = self.user_repository.find_by_email(email)

        if not user:
            raise ValueError("Usuário não encontrado")

        if not verify_password(password, user.hash):
            raise ValueError("Dados incorretos")

        return create_token({"email": email})
