from typing import final, Any
from uuid import UUID

from sqlalchemy import select

from common.database import CurrentDBSessionDependency, models


@final
class ArticleRepository:
    def __init__(self, db_session: CurrentDBSessionDependency):
        self._db_session = db_session

    async def update_article(self, *, article_id: UUID, dao: dict[str, Any]) -> None:
        stmt = select(models.Article).where(models.Article.id == article_id)
        article_orm = (await self._db_session.scalars(stmt)).one()

        for field, value in dao.items():
            setattr(article_orm, field, value)

        await self._db_session.flush()
