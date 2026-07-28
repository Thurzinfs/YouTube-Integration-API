from uuid import uuid4

from django.db import models

from django.contrib.auth.models import AbstractBaseUser

from app.accounts.infrastructure.manager import UserManager


class User(AbstractBaseUser, models.Model):
    """
    Modelo da conta do usuario
    """

    id = models.UUIDField(primary_key=True, editable=False, default=uuid4)
    name = models.CharField(max_length=190)
    email = models.EmailField(max_length=230, null=False)
    password = models.CharField(max_length=190, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    deleted_at = models.DateTimeField(null=True, default=None)
    deactive = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = ['name']

    class Meta:
        db_table = 'users'


class RefreshToken(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid4)
    user = models.ForeignKey(
        'accounts.User',
        on_delete=models.CASCADE
    )
    hash_token = models.CharField(max_length=120)
    revoked = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    expire_at = models.DateTimeField()

    class Meta:
        db_table = 'refresh_token'
