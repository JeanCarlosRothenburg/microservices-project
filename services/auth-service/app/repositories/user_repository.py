from abc import ABC, abstractmethod

from app.domain.user import User


class UserRepository(ABC):

    @abstractmethod
    def save(self, user: User) -> bool:
        pass

    @abstractmethod
    def find_by_email(self, email: str) -> User:
        pass
