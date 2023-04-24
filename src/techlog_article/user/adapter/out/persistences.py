from typing import final, Optional, Annotated

from fastapi import Depends

from application.port.out import CheckUserPort, CreateUserDTO, CreateUserPort
from domain.user import User

from ._user_repository import UserRepository


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
