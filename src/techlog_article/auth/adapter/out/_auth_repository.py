from typing import final, Any, Optional
from uuid import UUID

from sqlalchemy import select

from src.techlog_article.common.database import models, CurrentDBSessionDependency


@final
class AuthRepository:
    def __init__(self, db_session: CurrentDBSessionDependency):
        self._db_session = db_session

    async def read_by_user_id(self, user_id: UUID) -> Optional[models.Auth]:
        stmt = select(models.Auth).where(models.Auth.user_id == user_id)
        return await self._db_session.scalar(stmt)

    async def update(self, *, orm: models.Auth, dao: dict[str, Any]) -> models.Auth:
        for field, value in dao:
            setattr(orm, field, value)

        await self._db_session.flush()
