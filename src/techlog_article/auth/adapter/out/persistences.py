from typing import final, Optional
from uuid import UUID

from user.domain.user import User

from domain.auth import Auth
from application.port.out import (
    ReadUserPort,
    UpdateAuthDTO,
    UpdateAuthPort,
    ReadAuthPort,
)

from ._user_repository import UserRepository
from ._auth_repository import AuthRepository


@final
class UserPersistenceAdapter(ReadUserPort):
    async def __init__(self, *, user_repository: UserRepository):
        self._user_repository = user_repository

    async def read_user_by_name(self, *, username: str) -> Optional[User]:
        user_orm = await self._user_repository.read_by_username(username)
        return User.from_orm(user_orm) if user_orm else None


@final
class AuthPersistenceAdapter(UpdateAuthPort, ReadAuthPort):
    def __init__(self, *, auth_repository: AuthRepository):
        self._auth_repository = auth_repository

    async def read_auth_by_user_id(self, *, user_id: UUID) -> Optional[Auth]:
        auth_orm = await self._auth_repository.read_by_user_id(user_id)
        return Auth.from_orm(auth_orm) if auth_orm else None

    async def update_auth(self, *, dto: UpdateAuthDTO) -> None:
        auth_orm = await self._auth_repository.read_by_user_id(dto.user_id)
        await self._auth_repository.update(
            orm=auth_orm, dao=dto.dict(exclude={"id", "user_id"})
        )
