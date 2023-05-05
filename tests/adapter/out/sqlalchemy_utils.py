from typing import Any
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from src.techlog_article.common.database import models

"""
General cases
"""


async def db_commit(*, db_session: AsyncSession) -> None:
    await db_session.commit()


async def object_refresh(*, db_session: AsyncSession, object: Any) -> None:
    await db_session.refresh(object)


async def store_single_entity(
    *, db_session: AsyncSession, orm_model: Any, **kwargs: dict[str, Any]
) -> Any:
    db_session.add(orm_model(**kwargs))
    await db_session.commit()


async def read_single_entity_by_id(
    *, db_session: AsyncSession, orm_model: Any, id: UUID
) -> Any:
    return await db_session.scalar(select(orm_model).where(orm_model.id == id))


"""
Table-specific cases(due to relation, difficult to make as generic)
"""


async def read_user_with_auth_by_username(
    *, db_session: AsyncSession, username: str
) -> models.User:
    return await db_session.scalar(
        select(models.User)
        .options(selectinload(models.User.auth))
        .where(models.User.username == username)
    )
