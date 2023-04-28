from typing import final, Any, Optional
from uuid import UUID

from sqlalchemy import select, func
from sqlalchemy.orm import joinedload, selectinload

from common.database import CurrentDBSessionDependency, models


@final
class ArticleUserRepository:
    def __init__(self, db_session: CurrentDBSessionDependency):
        self._db_session = db_session

    async def create_article(
        self, *, author_id: UUID, article_dao: dict[str, Any]
    ) -> None:
        stmt = select(models.User).where(models.User.id == author_id)
        author_orm = (await self._db_session.scalars(stmt)).one()
        article_orm = models.Article(**article_dao)

        author_orm.articles.append(article_orm)

        await self._db_session.add(article_orm)
        await self._db_session.flush()

    async def read_article_by_id(self, id: UUID) -> Optional[models.Article]:
        stmt = (
            select(models.Article)
            .options(selectinload(models.Article.author))
            .where(models.Article.id == id, models.Article.deleted_at is None)
        )

        return await self._db_session.scalar(stmt)

    async def read_article_list(
        self, *, offset: int, limit: int, order_by: str
    ) -> list[models.Article]:
        stmt = (
            select(models.Article)
            .options(joinedload(models.Article.author))
            .where(models.Article.deleted_at is None)
            .offset(offset)
            .limit(limit)
            .order_by(getattr(models.Article, order_by))
        )

        return (await self._db_session.scalars(stmt)).all()

    async def get_total_articles_count(self) -> int:
        stmt = select(func.count(models.Article.id)).where(
            models.Article.deleted_at is None
        )
        result = await self._db_session.scalar(stmt)

        return result if result else 0
