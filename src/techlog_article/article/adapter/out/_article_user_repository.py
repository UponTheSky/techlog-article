from typing import final, Any
from uuid import UUID

from sqlalchemy import select

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
