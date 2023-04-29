from typing import Optional, final, Any
from uuid import UUID

from sqlalchemy import select

from src.techlog_article.common.database import models, CurrentDBSessionDependency


@final
class UserRepository:
    """
    Remark: we don't filter `deleted_at` != None in this case like we do
    in the article related repositories, since we want to preserve user-related
    data for some time.
    """

    def __init__(self, *, db_session: CurrentDBSessionDependency):
        self._db_session = db_session

    async def read_by_username(self, username: str) -> Optional[models.User]:
        stmt = select(models.User).where(models.User.username == username)
        return await self._db_session.scalar(stmt)

    async def read_by_email(self, email: str) -> Optional[models.User]:
        stmt = select(models.User).where(models.User.email == email)
        return await self._db_session.scalar(stmt)

    async def update_user(self, *, user_id: UUID, dao: dict[str, Any]) -> None:
        stmt = select(models.User).where(
            models.User.id == user_id, models.User.deleted_at is None
        )
        user_orm = (await self._db_session.scalars(stmt)).one()

        for field, new_value in dao:
            setattr(user_orm, field, new_value)

        await self._db_session.flush()
