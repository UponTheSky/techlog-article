from typing import final, Optional

from user.domain.user import User

from application.port.out import ReadUserPort, UpdateAuthDTO, UpdateAuthPort

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
class AuthPersistenceAdapter(UpdateAuthPort):
    def __init__(self, *, auth_repository: AuthRepository):
        self._auth_repository = auth_repository

    async def update_auth(self, *, dto: UpdateAuthDTO) -> None:
        auth_in_db = await self._auth_repository.read_by_user_id(dto.user_id)
        await self._auth_repository.update(
            orm=auth_in_db, dao=dto.dict(exclude={"id", "user_id"})
        )
