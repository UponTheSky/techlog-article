from typing import Any, Optional
from uuid import UUID, uuid4
from datetime import datetime

from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.exc import NoResultFound as _NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession

from techlog_article.common.database import models

"""
General cases
"""

NoResultFoundError = _NoResultFound


async def db_commit(*, db_session: AsyncSession) -> None:
    await db_session.commit()


async def object_refresh(*, db_session: AsyncSession, object: Any) -> None:
    await db_session.refresh(object)


async def store_single_entity(
    *, db_session: AsyncSession, orm_model: Any, **kwargs: dict[str, Any]
) -> None:
    db_session.add(orm_model(**kwargs))
    await db_session.commit()


async def read_single_entity_by_id(
    *, db_session: AsyncSession, orm_model: Any, id: UUID
) -> Any:
    return await db_session.scalar(select(orm_model).where(orm_model.id == id))


async def read_single_entity_by_field(
    *, db_session: AsyncSession, orm_model: Any, field_name: str, field_value: Any
) -> Any:
    return await db_session.scalar(
        select(orm_model).where(getattr(orm_model, field_name) == field_value)
    )


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


async def read_article_with_user(
    *, db_session: AsyncSession, article_id: UUID
) -> models.Article:
    return await db_session.scalar(
        select(models.Article)
        .options(selectinload(models.Article.author))
        .where(models.Article.id == article_id)
    )


async def store_user_with_auth(*, db_session: AsyncSession, **kwargs) -> None:
    user_orm = models.User(**kwargs)
    user_orm.auth = models.Auth(id=uuid4())
    db_session.add(user_orm)

    await db_session.commit()


async def store_user_with_article(
    *,
    db_session: AsyncSession,
    user_id: UUID,
    username: str,
    article_id: UUID,
    article_title: str,
    content: Optional[str] = None,
    user_deleted_at: Optional[datetime] = None,
    article_deleted_at: Optional[datetime] = None,
) -> None:
    user_orm = models.User(
        id=user_id,
        username=username,
        email="",
        hashed_password="",
        deleted_at=user_deleted_at,
    )
    user_orm.articles.append(
        models.Article(
            id=article_id,
            title=article_title,
            content=content,
            deleted_at=article_deleted_at,
        )
    )
    db_session.add(user_orm)

    await db_session.commit()
