from uuid import UUID

from app.accounts.domain.entities import RefreshTokenEntity, UserEntity
from app.accounts.infrastructure.models import RefreshToken, User
from app.accounts.domain.repositories import IRefreshTokenRepository, IUserRepository


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


class RefreshTokenRepository(IRefreshTokenRepository):
    def save(self, entity: RefreshTokenEntity) -> RefreshTokenEntity:
        RefreshToken.objects.update_or_create(
            id=entity.id,
            defaults={
                'hash_token': entity.hash_token,
                'revoked': entity.revoked,
                'user_id': entity.user,
                'created_at': entity.created_at,
                'expire_at': entity.expire_at,
            },
        )

        return entity

    def find_by_hash(self, hash: str) -> RefreshTokenEntity | None:
        try:
            return self._to_model(RefreshToken.objects.get(hash_token=hash))

        except RefreshToken.DoesNotExist:
            return None

    def revoke_all_by_user(self, user_id: UUID) -> None:
        RefreshToken.objects.filter(user=user_id).update(revoked=True)

    def _to_model(self, model: RefreshToken) -> RefreshTokenEntity:
        return RefreshTokenEntity(
            id=model.id,
            hash_token=model.hash_token,
            revoked=model.revoked,
            user=model.user.id,
            created_at=model.created_at,
            expire_at=model.expire_at,
        )
