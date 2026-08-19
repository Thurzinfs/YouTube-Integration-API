from uuid import UUID

from django.http import HttpResponse
from ninja import Router
from pydantic import EmailStr

from app.accounts.api.auth import auth_cookie
from app.accounts.api.dependencies import AccountContainer
from app.accounts.api.schemas import LoginIn, LoginOut, UserIn, UserOut, UserUpdate

from django.db.transaction import atomic

from app.accounts.application.dto import UserUpdateDTO
from config import settings

router = Router()

auth_router = Router()

container = AccountContainer()


@router.post('/', response={201: UserOut})
@atomic
def create_user(request, data: UserIn):
    dto = data.to_dto()

    use_case = container.register_user_use_case()

    user = use_case.execute(dto)

    return UserOut.from_domain(user)


@router.get('/{id}', response={200: UserOut})
def response_user_by_id(request, id: UUID):
    use_case = container.response_user_by_id_user_case()

    user = use_case.execute(id)

    return UserOut.from_domain(user)


@router.get('/search/by-email', response={200: UserOut})
def response_user_by_email(request, email: EmailStr):
    use_case = container.response_user_by_email_user_case()

    user = use_case.execute(email)

    return UserOut.from_domain(user)


@router.patch('/{id}', response={200: UserOut})
@atomic
def updte_user(request, id: UUID, data: UserUpdate):
    dto = data.to_dto()

    use_case = container.update_user_use_case()

    user = use_case.execute(id, dto)

    return UserOut.from_domain(user)


@router.delete('/{id}', response={200: UserOut})
@atomic
def deactive_user(request, id: UUID):
    use_case = container.deactive_user_use_case()

    user = use_case.execute(id)

    return UserOut.from_domain(user)


@auth_router.post('/login')
@atomic
def login(request, data: LoginIn):
    dto = data.to_dto()

    use_case = container.login_use_case()

    tokens = use_case.execute(dto)

    response = HttpResponse(
        content='{"detail": "Login realizado com sucesso"}',
        content_type="application/json",
        status=200
    )
    
    response.set_cookie(
        key="access_token",
        value=tokens.access_token,
        httponly=True,
        secure=True,  
        samesite="Lax", 
        max_age=settings.JWT_EXP_MINUTES * 60 * 60
    )

    response.set_cookie(
        key='refresh_token',
        value=tokens.refresh_token,
        httponly=True,
        secure=True,
        samesite="Lax",
        max_age=settings.JWT_EXP_DAYS * (24 * 60 * 60)
    )
    
    return response


@auth_router.get('/me', response={200: UserOut}, auth=auth_cookie)
def request_me(request):
    return UserOut.from_domain(request.auth)
