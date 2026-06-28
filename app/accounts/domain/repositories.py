from abc import ABC, abstractmethod
from uuid import UUID

from app.accounts.domain.entities import UserEntity


class IUserRepository(ABC):
    @abstractmethod
    def save(self, user: UserEntity) -> UserEntity:
        ...

    @abstractmethod
    def find_by_id(self, id: UUID) -> UserEntity | None:
        ...

    @abstractmethod
    def find_by_email(self, email: str) -> UserEntity | None:
        ...

    @abstractmethod
    def verify_exists_email(self, email: str) -> bool:
        ...
    