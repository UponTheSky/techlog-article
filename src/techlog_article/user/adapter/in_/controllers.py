from typing import Annotated, Optional

from fastapi import APIRouter, status, Form, Depends

from src.techlog_article.common.tags import Tags
from src.techlog_article.auth import CurrentUserIdDependency

from ...application.port.in_ import (
    SignUpDTO,
    SignUpPort,
    SignOutPort,
    UpdateAccountDTO,
    UpdateAccountPort,
)
from ...application.services import SignUpService, SignOutService, UpdateAccountService

router = APIRouter(
    prefix="/user",
    tags=[Tags.user],
    responses={status.HTTP_404_NOT_FOUND: {"description": "Not Found"}},
)


@router.post("/", status_code=status.HTTP_201_CREATED)
async def sign_up(
    *,
    username: str = Form(),
    email: str = Form(),
    password: str = Form(),
    password_recheck: str = Form(),
    sign_up_port: Annotated[SignUpPort, Depends(SignUpService)]
) -> None:
    sign_up_dto = SignUpDTO(
        username=username,
        email=email,
        password=password,
        password_recheck=password_recheck,
    )

    await sign_up_port.sign_up(dto=sign_up_dto)
    return None


@router.patch("/", status_code=status.HTTP_200_OK)
async def update_user_account(
    *,
    user_id: CurrentUserIdDependency,
    username: Optional[str] = Form(default=None),
    email: Optional[str] = Form(default=None),
    password: Optional[str] = Form(default=None),
    password_recheck: Optional[str] = Form(default=None),
    update_account_port: Annotated[UpdateAccountPort, Depends(UpdateAccountService)]
) -> None:
    await update_account_port.update_account(
        user_id=user_id,
        dto=UpdateAccountDTO(
            username=username,
            email=email,
            password=password,
            password_recheck=password_recheck,
        ),
    )

    return None


@router.delete("/", status_code=status.HTTP_204_NO_CONTENT)
async def sign_out(
    *,
    user_id: CurrentUserIdDependency,
    sign_out_port: Annotated[SignOutPort, Depends(SignOutService)]
) -> None:
    await sign_out_port.sign_out(user_id=user_id)

    return None
