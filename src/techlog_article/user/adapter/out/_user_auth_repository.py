from typing import final, Any
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import selectinload

from src.techlog_article.common.database import CurrentDBSessionDependency
from src.techlog_article.common.utils.datetime import get_now_utc_timestamp
from src.techlog_article.common.database import models


@final
class UserAuthRepository:
    def __init__(self, db_session: CurrentDBSessionDependency):
        self._db_session = db_session

    async def create_user_with_auth(self, *, user_dao: dict[str, Any]) -> None:
        user_orm = models.User(**user_dao)
        user_orm.auth = models.Auth()
        await self._db_session.add(user_orm)
        await self._db_session.flush()

    async def delete_user_auth(self, *, user_id: UUID) -> None:
        stmt = (
            select(models.User)
            .options(selectinload(models.User.auth))
            .where(models.User.id == user_id)
            # this work is idempotent; we don't filter `deleted_at` != None in this case
        )
        user_orm = (await self._db_session.scalars(stmt)).one()
        auth_orm = user_orm.auth

        user_orm.deleted_at = get_now_utc_timestamp()
        auth_orm.deleted_at = get_now_utc_timestamp()
        auth_orm.access_token = None

        await self._db_session.flush()
