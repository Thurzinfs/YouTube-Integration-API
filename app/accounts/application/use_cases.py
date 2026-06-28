from app.accounts.application.dto import UserInDTO, UserOutDTO
from app.accounts.domain.entities import UserEntity
from app.accounts.domain.exceptions import ConflictFieldException
from app.accounts.domain.repositories import IUserRepository
from app.accounts.domain.servicies import IHashService


class RegisterUserUseCase:
    def __init__(self, user_repo: IUserRepository, hash_service: IHashService) -> None:
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
