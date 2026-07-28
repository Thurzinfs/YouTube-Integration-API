from datetime import datetime
from typing import Optional
from uuid import UUID

from ninja import Schema
from pydantic import EmailStr

from app.accounts.application.dto import LoginInDTO, LoginOutDTO, UserInDTO, UserOutDTO, UserUpdateDTO


class UserIn(Schema):
    name: str
    email: str | EmailStr
    password: str

    def to_dto(self) -> UserInDTO:
        return UserInDTO(
            name=self.name, email=self.email, password=self.password
        )


class UserOut(Schema):
    id: UUID
    name: str
    email: str
    password: str

    created_at: datetime
    deleted_at: datetime | None

    deactive: bool

    @staticmethod
    def from_domain(dto: UserOutDTO):
        return UserOut(
            id=dto.id,
            name=dto.name,
            email=dto.email,
            password=dto.password,
            created_at=dto.created_at,
            deleted_at=dto.deleted_at,
            deactive=dto.deactive,
        )


class UserUpdate(Schema):
    name: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None

    def to_dto(self) -> UserUpdateDTO:
        return UserUpdateDTO(
            name=self.name, email=self.email, password=self.password
        )


class LoginIn(Schema):
    email: EmailStr
    password: str

    def to_dto(self) -> LoginInDTO:
        return LoginInDTO(email=str(self.email), password=self.password)


class LoginOut(Schema):
    access_token: str
    refresh_token: str

    @staticmethod
    def from_domain(dto: LoginOutDTO):
        return LoginOut(
            access_token=dto.access_token, refresh_token=dto.refresh_token
        )
