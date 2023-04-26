from typing import final, Any, Optional
from uuid import UUID

from sqlalchemy import select

from common.database import CurrentDBSessionDependency, models
from common.utils.datetime import get_now_utc_timestamp


@final
class ArticleRepository:
    def __init__(self, db_session: CurrentDBSessionDependency):
        self._db_session = db_session

    async def read_article_by_id(self, id: UUID) -> Optional[models.Article]:
        stmt = select(models.Article).where(models.Article.id == id)
        return await self._db_session.scalar(stmt)

    async def update_article(self, *, article_id: UUID, dao: dict[str, Any]) -> None:
        stmt = select(models.Article).where(models.Article.id == article_id)
        article_orm = (await self._db_session.scalars(stmt)).one()

        for field, value in dao.items():
            setattr(article_orm, field, value)

        await self._db_session.flush()

    async def delete_article(self, *, article_id: UUID) -> None:
        await self.update_article(
            article_id=article_id, dao={"deleted_at": get_now_utc_timestamp()}
        )
