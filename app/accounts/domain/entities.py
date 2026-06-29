from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID, uuid4

from pydantic import EmailStr

from app.accounts.domain.exceptions import RequiredFieldException


@dataclass
class UserEntity:
    id: UUID = field(default_factory=uuid4)
    name: str = field(default='')
    email: str = field(default='')
    password: str = field(default='')

    created_at: datetime = field(default_factory=datetime.now)
    deleted_at: datetime | None = field(default=None)

    deactive: bool = field(default=False)

    def change_password(self, new_password: str) -> None:
        if not new_password:
            RequiredFieldException('new password is required')

        self.password = new_password

    def change_email(self, new_email: EmailStr):
        if not new_email:
            raise RequiredFieldException('new email is required')
        
    def change_name(self, new_name: str):
        if not new_name:
            raise RequiredFieldException("new name is required")

    def deactive_user(self) -> None:
        if self.deactive:
            raise RequiredFieldException('user already deactive')
        
        self.deleted_at = datetime.now()
        self.deactive = True
