from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class UserInDTO(BaseModel):
    name: str
    email: str
    password: str


class UserOutDTO(BaseModel):
    id: UUID
    name: str
    email: str
    password: str

    created_at: datetime
    deleted_at: datetime

    deactive: bool

    @classmethod
    def from_domain(cls, model):
        return cls(
            id=model.id,
            name=model.name,
            email=model.name,
            password=model.password,
            created_at=model.created_at,
            deleted_at=model.deleted_at,
            deactive=model.deactive,
        )


class UserUpdateDTO(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None
