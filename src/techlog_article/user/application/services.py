from typing import final, Annotated
from uuid import UUID

from fastapi import status as HTTPStatus, HTTPException, Depends

from src.techlog_article.common.utils.password import hash_password

from ..adapter.out.persistences import (
    UserPersistenceAdapter,
    UserAuthPersistenceAdapter,
)

from .port.in_ import (
    SignUpDTO,
    SignUpPort,
    SignOutPort,
    UpdateAccountDTO,
    UpdateAccountPort,
)
from .port.out import (
    CheckUserPort,
    CreateUserDTO,
    CreateUserAuthPort,
    UpdateUserDTO,
    UpdateUserPort,
    DeleteUserAuthPort,
)


class _HashPasswordMixin:
    @staticmethod
    def _hash_password(*, password: str) -> str:
        return hash_password(password=password)


@final
class SignUpService(SignUpPort, _HashPasswordMixin):
    def __init__(
        self,
        *,
        check_user_port: Annotated[CheckUserPort, Depends(UserPersistenceAdapter)],
        create_user_auth_port: Annotated[
            CreateUserAuthPort, Depends(UserAuthPersistenceAdapter)
        ]
    ):
        self._check_user_port = check_user_port
        self._create_user_port = create_user_auth_port

    async def sign_up(self, *, dto: SignUpDTO) -> None:
        if await self._userinfo_exists(
            check_user_port=self._check_user_port,
            username=dto.username,
            email=dto.email,
        ):
            raise HTTPException(
                status_code=HTTPStatus.HTTP_400_BAD_REQUEST,
                detail="A user with the same username or email already exists",
            )

        await self._create_user_port.create_user_with_auth(
            dto=CreateUserDTO(
                username=dto.username,
                hashed_password=self._hash_password(password=dto.password),
                email=dto.email,
            )
        )

    @staticmethod
    async def _userinfo_exists(
        *, check_user_port: CheckUserPort, username: str, email: str
    ) -> bool:
        if await check_user_port.check_exists_by_username(username):
            return True

        if await check_user_port.check_exists_by_email(email):
            return True

        return False


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
class UpdateAccountService(UpdateAccountPort, _HashPasswordMixin):
    def __init__(
        self,
        *,
        check_user_port: Annotated[CheckUserPort, Depends(UserPersistenceAdapter)],
        update_user_port: Annotated[UpdateUserPort, Depends(UserPersistenceAdapter)]
    ):
        self._check_user_port = check_user_port
        self._update_user_port = update_user_port

    async def update_account(self, *, user_id: UUID, dto: UpdateAccountDTO) -> None:
        user_in_db = await self._check_user_port.check_exists_by_id(user_id)

        if not user_in_db:
            raise HTTPException(
                status_code=HTTPStatus.HTTP_404_NOT_FOUND, detail="User not found"
            )

        dto_kwargs = dto.dict(
            exclude_unset=True, exclude={"password", "password_recheck"}
        )
        if dto.password:
            dto_kwargs.update({"hashed_password": self._hash_password(dto.password)})

        update_user_dto = UpdateUserDTO(**dto_kwargs)

        await self._update_user_port.update_user(user_id=user_id, dto=update_user_dto)

        return None
