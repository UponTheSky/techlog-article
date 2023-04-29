from typing import Annotated

from fastapi import APIRouter, status as HTTPStatus, Depends
from fastapi.security import OAuth2PasswordRequestForm

from src.techlog_article.common.utils.jwt import JWTToken
from src.techlog_article.common.tags import Tags

from ...application.port.in_ import LoginPort, LoginDTO, LogoutPort
from ...application.services import LoginService, LogoutService, CurrentUserIdDependency

router = APIRouter(
    prefix="/auth",
    tags=[Tags.user, Tags.auth],
    responses={HTTPStatus.HTTP_404_NOT_FOUND: {"description": "Not Found"}},
)


@router.post("/login", status_code=HTTPStatus.HTTP_201_CREATED)
async def login(
    *,
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    login_service: Annotated[LoginPort, Depends(LoginService)],
) -> JWTToken:
    return await login_service.login(
        login_dto=LoginDTO(username=form_data.username, password=form_data.password)
    )


@router.post("/logout", status_code=HTTPStatus.HTTP_204_NO_CONTENT)
async def logout(
    current_user_id: CurrentUserIdDependency,
    auth_service: Annotated[LogoutPort, Depends(LogoutService)],
) -> None:
    await auth_service.logout(user_id=current_user_id)

    return None
