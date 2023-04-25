from typing import Optional, final, Any, cast
from uuid import UUID

from sqlalchemy import select

from common.database import models, CurrentDBSessionDependency


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

    async def create_user(self, *, dao: dict[str, Any]) -> None:
        user_orm = models.User(**dao)
        await self._db_session.add(user_orm)
        await self._db_session.flush(user_orm)

    async def update_user(self, *, user_id: UUID, dao: dict[str, Any]) -> None:
        stmt = select(models.User).where(models.User.id == user_id)
        user_orm = cast(
            models.User, (await self._db_session.scalars(stmt)).one_or_none()
        )

        for field, new_value in dao:
            setattr(user_orm, field, new_value)

        await self._db_session.flush(user_orm)
