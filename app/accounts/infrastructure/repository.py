from uuid import UUID

from app.accounts.domain.entities import UserEntity
from app.accounts.infrastructure.models import User
from app.accounts.domain.repositories import IUserRepository


class UserRepository(IUserRepository):
    def save(self, user: UserEntity) -> UserEntity:
        User.objects.update_or_create(
            id=user.id,
            defaults={
                'name': user.name,
                'email': user.email,
                'password': user.password,
                'created_at': user.created_at,
                'deleted_at': user.deleted_at,
                'deactive': user.deactive,
            },
        )

        return user

    def find_by_id(self, id: UUID) -> UserEntity | None:
        try:
            return self._to_entity(User.objects.get(id=id))

        except User.DoesNotExist:
            return None

    def find_by_email(self, email: str) -> UserEntity | None:
        try:
            return self._to_entity(User.objects.get(email=email))

        except User.DoesNotExist:
            return None

    def verify_exists_email(self, email: str) -> bool:
        return User.objects.filter(email=email).exists()

    def _to_entity(self, model: User) -> UserEntity:
        return UserEntity(
            id=model.id,
            name=model.name,
            email=model.email,
            password=model.password,
            created_at=model.created_at,
            deleted_at=model.deleted_at,
            deactive=model.deactive,
        )
