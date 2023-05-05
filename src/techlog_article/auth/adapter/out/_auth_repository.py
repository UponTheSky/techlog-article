from typing import final, Any, Optional
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.exc import NoResultFound

from src.techlog_article.common.database import models, CurrentDBSessionDependency


@final
class AuthRepository:
    def __init__(self, db_session: CurrentDBSessionDependency):
        self._db_session = db_session

    async def read_by_user_id(self, user_id: UUID) -> Optional[models.Auth]:
        stmt = select(models.Auth).where(models.Auth.user_id == user_id)
        return await self._db_session.scalar(stmt)

    async def update(self, *, user_id: UUID, dao: dict[str, Any]) -> models.Auth:
        auth_orm = await self.read_by_user_id(user_id)
        if not auth_orm:
            raise NoResultFound(
                f"The user auth corresponding to user id of {user_id} doesn't exist"
            )

        for field, value in dao.items():
            setattr(auth_orm, field, value)

        await self._db_session.flush()
