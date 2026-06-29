from uuid import UUID

from app.accounts.application.dto import UserInDTO, UserOutDTO, UserUpdateDTO
from app.accounts.domain.entities import UserEntity
from app.accounts.domain.exceptions import (
    ConflictFieldException,
    UserNotFoundException,
)
from app.accounts.domain.repositories import IUserRepository
from app.accounts.domain.servicies import IHashService


class RegisterUserUseCase:
    def __init__(
        self, user_repo: IUserRepository, hash_service: IHashService
    ) -> None:
        self.user_repo = user_repo
        self.hash_service = hash_service

    def execute(self, dto: UserInDTO) -> UserOutDTO:
        if self.user_repo.find_by_email(dto.email):
            raise ConflictFieldException('email already exists')

        password_hash = self.hash_service.hash(dto.password)

        user = UserEntity(
            name=dto.name,
            email=dto.email,
            password=password_hash,
        )

        self.user_repo.save(user)

        return UserOutDTO.from_domain(user)


class ResponseUserByIdUseCase:
    def __init__(self, user_repo: IUserRepository) -> None:
        self.user_repo = user_repo

    def execute(self, id: UUID) -> UserOutDTO:
        user = self.user_repo.find_by_id(id)
        if not user:
            raise UserNotFoundException('user not found')

        return UserOutDTO.from_domain(user)


class ResponseUserByEmailUseCase:
    def __init__(self, user_repo: IUserRepository) -> None:
        self.user_repo = user_repo

    def execute(self, email: str) -> UserOutDTO:
        user = self.user_repo.find_by_email(email)
        if not user:
            raise UserNotFoundException('user not found')

        return UserOutDTO.from_domain(user)


class UpdateUserUseCase:
    def __init__(self, user_repo: IUserRepository, hash_service: IHashService) -> None:
        self.user_repo = user_repo
        self.hash_service = hash_service

    def execute(self, id: UUID, dto: UserUpdateDTO) -> UserOutDTO:
        user = self.user_repo.find_by_id(id=id)
        if not user:
            raise UserNotFoundException('user not found')
        
        if user.deactive:
            raise ConflictFieldException('user is deactivate')
        
        if dto.email:
            if self.user_repo.verify_exists_email(dto.email):
                raise ConflictFieldException('email already exists')
            
            user.change_email(dto.email)

        if dto.name:
            user.change_name(dto.name)

        if dto.password:
            password_hash = self.hash_service.hash(dto.password)

            user.change_password(password_hash)

        self.user_repo.save(user)

        return UserOutDTO.from_domain(user)


class DeactiveUserUseCase:
    def __init__(self, user_repo: IUserRepository) -> None:
        self.user_repo = user_repo

    def execute(self, id: UUID) -> UserOutDTO:
        user = self.user_repo.find_by_id(id)
        if not user:
            raise UserNotFoundException("user not found")
        
        user.deactive_user()

        self.user_repo.save(user)
        return UserOutDTO.from_domain(user)
