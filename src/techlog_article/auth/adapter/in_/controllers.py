from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, status, Depends
from fastapi.security import OAuth2PasswordRequestForm

from common.utils.jwt import JWTToken
from common.tags import Tags

from application.port.in_ import LoginPort, LoginDTO, LogoutPort
from application.services import LoginService, LogoutService, CurrentUserIdDependency

router = APIRouter(
    prefix="/auth",
    tags=[Tags.user, Tags.auth],
    responses={status.HTTP_404_NOT_FOUND: {"description": "Not Found"}},
)


@router.post("/login", status_code=status.HTTP_201_CREATED)
async def login(
    *,
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    login_service: Annotated[LoginPort, Depends(LoginService)],
) -> JWTToken:
    return await login_service.login(
        login_dto=LoginDTO(username=form_data.username, password=form_data.password)
    )


@router.post("/logout/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def logout(
    id: UUID,
    current_user_id: CurrentUserIdDependency,
    auth_service: Annotated[LogoutPort, Depends(LogoutService)],
) -> None:
    await auth_service.logout(id, current_user_id)

    return None
