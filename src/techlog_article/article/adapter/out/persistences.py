from typing import final, Annotated

from fastapi import Depends

from application.port.out import CreateArticleOutDTO, CreateArticleOutPort

from ._article_user_repository import ArticleUserRepository


@final
class ArticleUserPersistenceAdapter(CreateArticleOutPort):
    def __init__(
        self, *, article_user_repository: Annotated[ArticleUserRepository, Depends()]
    ):
        self._article_user_repository = article_user_repository

    async def create_article(self, *, dto: CreateArticleOutDTO) -> None:
        await self._article_user_repository.create_article(
            author_id=dto.author_id, article_dao=dto.dict()
        )
