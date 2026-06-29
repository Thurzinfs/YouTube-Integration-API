from dependency_injector import containers, providers

from app.accounts.application.use_cases import (
    DeactiveUserUseCase,
    RegisterUserUseCase,
    ResponseUserByEmailUseCase,
    ResponseUserByIdUseCase,
    UpdateUserUseCase,
)
from app.accounts.infrastructure.repository import UserRepository
from app.accounts.infrastructure.services import HashService


class AccountContainer(containers.DeclarativeContainer):
    user_repo = providers.Factory(UserRepository)

    hash_service = providers.Factory(HashService)

    register_user_use_case = providers.Factory(
        RegisterUserUseCase, user_repo=user_repo, hash_service=hash_service
    )

    response_user_by_id_user_case = providers.Factory(
        ResponseUserByIdUseCase, user_repo=user_repo
    )

    response_user_by_email_user_case = providers.Factory(
        ResponseUserByEmailUseCase, user_repo=user_repo
    )

    update_user_use_case = providers.Factory(
        UpdateUserUseCase, user_repo=user_repo, hash_service=hash_service
    )

    deactive_user_use_case = providers.Factory(
        DeactiveUserUseCase, user_repo=user_repo
    )
