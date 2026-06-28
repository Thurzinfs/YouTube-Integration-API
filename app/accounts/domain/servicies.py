from abc import ABC


class IHashService(ABC):
    def hash(self, raw_password) -> str:
        ...

    def verify(self, raw_password: str, hash_password: str) -> bool:
        ...
