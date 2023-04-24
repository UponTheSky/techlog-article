from typing import final, Optional, Annotated
from uuid import UUID

from fastapi import Depends

from application.port.out import (
    CheckUserPort,
    CreateUserDTO,
    CreateUserPort,
    DeleteUserAuthPort,
)
from domain.user import User

from ._user_repository import UserRepository
from ._user_auth_repository import UserAuthRepository


@final
class UserPersistenceAdapter(CheckUserPort, CreateUserPort):
    def __init__(self, *, user_repository: Annotated[UserRepository, Depends()]):
        self._user_repository = user_repository

    async def check_by_username(self, username: str) -> Optional[User]:
        user_orm = await self._user_repository.read_by_username(username)
        return user_orm is not None

    async def check_by_email(self, email: str) -> Optional[User]:
        user_orm = await self._user_repository.read_by_email(email)
        return user_orm is not None

    async def create_user(self, dto: CreateUserDTO) -> None:
        await self._user_repository.create_user(dto=dto)


@final
class UserAuthPersistenceAdapter(DeleteUserAuthPort):
    def __init__(
        self, *, user_auth_repository: Annotated[UserAuthRepository, Depends()]
    ):
        self._user_auth_repository = user_auth_repository

    async def delete_user_auth(self, *, user_id: UUID) -> None:
        await self._user_auth_repository.delete_user_auth(user_id=user_id)
