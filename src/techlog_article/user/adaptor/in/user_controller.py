from uuid import UUID

from fastapi import APIRouter, status, Path, Form, Body
from common.dependencies.oauth2 import CurrentUserDependency

from routers.tags import Tags

from ._schema.request import UpdateUser
from ._schema.response import UserResponse

# TODO: add dependencies
router = APIRouter(
    prefix="/user",
    tags=[Tags.user],
    responses={status.HTTP_404_NOT_FOUND: {"description": "Not Found"}},
)


# CREATE
@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user(
    username: str = Form(description="username required for usage within the app"),
    email: str = Form(description="email requiured for login"),
    password: str = Form(description="password required for login"),
    password_recheck: str = Form(
        description="rechecking whether the current password \
            is given correctly from the user"
    ),
) -> UserResponse:
    # make a DTO(CreateUser) here so that we can utilize the validators in there
    raise NotImplementedError()


@router.get("/{id}", status_code=status.HTTP_200_OK)
async def read_user_by_id(
    *, id: UUID = Path(), admin: CurrentUserDependency  # TODO: change this to admin
) -> UserResponse:
    raise NotImplementedError()


# UPDATE
@router.patch("/{id}", status_code=status.HTTP_200_OK)
async def update_user(
    *,
    id: UUID = Path(),
    data: UpdateUser = Body(
        description="data required for updating the current user info; \
            however, the email couldn't be changed"
    ),
    admin: CurrentUserDependency  # TODO: change this to admin
) -> UserResponse:
    raise NotImplementedError()


# DELETE
@router.delete("/{id}", status_code=status.HTTP_200_OK)
async def delete_user(
    *, id: UUID = Path(), admin: CurrentUserDependency
):  # TODO: change this to admin
    raise NotImplementedError()
