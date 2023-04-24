from typing import Annotated

from fastapi import APIRouter, status, Path, Form, Body, Depends  # noqa: F401

from common.tags import Tags
from auth.application.services import CurrentUserIdDependency  # noqa: F401

from application.port.in_ import SignUpDTO, SignUpPort, SignOutPort
from application.services import SignUpService, SignOutService

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


# @router.patch("/{id}", status_code=status.HTTP_200_OK)
# async def update_user(
#     *,
#     id: UUID = Path(),
#     data: UpdateUser = Body(
#         description="data required for updating the current user info; \
#             however, the email couldn't be changed"
#     ),
#     admin: CurrentUserDependency  # TODO: change this to admin
# ) -> UserResponse:
#     raise NotImplementedError()


@router.delete("/", status_code=status.HTTP_204_NO_CONTENT)
async def sign_out(
    *,
    user_id: CurrentUserIdDependency,
    sign_out_port: Annotated[SignOutPort, Depends(SignOutService)]
) -> None:
    await sign_out_port.sign_out(user_id=user_id)

    return None
