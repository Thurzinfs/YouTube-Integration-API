from typing import Any

from django.http import HttpRequest
import jwt
from ninja.security import HttpBearer, APIKeyCookie

from app.accounts.infrastructure.models import User
from config import settings
from core.exceptions import BaseDomainException


class AuthCookie(APIKeyCookie):
    param_name: str = "access_token"

    def authenticate(self, request: HttpRequest, key: str | None) -> Any | None:
        if not key:
            return None
        
        try:
            payload = jwt.decode(
                key,
                settings.JWT_SECRET_KEY,
                algorithms=[settings.JWT_ALGORITHIM]
            )
            user = User.objects.filter(id=payload['sub']).first()
            if not user:
                raise BaseDomainException('User not found')
            return user

        except jwt.PyJWTError:
            return None

auth_cookie = AuthCookie()
