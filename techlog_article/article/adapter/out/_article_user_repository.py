from typing import final, Any, Optional
from uuid import UUID, uuid4

from sqlalchemy import select, func
from sqlalchemy.orm import contains_eager, selectinload

from techlog_article.common.database import CurrentDBSessionDependency, models


@final
class ArticleUserRepository:
    def __init__(self, db_session: CurrentDBSessionDependency):
        self._db_session = db_session

    async def create_article(
        self, *, author_id: UUID, article_dao: dict[str, Any]
    ) -> None:
        # to "mount" models.User.articles, we have to use selectinload
        stmt = (
            select(models.User)
            .options(selectinload(models.User.articles))
            .where(models.User.id == author_id)
        )
        author_orm = (await self._db_session.scalars(stmt)).one()
        article_orm = models.Article(id=uuid4(), **article_dao)

        author_orm.articles.append(article_orm)
        self._db_session.add(article_orm)
        await self._db_session.flush()

    async def read_article_by_id_with_user(self, id: UUID) -> Optional[models.Article]:
        # we want to have filters on both of the models, so we use explicit join
        # for details: https://docs.sqlalchemy.org/en/20/tutorial/orm_related_objects.html#explicit-join-eager-load
        stmt = (
            select(models.Article)
            .join(models.Article.author)
            .where(models.Article.id == id)
            .where(models.Article.deleted_at.is_(None))
            .where(models.User.deleted_at.is_(None))
            .options(selectinload(models.Article.author))
        )

        return await self._db_session.scalar(stmt)

    async def read_article_with_user_list(
        self, *, offset: int, limit: int, order_by: str
    ) -> list[models.Article]:
        stmt = (
            select(models.Article)
            .join(models.Article.author)
            .where(models.Article.deleted_at.is_(None))
            .where(models.User.deleted_at.is_(None))
            .options(contains_eager(models.Article.author))
            .offset(offset)
            .limit(limit)
            .order_by(getattr(models.Article, order_by))
        )

        return (await self._db_session.scalars(stmt)).all()

    async def get_total_articles_count(self) -> int:
        stmt = select(func.count(models.Article.id)).where(
            models.Article.deleted_at.is_(None)
        )
        result = await self._db_session.scalar(stmt)

        return result if result else 0
