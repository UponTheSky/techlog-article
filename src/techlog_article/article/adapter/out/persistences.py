from typing import final, Annotated, Optional
from uuid import UUID

from fastapi import Depends

from user.domain.user import User

from domain.article import Article
from application.port.out import (
    CreateArticleOutDTO,
    CreateArticleOutPort,
    ReadArticleOutPort,
    ArticleWithAuthor,
)

from ._article_user_repository import ArticleUserRepository


@final
class ArticleUserPersistenceAdapter(CreateArticleOutPort, ReadArticleOutPort):
    def __init__(
        self, *, article_user_repository: Annotated[ArticleUserRepository, Depends()]
    ):
        self._article_user_repository = article_user_repository

    async def create_article(self, *, dto: CreateArticleOutDTO) -> None:
        await self._article_user_repository.create_article(
            author_id=dto.author_id, article_dao=dto.dict()
        )

    async def read_article_by_id_with_author(
        self, id: UUID
    ) -> Optional[ArticleWithAuthor]:
        article_orm = await self._article_user_repository.read_article_by_id(id)
        if not article_orm:
            return None

        return ArticleWithAuthor(
            article=Article.from_orm(article_orm),
            author=User.from_orm(article_orm.author),
        )

    async def read_article_list(
        self, *, offset: int, limit: int, order_by: str
    ) -> list[ArticleWithAuthor]:
        article_orms = await self._article_user_repository.read_article_list(
            offset=offset, limit=limit, order_by=order_by
        )

        return [
            ArticleWithAuthor(
                article=Article.from_orm(article_orm),
                author=User.from_orm(article_orm.author),
            )
            for article_orm in article_orms
        ]

    async def get_total_articles_count(self) -> int:
        return await self._article_user_repository.get_total_articles_count()
