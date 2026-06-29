from uuid import UUID

from ninja import Router
from pydantic import EmailStr

from app.accounts.api.dependencies import AccountContainer
from app.accounts.api.schemas import UserIn, UserOut, UserUpdate

from django.db.transaction import atomic

from app.accounts.application.dto import UserUpdateDTO

router = Router()

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
