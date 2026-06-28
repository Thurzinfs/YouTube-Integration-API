from passlib.context import CryptContext

from app.accounts.domain.servicies import IHashService


pwd_context = CryptContext(schemes=['bcrypt'])


class HashService(IHashService):
    def hash(self, raw_password) -> str:
        return pwd_context.hash(raw_password)

    def verify(self, raw_password: str, hash_password: str) -> bool:
        return pwd_context.verify(raw_password, hash_password)
