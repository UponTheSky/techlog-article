from typing import Optional, final

from sqlalchemy import select

from common.database import models, CurrentDBSessionDependency


@final
class UserRepository:
    def __init__(self, *, db_session: CurrentDBSessionDependency):
        self._db_session = db_session

    async def read_by_username(self, username: str) -> Optional[models.User]:
        stmt = select(models.User).where(models.User.username == username)
        return await self._db_session.scalar(stmt)
