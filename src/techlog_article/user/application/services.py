from typing import final, Annotated
from uuid import UUID

from fastapi import status as HTTPStatus, HTTPException, Depends

from common.utils.password import hash_password
from adapter.out.persistences import UserPersistenceAdapter, UserAuthPersistenceAdapter

from .port.in_ import SignUpDTO, SignUpPort, SignOutPort
from .port.out import (
    CheckUserPort,
    CreateUserDTO,
    CreateUserPort,
    UpdateUserDTO,  # noqa: F401
    UpdateUserPort,  # noqa: F401
    DeleteUserAuthPort,
)


@final
class SignUpService(SignUpPort):
    def __init__(
        self,
        *,
        read_user_port: Annotated[CheckUserPort, Depends(UserPersistenceAdapter)],
        create_user_port: Annotated[CreateUserPort, Depends(UserPersistenceAdapter)]
    ):
        self._read_user_port = read_user_port
        self._create_user_port = create_user_port

    async def sign_up(self, *, dto: SignUpDTO) -> None:
        if await self._read_user_port.check_by_username(dto.username):
            raise HTTPException(
                status_code=HTTPStatus.HTTP_400_BAD_REQUEST,
                detail="A user with the same username already exists",
            )

        if await self._read_user_port.check_by_email(dto.email):
            raise HTTPException(
                status_code=HTTPStatus.HTTP_400_BAD_REQUEST,
                detail="A user with the same email already exists",
            )

        await self._create_user_port.create_user(
            dto=CreateUserDTO(
                username=dto.username,
                hashed_password=self._hash_password(password=dto.password),
                email=dto.email,
            )
        )

    def _hash_password(self, *, password: str) -> str:
        return hash_password(password=password)


@final
class SignOutService(SignOutPort):
    def __init__(
        self,
        delete_user_auth_port: Annotated[
            DeleteUserAuthPort, Depends(UserAuthPersistenceAdapter)
        ],
    ):
        self._delete_user_auth_port = delete_user_auth_port

    async def sign_out(self, *, user_id: UUID) -> None:
        await self._delete_user_auth_port.delete_user_auth(user_id=user_id)

        return None


@final
class UpdateAccountService:
    def __init__(self):
        ...
