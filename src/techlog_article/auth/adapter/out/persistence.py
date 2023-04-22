from typing import final, Optional
from uuid import UUID

from common.database import models
from user.domain.user import User

from application.port.out.read_user_port import ReadUserPort
from application.port.out.update_auth_port import UpdateAuthPort
from application.port.out.dto import UpdateAuthDTO

from ._user_repository import UserRepository
from ._auth_repository import AuthRepository


@final
class UserPersistenceAdapter(ReadUserPort):
    def __init__(self, *, user_repository: UserRepository):
        self._user_repository = user_repository

    def read_user(
        self, *, username: Optional[str], id: Optional[UUID]
    ) -> Optional[User]:
        if not username or not id:
            raise ValueError("Either username or user_id should be provided")

        result: Optional[models.User] = None
        if username:
            result = self._user_repository.read_by_username(username)

        elif id:
            result = self._user_repository.read_by_id(id)

        if result:
            return User.from_orm(models.User)

        return None


@final
class AuthPersistenceAdapter(UpdateAuthPort):
    def __init__(self, *, auth_repository: AuthRepository):
        self._auth_repository = auth_repository

    def update_auth(self, *, dto: UpdateAuthDTO) -> None:
        auth_in_db = self._auth_repository.read_by_user_id(dto.user_id)
        self._auth_repository.update(
            orm=auth_in_db, dao=dto.dict(exclude={"id", "user_id"})
        )
