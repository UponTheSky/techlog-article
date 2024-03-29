from typing import final, Any, Optional
from uuid import UUID

from sqlalchemy import select

from techlog_article.common.database import CurrentDBSessionDependency, models
from techlog_article.common.utils.datetime import get_now_datetime


@final
class ArticleRepository:
    def __init__(self, db_session: CurrentDBSessionDependency):
        self._db_session = db_session

    async def read_article_by_id(self, id: UUID) -> Optional[models.Article]:
        stmt = select(models.Article).where(
            models.Article.id == id, models.Article.deleted_at.is_(None)
        )
        return await self._db_session.scalar(stmt)

    async def update_article(self, *, article_id: UUID, dao: dict[str, Any]) -> None:
        stmt = select(models.Article).where(
            models.Article.id == article_id, models.Article.deleted_at.is_(None)
        )
        article_orm = (await self._db_session.scalars(stmt)).one()

        for field, value in dao.items():
            setattr(article_orm, field, value)

        await self._db_session.flush()

    async def delete_article(self, *, article_id: UUID) -> None:
        await self.update_article(
            article_id=article_id, dao={"deleted_at": get_now_datetime()}
        )
