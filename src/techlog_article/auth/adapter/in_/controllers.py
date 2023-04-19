from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, status, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from common.schema.auth import JWTToken
from common.dependencies.oauth2 import CurrentUserDependency
from common.tags import Tags
from common.utils import ServiceMessageTitle

from application.port.in_.login import LoginPort, LoginDTO
from application.port.in_.logout import LogoutPort
from application.services import LoginService
from techlog_article.auth.application.services import LogoutService

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
    service_message = login_service.login(
        login_dto=LoginDTO(username=form_data.username, password=form_data.password)
    )
    if service_message.title == ServiceMessageTitle.ERROR:
        raise HTTPException(
            status_code=service_message.code,
            detail=service_message.payload,
        )

    return login_service


@router.post("/logout/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def logout(
    id: UUID,
    current_user: CurrentUserDependency,
    auth_service: Annotated[LogoutPort, Depends(LogoutService)],
) -> None:
    if current_user.id != id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Permission denied: \
                {current_user.id} requested for a different user",
        )

    service_message = auth_service.logout(id, current_user)

    if service_message.title == ServiceMessageTitle.ERROR:
        raise HTTPException(
            status_code=service_message.code, detail=service_message.payload
        )

    return None
