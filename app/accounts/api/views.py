from uuid import UUID

from ninja import Router
from pydantic import EmailStr

from app.accounts.api.dependencies import AccountContainer
from app.accounts.api.schemas import UserIn, UserOut

from django.db.transaction import atomic

router = Router()

container = AccountContainer()


@router.post('/', response={201: UserOut})
@atomic
def create_user(request, data: UserIn):
    dto = data.to_dto()

    use_case = container.register_user_use_case()

    user = use_case.execute(dto)

    return UserOut.from_domain(user)
