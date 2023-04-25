from typing import final
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import selectinload

from common.database import CurrentDBSessionDependency
from common.utils.datetime import get_now_utc_timestamp
from common.database import models


@final
class UserAuthRepository:
    def __init__(self, db_session: CurrentDBSessionDependency):
        self._db_session = db_session

    async def delete_user_auth(self, *, user_id: UUID) -> None:
        stmt = (
            select(models.User)
            .options(selectinload(models.User.auth))
            .where(models.User.id == user_id)
        )
        user_orm = (await self._db_session.scalars(stmt)).one()
        auth_orm = user_orm.auth

        user_orm.deleted_at = get_now_utc_timestamp()
        auth_orm.deleted_at = get_now_utc_timestamp()
        auth_orm.access_token = None

        await self._db_session.flush()
