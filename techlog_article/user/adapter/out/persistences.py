from typing import final, Annotated
from uuid import UUID

from fastapi import Depends

from ...application.port.out import (
    CheckUserPort,
    CreateUserDTO,
    CreateUserAuthPort,
    DeleteUserAuthPort,
    UpdateUserDTO,
    UpdateUserPort,
)

from ._user_repository import UserRepository
from ._user_auth_repository import UserAuthRepository


@final
class UserPersistenceAdapter(CheckUserPort, UpdateUserPort):
    def __init__(self, *, user_repository: Annotated[UserRepository, Depends()]):
        self._user_repository = user_repository

    async def check_exists_by_username(self, username: str) -> bool:
        user_orm = await self._user_repository.read_by_username(username)
        return user_orm is not None

    async def check_exists_by_email(self, email: str) -> bool:
        user_orm = await self._user_repository.read_by_email(email)
        return user_orm is not None

    async def check_exists_by_id(self, id: UUID) -> bool:
        user_orm = await self._user_repository.read_by_id(id)
        return user_orm is not None

    async def update_user(self, *, user_id: UUID, dto: UpdateUserDTO) -> None:
        await self._user_repository.update_user(
            user_id=user_id, dao=dto.dict(exclude_unset=True)
        )


@final
class UserAuthPersistenceAdapter(CreateUserAuthPort, DeleteUserAuthPort):
    def __init__(
        self, *, user_auth_repository: Annotated[UserAuthRepository, Depends()]
    ):
        self._user_auth_repository = user_auth_repository

    async def create_user_with_auth(self, *, dto: CreateUserDTO) -> None:
        await self._user_auth_repository.create_user_with_auth(user_dao=dto.dict())

    async def delete_user_auth(self, *, user_id: UUID) -> None:
        await self._user_auth_repository.delete_user_auth(user_id=user_id)
