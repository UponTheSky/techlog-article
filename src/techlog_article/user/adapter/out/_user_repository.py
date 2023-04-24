from typing import Optional, final
from dataclasses import dataclass, asdict

from sqlalchemy import select

from common.database import models, CurrentDBSessionDependency


@dataclass
class CreateUserDAO:
    username: str
    email: str
    hashed_password: str


@final
class UserRepository:
    def __init__(self, *, db_session: CurrentDBSessionDependency):
        self._db_session = db_session

    async def read_by_username(self, username: str) -> Optional[models.User]:
        stmt = select(models.User).where(models.User.username == username)
        return (await self._db_session.scalars(stmt)).one_or_none()

    async def read_by_email(self, email: str) -> Optional[models.User]:
        stmt = select(models.User).where(models.User.email == email)
        return (await self._db_session.scalars(stmt)).one_or_none()

    async def create_user(self, dao: CreateUserDAO) -> None:
        user_orm = models.User(**asdict(dao))
        await self._db_session.add(user_orm)
        await self._db_session.flush(user_orm)
