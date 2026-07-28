from abc import ABC, abstractmethod
from typing import Tuple

from app.accounts.domain.entities import UserEntity


class IHashService(ABC):
    def hash(self, raw_password) -> str:
        ...

    def verify(self, raw_password: str, hash_password: str) -> bool:
        ...


class IRefreshTokenService(ABC):
    @abstractmethod
    def generate_access_token(self, user: UserEntity) -> str:
        ...

    @abstractmethod
    def generate_refresh_token(self, user: UserEntity) -> Tuple[str, ...]:
        ...