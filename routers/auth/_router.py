from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, status, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from common.schema.auth import JWTToken
from common.dependencies.oauth2 import CurrentUserDependency
from common.schema.user import User

from routers.tags import Tags
from internal.auth import AuthService

router = APIRouter(
    prefix="/auth",
    tags=[Tags.user, Tags.auth],
    responses={status.HTTP_404_NOT_FOUND: {"description": "Not Found"}},
)


# LOGIN
@router.post("/login", status_code=status.HTTP_200_OK)
async def login(
    *,
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    auth_service: Annotated[AuthService, Depends()],
) -> JWTToken:
    verified_user = auth_service.authenticate_user(form_data)
    if not verified_user:
        raise HTTPException(
            status_code=401,
            detail="Unauthorized: Incorrect username or password",
        )

    return auth_service.create_access_token(verified_user.id)


# LOGOUT
@router.post("/logout/{id}", status_code=status.HTTP_200_OK)
async def logout(
    id: UUID,
    current_user: CurrentUserDependency,
    auth_service: Annotated[AuthService, Depends()],
) -> User:
    if current_user.id != id:
        raise HTTPException(
            status_code=403,
            detail=f"Permission denied: \
                {current_user.id} requested for a different user",
        )

    return auth_service.logout_user(id, current_user)
