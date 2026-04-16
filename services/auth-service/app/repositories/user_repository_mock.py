from app.domain.user import User
from app.repositories.user_repository import UserRepository
from tests.stubs.user_stub import get_users_stub


class UserRepositoryMock(UserRepository):
    users: list[User] = get_users_stub()

    def save(self, user):
        return True

    def find_by_email(self, email) -> User | None:
        return next((user for user in self.users if user.email == email), None)
