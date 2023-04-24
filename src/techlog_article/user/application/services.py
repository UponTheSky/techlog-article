from typing import final, Annotated
from common.utils.password import hash_password

from fastapi import status as HTTPStatus, HTTPException, Depends

from adapter.out.persistences import UserPersistenceAdapter

from .port.in_ import SignUpDTO, SignUpPort
from .port.out import CheckUserPort, CreateUserDTO, CreateUserPort


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
class SignOutService:
    def __init__(self):
        ...


@final
class UpdateAccountService:
    def __init__(self):
        ...
