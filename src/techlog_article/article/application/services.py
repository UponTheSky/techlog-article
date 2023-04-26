from typing import final, Annotated, Optional
from uuid import UUID

from fastapi import Depends, HTTPException, status as HTTPStatus

from user.domain.user import User

from domain.article import Article
from adapter.out.persistences import (
    ArticleUserPersistenceAdapter,
    ArticlePersistenceAdapter,
)

from .port.in_ import (
    CreateArticleInDTO,
    CreateArticleInPort,
    ReadArticleInPort,
    ReadArticleResponse,
    ReadArticleListInDTO,
    ReadArticleListResponse,
    UpdateArticleInDTO,
    UpdateArticleInPort,
    DeleteArticleInPort,
)
from .port.out import (
    CreateArticleOutDTO,
    CreateArticleOutPort,
    ReadArticleOutPort,
    UpdateArticleOutDTO,
    UpdateArticleOutPort,
    DeleteArticleOutPort,
)


@final
class CreateArticleService(CreateArticleInPort):
    def __init__(
        self,
        create_article_out_port: Annotated[
            CreateArticleOutPort, Depends(ArticleUserPersistenceAdapter)
        ],
    ):
        self._create_article_out_port = create_article_out_port

    async def create_article(self, *, dto: CreateArticleInDTO) -> None:
        await self._create_article_out_port.create_article(
            dto=CreateArticleOutDTO(**dto.dict())
        )

        return None


@final
class ReadArticeService(ReadArticleInPort):
    def __init__(
        self,
        read_article_port: Annotated[
            ReadArticleOutPort, Depends(ArticleUserPersistenceAdapter)
        ],
    ):
        self._read_article_out_port = read_article_port

    async def read_article_by_id(self, id: UUID) -> Optional[ReadArticleResponse]:
        article_with_author = (
            await self._read_article_out_port.read_article_by_id_with_author(id)
        )
        if not article_with_author:
            return None

        return self._make_read_article_response(
            article=article_with_author.article, author=article_with_author.author
        )

    async def read_article_list(
        self, *, dto: ReadArticleListInDTO
    ) -> ReadArticleListResponse:
        articles_with_authors = await self._read_article_out_port.read_article_list(
            offset=dto.offset, limit=dto.limit, order_by=dto.order_by
        )
        total_articles_count = (
            await self._read_article_out_port.get_total_articles_count()
        )

        return ReadArticleListResponse(
            total_articles_count=total_articles_count,
            article_list=[
                ReadArticleResponse(article=element.article, author=element.author)
                for element in articles_with_authors
            ],
        )

    @staticmethod
    def _make_read_article_response(
        *, article: Article, author: User
    ) -> ReadArticleResponse:
        return ReadArticleResponse(
            title=article.title,
            content=article.content,
            author_name=author.username,
            author_email=author.email,
            created_at=article.created_at,
            updated_at=article.updated_at,
        )


@final
class UpdateArticeService(UpdateArticleInPort):
    def __init__(
        self,
        *,
        update_article_out_port: Annotated[
            UpdateArticleOutPort, Depends(ArticlePersistenceAdapter)
        ]
    ):
        self._update_article_out_port = update_article_out_port

    async def update_article(
        self, *, author_id: UUID, article_id: UUID, dto: UpdateArticleInDTO
    ) -> None:
        article_in_db = await self._update_article_out_port.read_article_by_id(
            article_id
        )

        if not article_in_db:
            raise HTTPException(
                status_code=HTTPStatus.HTTP_404_NOT_FOUND, detail="Content not found"
            )

        if article_in_db.author_id != author_id:
            raise HTTPException(
                status_code=HTTPStatus.HTTP_403_FORBIDDEN,
                detail="The user doesn't have the permission to modify this content",
            )

        await self._update_article_out_port.update_article(
            article_id=article_id,
            dto=UpdateArticleOutDTO(**dto.dict(exclude_unset=True)),
        )

        return None


@final
class DeleteArticleService(DeleteArticleInPort):
    def __init__(
        self,
        *,
        delete_article_out_port: Annotated[
            DeleteArticleOutPort, Depends(ArticlePersistenceAdapter)
        ]
    ):
        self._delete_article_out_port = delete_article_out_port

    async def delete_article(self, *, author_id: UUID, article_id: UUID) -> None:
        article_in_db = await self._delete_article_out_port.read_article_by_id(
            article_id
        )

        if not article_in_db:
            raise HTTPException(
                status_code=HTTPStatus.HTTP_404_NOT_FOUND, detail="Content not found"
            )

        if article_in_db.author_id != author_id:
            raise HTTPException(
                status_code=HTTPStatus.HTTP_403_FORBIDDEN,
                detail="The user doesn't have the permission to modify this content",
            )

        await self._delete_article_out_port.delete_article(article_id=article_id)

        return None
