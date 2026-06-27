from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID, uuid4

from core.exceptions import BaseDomainException


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
            BaseDomainException('new password is required')

        self.password = new_password

    def deactive_user(self) -> None:
        if self.deactive:
            BaseDomainException('user already deactive')

        self.deactive = True
