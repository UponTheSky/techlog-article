from typing import final, Any
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from common.database import models


@final
class AuthRepository:
    def __init__(self, db_session: AsyncSession):
        self._db_session = db_session

    async def read_by_user_id(self, user_id: UUID) -> models.Auth:
        stmt = select(models.Auth).where(models.Auth.user_id == user_id)
        return (await self._db_session.scalars(stmt)).one_or_none()

    async def update(self, *, orm: models.Auth, dao: dict[str, Any]) -> models.Auth:
        for field, value in dao:
            setattr(orm, field, value)

        await self._db_session.flush(orm)
