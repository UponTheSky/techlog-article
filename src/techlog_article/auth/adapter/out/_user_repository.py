from typing import Optional, final
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from common.database import models


@final
class UserRepository:
    def __init__(self, *, db_session: AsyncSession):
        self._db_session = db_session

    async def read_by_username(self, username: str) -> Optional[models.User]:
        stmt = select(models.User).where(models.User.username == username)
        return (await self._db_session.scalars(stmt)).one_or_none()

    async def read_by_id(self, id: UUID) -> Optional[models.User]:
        stmt = select(models.User).where(models.User.id == id)
        return (await self._db_session.scalars(stmt)).one_or_none()
